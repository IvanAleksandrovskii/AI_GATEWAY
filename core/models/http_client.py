import asyncio
import time
from typing import List
import httpx
from asyncio import Lock

from core import logger
from core import settings


class UberClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.is_busy = False
        self.last_used = time.time()

    async def request(self, *args, **kwargs) -> httpx.Response:
        """
        Make an HTTP request using the client.

        :param args: Positional arguments for the request
        :param kwargs: Keyword arguments for the request
        :return: HTTP response
        """
        self.is_busy = True
        try:
            response = await self.client.request(*args, **kwargs)
            return response
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise
        finally:
            self.is_busy = False
            self.last_used = time.time()


class ClientManager:
    # TODO: Make this configurable
    def __init__(self, client_timeout=settings.http_client.timeout,
                 max_keepalive_connections=settings.http_client.max_keepalive_connections):
        self.clients: List[UberClient] = []
        self.max_clients = max_keepalive_connections
        self.client_timeout = client_timeout
        self.limits = httpx.Limits(max_keepalive_connections=max_keepalive_connections,
                                   keepalive_expiry=client_timeout)
        self.lock = Lock()  # For thread-safety
        self.cleanup_task = None
        self.is_shutting_down = False

    async def start(self):
        """Initialize the cleanup task."""
        if self.cleanup_task is None:
            self.cleanup_task = asyncio.create_task(self.periodic_cleanup())

    async def periodic_cleanup(self) -> None:
        """Periodically clean up inactive clients."""
        while not self.is_shutting_down:
            await asyncio.sleep(60)
            await self.cleanup_inactive_clients()

    async def cleanup_inactive_clients(self) -> None:
        """Remove inactive clients from the pool."""
        async with self.lock:
            current_time = time.time()
            self.clients = [client for client in self.clients
                            if client.is_busy or (current_time - client.last_used < self.client_timeout)]
            logger.info(f"Cleanup completed. {len(self.clients)} clients remaining.")

    async def get_client(self) -> UberClient:
        """
        Get an available client or create a new one if needed.

        :return: An UberClient instance
        """
        async with self.lock:
            # Try to find an available client
            for client in self.clients:
                if not client.is_busy:
                    logger.debug(f"Reusing existing client: {id(client)}")
                    return client

            # If no available clients and we haven't reached the limit, create a new one
            if len(self.clients) < self.max_clients:
                new_client = UberClient(httpx.AsyncClient(limits=self.limits))
                self.clients.append(new_client)
                logger.info(f"Created new client: {id(new_client)}")
                return new_client

        # If all clients are busy, and we've reached the limit, wait and try again
        logger.warning("All clients busy. Waiting for an available client.")
        await asyncio.sleep(1)
        return await self.get_client()

    async def dispose_all_clients(self) -> None:
        """Dispose of all clients during shutdown."""
        self.is_shutting_down = True
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass

        async with self.lock:
            for client in self.clients:
                await client.client.aclose()
            self.clients.clear()
        logger.info("All clients disposed.")


# Global ClientManager instance
client_manager = ClientManager()
