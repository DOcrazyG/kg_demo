from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ._type import ConfidenceLevel, EntityType, RelationType


class BaseEntity(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        use_enum_values=False,
    )

    id: Optional[int] = Field(None, description="Unique entity identifier")
    name: str = Field(..., description="Entity name", examples=["高血压", "阿莫西林"])
    entity_type: EntityType = Field(..., description="Entity type")
    description: Optional[str] = Field(None, description="Entity description")
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Extraction confidence [0, 1]",
    )
    confidence_level: ConfidenceLevel = Field(
        default=ConfidenceLevel.HIGH,
        description="Confidence level category",
    )
    source_text: Optional[str] = Field(None, description="Source text mention")
    attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional attributes",
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

    @field_validator("confidence_level", mode="before")
    @classmethod
    def parse_confidence_level(cls, v: Union[str, ConfidenceLevel]) -> ConfidenceLevel:
        if isinstance(v, ConfidenceLevel):
            return v
        try:
            return ConfidenceLevel(v.lower())
        except ValueError:
            return ConfidenceLevel.UNKNOWN


class BaseRelation(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        use_enum_values=False,
    )

    id: Optional[int] = Field(None, description="Unique relation identifier")
    source_id: Optional[int] = Field(None, description="Source entity ID")
    target_id: Optional[int] = Field(None, description="Target entity ID")
    source_name: str = Field(..., description="Source entity name")
    target_name: str = Field(..., description="Target entity name")
    source_type: EntityType = Field(..., description="Source entity type")
    target_type: EntityType = Field(..., description="Target entity type")
    relation: str = Field(..., description="Relation name")
    relation_type: RelationType = Field(..., description="Relation type")
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Extraction confidence [0, 1]",
    )
    source_text: Optional[str] = Field(None, description="Supporting text from source")
    attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional relation attributes",
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
