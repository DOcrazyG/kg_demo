"""Extract entities and relations from text."""

from .example import medical_few_shot_examples
from .lx_extractor import MedicalLangExtractResult, extract_medical_knowledge_graph
from .mapping import (
    annotated_document_to_base_graph,
    coerce_lx_attribute,
    parse_entity_type_label,
    parse_relation_type_label,
)
from .prompt import (
    MEDICAL_ENTITY_CLASSES,
    MEDICAL_RELATION_TYPES,
    medical_extraction_prompt,
)
from .provider import create_openai_compatible_langextract_model

__all__ = [
    "MedicalLangExtractResult",
    "annotated_document_to_base_graph",
    "coerce_lx_attribute",
    "create_openai_compatible_langextract_model",
    "extract_medical_knowledge_graph",
    "MEDICAL_ENTITY_CLASSES",
    "MEDICAL_RELATION_TYPES",
    "medical_extraction_prompt",
    "medical_few_shot_examples",
    "parse_entity_type_label",
    "parse_relation_type_label",
]
