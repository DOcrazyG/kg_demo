"""
Neo4j 图数据库客户端 - 同步与异步调用.

参考 neo4j-graphrag-python、官方 neo4j-python-driver 文档实现。
支持：执行 Cypher、写入实体关系、连通性校验。
"""

from typing import Any

from neo4j import AsyncGraphDatabase, GraphDatabase

from app.config.provider_config import Neo4jProviderConfig


def _flatten_props(props: dict[str, Any]) -> dict[str, Any]:
    """将 props 展平为 Neo4j 兼容的键值对（跳过嵌套 dict/list、None）。"""
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
        elif isinstance(v, list) and v and all(isinstance(x, (str, int, float, bool)) for x in v):
            out[k] = v
    return out


def _record_to_dict(record: Any) -> dict[str, Any]:
    """将 neo4j.Record 转为普通 dict（处理 Node/Relationship 等类型）."""
    if hasattr(record, "data"):
        return record.data()
    return dict(record)


class Neo4jClient:
    """
    Neo4j 图数据库客户端，提供同步与异步接口，支持上下文管理。

    用法:
        # 同步，单次查询后自动关闭
        with Neo4jClient(config) as client:
            records = client.run("MATCH (n) RETURN n LIMIT 10")

        # 异步，单次查询后自动关闭
        async with Neo4jClient(config) as client:
            records = await client.arun("MATCH (n) RETURN n LIMIT 10")

        # 非上下文用法（需手动 close/aclose）
        client = Neo4jClient(config)
        records = client.run("MATCH (n) RETURN n LIMIT 10")
        client.close()
    """

    def __init__(self, config: Neo4jProviderConfig | None = None):
        """
        Args:
            config: Neo4j 连接配置，默认从 get_provider_config().neo4j 获取
        """
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

    # ---------- 上下文管理 ----------

    def __enter__(self) -> "Neo4jClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    async def __aenter__(self) -> "Neo4jClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.aclose()

    # ---------- 同步接口 ----------

    def execute_query(
        self,
        query: str,
        parameters_: dict[str, Any] | None = None,
        routing_: str | None = None,
        **kwargs: Any,
    ) -> tuple[list[Any], Any, list[str]]:
        """
        同步执行 Cypher 查询。

        Args:
            query: Cypher 查询
            parameters_: 查询参数（与 kwargs 中的参数可并存，kwargs 优先）
            routing_: "r" 表示只读路由
            **kwargs: 查询参数或 driver 配置（database_, parameters_ 等）

        Returns:
            (records, summary, keys)
        """
        kw = dict(kwargs)
        kw.setdefault("database_", self.database)
        if parameters_ is not None:
            kw.setdefault("parameters_", parameters_)
        if routing_ is not None:
            kw["routing_"] = routing_
        driver = self._get_sync_driver()
        return driver.execute_query(query, **kw)

    def verify_connectivity(self) -> None:
        """同步校验连接."""
        self._get_sync_driver().verify_connectivity()

    def close(self) -> None:
        """关闭同步驱动。异步应用中请使用 aclose() 关闭异步驱动."""
        if self._sync_driver:
            self._sync_driver.close()
            self._sync_driver = None

    # ---------- 异步接口 ----------

    async def aexecute_query(
        self,
        query: str,
        parameters_: dict[str, Any] | None = None,
        routing_: str | None = None,
        **kwargs: Any,
    ) -> tuple[list[Any], Any, list[str]]:
        """
        异步执行 Cypher 查询。

        Args:
            query: Cypher 查询
            parameters_: 查询参数
            routing_: "r" 表示只读路由
            **kwargs: 查询参数或 driver 配置

        Returns:
            (records, summary, keys)
        """
        kw = dict(kwargs)
        kw.setdefault("database_", self.database)
        if parameters_ is not None:
            kw.setdefault("parameters_", parameters_)
        if routing_ is not None:
            kw["routing_"] = routing_
        driver = self._get_async_driver()
        return await driver.execute_query(query, **kw)

    async def averify_connectivity(self) -> None:
        """异步校验连接."""
        await self._get_async_driver().verify_connectivity()

    def run(
        self,
        query: str,
        parameters_: dict[str, Any] | None = None,
        routing_: str = "r",
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        同步执行 Cypher 并返回记录列表（每条为 dict）。

        常用于 QA 查询：client.run("MATCH (n) RETURN n.name AS name LIMIT 10")
        """
        records, _, _ = self.execute_query(
            query, parameters_=parameters_, routing_=routing_, **kwargs
        )
        return [_record_to_dict(r) for r in records]

    async def arun(
        self,
        query: str,
        parameters_: dict[str, Any] | None = None,
        routing_: str = "r",
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """异步执行 Cypher 并返回记录列表."""
        records, _, _ = await self.aexecute_query(
            query, parameters_=parameters_, routing_=routing_, **kwargs
        )
        return [_record_to_dict(r) for r in records]

    async def aclose(self) -> None:
        """关闭异步驱动."""
        if self._async_driver:
            await self._async_driver.close()
            self._async_driver = None

    # ---------- 知识图谱专用 ----------

    def create_entities_and_relations(
        self,
        entities: list[dict[str, Any]],
        relations: list[dict[str, Any]],
    ) -> dict[str, int]:
        """
        同步将实体和关系写入 Neo4j。

        Args:
            entities: [{"type": "Person", "name": "张三", "props": {...}}, ...]
            relations: [{"from": "张三", "to": "公司A", "type": "WORKS_AT", "from_type": "...", "to_type": "...", "props": {}}, ...]

        Returns:
            {"entities_created": n, "relations_created": m}
        """
        driver = self._get_sync_driver()
        total_nodes = 0
        total_rels = 0

        # 写入实体
        for e in entities:
            label = str(e.get("type", "Entity")).replace(" ", "_")
            name = str(e.get("name", "")).strip()
            if not name:
                continue
            props = _flatten_props(e.get("props") or {})
            query = "MERGE (n:" + label + " {name: $name})"
            if props:
                query += " SET n += $props"
            params = {"name": name, "database_": self.database}
            if props:
                params["props"] = props
            driver.execute_query(query, **params)
            total_nodes += 1

        # 写入关系
        for r in relations:
            from_name = str(r.get("from", "")).strip()
            to_name = str(r.get("to", "")).strip()
            rel_type = str(r.get("type", "RELATED_TO")).replace(" ", "_").upper()
            from_label = str(r.get("from_type", "Entity")).replace(" ", "_")
            to_label = str(r.get("to_type", "Entity")).replace(" ", "_")
            if not from_name or not to_name:
                continue
            props = _flatten_props(r.get("props") or {})
            query = f"""
                MATCH (a:{from_label} {{name: $from_name}})
                MATCH (b:{to_label} {{name: $to_name}})
                MERGE (a)-[r:{rel_type}]->(b)
                """
            if props:
                query += " SET r += $props"
            params = {"from_name": from_name, "to_name": to_name, "database_": self.database}
            if props:
                params["props"] = props
            driver.execute_query(query, **params)
            total_rels += 1

        return {"entities_created": total_nodes, "relations_created": total_rels}

    async def acreate_entities_and_relations(
        self,
        entities: list[dict[str, Any]],
        relations: list[dict[str, Any]],
    ) -> dict[str, int]:
        """异步将实体和关系写入 Neo4j."""
        driver = self._get_async_driver()
        total_nodes = 0
        total_rels = 0

        for e in entities:
            label = str(e.get("type", "Entity")).replace(" ", "_")
            name = str(e.get("name", "")).strip()
            if not name:
                continue
            props = _flatten_props(e.get("props") or {})
            query = "MERGE (n:" + label + " {name: $name})"
            if props:
                query += " SET n += $props"
            params = {"name": name, "database_": self.database}
            if props:
                params["props"] = props
            await driver.execute_query(query, **params)
            total_nodes += 1

        for r in relations:
            from_name = str(r.get("from", "")).strip()
            to_name = str(r.get("to", "")).strip()
            rel_type = str(r.get("type", "RELATED_TO")).replace(" ", "_").upper()
            from_label = str(r.get("from_type", "Entity")).replace(" ", "_")
            to_label = str(r.get("to_type", "Entity")).replace(" ", "_")
            if not from_name or not to_name:
                continue
            props = _flatten_props(r.get("props") or {})
            query = f"""
                MATCH (a:{from_label} {{name: $from_name}})
                MATCH (b:{to_label} {{name: $to_name}})
                MERGE (a)-[r:{rel_type}]->(b)
                """
            if props:
                query += " SET r += $props"
            params = {"from_name": from_name, "to_name": to_name, "database_": self.database}
            if props:
                params["props"] = props
            await driver.execute_query(query, **params)
            total_rels += 1

        return {"entities_created": total_nodes, "relations_created": total_rels}
