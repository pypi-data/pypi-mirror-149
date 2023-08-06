import logging
import trio
from functools import wraps
from contextlib import asynccontextmanager
from ._connection import Connection
from ._utils import set_event_when_done


logger = logging.getLogger(__name__)


class Pool:
    def __init__(self, database, *,
                 pool_min_size=5,
                 pool_max_size=10,
                 pool_close_timeout=5,
                 pool_conn_init=None,
                 **connection_kwargs):
        if pool_min_size < 1:
            raise ValueError('pool_min_size cannot be less than 1')
        if pool_max_size < pool_min_size:
            raise ValueError(
                'pool_max_size cannot be less than pool_min_size')

        self.database = database
        self.min_size = pool_min_size
        self.max_size = pool_max_size
        self.close_timeout = pool_close_timeout

        # this will be set by 'set_event_when_done' when _run returns
        self.closed = trio.Event()

        self._conn_kwargs = connection_kwargs
        self._conn_init = pool_conn_init

        self._free_conns = []
        self._in_use_conns = []
        self._codec_helper = None
        self._nursery = None
        self._conn_limit = trio.CapacityLimiter(self.max_size)
        self._started = trio.Event()
        self._start_closing = trio.Event()

    @asynccontextmanager
    async def acquire(self):
        async with self._conn_limit:
            while True:
                if not self._free_conns:
                    await self._add_connection()
                conn = self._free_conns.pop()
                if not conn.closed.is_set() and \
                   not conn._start_closing.is_set():
                    break
                # the connection will be discarded (since we just
                # popped it), and later another one will be created to
                # replace it
            self._in_use_conns.append(conn)

            conn._owner = trio.lowlevel.current_task()
            try:
                yield conn
            finally:
                self._in_use_conns.remove(conn)
                self._free_conns.append(conn)

    def close(self):
        self._start_closing.set()

    @set_event_when_done('closed')
    async def _run(self):
        async with trio.open_nursery() as nursery:
            self._nursery = nursery

            for i in range(self.min_size):
                await self._add_connection()

            self._started.set()
            await self._start_closing.wait()

            all_conns = self._free_conns + self._in_use_conns
            for conn in all_conns:
                conn.close()

            with trio.move_on_after(self.close_timeout):
                for conn in all_conns:
                    await conn.closed.wait()

            nursery.cancel_scope.cancel()

    async def _add_connection(self):
        conn = await self._create_connection()
        self._free_conns.append(conn)

    async def _create_connection(self):
        conn = Connection(
            self.database,
            codec_helper=self._codec_helper,
            **self._conn_kwargs)
        self._nursery.start_soon(conn._run)

        async with conn._is_ready_cv:
            while not conn._is_ready:
                await conn._is_ready_cv.wait()

        if not self._codec_helper:
            await conn._pg_types_loaded.wait()
            self._codec_helper = conn._codec_helper

        if self._conn_init:
            self._conn_init(conn)

        conn._broken_handler = self._handle_broken_conn

        return conn

    def _handle_broken_conn(self, conn):
        logger.info('Discarding closed connection in Pool')
        if conn in self._free_conns:
            self._free_conns.remove(conn)
        if conn in self._in_use_conns:
            self._in_use_conns.remove(conn)


@asynccontextmanager
@wraps(Pool)
async def create_pool(*args, **kwargs):
    pool = Pool(*args, **kwargs)
    async with trio.open_nursery() as nursery:
        nursery.start_soon(pool._run)
        await pool._started.wait()

        try:
            yield pool
        finally:
            pool.close()
