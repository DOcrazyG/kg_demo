"""医疗关系类型（中文说明）。"""

from __future__ import annotations

from typing import Optional, Union

from pydantic import Field

from ._type import AllergyType, RelationType, Severity
from .base import BaseRelation


class DiseaseHasSymptom(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_HAS_SYMPTOM,
        description="疾病表现/伴有某症状",
    )


class DiseaseCommonDrug(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_COMMON_DRUG,
        description="疾病常用治疗药物",
    )


class DiseaseRecommandDrug(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_RECOMMAND_DRUG,
        description="疾病推荐/建议用药",
    )


class DiseaseBelongDepartment(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_BELONG_DEPARTMENT,
        description="疾病归属科室（诊疗分科）",
    )


class DiseaseAccompanyDisease(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_ACOMPANY_DISEASE,
        description="合并症/伴随疾病",
    )


class DiseaseEatFood(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_EAT_FOOD,
        description="疾病适宜摄入的食物",
    )


class DiseaseNoteatFood(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_NOTEAT_FOOD,
        description="疾病应避免的食物",
    )


class DiseaseRecommandFood(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_RECOMMAND_FOOD,
        description="疾病推荐食物",
    )


class DiseaseNeedCheck(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_NEED_CHECK,
        description="疾病需要做的检查/检验",
    )


class DiseaseNeedTreatment(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_NEED_TREATMENT,
        description="疾病需要的治疗方式",
    )


class DrugRelateProducer(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DRUG_RELATE_PRODUCER,
        description="药品与生产企业",
    )


class DepartmentBelongDepartment(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DEPARTMENT_BELONG_DEPARTMENT,
        description="科室隶属上级科室",
    )


class PatientHasDiagnosis(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PATIENT_HAS_DIAGNOSIS,
        description="患者被赋予某诊断",
    )
    severity: Optional[Severity] = Field(None, description="诊断严重程度")
    is_primary: Optional[bool] = Field(None, description="是否主要诊断")


class PatientPrescribedMedication(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PATIENT_PRESCRIBED_MEDICATION,
        description="患者用药/开立药物",
    )
    dosage: Optional[str] = Field(None, description="用法用量")
    frequency: Optional[str] = Field(None, description="用药频次")
    duration: Optional[str] = Field(None, description="疗程")


class PatientHasAllergy(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PATIENT_HAS_ALLERGY,
        description="患者有过敏史",
    )
    allergy_type: Optional[AllergyType] = Field(None, description="过敏类型")
    reaction: Optional[str] = Field(None, description="过敏反应描述")


class PatientHasLabTest(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PATIENT_HAS_LAB_TEST,
        description="患者进行/开具某检验",
    )


class PhysicianBelongsToDepartment(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PHYSICIAN_BELONGS_TO_DEPARTMENT,
        description="医护人员所属科室",
    )


class LabTestMapToCheck(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.LAB_TEST_MAP_TO_CHECK,
        description="检验项目对应检查项目",
    )


class ProcedureMapToCheck(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PROCEDURE_MAP_TO_CHECK,
        description="操作/处置对应检查",
    )


class ProcedureMapToSurgery(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PROCEDURE_MAP_TO_SURGERY,
        description="操作/处置对应手术",
    )


class PrescriptionReferencesDrug(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PRESCRIPTION_REFERENCES_DRUG,
        description="处方涉及的具体药品",
    )


class DiagnosisMapsToDisease(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DIAGNOSIS_MAPS_TO_DISEASE,
        description="诊断对应到标准/规范化疾病",
    )


RELATION_TYPE_MAPPING = {
    RelationType.DISEASE_HAS_SYMPTOM: DiseaseHasSymptom,
    RelationType.DISEASE_COMMON_DRUG: DiseaseCommonDrug,
    RelationType.DISEASE_RECOMMAND_DRUG: DiseaseRecommandDrug,
    RelationType.DISEASE_BELONG_DEPARTMENT: DiseaseBelongDepartment,
    RelationType.DISEASE_ACOMPANY_DISEASE: DiseaseAccompanyDisease,
    RelationType.DISEASE_EAT_FOOD: DiseaseEatFood,
    RelationType.DISEASE_NOTEAT_FOOD: DiseaseNoteatFood,
    RelationType.DISEASE_RECOMMAND_FOOD: DiseaseRecommandFood,
    RelationType.DISEASE_NEED_CHECK: DiseaseNeedCheck,
    RelationType.DISEASE_NEED_TREATMENT: DiseaseNeedTreatment,
    RelationType.DRUG_RELATE_PRODUCER: DrugRelateProducer,
    RelationType.DEPARTMENT_BELONG_DEPARTMENT: DepartmentBelongDepartment,
    RelationType.PATIENT_HAS_DIAGNOSIS: PatientHasDiagnosis,
    RelationType.PATIENT_PRESCRIBED_MEDICATION: PatientPrescribedMedication,
    RelationType.PATIENT_HAS_ALLERGY: PatientHasAllergy,
    RelationType.PATIENT_HAS_LAB_TEST: PatientHasLabTest,
    RelationType.PHYSICIAN_BELONGS_TO_DEPARTMENT: PhysicianBelongsToDepartment,
    RelationType.LAB_TEST_MAP_TO_CHECK: LabTestMapToCheck,
    RelationType.PROCEDURE_MAP_TO_CHECK: ProcedureMapToCheck,
    RelationType.PROCEDURE_MAP_TO_SURGERY: ProcedureMapToSurgery,
    RelationType.PRESCRIPTION_REFERENCES_DRUG: PrescriptionReferencesDrug,
    RelationType.DIAGNOSIS_MAPS_TO_DISEASE: DiagnosisMapsToDisease,
}


def get_relation_class(relation_type: Union[str, RelationType]) -> type[BaseRelation]:
    if isinstance(relation_type, RelationType):
        relation_type = relation_type
    else:
        try:
            relation_type = RelationType(relation_type.lower())
        except ValueError:
            return BaseRelation
    return RELATION_TYPE_MAPPING.get(relation_type, BaseRelation)
