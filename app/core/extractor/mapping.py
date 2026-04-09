"""Convert LangExtract structures into ``app.graph`` models."""

from __future__ import annotations

from langextract.core import data as lx_data

from app.graph.base import BaseEntity, BaseGraph, BaseRelation
from app.graph._type import EntityType, RelationType


def coerce_lx_attribute(value: str | list[str] | None) -> str | None:
    """Normalize LangExtract attribute values (often strings; sometimes lists)."""
    if value is None:
        return None
    if isinstance(value, list):
        return ", ".join(str(x) for x in value)
    return str(value)


def parse_entity_type_label(raw: str) -> EntityType:
    """Map extraction_class string to ``EntityType`` (unknown → ``UNKNOWN``)."""
    key = raw.strip().lower()
    if key in ("relationship", "relation"):
        return EntityType.UNKNOWN
    try:
        return EntityType(key)
    except ValueError:
        return EntityType.UNKNOWN


def parse_relation_type_label(raw: str | None) -> RelationType:
    """Map Relationship.attributes[\"type\"] to ``RelationType``."""
    if not raw:
        return RelationType.UNKNOWN
    key = str(raw).strip().lower()
    try:
        return RelationType(key)
    except ValueError:
        return RelationType.UNKNOWN


def annotated_document_to_base_graph(doc: lx_data.AnnotatedDocument) -> BaseGraph:
    """Map LangExtract ``AnnotatedDocument`` to ``BaseGraph``."""
    nodes: list[BaseEntity] = []
    edges: list[BaseRelation] = []
    seen_entity_keys: set[tuple[str, str]] = set()

    for ex in doc.extractions or []:
        cls_raw = (ex.extraction_class or "").strip()
        if cls_raw.lower() == "relationship":
            attrs = ex.attributes or {}
            st = parse_relation_type_label(coerce_lx_attribute(attrs.get("type")))
            if st == RelationType.UNKNOWN:
                continue
            src = coerce_lx_attribute(attrs.get("source")) or ""
            tgt = coerce_lx_attribute(attrs.get("target")) or ""
            if not src or not tgt:
                continue
            src_t = parse_entity_type_label(coerce_lx_attribute(attrs.get("source_type")) or "")
            tgt_t = parse_entity_type_label(coerce_lx_attribute(attrs.get("target_type")) or "")
            extra = {
                k: v
                for k, v in attrs.items()
                if k
                not in ("type", "source", "target", "source_type", "target_type")
            }
            edges.append(
                BaseRelation(
                    source_name=src,
                    target_name=tgt,
                    source_type=src_t,
                    target_type=tgt_t,
                    relation=st.value,
                    relation_type=st,
                    source_text=ex.extraction_text,
                    attributes=extra if isinstance(extra, dict) else {},
                )
            )
            continue

        et = parse_entity_type_label(cls_raw)
        name = (ex.extraction_text or "").strip()
        if not name:
            continue
        dedupe_key = (name.lower(), et.value)
        if dedupe_key in seen_entity_keys:
            continue
        seen_entity_keys.add(dedupe_key)
        attrs = dict(ex.attributes) if ex.attributes else {}
        nodes.append(
            BaseEntity(
                name=name,
                entity_type=et,
                source_text=ex.extraction_text,
                attributes=attrs,
            )
        )

    return BaseGraph(nodes=nodes, edges=edges)
