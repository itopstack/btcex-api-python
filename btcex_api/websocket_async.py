import asyncio

from btcex_api.websocket_client import WebsocketClient


class WebsocketAsync(object):
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_key = client_id
        self.client_secret = client_secret
        self.ws_client = WebsocketClient(client_id, client_secret)

    async def subscribe_private_trades(self, symbols: list = None):
        if not symbols:
            return
        asyncio.create_task(self.ws_client.run_private())
        topics = list(map(lambda s: f'user.trades.{s}.raw', symbols))
        await self.ws_client.subscribe(method='/private/subscribe', topics=topics)

    async def subscribe_public_charts(self, timeframe: str, symbols: list = None):
        if not symbols:
            return
        asyncio.create_task(self.ws_client.run_public())
        topics = list(map(lambda s: f'chart.trades.{s}.{timeframe}', symbols))
        await self.ws_client.subscribe(method='/public/subscribe', topics=topics)
