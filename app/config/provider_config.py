"""Provider configuration: external service connections (LLM, Neo4j)."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProviderConfig(BaseSettings):
    """LLM provider connection settings."""

    model_config = SettingsConfigDict(
        env_prefix="OPENAI_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_key: str = Field(default="", description="API key")
    api_base: str | None = Field(default=None, description="Custom API base URL")


class Neo4jProviderConfig(BaseSettings):
    """Neo4j connection settings."""

    model_config = SettingsConfigDict(
        env_prefix="NEO4J_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    uri: str = Field(default="bolt://localhost:7687", description="Neo4j URI")
    user: str = Field(default="neo4j", description="Username")
    password: str = Field(default="", description="Password")
    database: str = Field(default="neo4j", description="Database name")


class ProviderConfig(BaseSettings):
    """Aggregated provider configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm: LLMProviderConfig = Field(default_factory=LLMProviderConfig)
    neo4j: Neo4jProviderConfig = Field(default_factory=Neo4jProviderConfig)
