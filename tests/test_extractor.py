"""``app.core.extractor``：按模块分组的单元测试（单文件、多类）。"""

from unittest.mock import MagicMock, patch

import langextract as lx
from langextract.core.data import AnnotatedDocument, Extraction

import app.core.extractor as extractor_pkg
from app.core.extractor.example import medical_few_shot_examples
from app.core.extractor.mapping import (
    annotated_document_to_base_graph,
    coerce_lx_attribute,
    parse_entity_type_label,
    parse_relation_type_label,
)
from app.core.extractor.prompt import (
    MEDICAL_ENTITY_CLASSES,
    MEDICAL_RELATION_TYPES,
    RELATION_ENDPOINT_GUIDE,
    medical_extraction_prompt,
)
from app.core.extractor.provider import create_openai_compatible_langextract_model
from app.graph._type import EntityType, RelationType


class TestExtractorMapping:
    """``mapping.py``：LangExtract → BaseGraph 与解析辅助函数。"""

    def test_coerce_lx_attribute(self):
        assert coerce_lx_attribute(None) is None
        assert coerce_lx_attribute("a") == "a"
        assert coerce_lx_attribute(["x", "y"]) == "x, y"

    def test_parse_entity_type_label(self):
        assert parse_entity_type_label("disease") == EntityType.DISEASE
        assert parse_entity_type_label("diagnosis") == EntityType.DIAGNOSIS
        assert parse_entity_type_label("Relationship") == EntityType.UNKNOWN
        assert parse_entity_type_label("not_a_type") == EntityType.UNKNOWN

    def test_parse_relation_type_label(self):
        assert parse_relation_type_label("disease_has_symptom") == RelationType.DISEASE_HAS_SYMPTOM
        assert parse_relation_type_label(None) == RelationType.UNKNOWN
        assert parse_relation_type_label("bad") == RelationType.UNKNOWN

    def test_annotated_document_to_base_graph_entities_and_relations(self):
        doc = AnnotatedDocument(
            text="患者诊断哮喘，使用沙丁胺醇吸入。",
            extractions=[
                Extraction(extraction_class="disease", extraction_text="哮喘", attributes={}),
                Extraction(extraction_class="drug", extraction_text="沙丁胺醇", attributes={}),
                Extraction(
                    extraction_class="Relationship",
                    extraction_text="哮喘，使用沙丁胺醇",
                    attributes={
                        "source": "哮喘",
                        "target": "沙丁胺醇",
                        "type": "disease_common_drug",
                        "source_type": "disease",
                        "target_type": "drug",
                    },
                ),
            ],
        )
        g = annotated_document_to_base_graph(doc)
        assert len(g.nodes) == 2
        assert {n.name for n in g.nodes} == {"哮喘", "沙丁胺醇"}
        assert any(n.entity_type == EntityType.DISEASE for n in g.nodes)
        assert any(n.entity_type == EntityType.DRUG for n in g.nodes)
        assert len(g.edges) == 1
        assert g.edges[0].relation_type == RelationType.DISEASE_COMMON_DRUG
        assert g.edges[0].source_name == "哮喘" and g.edges[0].target_name == "沙丁胺醇"

    def test_skips_unknown_relation_type(self):
        doc = AnnotatedDocument(
            text="x",
            extractions=[
                Extraction(
                    extraction_class="Relationship",
                    extraction_text="x",
                    attributes={
                        "source": "a",
                        "target": "b",
                        "type": "not_a_real_relation",
                        "source_type": "disease",
                        "target_type": "symptom",
                    },
                ),
            ],
        )
        g = annotated_document_to_base_graph(doc)
        assert g.edges == []

    def test_entity_dedupe_by_name_and_type(self):
        doc = AnnotatedDocument(
            text="哮喘 哮喘",
            extractions=[
                Extraction(extraction_class="disease", extraction_text="哮喘", attributes={}),
                Extraction(extraction_class="disease", extraction_text="哮喘", attributes={"x": "1"}),
            ],
        )
        g = annotated_document_to_base_graph(doc)
        assert len(g.nodes) == 1


class TestExtractorPrompt:
    """``prompt.py``：中文医疗提示词与关系端点表。"""

    def test_medical_entity_classes_includes_diagnosis(self):
        assert "diagnosis" in MEDICAL_ENTITY_CLASSES
        assert "unknown" not in MEDICAL_ENTITY_CLASSES

    def test_relation_endpoint_guide_matches_relation_types(self):
        assert set(RELATION_ENDPOINT_GUIDE) == set(MEDICAL_RELATION_TYPES)

    def test_medical_extraction_prompt_chinese_schema(self):
        p = medical_extraction_prompt()
        assert "中文医疗" in p or "医疗知识图谱" in p
        assert "[disease]" in p and "疾病" in p
        assert "[drug]" in p and "剂型" in p
        assert "[patient]" in p and "patient_id" in p
        assert "[diagnosis]" in p
        assert "disease_has_symptom" in p and "疾病—症状" in p
        assert "patient_has_diagnosis" in p and "严重程度" in p


class TestExtractorExample:
    """``example.py``：few-shot 示例。"""

    def test_medical_few_shot_examples_structure(self):
        examples = medical_few_shot_examples()
        assert len(examples) >= 2
        assert all(isinstance(ex, lx.data.ExampleData) for ex in examples)
        assert examples[0].text
        assert examples[0].extractions
        assert "糖尿病" in examples[0].text or "2型" in examples[0].text

    def test_examples_include_relationship_rows(self):
        examples = medical_few_shot_examples()
        classes = [e.extraction_class for e in examples[0].extractions]
        assert "Relationship" in classes
        assert "disease" in classes


class TestExtractorProvider:
    """``provider.py``：OpenAI 兼容 LangExtract 模型。"""

    def test_create_model_with_explicit_api_key(self):
        model = create_openai_compatible_langextract_model(
            provider_kwargs={"api_key": "unit-test-key-not-for-real_api"},
            model_id="gpt-4o-mini",
        )
        assert model is not None
        assert getattr(model, "model_id", None) == "gpt-4o-mini"


class TestExtractorPackage:
    """包 ``__init__`` 与 ``lx_extractor`` 编排。"""

    def test_package_all_exports_exist(self):
        for name in extractor_pkg.__all__:
            assert hasattr(extractor_pkg, name), f"missing __all__ export: {name}"

    @patch("app.core.extractor.lx_extractor.lx.extract")
    def test_extract_medical_knowledge_graph_builds_graph(self, mock_lx_extract):
        mock_lx_extract.return_value = AnnotatedDocument(
            text="示例：高血压。",
            extractions=[
                Extraction(extraction_class="disease", extraction_text="高血压", attributes={}),
            ],
        )
        result = extractor_pkg.extract_medical_knowledge_graph(
            "示例：高血压。",
            model=MagicMock(),
        )
        assert result.annotated.text == "示例：高血压。"
        assert len(result.graph.nodes) == 1
        assert result.graph.nodes[0].name == "高血压"
        mock_lx_extract.assert_called_once()
