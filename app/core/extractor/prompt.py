"""中文医疗场景下的 LangExtract 提示词（与 ``app.graph`` 对齐）。"""

from __future__ import annotations

import textwrap
from enum import Enum
from types import UnionType
from typing import Any, Union, get_args, get_origin

from pydantic.fields import FieldInfo

from app.graph._type import (
    ENTITY_TYPE_LABEL_ZH,
    RELATION_TYPE_LABEL_ZH,
    EntityType,
    RelationType,
)
from app.graph.base import BaseEntity, BaseRelation
from app.graph.entity import ENTITY_TYPE_MAPPING
from app.graph.relation import RELATION_TYPE_MAPPING

# LangExtract 的 extraction_class 取值（英文 snake_case，与存储/代码一致）
MEDICAL_ENTITY_CLASSES: tuple[str, ...] = tuple(
    sorted(e.value for e in EntityType if e != EntityType.UNKNOWN)
)

MEDICAL_RELATION_TYPES: tuple[str, ...] = tuple(
    sorted(r.value for r in RelationType if r != RelationType.UNKNOWN)
)

# extraction_text 对应图模型中的 name；下列字段由结构承载，勿在 attributes 重复堆砌
_SKIP_ENTITY_FIELD_NAMES: frozenset[str] = frozenset(
    {
        "entity_type",
        "name",
        "attributes",
    }
)

_SKIP_RELATION_FIELD_NAMES: frozenset[str] = frozenset(
    {
        "source_name",
        "target_name",
        "source_type",
        "target_type",
        "relation",
        "relation_type",
        "attributes",
    }
)

RELATION_ENDPOINT_GUIDE: dict[str, tuple[str, str]] = {
    RelationType.DISEASE_HAS_SYMPTOM.value: ("disease", "symptom"),
    RelationType.DISEASE_COMMON_DRUG.value: ("disease", "drug"),
    RelationType.DISEASE_RECOMMAND_DRUG.value: ("disease", "drug"),
    RelationType.DISEASE_BELONG_DEPARTMENT.value: ("disease", "department"),
    RelationType.DISEASE_ACOMPANY_DISEASE.value: ("disease", "disease"),
    RelationType.DISEASE_EAT_FOOD.value: ("disease", "food"),
    RelationType.DISEASE_NOTEAT_FOOD.value: ("disease", "food"),
    RelationType.DISEASE_RECOMMAND_FOOD.value: ("disease", "food"),
    RelationType.DISEASE_NEED_CHECK.value: ("disease", "check"),
    RelationType.DISEASE_NEED_TREATMENT.value: ("disease", "treatment"),
    RelationType.DRUG_RELATE_PRODUCER.value: ("drug", "producer"),
    RelationType.DEPARTMENT_BELONG_DEPARTMENT.value: ("department", "department"),
    RelationType.PATIENT_HAS_DIAGNOSIS.value: ("patient", "diagnosis"),
    RelationType.PATIENT_PRESCRIBED_MEDICATION.value: ("patient", "drug"),
    RelationType.PATIENT_HAS_ALLERGY.value: ("patient", "allergy"),
    RelationType.PATIENT_HAS_LAB_TEST.value: ("patient", "lab_test"),
    RelationType.PHYSICIAN_BELONGS_TO_DEPARTMENT.value: ("physician", "department"),
    RelationType.LAB_TEST_MAP_TO_CHECK.value: ("lab_test", "check"),
    RelationType.PROCEDURE_MAP_TO_CHECK.value: ("procedure", "check"),
    RelationType.PROCEDURE_MAP_TO_SURGERY.value: ("procedure", "surgery"),
    RelationType.PRESCRIPTION_REFERENCES_DRUG.value: ("prescription", "drug"),
    RelationType.DIAGNOSIS_MAPS_TO_DISEASE.value: ("diagnosis", "disease"),
}


def _unwrap_optional(annotation: Any) -> Any:
    origin = get_origin(annotation)
    if origin is Union:
        args = [a for a in get_args(annotation) if a is not type(None)]
        return args[0] if len(args) == 1 else annotation
    if origin is UnionType:
        args = [a for a in get_args(annotation) if a is not type(None)]
        return args[0] if len(args) == 1 else annotation
    return annotation


def _annotation_hint(annotation: Any) -> str:
    if annotation is None:
        return "字符串"
    ann = _unwrap_optional(annotation)
    if ann is str:
        return "字符串"
    if ann is int:
        return "整数"
    if ann is float:
        return "数值"
    if ann is bool:
        return "布尔"
    origin = get_origin(ann)
    if origin is list:
        inner = get_args(ann)
        return f"列表[{_annotation_hint(inner[0]) if inner else '任意'}]"
    try:
        if isinstance(ann, type) and issubclass(ann, Enum):
            vals = [str(e.value) for e in ann]
            return "枚举: " + ", ".join(vals[:12]) + ("…" if len(vals) > 12 else "")
    except TypeError:
        pass
    if hasattr(ann, "__name__"):
        return ann.__name__
    return str(ann)


def _field_line(fname: str, finfo: FieldInfo) -> str:
    req_zh = "必填" if finfo.is_required() else "可选"
    desc = (finfo.description or "").strip()
    hint = _annotation_hint(finfo.annotation)
    ex = finfo.examples
    ex_s = ""
    if ex is not None:
        ex_s = f" 示例={ex!r}"
    desc_part = f" — {desc}" if desc else ""
    return f"        • {fname}（{req_zh}，{hint}）{desc_part}{ex_s}"


def _entity_attribute_spec_lines() -> list[str]:
    lines: list[str] = []
    for key in sorted(ENTITY_TYPE_MAPPING.keys()):
        cls = ENTITY_TYPE_MAPPING[key]
        if not issubclass(cls, BaseEntity):
            continue
        label = ENTITY_TYPE_LABEL_ZH.get(key, key)
        sub_lines = [
            _field_line(n, f)
            for n, f in cls.model_fields.items()
            if n not in _SKIP_ENTITY_FIELD_NAMES
        ]
        if not sub_lines:
            lines.append(
                f"    [{key}]（{label}）extraction_text 为规范名称；无额外 schema 字段。"
            )
        else:
            lines.append(
                f"    [{key}]（{label}）extraction_text 对应图模型中的 name，下列字段放入 attributes（键名必须一致）："
            )
            lines.extend(sub_lines)
    return lines


def _relation_type_description(cls: type[BaseRelation]) -> str:
    finfo = cls.model_fields.get("relation_type")
    if finfo and finfo.description:
        return finfo.description.strip()
    return ""


def _relation_extra_field_lines(cls: type[BaseRelation]) -> list[str]:
    return [
        _field_line(n, f)
        for n, f in cls.model_fields.items()
        if n not in _SKIP_RELATION_FIELD_NAMES
    ]


def _relation_spec_lines() -> list[str]:
    lines: list[str] = []
    for rt in sorted(RELATION_TYPE_MAPPING.keys(), key=lambda x: x.value):
        cls = RELATION_TYPE_MAPPING[rt]
        rid = rt.value
        rzh = RELATION_TYPE_LABEL_ZH.get(rid, rid)
        ends = RELATION_ENDPOINT_GUIDE.get(rid)
        desc = _relation_type_description(cls)
        head = f"    [{rid}]（{rzh}）"
        if ends:
            head += f"source_type={ends[0]!r}, target_type={ends[1]!r}"
        if desc:
            head += f" — {desc}"
        lines.append(head)
        extras = _relation_extra_field_lines(cls)
        if extras:
            lines.append("        关系上额外 attributes（仅原文有据时填写；无则省略）：")
            lines.extend(extras)
    return lines


def medical_extraction_prompt() -> str:
    """完整中文指令：实体/关系类型 + 由 Pydantic 生成的属性说明。"""
    entity_lines = []
    for c in MEDICAL_ENTITY_CLASSES:
        zh = ENTITY_TYPE_LABEL_ZH.get(c, c)
        entity_lines.append(f"    - {c}（{zh}）")
    entity_class_block = "\n".join(entity_lines)
    entity_attr_block = "\n".join(_entity_attribute_spec_lines())
    relation_block = "\n".join(_relation_spec_lines())

    return textwrap.dedent(
        f"""
        你是中文医疗文本信息抽取助手，从给定文本中构建医疗知识图谱三元组（实体 + 关系）。

        总体要求：
        - 文本为中文临床记录为主；extraction_text 尽量为原文中的连续子串（勿改写、勿翻译）。
        - 实体行：extraction_class 必须为下列英文键之一（与系统枚举一致）；结构化字段放在 attributes 中，键名与下表完全一致。
        - 可选字段：原文无依据则不要输出该键；禁止编造 ICD、LOINC、病历号等。
        - extraction_text 即该实体在图中的规范名称（对应 schema 的 name），不要在 attributes 里再用其它键重复同一字符串。
        - 输出一个 JSON 对象，顶层必须有键 "extractions"（数组）。禁止省略 "extractions"。

        实体类型（extraction_class = 英文键）：
{entity_class_block}

        各实体类型的 attributes 字段说明：
{entity_attr_block}

        关系（放在实体之后，按证据在文中首次出现的顺序）：
        - extraction_class 固定为：Relationship
        - extraction_text：支持该关系的原文证据子串
        - attributes 必须包含：source, target, type, source_type, target_type
            · source / target 的字符串必须与所指实体的 extraction_text 一致
            · type 必须为下列关系 id 之一（英文，与枚举一致）
            · source_type / target_type 必须与该关系定义一致（见下表）
            · 若该关系类型下列出了额外字段，仅在有文本依据时写入 attributes

{relation_block}

        其它规则：
        - 同一实体类型、同一规范名称只保留一条实体抽取（去重）。
        - 不做临床推理：仅抽取文中明确或可直读的信息，不推断未写明的诊断或用药。
        """
    ).strip()
