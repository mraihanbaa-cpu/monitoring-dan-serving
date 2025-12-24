import asyncio
import uuid
from typing import Any, Dict


class Batcher:
    """Minimal async Batcher used by the FastAPI app.

    - `futures` stores asyncio.Future objects keyed by request id.
    - `enqueue(input_data)` is async and returns a request id immediately,
      while processing continues in background.
    """

    def __init__(self) -> None:
        self.futures: Dict[str, asyncio.Future] = {}

    async def enqueue(self, input_data: Any) -> str:
        """Create a request id, register a future and start background work.

        Returns the request id which the caller can poll via `futures`.
        """
        rid = uuid.uuid4().hex
        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        self.futures[rid] = fut
        asyncio.create_task(self._process(rid, input_data))
        return rid

    async def _process(self, rid: str, input_data: Any) -> None:
        """Background processing stub. Replace with real model call."""
        try:
            # Simulate some async work; replace with real prediction logic.
            await asyncio.sleep(0.1)
            # Example result - adapt to your real model output shape.
            result = {"status": "ok", "input_length": len(input_data) if hasattr(input_data, '__len__') else None}
            fut = self.futures.get(rid)
            if fut and not fut.done():
                fut.set_result(result)
        except Exception as exc:
            fut = self.futures.get(rid)
            if fut and not fut.done():
                fut.set_exception(exc)
