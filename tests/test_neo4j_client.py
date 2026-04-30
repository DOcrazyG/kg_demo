"""Tests for Neo4jClient."""

import pytest

from app.db.neo4j_client import Neo4jClient, _flatten_props
from app.graph import BaseEntity, BaseRelation
from app.graph._type import EntityType, RelationType


class TestFlattenProps:
    def test_primitive_values(self):
        assert _flatten_props({"a": 1, "b": "x", "c": 1.0, "d": True}) == {
            "a": 1,
            "b": "x",
            "c": 1.0,
            "d": True,
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

        cfg = Neo4jProviderConfig(
            uri="bolt://localhost:7687", user="neo4j", password="x", database="test"
        )
        client = Neo4jClient(cfg)
        assert client.database == "test"

    def test_init_default_config(self):
        client = Neo4jClient()
        assert client.database == "neo4j"  # default from env/config

    def test_sync_context_manager_closes_on_exit(self):
        from app.config.provider_config import Neo4jProviderConfig

        cfg = Neo4jProviderConfig(
            uri="bolt://localhost:7687", user="neo4j", password="x", database="test"
        )
        with Neo4jClient(cfg) as client:
            assert client.database == "test"
        assert client._sync_driver is None

    @pytest.mark.asyncio
    async def test_async_context_manager_closes_on_exit(self):
        from app.config.provider_config import Neo4jProviderConfig

        cfg = Neo4jProviderConfig(
            uri="bolt://localhost:7687", user="neo4j", password="x", database="test"
        )
        async with Neo4jClient(cfg) as client:
            assert client.database == "test"
        assert client._async_driver is None

    def test_get_entity_props_with_base_entity(self):
        from app.config.provider_config import Neo4jProviderConfig

        cfg = Neo4jProviderConfig(
            uri="bolt://localhost:7687", user="neo4j", password="x", database="test"
        )
        client = Neo4jClient(cfg)

        entity = BaseEntity(name="TestEntity", entity_type=EntityType.DISEASE)
        props = client._get_entity_props(entity)

        assert "name" in props
        assert props["name"] == "TestEntity"
        assert "entity_type" not in props

    def test_get_entity_props_with_subclass(self):
        from app.config.provider_config import Neo4jProviderConfig
        from app.graph.entity import Disease

        cfg = Neo4jProviderConfig(
            uri="bolt://localhost:7687", user="neo4j", password="x", database="test"
        )
        client = Neo4jClient(cfg)

        disease = Disease(name="2型糖尿病", code="E11.9", alias="糖尿病")
        props = client._get_entity_props(disease)

        assert props["name"] == "2型糖尿病"
        assert props["code"] == "E11.9"
        assert props["alias"] == "糖尿病"
        assert "entity_type" not in props

    def test_get_entity_props_excludes_none(self):
        from app.config.provider_config import Neo4jProviderConfig
        from app.graph.entity import Disease

        cfg = Neo4jProviderConfig(
            uri="bolt://localhost:7687", user="neo4j", password="x", database="test"
        )
        client = Neo4jClient(cfg)

        disease = Disease(name="糖尿病", code=None)
        props = client._get_entity_props(disease)

        assert props["name"] == "糖尿病"
        assert "code" not in props

    def test_get_relation_props_with_base_relation(self):
        from app.config.provider_config import Neo4jProviderConfig

        cfg = Neo4jProviderConfig(
            uri="bolt://localhost:7687", user="neo4j", password="x", database="test"
        )
        client = Neo4jClient(cfg)

        relation = BaseRelation(
            source_name="患者A",
            target_name="糖尿病",
            source_type=EntityType.PATIENT,
            target_type=EntityType.DISEASE,
            relation="诊断为",
            relation_type=RelationType.PATIENT_HAS_DIAGNOSIS,
        )
        props = client._get_relation_props(relation)

        assert props["relation"] == "诊断为"
        assert "source_name" not in props
        assert "target_name" not in props
        assert "source_type" not in props
        assert "target_type" not in props
        assert "relation_type" not in props

    def test_get_relation_props_with_subclass(self):
        from app.config.provider_config import Neo4jProviderConfig
        from app.graph._type import Severity
        from app.graph.relation import PatientHasDiagnosis

        cfg = Neo4jProviderConfig(
            uri="bolt://localhost:7687", user="neo4j", password="x", database="test"
        )
        client = Neo4jClient(cfg)

        relation = PatientHasDiagnosis(
            source_name="患者A",
            target_name="糖尿病",
            source_type=EntityType.PATIENT,
            target_type=EntityType.DISEASE,
            relation="诊断为",
            severity=Severity.SEVERE,
            is_primary=True,
        )
        props = client._get_relation_props(relation)

        assert props["relation"] == "诊断为"
        assert props["severity"] == "重度"
        assert props["is_primary"]
        assert "source_name" not in props
        assert "relation_type" not in props
