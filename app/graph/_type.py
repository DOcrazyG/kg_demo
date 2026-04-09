from enum import Enum


class EntityType(str, Enum):
    """实体类型（取值保持英文 snake_case，便于代码与存储；中文见 ENTITY_TYPE_LABEL_ZH）。"""

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
    DIAGNOSIS = "diagnosis"
    UNKNOWN = "unknown"


ENTITY_TYPE_LABEL_ZH: dict[str, str] = {
    EntityType.DISEASE.value: "疾病",
    EntityType.SYMPTOM.value: "症状",
    EntityType.DRUG.value: "药品",
    EntityType.FOOD.value: "食物",
    EntityType.DEPARTMENT.value: "科室",
    EntityType.PRODUCER.value: "生产厂商",
    EntityType.TREATMENT.value: "治疗方式",
    EntityType.CHECK.value: "检查项目",
    EntityType.SURGERY.value: "手术",
    EntityType.PATIENT.value: "患者",
    EntityType.PHYSICIAN.value: "医护人员",
    EntityType.LAB_TEST.value: "检验项目",
    EntityType.PROCEDURE.value: "操作/处置",
    EntityType.PRESCRIPTION.value: "处方",
    EntityType.ALLERGY.value: "过敏",
    EntityType.VITAL_SIGN.value: "生命体征",
    EntityType.LAB_VALUE.value: "检验结果",
    EntityType.DIAGNOSIS.value: "诊断",
    EntityType.UNKNOWN.value: "未知",
}


class RelationType(str, Enum):
    """关系类型（取值英文 snake_case；中文语义见 RELATION_TYPE_LABEL_ZH）。"""

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


RELATION_TYPE_LABEL_ZH: dict[str, str] = {
    RelationType.DISEASE_HAS_SYMPTOM.value: "疾病—症状",
    RelationType.DISEASE_COMMON_DRUG.value: "疾病—常用药品",
    RelationType.DISEASE_RECOMMAND_DRUG.value: "疾病—推荐药品",
    RelationType.DISEASE_BELONG_DEPARTMENT.value: "疾病—所属科室",
    RelationType.DISEASE_ACOMPANY_DISEASE.value: "疾病—合并/伴随疾病",
    RelationType.DISEASE_EAT_FOOD.value: "疾病—宜食",
    RelationType.DISEASE_NOTEAT_FOOD.value: "疾病—忌食",
    RelationType.DISEASE_RECOMMAND_FOOD.value: "疾病—推荐食物",
    RelationType.DISEASE_NEED_CHECK.value: "疾病—需做检查",
    RelationType.DISEASE_NEED_TREATMENT.value: "疾病—需治疗方式",
    RelationType.DRUG_RELATE_PRODUCER.value: "药品—生产企业",
    RelationType.DEPARTMENT_BELONG_DEPARTMENT.value: "科室—上级科室",
    RelationType.PATIENT_HAS_DIAGNOSIS.value: "患者—诊断",
    RelationType.PATIENT_PRESCRIBED_MEDICATION.value: "患者—用药/处方药品",
    RelationType.PATIENT_HAS_ALLERGY.value: "患者—过敏",
    RelationType.PATIENT_HAS_LAB_TEST.value: "患者—检验项目",
    RelationType.PHYSICIAN_BELONGS_TO_DEPARTMENT.value: "医护人员—所属科室",
    RelationType.LAB_TEST_MAP_TO_CHECK.value: "检验—对应检查",
    RelationType.PROCEDURE_MAP_TO_CHECK.value: "操作—对应检查",
    RelationType.PROCEDURE_MAP_TO_SURGERY.value: "操作—对应手术",
    RelationType.PRESCRIPTION_REFERENCES_DRUG.value: "处方—涉及药品",
    RelationType.DIAGNOSIS_MAPS_TO_DISEASE.value: "诊断—对应疾病",
    RelationType.UNKNOWN.value: "未知关系",
}


class Severity(str, Enum):
    """严重程度（中文取值，便于中文病历与抽取）。"""

    MILD = "轻度"
    MODERATE = "中度"
    SEVERE = "重度"
    CRITICAL = "危重"
    UNKNOWN = "未知"


class AllergyType(str, Enum):
    """过敏类型（中文取值）。"""

    DRUG = "药物"
    FOOD = "食物"
    ENVIRONMENTAL = "环境"
    LATEX = "乳胶"
    OTHER = "其他"
