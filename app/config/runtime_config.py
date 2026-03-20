"""Runtime configuration: model parameters, extraction, QA behavior."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMRuntimeConfig(BaseSettings):
    """LLM runtime parameters (model, temperature, etc.)."""

    model_config = SettingsConfigDict(
        env_prefix="LLM_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    model: str = Field(default="gpt-4o-mini", description="Model name")
    temperature: float = Field(default=0.0, ge=0, le=2, description="Sampling temperature")
    max_tokens: int = Field(default=4096, ge=1, description="Max output tokens")


class ExtractorRuntimeConfig(BaseSettings):
    """Entity/relation extraction runtime parameters."""

    model_config = SettingsConfigDict(
        env_prefix="EXTRACTOR_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    chunk_size: int = Field(default=4000, ge=100, description="Text chunk size for extraction")
    chunk_overlap: int = Field(default=200, ge=0, description="Chunk overlap")


class QARuntimeConfig(BaseSettings):
    """QA / Cypher generation runtime parameters."""

    model_config = SettingsConfigDict(
        env_prefix="QA_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    max_cypher_results: int = Field(default=50, ge=1, description="Max results from Cypher query")


class RuntimeConfig(BaseSettings):
    """Aggregated runtime configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm: LLMRuntimeConfig = Field(default_factory=LLMRuntimeConfig)
    extractor: ExtractorRuntimeConfig = Field(default_factory=ExtractorRuntimeConfig)
    qa: QARuntimeConfig = Field(default_factory=QARuntimeConfig)
