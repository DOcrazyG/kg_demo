"""Unified settings access: lazy-loaded singleton instances."""

from functools import lru_cache

from app.config.provider_config import ProviderConfig
from app.config.runtime_config import RuntimeConfig


@lru_cache
def get_provider_config() -> ProviderConfig:
    """Cached provider config. Use for LLM/Neo4j connections."""
    return ProviderConfig()


@lru_cache
def get_runtime_config() -> RuntimeConfig:
    """Cached runtime config. Use for model/extractor/QA params."""
    return RuntimeConfig()


