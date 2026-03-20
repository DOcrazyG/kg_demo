"""Medical knowledge graph schema. OpenCMKG/MedicalKG compatible."""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Any, List

from pydantic import BaseModel, ConfigDict, Field


def edge(label: str, **kwargs: Any) -> Any:
    """Field with edge metadata for graph relationships."""
    if "default" not in kwargs and "default_factory" not in kwargs:
        kwargs["default"] = ...
    return Field(json_schema_extra={"edge_label": label}, **kwargs)


KG_RELATIONS = {
    "disease_has_symptom",
    "disease_acompany_disease",
    "disease_belong_department",
    "disease_common_drug",
    "disease_recommand_drug",
    "disease_eat_food",
    "disease_noteat_food",
    "disease_recommand_food",
    "disease_need_check",
    "disease_need_treatment",
    "department_belong_department",
    "drug_relate_producer",
    "SameAs",
}


class DocumentType(str, Enum):
    OUTPATIENT_RECORD = "Outpatient Record"
    INPATIENT_RECORD = "Inpatient Record"
    DISCHARGE_SUMMARY = "Discharge Summary"
    PRESCRIPTION = "Prescription"
    LAB_REPORT = "Lab Report"
    IMAGING_REPORT = "Imaging Report"
    REFERRAL = "Referral"
    OTHER = "Other"


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


class Address(BaseModel):

    model_config = ConfigDict(is_entity=False, extra="ignore")

    street: str | None = Field(None, description="Street address")
    city: str | None = Field(None, description="City")
    district: str | None = Field(None, description="District or county")
    province: str | None = Field(None, description="Province or state")
    postal_code: str | None = Field(None, description="Postal/ZIP code")
    country: str | None = Field(None, description="Country")


class VitalSigns(BaseModel):
    model_config = ConfigDict(is_entity=False)

    blood_pressure_systolic: float | None = Field(
        None, description="Systolic blood pressure (mmHg)"
    )
    blood_pressure_diastolic: float | None = Field(
        None, description="Diastolic blood pressure (mmHg)"
    )
    heart_rate: float | None = Field(None, description="Heart rate (bpm)")
    temperature: float | None = Field(None, description="Body temperature (°C)")
    respiratory_rate: float | None = Field(None, description="Respiratory rate (/min)")
    oxygen_saturation: float | None = Field(None, description="SpO2 (%)")
    weight_kg: float | None = Field(None, description="Weight in kg")
    height_cm: float | None = Field(None, description="Height in cm")


class LabValue(BaseModel):
    model_config = ConfigDict(is_entity=False)

    test_name: str = Field(..., description="Name of the lab test")
    value: str | float | None = Field(
        None,
        description="Test result value (numeric or string for qualitative results)",
    )
    unit: str | None = Field(None, description="Unit of measurement")
    reference_range: str | None = Field(
        None,
        description="Normal reference range (e.g., '3.5-5.5 mmol/L')",
    )
    abnormal_flag: str | None = Field(
        None,
        description="Abnormality indicator: H (high), L (low), HH, LL, etc.",
    )


class Disease(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["name"],
        extra="ignore",
        populate_by_name=True,
    )

    name: str = Field(
        ...,
        description="Disease name (疾病名)",
        examples=["高血压", "糖尿病", "急性上呼吸道感染", "百日咳", "苯中毒"],
    )

    code: str | None = Field(
        None,
        description="ICD-10/ICD-9 code if available",
        examples=["I10", "E11.9", "J06.9"],
    )

    alias: str | None = Field(
        None,
        description="Alternative name or alias",
    )

    symptoms: List["Symptom"] = edge(
        label="DISEASE_HAS_SYMPTOM",
        default_factory=list,
        description="Symptoms associated with this disease",
    )

    complications: List["Disease"] = edge(
        label="DISEASE_ACOMPANY_DISEASE",
        default_factory=list,
        description="Comorbidities or complications",
    )

    department: Department | None = edge(
        label="DISEASE_BELONG_DEPARTMENT",
        default=None,
        description="Department that treats this disease",
    )

    common_drugs: List["Drug"] = edge(
        label="DISEASE_COMMON_DRUG",
        default_factory=list,
        description="Commonly used drugs for this disease",
    )

    recommand_drugs: List["Drug"] = edge(
        label="DISEASE_RECOMMAND_DRUG",
        default_factory=list,
        description="Recommended drugs for this disease",
    )

    eat_food: List["Food"] = edge(
        label="DISEASE_EAT_FOOD",
        default_factory=list,
        description="Foods that can be eaten with this disease",
    )

    noteat_food: List["Food"] = edge(
        label="DISEASE_NOTEAT_FOOD",
        default_factory=list,
        description="Foods to avoid with this disease",
    )

    recommand_food: List["Food"] = edge(
        label="DISEASE_RECOMMAND_FOOD",
        default_factory=list,
        description="Recommended foods for this disease",
    )

    need_check: List["Check"] = edge(
        label="DISEASE_NEED_CHECK",
        default_factory=list,
        description="Required lab/imaging checks",
    )

    need_treatment: List["Treatment"] = edge(
        label="DISEASE_NEED_TREATMENT",
        default_factory=list,
        description="Required treatment modalities",
    )


class Symptom(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["name"],
        extra="ignore",
    )

    name: str = Field(
        ...,
        description="Symptom name (症状名)",
        examples=["发热", "头痛", "咳嗽", "胸痛", "呼吸困难", "恶心", "乏力"],
    )


class Drug(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["name"],
        extra="ignore",
        populate_by_name=True,
    )

    name: str = Field(
        ...,
        description="Drug name (药物名)",
        examples=["阿莫西林", "琥乙红霉素片", "穿心莲内酯片", "Metformin", "Aspirin"],
    )

    dosage_form: str | None = Field(
        None,
        description="Dosage form (剂型)",
        examples=["片剂", "胶囊", "注射液", "糖浆", "颗粒"],
    )

    strength: str | None = Field(
        None,
        description="Strength/concentration",
        examples=["500mg", "0.5g"],
    )

    atc_code: str | None = Field(
        None,
        description="ATC classification code",
    )

    producer: Producer | None = edge(
        label="DRUG_RELATE_PRODUCER",
        default=None,
        description="Drug manufacturer",
    )


class Food(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["name"],
        extra="ignore",
    )

    name: str = Field(
        ...,
        description="Food name (食物名)",
        examples=["南瓜子仁", "圆白菜", "排骨汤", "螃蟹", "海虾"],
    )


class Department(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["name"],
        extra="ignore",
    )

    name: str = Field(
        ...,
        description="Department name (科室名)",
        examples=["内科", "呼吸内科", "小儿内科", "急诊科", "骨科"],
    )

    parent: Department | None = edge(
        label="DEPARTMENT_BELONG_DEPARTMENT",
        default=None,
        description="Parent department",
    )


class Producer(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["name"],
        extra="ignore",
    )

    name: str = Field(
        ...,
        description="Producer/manufacturer name (生产商名)",
        examples=["北京同仁堂", "康美药业", "白云山医药"],
    )


class Treatment(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["name"],
        extra="ignore",
    )

    name: str = Field(
        ...,
        description="Treatment name (治疗方式)",
        examples=["手术治疗", "药物治疗", "物理治疗"],
    )


class Check(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["name"],
        extra="ignore",
    )

    name: str = Field(
        ...,
        description="Check/exam name (检查项目)",
        examples=["血常规", "胸部CT检查", "肺活检", "支气管镜检查", "心电图"],
    )

    category: str | None = Field(
        None,
        description="Category: lab, imaging, etc.",
    )


class Surgery(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["name"],
        extra="ignore",
    )

    name: str = Field(
        ...,
        description="Surgery/procedure name (手术名)",
        examples=["阑尾切除术", "冠状动脉搭桥术"],
    )

    code: str | None = Field(
        None,
        description="Procedure code (CPT, ICD-9-PCS)",
    )


class KGTriple(BaseModel):
    model_config = ConfigDict(is_entity=False)

    subject: str = Field(..., description="Subject entity name")
    relation: str = Field(
        ...,
        description="Relation name (e.g., disease_has_symptom, disease_recommand_drug)",
    )
    object: str = Field(..., description="Object entity name")


class Patient(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["patient_id"],
        extra="ignore",
        populate_by_name=True,
    )

    patient_id: str = Field(
        ...,
        description="Unique patient identifier (MRN, SUBJECT_ID)",
        examples=["MRN-2024001", "P12345678"],
    )

    name: str | None = Field(None, description="Patient full name")
    date_of_birth: date | None = Field(None, description="Date of birth (YYYY-MM-DD)")
    gender: str | None = Field(None, description="Gender")
    phone: str | None = Field(None, description="Contact phone")
    id_number: str | None = Field(None, description="National ID or insurance number")
    address: Address | None = None


class Physician(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["name", "license_number"],
        extra="ignore",
        populate_by_name=True,
    )

    name: str = Field(..., description="Physician full name")
    license_number: str | None = Field(None, description="Medical license number")
    department: Department | None = edge(
        label="BELONGS_TO_DEPARTMENT",
        default=None,
        description="Department or specialty",
    )
    title: str | None = Field(None, description="Professional title")
    hospital: str | None = Field(None, description="Affiliated hospital")


class Diagnosis(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["code", "description"],
        extra="ignore",
    )

    code: str | None = Field(None, description="ICD-10/ICD-9 code", examples=["I10", "E11.9"])
    description: str = Field(..., description="Diagnosis name")
    severity: Severity | None = None
    is_primary: bool | None = None

    disease: Disease | None = edge(
        label="MAPS_TO_DISEASE",
        default=None,
        description="Links to KG Disease entity",
    )


Medication = Drug


class Allergy(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["allergen", "reaction"],
        extra="ignore",
    )

    allergen: str = Field(..., description="Allergen (drug, food, substance)")
    allergy_type: AllergyType | None = None
    reaction: str | None = Field(None, description="Reaction description")
    severity: Severity | None = None
    onset_date: date | None = None


class LabTest(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["test_code", "test_name"],
        extra="ignore",
    )

    test_code: str | None = Field(None, description="LOINC or local code")
    test_name: str = Field(..., description="Test name")
    category: str | None = Field(None, description="Test category")

    check: Check | None = edge(
        label="MAPS_TO_CHECK",
        default=None,
        description="Links to KG Check entity",
    )


class Procedure(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["procedure_code", "name"],
        extra="ignore",
    )

    procedure_code: str | None = Field(None, description="CPT, ICD-9-PCS code")
    name: str = Field(..., description="Procedure name")
    procedure_type: str | None = Field(None, description="surgery, imaging, examination")

    surgery: Surgery | None = edge(
        label="MAPS_TO_SURGERY",
        default=None,
        description="Links to KG Surgery entity when procedure_type is surgery",
    )

    check: Check | None = edge(
        label="MAPS_TO_CHECK",
        default=None,
        description="Links to KG Check entity when procedure_type is imaging/examination",
    )


class PrescriptionItem(BaseModel):
    model_config = ConfigDict(is_entity=False)

    drug_name: str = Field(..., description="Drug name for this line")
    dosage: str | None = Field(None, description="Dosage instructions")
    frequency: str | None = Field(None, description="Frequency")
    duration: str | None = Field(None, description="Duration of treatment")
    quantity: str | None = Field(None, description="Quantity prescribed")
    route: str | None = Field(None, description="Route of administration")
    special_instructions: str | None = None

    drug: Drug | None = edge(
        label="REFERENCES_DRUG",
        default=None,
        description="Drug entity for graph linkage",
    )


class MedicalRecord(BaseModel):
    model_config = ConfigDict(
        graph_id_fields=["record_id"],
        extra="ignore",
        populate_by_name=True,
    )

    record_id: str = Field(..., description="Unique medical record/visit identifier")
    document_type: DocumentType | None = None
    visit_date: date | None = None
    admission_date: date | None = None
    discharge_date: date | None = None
    chief_complaint: str | None = None
    present_illness: str | None = None
    past_medical_history: str | None = None
    physical_exam: str | None = None
    vital_signs: VitalSigns | None = None

    patient: Patient | None = edge(label="BELONGS_TO", default=None)
    attending_physician: Physician | None = edge(label="ATTENDED_BY", default=None)
    diagnoses: List[Diagnosis] = edge(label="HAS_DIAGNOSIS", default_factory=list)
    prescriptions: List[PrescriptionItem] = Field(default_factory=list)
    medications: List[Drug] = edge(label="PRESCRIBED_MEDICATION", default_factory=list)
    lab_tests: List[LabTest] = edge(label="HAS_LAB_TEST", default_factory=list)
    lab_results: List[LabValue] = Field(default_factory=list)
    procedures: List[Procedure] = edge(label="HAS_PROCEDURE", default_factory=list)
    allergies: List[Allergy] = edge(label="HAS_ALLERGY", default_factory=list)
    referral_to: Physician | None = edge(label="REFERRED_TO", default=None)

    notes: str | None = None
    follow_up: str | None = None


KG_ENTITY_TYPES = {
    "disease": Disease,
    "symptom": Symptom,
    "drug": Drug,
    "food": Food,
    "department": Department,
    "producer": Producer,
    "treatment": Treatment,
    "check": Check,
    "surgery": Surgery,
}

Disease.model_rebuild()
Department.model_rebuild()
Drug.model_rebuild()
LabTest.model_rebuild()
Procedure.model_rebuild()
