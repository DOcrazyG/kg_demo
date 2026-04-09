"""中文医疗场景 few-shot 示例（LangExtract）。"""

from __future__ import annotations

import langextract as lx


def medical_few_shot_examples() -> list[lx.data.ExampleData]:
    """疾病—症状—用药与科室的简短中文示例。"""
    return [
        lx.data.ExampleData(
            text=(
                "患者既往诊断2型糖尿病，近日多尿明显。内分泌科予二甲双胍片 500mg 每日两次口服。"
            ),
            extractions=[
                lx.data.Extraction(
                    extraction_class="patient",
                    extraction_text="患者",
                    attributes={"patient_id": "患者"},
                ),
                lx.data.Extraction(
                    extraction_class="disease",
                    extraction_text="2型糖尿病",
                    attributes={},
                ),
                lx.data.Extraction(
                    extraction_class="symptom",
                    extraction_text="多尿",
                    attributes={},
                ),
                lx.data.Extraction(
                    extraction_class="drug",
                    extraction_text="二甲双胍片",
                    attributes={"strength": "500mg", "dosage_form": "片剂"},
                ),
                lx.data.Extraction(
                    extraction_class="department",
                    extraction_text="内分泌科",
                    attributes={},
                ),
                lx.data.Extraction(
                    extraction_class="Relationship",
                    extraction_text="2型糖尿病，近日多尿明显",
                    attributes={
                        "source": "2型糖尿病",
                        "target": "多尿",
                        "type": "disease_has_symptom",
                        "source_type": "disease",
                        "target_type": "symptom",
                    },
                ),
                lx.data.Extraction(
                    extraction_class="Relationship",
                    extraction_text="内分泌科予二甲双胍片 500mg 每日两次口服",
                    attributes={
                        "source": "2型糖尿病",
                        "target": "二甲双胍片",
                        "type": "disease_recommand_drug",
                        "source_type": "disease",
                        "target_type": "drug",
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text="原发性高血压可出现头痛。心内科随诊较多；氨氯地平为常用降压药之一。",
            extractions=[
                lx.data.Extraction(
                    extraction_class="disease",
                    extraction_text="原发性高血压",
                    attributes={},
                ),
                lx.data.Extraction(
                    extraction_class="symptom",
                    extraction_text="头痛",
                    attributes={},
                ),
                lx.data.Extraction(
                    extraction_class="department",
                    extraction_text="心内科",
                    attributes={},
                ),
                lx.data.Extraction(
                    extraction_class="drug",
                    extraction_text="氨氯地平",
                    attributes={},
                ),
                lx.data.Extraction(
                    extraction_class="Relationship",
                    extraction_text="原发性高血压可出现头痛",
                    attributes={
                        "source": "原发性高血压",
                        "target": "头痛",
                        "type": "disease_has_symptom",
                        "source_type": "disease",
                        "target_type": "symptom",
                    },
                ),
                lx.data.Extraction(
                    extraction_class="Relationship",
                    extraction_text="氨氯地平为常用降压药之一",
                    attributes={
                        "source": "原发性高血压",
                        "target": "氨氯地平",
                        "type": "disease_common_drug",
                        "source_type": "disease",
                        "target_type": "drug",
                    },
                ),
            ],
        ),
    ]
