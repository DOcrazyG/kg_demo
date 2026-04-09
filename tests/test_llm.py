"""Tests for LLM client connection."""

import pytest
from pydantic import BaseModel

from app.config import get_provider_config
from app.llm import ChatMessage, LLMClient

# Skip all tests if OPENAI_API_KEY is not set (loads from .env via config)
pytestmark = pytest.mark.skipif(
    not get_provider_config().llm.api_key,
    reason="OPENAI_API_KEY not set",
)


class Person(BaseModel):
    name: str
    age: int


class TestLLMConnection:
    """Test LLM client connection and basic calls."""

    def test_invoke_simple(self):
        """Non-streaming: simple string prompt."""
        client = LLMClient()
        resp = client.chat("Say hello in one word.")
        assert isinstance(resp, str)
        assert len(resp) > 0

    def test_invoke_with_system(self):
        """Non-streaming: with system prompt."""
        client = LLMClient()
        resp = client.chat(
            "Reply with only: OK",
            system="You are a minimal assistant. Reply with exactly what the user asks.",
        )
        assert isinstance(resp, str)
        assert len(resp) > 0

    def test_invoke_with_messages(self):
        """Non-streaming: message list."""
        client = LLMClient()
        messages = [ChatMessage("user", "What is 1+1? Reply with just the number.")]
        resp = client.chat(messages)
        assert isinstance(resp, str)
        assert len(resp) > 0

    def test_stream_simple(self):
        """Streaming: yields chunks."""
        client = LLMClient()
        chunks = list(client.stream_chat("Count from 1 to 3."))
        assert isinstance(chunks, list)
        full = "".join(chunks)
        assert len(full) > 0

    def test_stream_yields_strings(self):
        """Streaming: each chunk is non-empty string when present."""
        client = LLMClient()
        for chunk in client.stream_chat("Hi"):
            assert isinstance(chunk, str)


@pytest.mark.asyncio
class TestLLMConnectionAsync:
    """Test async LLM client connection."""

    async def test_chat_async(self):
        """Async non-streaming."""
        client = LLMClient()
        resp = await client.chat_async("Say hi in one word.")
        assert isinstance(resp, str)
        assert len(resp) > 0

    async def test_stream_chat_async(self):
        """Async streaming."""
        client = LLMClient()
        chunks = []
        async for chunk in client.stream_chat_async("Say OK"):
            chunks.append(chunk)
        full = "".join(chunks)
        assert len(full) > 0


class TestLLMExtract:
    """Test extract and extract_async methods."""

    def test_extract_simple(self):
        """Extract: simple Pydantic model."""
        client = LLMClient()
        resp = client.extract(
            "My name is Tom and I am 25 years old.",
            Person,
        )
        assert isinstance(resp, Person)
        assert resp.name == "Tom"
        assert resp.age == 25

    def test_extract_with_system(self):
        """Extract: with system prompt."""
        client = LLMClient()
        resp = client.extract(
            "Tom is 30 years old.",
            Person,
            system="Extract the name and age from the text.",
        )
        assert isinstance(resp, Person)
        assert resp.name == "Tom"
        assert resp.age == 30


@pytest.mark.asyncio
class TestLLMExtractAsync:
    """Test async extract method."""

    async def test_extract_async(self):
        """Async extract."""
        client = LLMClient()
        resp = await client.extract_async(
            "My name is Alice and I am 28 years old.",
            Person,
        )
        assert isinstance(resp, Person)
        assert resp.name == "Alice"
        assert resp.age == 28
