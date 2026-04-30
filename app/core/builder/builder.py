"""Build the graph from pydantic models"""

from app.db import Neo4jClient
from app.graph import BaseEntity, BaseGraph, BaseRelation


class GraphBuilder:
    """Build the graph from the entity and relation."""

    def __init__(self, graph: BaseGraph, Neo4j: Neo4jClient):
        self.graph = graph
        self.neo4j = Neo4j

    async def build(self):
        """Build the graph from the entity and relation."""
        await self.add_entities(self.graph.nodes)
        await self.add_relations(self.graph.edges)
        return self.graph

    async def add_entities(self, nodes: list[BaseEntity]):
        """Add entities to the graph."""
        for node in nodes:
            await self.neo4j.async_create_entity(node)

    async def add_relations(self, edges: list[BaseRelation]):
        """Add relations to the graph."""
        for edge in edges:
            await self.neo4j.async_create_relation(edge)
