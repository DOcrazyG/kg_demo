"""LLM client using OpenAI SDK. Supports streaming and non-streaming chat."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Iterator
from typing import TypeVar

from openai import AsyncOpenAI, OpenAI
from pydantic import BaseModel

from app.config import get_provider_config, get_runtime_config

TModel = TypeVar("TModel", bound=BaseModel)


def ChatMessage(role: str, content: str) -> dict[str, str]:
    """Build chat message dict: {"role": ..., "content": ...}."""
    return {"role": role, "content": content}


class LLMClient:
    """
    OpenAI chat completion client with streaming and non-streaming interfaces.
    Uses provider config (api_key, api_base) and runtime config (model, temperature, max_tokens).
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        api_base: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ):
        provider = get_provider_config()
        runtime = get_runtime_config()

        self._api_key = api_key if api_key is not None else provider.llm.api_key
        self._api_base = api_base if api_base is not None else provider.llm.api_base
        self._model = model if model is not None else runtime.llm.model
        self._temperature = temperature if temperature is not None else runtime.llm.temperature
        self._max_tokens = max_tokens if max_tokens is not None else runtime.llm.max_tokens

        self._client = OpenAI(
            api_key=self._api_key or None,
            base_url=self._api_base,
        )
        self._async_client = AsyncOpenAI(
            api_key=self._api_key or None,
            base_url=self._api_base,
        )

    def _to_messages(
        self,
        messages: list[dict[str, str]] | str,
        system: str | None = None,
    ) -> list[dict[str, str]]:
        if isinstance(messages, str):
            msgs: list[dict[str, str]] = []
            if system:
                msgs.append({"role": "system", "content": system})
            msgs.append({"role": "user", "content": messages})
            return msgs
        out = []
        if system:
            out.append({"role": "system", "content": system})
        for m in messages:
            out.append(m)
        return out

    def chat(
        self,
        messages: list[dict[str, str]] | str,
        *,
        system: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Non-streaming chat completion. Returns full response text."""
        msgs = self._to_messages(messages, system)
        resp = self._client.chat.completions.create(
            model=model or self._model,
            messages=msgs,
            temperature=temperature if temperature is not None else self._temperature,
            max_tokens=max_tokens or self._max_tokens,
            stream=False,
        )
        choice = resp.choices[0]
        return choice.message.content or ""

    def stream_chat(
        self,
        messages: list[dict[str, str]] | str,
        *,
        system: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> Iterator[str]:
        """Streaming chat completion. Yields content chunks."""
        msgs = self._to_messages(messages, system)
        completion_stream = self._client.chat.completions.create(
            model=model or self._model,
            messages=msgs,
            temperature=temperature if temperature is not None else self._temperature,
            max_tokens=max_tokens or self._max_tokens,
            stream=True,
        )
        for chunk in completion_stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def chat_async(
        self,
        messages: list[dict[str, str]] | str,
        *,
        system: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Async non-streaming chat completion."""
        msgs = self._to_messages(messages, system)
        resp = await self._async_client.chat.completions.create(
            model=model or self._model,
            messages=msgs,
            temperature=temperature if temperature is not None else self._temperature,
            max_tokens=max_tokens or self._max_tokens,
            stream=False,
        )
        choice = resp.choices[0]
        return choice.message.content or ""

    async def stream_chat_async(
        self,
        messages: list[dict[str, str]] | str,
        *,
        system: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """Async streaming chat completion. Yields content chunks."""
        msgs = self._to_messages(messages, system)
        completion_stream = await self._async_client.chat.completions.create(
            model=model or self._model,
            messages=msgs,
            temperature=temperature if temperature is not None else self._temperature,
            max_tokens=max_tokens or self._max_tokens,
            stream=True,
        )
        async for chunk in completion_stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def extract(
        self,
        messages: list[dict[str, str]] | str,
        response_model: type[TModel],
        *,
        system: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> TModel:
        """Chat completion with JSON object output, parsed into ``response_model``."""
        if not (isinstance(response_model, type) and issubclass(response_model, BaseModel)):
            raise TypeError("response_model must be a Pydantic BaseModel subclass")
        keys = list(response_model.model_fields.keys())
        json_hint = (
            "Respond with a single JSON object only, with these keys: "
            f"{keys}. Use JSON types (strings, numbers, booleans). No markdown or extra text."
        )
        full_system = f"{system}\n{json_hint}" if system else json_hint
        msgs = self._to_messages(messages, full_system)
        resp = self._client.chat.completions.create(
            model=model or self._model,
            messages=msgs,
            temperature=temperature if temperature is not None else self._temperature,
            max_tokens=max_tokens or self._max_tokens,
            stream=False,
            response_format={"type": "json_object"},
        )
        raw = resp.choices[0].message.content or "{}"
        return response_model.model_validate(json.loads(raw))

    async def extract_async(
        self,
        messages: list[dict[str, str]] | str,
        response_model: type[TModel],
        *,
        system: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> TModel:
        """Async chat completion with JSON object output, parsed into ``response_model``."""
        if not (isinstance(response_model, type) and issubclass(response_model, BaseModel)):
            raise TypeError("response_model must be a Pydantic BaseModel subclass")
        keys = list(response_model.model_fields.keys())
        json_hint = (
            "Respond with a single JSON object only, with these keys: "
            f"{keys}. Use JSON types (strings, numbers, booleans). No markdown or extra text."
        )
        full_system = f"{system}\n{json_hint}" if system else json_hint
        msgs = self._to_messages(messages, full_system)
        resp = await self._async_client.chat.completions.create(
            model=model or self._model,
            messages=msgs,
            temperature=temperature if temperature is not None else self._temperature,
            max_tokens=max_tokens or self._max_tokens,
            stream=False,
            response_format={"type": "json_object"},
        )
        raw = resp.choices[0].message.content or "{}"
        return response_model.model_validate(json.loads(raw))
