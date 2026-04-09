"""中文医疗知识图谱：实体与关系类型清单（与 ``entity`` / ``relation`` 模块一致）。"""

from .base import BaseGraph
from .entity import (
    Disease,
    Symptom,
    Drug,
    Food,
    Department,
    Producer,
    Treatment,
    Check,
    Surgery,
    Patient,
    Physician,
    Diagnosis,
    LabTest,
    Procedure,
    Prescription,
    Allergy,
    VitalSign,
    LabValue,
)
from .relation import (
    DiseaseHasSymptom,
    DiseaseCommonDrug,
    DiseaseRecommandDrug,
    DiseaseBelongDepartment,
    DiseaseAccompanyDisease,
    DiseaseEatFood,
    DiseaseNoteatFood,
    DiseaseRecommandFood,
    DiseaseNeedCheck,
    DiseaseNeedTreatment,
    DrugRelateProducer,
    DepartmentBelongDepartment,
    PatientHasDiagnosis,
    PatientPrescribedMedication,
    PatientHasAllergy,
    PatientHasLabTest,
    PhysicianBelongsToDepartment,
    LabTestMapToCheck,
    ProcedureMapToCheck,
    ProcedureMapToSurgery,
    PrescriptionReferencesDrug,
    DiagnosisMapsToDisease,
)

ENTITY_TYPES = [
    Disease,
    Symptom,
    Drug,
    Food,
    Department,
    Producer,
    Treatment,
    Check,
    Surgery,
    Patient,
    Physician,
    Diagnosis,
    LabTest,
    Procedure,
    Prescription,
    Allergy,
    VitalSign,
    LabValue,
]

RELATION_TYPES = [
    DiseaseHasSymptom,
    DiseaseCommonDrug,
    DiseaseRecommandDrug,
    DiseaseBelongDepartment,
    DiseaseAccompanyDisease,
    DiseaseEatFood,
    DiseaseNoteatFood,
    DiseaseRecommandFood,
    DiseaseNeedCheck,
    DiseaseNeedTreatment,
    DrugRelateProducer,
    DepartmentBelongDepartment,
    PatientHasDiagnosis,
    PatientPrescribedMedication,
    PatientHasAllergy,
    PatientHasLabTest,
    PhysicianBelongsToDepartment,
    LabTestMapToCheck,
    ProcedureMapToCheck,
    ProcedureMapToSurgery,
    PrescriptionReferencesDrug,
    DiagnosisMapsToDisease,
]


class MedicalGraph(BaseGraph):
    pass


MedicalGraph.model_rebuild()
MedicalGraph.nodes = ENTITY_TYPES
MedicalGraph.edges = RELATION_TYPES
