from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ._type import EntityType, RelationType


class BaseEntity(BaseModel):
    """医疗知识图谱实体基类（不含数据库主键与置信度，避免与抽取字段冗余）。"""

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        use_enum_values=False,
    )

    name: str = Field(..., description="实体规范名称（与原文 mention 对应）", examples=["2型糖尿病", "二甲双胍"])
    entity_type: EntityType = Field(..., description="实体类型枚举")
    description: Optional[str] = Field(None, description="补充说明（原文有据时填写）")
    source_text: Optional[str] = Field(None, description="原文中的提及片段（与抽取对齐）")
    attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description="其它结构化属性（与 LangExtract attributes 对齐）",
    )

    @field_validator("entity_type", mode="before")
    @classmethod
    def parse_entity_type(cls, v: Union[str, EntityType]) -> EntityType:
        if isinstance(v, EntityType):
            return v
        try:
            return EntityType(v.lower())
        except ValueError:
            return EntityType.UNKNOWN


class BaseRelation(BaseModel):
    """医疗知识图谱关系基类（用名称+类型关联实体，不用数值 id）。"""

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        use_enum_values=False,
    )

    source_name: str = Field(..., description="头实体名称（与对应实体的 name / extraction_text 一致）")
    target_name: str = Field(..., description="尾实体名称")
    source_type: EntityType = Field(..., description="头实体类型")
    target_type: EntityType = Field(..., description="尾实体类型")
    relation: str = Field(..., description="关系可读名称（可与 relation_type 取值一致）")
    relation_type: RelationType = Field(..., description="关系类型枚举")
    source_text: Optional[str] = Field(None, description="支持该关系的原文证据片段")
    attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description="关系上的附加属性（如剂量、严重程度等）",
    )

    @field_validator("relation_type", mode="before")
    @classmethod
    def parse_relation_type(cls, v: Union[str, RelationType]) -> RelationType:
        if isinstance(v, RelationType):
            return v
        try:
            return RelationType(v.lower())
        except ValueError:
            return RelationType.UNKNOWN

    @field_validator("source_type", mode="before")
    @classmethod
    def parse_source_type(cls, v: Union[str, EntityType]) -> EntityType:
        if isinstance(v, EntityType):
            return v
        try:
            return EntityType(v.lower())
        except ValueError:
            return EntityType.UNKNOWN

    @field_validator("target_type", mode="before")
    @classmethod
    def parse_target_type(cls, v: Union[str, EntityType]) -> EntityType:
        if isinstance(v, EntityType):
            return v
        try:
            return EntityType(v.lower())
        except ValueError:
            return EntityType.UNKNOWN


class BaseGraph(BaseModel):
    nodes: List[BaseEntity] = []
    edges: List[BaseRelation] = []
