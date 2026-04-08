from enum import Enum


class EntityType(str, Enum):
    DISEASE = "disease"
    SYMPTOM = "symptom"
    DRUG = "drug"
    FOOD = "food"
    DEPARTMENT = "department"
    PRODUCER = "producer"
    TREATMENT = "treatment"
    CHECK = "check"
    SURGERY = "surgery"
    PATIENT = "patient"
    PHYSICIAN = "physician"
    LAB_TEST = "lab_test"
    PROCEDURE = "procedure"
    PRESCRIPTION = "prescription"
    ALLERGY = "allergy"
    VITAL_SIGN = "vital_sign"
    LAB_VALUE = "lab_value"
    UNKNOWN = "unknown"


class RelationType(str, Enum):
    DISEASE_HAS_SYMPTOM = "disease_has_symptom"
    DISEASE_COMMON_DRUG = "disease_common_drug"
    DISEASE_RECOMMAND_DRUG = "disease_recommand_drug"
    DISEASE_BELONG_DEPARTMENT = "disease_belong_department"
    DISEASE_ACOMPANY_DISEASE = "disease_accompany_disease"
    DISEASE_EAT_FOOD = "disease_eat_food"
    DISEASE_NOTEAT_FOOD = "disease_noteat_food"
    DISEASE_RECOMMAND_FOOD = "disease_recommand_food"
    DISEASE_NEED_CHECK = "disease_need_check"
    DISEASE_NEED_TREATMENT = "disease_need_treatment"
    DRUG_RELATE_PRODUCER = "drug_relate_producer"
    DEPARTMENT_BELONG_DEPARTMENT = "department_belong_department"
    PATIENT_HAS_DIAGNOSIS = "patient_has_diagnosis"
    PATIENT_PRESCRIBED_MEDICATION = "patient_prescribed_medication"
    PATIENT_HAS_ALLERGY = "patient_has_allergy"
    PATIENT_HAS_LAB_TEST = "patient_has_lab_test"
    PHYSICIAN_BELONGS_TO_DEPARTMENT = "physician_belongs_to_department"
    LAB_TEST_MAP_TO_CHECK = "lab_test_map_to_check"
    PROCEDURE_MAP_TO_CHECK = "procedure_map_to_check"
    PROCEDURE_MAP_TO_SURGERY = "procedure_map_to_surgery"
    PRESCRIPTION_REFERENCES_DRUG = "prescription_references_drug"
    DIAGNOSIS_MAPS_TO_DISEASE = "diagnosis_maps_to_disease"
    UNKNOWN = "unknown"


class Severity(str, Enum):
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    CRITICAL = "Critical"
    UNKNOWN = "Unknown"


class AllergyType(str, Enum):
    DRUG = "Drug"
    FOOD = "Food"
    ENVIRONMENTAL = "Environmental"
    LATEX = "Latex"
    OTHER = "Other"


class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"
