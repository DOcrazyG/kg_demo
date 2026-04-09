"""KG extraction demo using an OpenAI-compatible HTTP API (Chat Completions).

See LangExtract docs: https://github.com/google/langextract#using-openai-models
The OpenAI driver uses the official ``openai`` client; ``base_url`` points at any
OpenAI-compatible gateway (vLLM, LiteLLM, One API, etc.).
"""

from pathlib import Path

import langextract as lx
import textwrap
from langextract.factory import ModelConfig, create_model

from app.config import get_provider_config, get_runtime_config

provider_config = get_provider_config()
runtime_config = get_runtime_config()

prompt = textwrap.dedent(
    """
    Extract entities and relationships for a knowledge graph.

    Rules:
    - For every distinct person, company, and place mentioned, emit one extraction
      with extraction_class Person, Organization, or Location. Use exact spans from
      the source text (verbatim, no paraphrase).
    - Then emit Relationship extractions for ties you can justify from the text
      (Works_At, Located_In, Knows). extraction_text must be a verbatim substring.
    - List extractions in order of first appearance in the text.
    - Output a single JSON object with top-level key "extractions" (array). Each
      item must include extraction_class, extraction_text, and attributes where
      relevant. Do not omit "extractions" or use a different top-level shape.
    """
).strip()

examples = [
    lx.data.ExampleData(
        text="Elon Musk founded SpaceX in Hawthorne, California.",
        extractions=[
            lx.data.Extraction(extraction_class="Person", extraction_text="Elon Musk", attributes={"role": "Founder"}),
            lx.data.Extraction(
                extraction_class="Organization", extraction_text="SpaceX", attributes={"type": "Private"}
            ),
            lx.data.Extraction(extraction_class="Location", extraction_text="Hawthorne", attributes={"kind": "city"}),
            lx.data.Extraction(
                extraction_class="Location", extraction_text="California", attributes={"kind": "region"}
            ),
            lx.data.Extraction(
                extraction_class="Relationship",
                extraction_text="Elon Musk founded SpaceX",
                attributes={"source": "Elon Musk", "target": "SpaceX", "type": "Works_At"},
            ),
            lx.data.Extraction(
                extraction_class="Relationship",
                extraction_text="SpaceX in Hawthorne",
                attributes={"source": "SpaceX", "target": "Hawthorne", "type": "Located_In"},
            ),
        ],
    ),
    lx.data.ExampleData(
        text="Larry Page works at Google in Mountain View.",
        extractions=[
            lx.data.Extraction(extraction_class="Person", extraction_text="Larry Page", attributes={}),
            lx.data.Extraction(extraction_class="Organization", extraction_text="Google", attributes={}),
            lx.data.Extraction(
                extraction_class="Location", extraction_text="Mountain View", attributes={"kind": "city"}
            ),
            lx.data.Extraction(
                extraction_class="Relationship",
                extraction_text="Larry Page works at Google",
                attributes={"source": "Larry Page", "target": "Google", "type": "Works_At"},
            ),
            lx.data.Extraction(
                extraction_class="Relationship",
                extraction_text="Google in Mountain View",
                attributes={"source": "Google", "target": "Mountain View", "type": "Located_In"},
            ),
        ],
    ),
]

# OpenAI-compatible endpoint: same env as the rest of the app (OPENAI_API_KEY, OPENAI_API_BASE).
# Explicit provider is required when model_id is not gpt-* (LangExtract only auto-routes those patterns).
provider_kwargs: dict = {
    "api_key": provider_config.llm.api_key,
    "temperature": runtime_config.llm.temperature,
    "max_output_tokens": runtime_config.llm.max_tokens,
}
if provider_config.llm.api_base:
    provider_kwargs["base_url"] = provider_config.llm.api_base

config = ModelConfig(
    model_id=runtime_config.llm.model,
    provider="OpenAILanguageModel",
    provider_kwargs=provider_kwargs,
)
# OpenAI path does not use LangExtract schema constraints yet (per upstream README).
model = create_model(config, use_schema_constraints=False)

# LangExtract only auto-fetches http(s) URLs. A bare string is treated as the
# document body, so "test_document.txt" was analyzed as 17 characters of text
# (hence empty extractions). Read the file explicitly.
_document_path = Path(__file__).resolve().parent / "test_document.txt"
input_text = _document_path.read_text(encoding="utf-8")

result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model=model,
    use_schema_constraints=False,
    # OpenAI provider uses JSON response_format; output is raw JSON, not ```json fences.
    fence_output=False,
    # Avoid splitting short articles across chunks (reduces parse failures and lost entities).
    max_char_buffer=runtime_config.extractor.chunk_size,
)
# print(f"result type: {type(result)}")
# print(f"result: {result}")
print(f"extractions: {result.extractions}")

lx.io.save_annotated_documents([result], output_name="app/demo/kg_extractions.jsonl", output_dir=".")

lx.visualize("app/demo/kg_extractions.jsonl")
