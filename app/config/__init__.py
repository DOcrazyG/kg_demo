"""Configuration: provider config (connections) and runtime config (behavior)."""

from app.config.provider_config import (
    LLMProviderConfig,
    Neo4jProviderConfig,
    ProviderConfig,
)
from app.config.runtime_config import (
    ExtractorRuntimeConfig,
    LLMRuntimeConfig,
    QARuntimeConfig,
    RuntimeConfig,
)
from app.config.settings import get_provider_config, get_runtime_config

__all__ = [
    "ProviderConfig",
    "LLMProviderConfig",
    "Neo4jProviderConfig",
    "RuntimeConfig",
    "LLMRuntimeConfig",
    "ExtractorRuntimeConfig",
    "QARuntimeConfig",
    "get_provider_config",
    "get_runtime_config",
    "provider",
    "runtime",
]


def __getattr__(name: str):
    """Lazy access: from app.config import provider, runtime."""
    if name == "provider":
        return get_provider_config()
    if name == "runtime":
        return get_runtime_config()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
