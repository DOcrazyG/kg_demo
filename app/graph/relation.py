"""Medical relations."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import Field

from ._type import AllergyType, RelationType, Severity
from .base import BaseRelation


class DiseaseHasSymptom(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_HAS_SYMPTOM,
        description="Disease has symptom relation",
    )


class DiseaseCommonDrug(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_COMMON_DRUG,
        description="Disease commonly used drug",
    )


class DiseaseRecommandDrug(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_RECOMMAND_DRUG,
        description="Disease recommended drug",
    )


class DiseaseBelongDepartment(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_BELONG_DEPARTMENT,
        description="Disease belongs to department",
    )


class DiseaseAccompanyDisease(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_ACOMPANY_DISEASE,
        description="Disease accompanies disease (comorbidity)",
    )


class DiseaseEatFood(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_EAT_FOOD,
        description="Disease can eat food",
    )


class DiseaseNoteatFood(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_NOTEAT_FOOD,
        description="Disease should avoid food",
    )


class DiseaseRecommandFood(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_RECOMMAND_FOOD,
        description="Disease recommended food",
    )


class DiseaseNeedCheck(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_NEED_CHECK,
        description="Disease requires check/exam",
    )


class DiseaseNeedTreatment(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DISEASE_NEED_TREATMENT,
        description="Disease requires treatment",
    )


class DrugRelateProducer(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DRUG_RELATE_PRODUCER,
        description="Drug related to producer/manufacturer",
    )


class DepartmentBelongDepartment(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DEPARTMENT_BELONG_DEPARTMENT,
        description="Department belongs to parent department",
    )


class PatientHasDiagnosis(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PATIENT_HAS_DIAGNOSIS,
        description="Patient has diagnosis",
    )
    severity: Optional[Severity] = Field(None, description="Diagnosis severity")
    is_primary: Optional[bool] = Field(None, description="Primary diagnosis")


class PatientPrescribedMedication(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PATIENT_PRESCRIBED_MEDICATION,
        description="Patient prescribed medication",
    )
    dosage: Optional[str] = Field(None, description="Dosage instructions")
    frequency: Optional[str] = Field(None, description="Frequency")
    duration: Optional[str] = Field(None, description="Treatment duration")


class PatientHasAllergy(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PATIENT_HAS_ALLERGY,
        description="Patient has allergy",
    )
    allergy_type: Optional[AllergyType] = Field(None, description="Allergy type")
    reaction: Optional[str] = Field(None, description="Allergic reaction")


class PatientHasLabTest(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PATIENT_HAS_LAB_TEST,
        description="Patient has lab test",
    )


class PhysicianBelongsToDepartment(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PHYSICIAN_BELONGS_TO_DEPARTMENT,
        description="Physician belongs to department",
    )


class LabTestMapToCheck(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.LAB_TEST_MAP_TO_CHECK,
        description="Lab test maps to check entity",
    )


class ProcedureMapToCheck(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PROCEDURE_MAP_TO_CHECK,
        description="Procedure maps to check entity",
    )


class ProcedureMapToSurgery(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PROCEDURE_MAP_TO_SURGERY,
        description="Procedure maps to surgery entity",
    )


class PrescriptionReferencesDrug(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.PRESCRIPTION_REFERENCES_DRUG,
        description="Prescription references drug entity",
    )


class DiagnosisMapsToDisease(BaseRelation):
    relation_type: RelationType = Field(
        default=RelationType.DIAGNOSIS_MAPS_TO_DISEASE,
        description="Diagnosis maps to disease entity",
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
