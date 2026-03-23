"""Tests for Neo4jClient."""

import pytest

from app.db.neo4j_client import Neo4jClient, _flatten_props


class TestFlattenProps:
    def test_primitive_values(self):
        assert _flatten_props({"a": 1, "b": "x", "c": 1.0, "d": True}) == {
            "a": 1, "b": "x", "c": 1.0, "d": True
        }

    def test_skips_none(self):
        assert _flatten_props({"a": 1, "b": None}) == {"a": 1}

    def test_nested_dict_flattened(self):
        assert _flatten_props({"outer": {"inner": 42}}) == {"outer_inner": 42}

    def test_list_of_primitives_kept(self):
        assert _flatten_props({"tags": ["a", "b"]}) == {"tags": ["a", "b"]}

    def test_empty_dict(self):
        assert _flatten_props({}) == {}


class TestNeo4jClient:
    """Neo4jClient unit tests (no DB required)."""

    def test_init_with_config(self):
        from app.config.provider_config import Neo4jProviderConfig
        cfg = Neo4jProviderConfig(uri="bolt://localhost:7687", user="neo4j", password="x", database="test")
        client = Neo4jClient(cfg)
        assert client.database == "test"

    def test_init_default_config(self):
        client = Neo4jClient()
        assert client.database == "neo4j"  # default from env/config

    def test_sync_context_manager_closes_on_exit(self):
        from app.config.provider_config import Neo4jProviderConfig
        cfg = Neo4jProviderConfig(uri="bolt://localhost:7687", user="neo4j", password="x", database="test")
        with Neo4jClient(cfg) as client:
            assert client.database == "test"
        assert client._sync_driver is None

    @pytest.mark.asyncio
    async def test_async_context_manager_closes_on_exit(self):
        from app.config.provider_config import Neo4jProviderConfig
        cfg = Neo4jProviderConfig(uri="bolt://localhost:7687", user="neo4j", password="x", database="test")
        async with Neo4jClient(cfg) as client:
            assert client.database == "test"
        assert client._async_driver is None
