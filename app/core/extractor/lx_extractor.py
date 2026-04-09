"""Orchestrate LangExtract: provider + prompt + examples → medical KG graph."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import langextract as lx
from langextract.core import data as lx_data

from app.config import get_runtime_config
from app.graph.base import BaseGraph

from .example import medical_few_shot_examples
from .mapping import annotated_document_to_base_graph
from .prompt import medical_extraction_prompt
from .provider import create_openai_compatible_langextract_model


@dataclass
class MedicalLangExtractResult:
    """Raw LangExtract output plus graph view."""

    annotated: lx_data.AnnotatedDocument
    graph: BaseGraph


def extract_medical_knowledge_graph(
    text: str,
    *,
    model: Any | None = None,
    max_char_buffer: int | None = None,
    max_workers: int = 10,
    batch_length: int = 10,
) -> MedicalLangExtractResult:
    """
    Run LangExtract on clinical or biomedical text using the medical schema
    from ``app.graph.medical``.
    """
    runtime_config = get_runtime_config()
    lm = model or create_openai_compatible_langextract_model()
    buf = max_char_buffer if max_char_buffer is not None else runtime_config.extractor.chunk_size

    annotated = lx.extract(
        text_or_documents=text,
        prompt_description=medical_extraction_prompt(),
        examples=medical_few_shot_examples(),
        model=lm,
        use_schema_constraints=False,
        fence_output=False,
        max_char_buffer=buf,
        max_workers=max_workers,
        batch_length=batch_length,
    )
    if not isinstance(annotated, lx_data.AnnotatedDocument):
        raise TypeError("Expected a single AnnotatedDocument for string input")
    graph = annotated_document_to_base_graph(annotated)
    return MedicalLangExtractResult(annotated=annotated, graph=graph)
