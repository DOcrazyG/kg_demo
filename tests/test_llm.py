"""Tests for LLM client connection."""

import pytest

from app.config import get_provider_config
from app.llm import ChatMessage, LLMClient

# Skip all tests if OPENAI_API_KEY is not set (loads from .env via config)
pytestmark = pytest.mark.skipif(
    not get_provider_config().llm.api_key,
    reason="OPENAI_API_KEY not set",
)


class TestLLMConnection:
    """Test LLM client connection and basic calls."""

    def test_invoke_simple(self):
        """Non-streaming: simple string prompt."""
        client = LLMClient()
        resp = client.invoke("Say hello in one word.")
        assert isinstance(resp, str)
        assert len(resp) > 0

    def test_invoke_with_system(self):
        """Non-streaming: with system prompt."""
        client = LLMClient()
        resp = client.invoke(
            "Reply with only: OK",
            system="You are a minimal assistant. Reply with exactly what the user asks.",
        )
        assert isinstance(resp, str)
        assert len(resp) > 0

    def test_invoke_with_messages(self):
        """Non-streaming: message list."""
        client = LLMClient()
        messages = [ChatMessage("user", "What is 1+1? Reply with just the number.")]
        resp = client.invoke(messages)
        assert isinstance(resp, str)
        assert len(resp) > 0

    def test_stream_simple(self):
        """Streaming: yields chunks."""
        client = LLMClient()
        chunks = list(client.stream("Count from 1 to 3."))
        assert isinstance(chunks, list)
        full = "".join(chunks)
        assert len(full) > 0

    def test_stream_yields_strings(self):
        """Streaming: each chunk is non-empty string when present."""
        client = LLMClient()
        for chunk in client.stream("Hi"):
            assert isinstance(chunk, str)


@pytest.mark.asyncio
class TestLLMConnectionAsync:
    """Test async LLM client connection."""

    async def test_invoke_async(self):
        """Async non-streaming."""
        client = LLMClient()
        resp = await client.invoke_async("Say hi in one word.")
        assert isinstance(resp, str)
        assert len(resp) > 0

    async def test_stream_async(self):
        """Async streaming."""
        client = LLMClient()
        chunks = []
        async for chunk in client.stream_async("Say OK"):
            chunks.append(chunk)
        full = "".join(chunks)
        assert len(full) > 0
