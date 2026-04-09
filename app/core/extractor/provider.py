"""LangExtract language-model providers (e.g. OpenAI-compatible HTTP API)."""

from __future__ import annotations

from typing import Any

from langextract.factory import ModelConfig, create_model

from app.config import get_provider_config, get_runtime_config


def create_openai_compatible_langextract_model(
    *,
    provider_kwargs: dict[str, Any] | None = None,
    model_id: str | None = None,
) -> Any:
    """Build LangExtract ``OpenAILanguageModel`` (supports custom ``base_url``)."""
    provider_config = get_provider_config()
    runtime_config = get_runtime_config()
    kwargs: dict[str, Any] = dict(provider_kwargs or {})
    kwargs.setdefault("api_key", provider_config.llm.api_key)
    kwargs.setdefault("temperature", runtime_config.llm.temperature)
    kwargs.setdefault("max_output_tokens", runtime_config.llm.max_tokens)
    if provider_config.llm.api_base:
        kwargs["base_url"] = provider_config.llm.api_base
    mid = model_id if model_id is not None else runtime_config.llm.model
    config = ModelConfig(
        model_id=mid,
        provider="OpenAILanguageModel",
        provider_kwargs=kwargs,
    )
    return create_model(config, use_schema_constraints=False)
