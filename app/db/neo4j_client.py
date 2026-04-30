"""
Neo4j graph database client - sync and async operations.

Based on neo4j-graphrag-python and official neo4j-python-driver docs.
Supports: Cypher execution, entity/relation writing, connectivity check.
"""

from typing import Any

from neo4j import AsyncGraphDatabase, GraphDatabase

from app.config.provider_config import Neo4jProviderConfig
from app.graph import BaseEntity, BaseRelation


def _flatten_props(props: dict[str, Any]) -> dict[str, Any]:
    """Flatten props to Neo4j-compatible key-value pairs."""
    out: dict[str, Any] = {}
    for k, v in props.items():
        if v is None:
            continue
        if isinstance(v, (str, int, float, bool)):
            out[k] = v
        elif isinstance(v, dict):
            for sk, sv in v.items():
                if sv is not None and isinstance(sv, (str, int, float, bool)):
                    out[f"{k}_{sk}"] = sv
        elif (
            isinstance(v, list)
            and v
            and all(isinstance(x, (str, int, float, bool)) for x in v)
        ):
            out[k] = v
    return out


def _record_to_dict(record: Any) -> dict[str, Any]:
    """Convert neo4j.Record to plain dict."""
    if hasattr(record, "data"):
        return record.data()
    return dict(record)


class Neo4jClient:
    """
    Neo4j graph database client with sync/async interfaces and context management.

    Usage:
        with Neo4jClient(config) as client:
            records = client.run("MATCH (n) RETURN n LIMIT 10")

        async with Neo4jClient(config) as client:
            records = await client.arun("MATCH (n) RETURN n LIMIT 10")
    """

    def __init__(self, config: Neo4jProviderConfig | None = None):
        """Initialize Neo4j client."""
        from app.config import get_provider_config

        self._config = config or get_provider_config().neo4j
        self._sync_driver = None
        self._async_driver = None

    def _get_sync_driver(self):
        if self._sync_driver is None:
            self._sync_driver = GraphDatabase.driver(
                self._config.uri,
                auth=(self._config.user, self._config.password),
            )
        return self._sync_driver

    def _get_async_driver(self):
        if self._async_driver is None:
            self._async_driver = AsyncGraphDatabase.driver(
                self._config.uri,
                auth=(self._config.user, self._config.password),
            )
        return self._async_driver

    @property
    def database(self) -> str:
        return self._config.database

    def __enter__(self) -> "Neo4jClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    async def __aenter__(self) -> "Neo4jClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.async_close()

    def execute_query(
        self,
        query: str,
        parameters_: dict[str, Any] | None = None,
        routing_: str | None = None,
        **kwargs: Any,
    ) -> tuple[list[Any], Any, list[str]]:
        """Execute Cypher query synchronously."""
        kw = dict(kwargs)
        kw.setdefault("database_", self.database)
        if parameters_ is not None:
            kw.setdefault("parameters_", parameters_)
        if routing_ is not None:
            kw["routing_"] = routing_
        driver = self._get_sync_driver()
        return driver.execute_query(query, **kw)

    def verify_connectivity(self) -> None:
        """Verify connectivity synchronously."""
        self._get_sync_driver().verify_connectivity()

    def close(self) -> None:
        """Close sync driver."""
        if self._sync_driver:
            self._sync_driver.close()
            self._sync_driver = None

    async def async_execute_query(
        self,
        query: str,
        parameters_: dict[str, Any] | None = None,
        routing_: str | None = None,
        **kwargs: Any,
    ) -> tuple[list[Any], Any, list[str]]:
        """Execute Cypher query asynchronously."""
        kw = dict(kwargs)
        kw.setdefault("database_", self.database)
        if parameters_ is not None:
            kw.setdefault("parameters_", parameters_)
        if routing_ is not None:
            kw["routing_"] = routing_
        driver = self._get_async_driver()
        return await driver.execute_query(query, **kw)

    async def async_verify_connectivity(self) -> None:
        """Verify connectivity asynchronously."""
        await self._get_async_driver().verify_connectivity()

    def run(
        self,
        query: str,
        parameters_: dict[str, Any] | None = None,
        routing_: str = "r",
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Run Cypher query and return records as list of dicts."""
        records, _, _ = self.execute_query(
            query, parameters_=parameters_, routing_=routing_, **kwargs
        )
        return [_record_to_dict(r) for r in records]

    async def async_run(
        self,
        query: str,
        parameters_: dict[str, Any] | None = None,
        routing_: str = "r",
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Run Cypher query asynchronously and return records."""
        records, _, _ = await self.async_execute_query(
            query, parameters_=parameters_, routing_=routing_, **kwargs
        )
        return [_record_to_dict(r) for r in records]

    async def async_close(self) -> None:
        """Close async driver."""
        if self._async_driver:
            await self._async_driver.close()
            self._async_driver = None

    def _get_entity_props(self, entity: BaseEntity) -> dict[str, Any]:
        """Get all entity properties including subclass fields."""
        props = entity.model_dump(exclude_none=True, by_alias=False)
        props.pop("entity_type", None)
        return _flatten_props(props)

    def _get_relation_props(self, relation: BaseRelation) -> dict[str, Any]:
        """Get all relation properties including subclass fields."""
        props = relation.model_dump(exclude_none=True, by_alias=False)
        props.pop("source_name", None)
        props.pop("target_name", None)
        props.pop("source_type", None)
        props.pop("target_type", None)
        props.pop("relation_type", None)
        return _flatten_props(props)

    def create_entity(self, entity: BaseEntity) -> None:
        """Create entity with all properties."""
        props = self._get_entity_props(entity)
        entity_type = (
            entity.entity_type.value
            if hasattr(entity.entity_type, "value")
            else str(entity.entity_type)
        )
        if props:
            query = f"CREATE (n:{entity_type} $props)"
            self.run(query, parameters_={"props": props}, routing_="w")
        else:
            query = f"CREATE (n:{entity_type} {{name: $name}})"
            self.run(query, parameters_={"name": entity.name}, routing_="w")

    def create_relation(self, relation: BaseRelation) -> None:
        """Create relation with all properties."""
        props = self._get_relation_props(relation)
        source_type = (
            relation.source_type.value
            if hasattr(relation.source_type, "value")
            else str(relation.source_type)
        )
        target_type = (
            relation.target_type.value
            if hasattr(relation.target_type, "value")
            else str(relation.target_type)
        )
        rel_type = (
            relation.relation_type.value
            if hasattr(relation.relation_type, "value")
            else str(relation.relation_type)
        )

        if props:
            query = (
                f"MATCH (source:{source_type} {{name: $source_name}}), (target:{target_type} {{name: $target_name}}) "
                f"CREATE (source)-[r:{rel_type} $props]->(target)"
            )
            params = {
                "source_name": relation.source_name,
                "target_name": relation.target_name,
                "props": props,
            }
            self.run(query, parameters_=params, routing_="w")
        else:
            query = (
                f"MATCH (source:{source_type} {{name: $source_name}}), (target:{target_type} {{name: $target_name}}) "
                f"CREATE (source)-[r:{rel_type}]->(target)"
            )
            params = {
                "source_name": relation.source_name,
                "target_name": relation.target_name,
            }
            self.run(query, parameters_=params, routing_="w")

    async def async_create_entity(self, entity: BaseEntity) -> None:
        """Create entity asynchronously with all properties."""
        props = self._get_entity_props(entity)
        entity_type = (
            entity.entity_type.value
            if hasattr(entity.entity_type, "value")
            else str(entity.entity_type)
        )
        if props:
            query = f"CREATE (n:{entity_type} $props)"
            await self.async_run(query, parameters_={"props": props}, routing_="w")
        else:
            query = f"CREATE (n:{entity_type} {{name: $name}})"
            await self.async_run(query, parameters_={"name": entity.name}, routing_="w")

    async def async_create_relation(self, relation: BaseRelation) -> None:
        """Create relation asynchronously with all properties."""
        props = self._get_relation_props(relation)
        source_type = (
            relation.source_type.value
            if hasattr(relation.source_type, "value")
            else str(relation.source_type)
        )
        target_type = (
            relation.target_type.value
            if hasattr(relation.target_type, "value")
            else str(relation.target_type)
        )
        rel_type = (
            relation.relation_type.value
            if hasattr(relation.relation_type, "value")
            else str(relation.relation_type)
        )

        if props:
            query = (
                f"MATCH (source:{source_type} {{name: $source_name}}), (target:{target_type} {{name: $target_name}}) "
                f"CREATE (source)-[r:{rel_type} $props]->(target)"
            )
            params = {
                "source_name": relation.source_name,
                "target_name": relation.target_name,
                "props": props,
            }
            await self.async_run(query, parameters_=params, routing_="w")
        else:
            query = (
                f"MATCH (source:{source_type} {{name: $source_name}}), (target:{target_type} {{name: $target_name}}) "
                f"CREATE (source)-[r:{rel_type}]->(target)"
            )
            params = {
                "source_name": relation.source_name,
                "target_name": relation.target_name,
            }
            await self.async_run(query, parameters_=params, routing_="w")
