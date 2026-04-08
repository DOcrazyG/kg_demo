"""
Medical entities
"""

from __future__ import annotations

from datetime import date
from typing import Optional, Union

from pydantic import ConfigDict, Field

from ._type import AllergyType, EntityType, Severity
from .base import BaseEntity


class Disease(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    entity_type: EntityType = Field(
        default=EntityType.DISEASE, description="Entity type"
    )
    code: Optional[str] = Field(
        None, description="ICD-10/ICD-9 code", examples=["I10", "E11.9"]
    )
    alias: Optional[str] = Field(None, description="Alternative name")


class Symptom(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(
        default=EntityType.SYMPTOM, description="Entity type"
    )


class Drug(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    entity_type: EntityType = Field(default=EntityType.DRUG, description="Entity type")
    dosage_form: Optional[str] = Field(
        None, description="Dosage form", examples=["片剂", "胶囊"]
    )
    strength: Optional[str] = Field(
        None, description="Strength/concentration", examples=["500mg"]
    )
    atc_code: Optional[str] = Field(None, description="ATC classification code")


class Food(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.FOOD, description="Entity type")


class Department(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(
        default=EntityType.DEPARTMENT, description="Entity type"
    )


class Producer(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(
        default=EntityType.PRODUCER, description="Entity type"
    )


class Treatment(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(
        default=EntityType.TREATMENT, description="Entity type"
    )


class Check(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.CHECK, description="Entity type")
    category: Optional[str] = Field(None, description="Category: lab, imaging, etc.")


class Surgery(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(
        default=EntityType.SURGERY, description="Entity type"
    )
    code: Optional[str] = Field(None, description="Procedure code (CPT, ICD-9-PCS)")


class Patient(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    entity_type: EntityType = Field(
        default=EntityType.PATIENT, description="Entity type"
    )
    patient_id: str = Field(
        ..., description="Unique patient identifier", examples=["MRN-2024001"]
    )
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender")
    phone: Optional[str] = Field(None, description="Contact phone")
    id_number: Optional[str] = Field(
        None, description="National ID or insurance number"
    )


class Physician(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    entity_type: EntityType = Field(
        default=EntityType.PHYSICIAN, description="Entity type"
    )
    license_number: Optional[str] = Field(None, description="Medical license number")
    title: Optional[str] = Field(None, description="Professional title")
    hospital: Optional[str] = Field(None, description="Affiliated hospital")


class Diagnosis(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(
        default=EntityType.UNKNOWN, description="Entity type"
    )
    code: Optional[str] = Field(None, description="ICD-10/ICD-9 code", examples=["I10"])
    severity: Optional[Severity] = Field(None, description="Diagnosis severity")
    is_primary: Optional[bool] = Field(None, description="Primary diagnosis flag")


class LabTest(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(
        default=EntityType.LAB_TEST, description="Entity type"
    )
    test_code: Optional[str] = Field(None, description="LOINC or local code")
    category: Optional[str] = Field(None, description="Test category")


class Procedure(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(
        default=EntityType.PROCEDURE, description="Entity type"
    )
    procedure_code: Optional[str] = Field(None, description="CPT, ICD-9-PCS code")
    procedure_type: Optional[str] = Field(
        None, description="surgery, imaging, examination"
    )


class Prescription(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(
        default=EntityType.PRESCRIPTION, description="Entity type"
    )
    drug_name: str = Field(..., description="Drug name")
    dosage: Optional[str] = Field(None, description="Dosage instructions")
    frequency: Optional[str] = Field(None, description="Frequency")
    duration: Optional[str] = Field(None, description="Duration")
    quantity: Optional[str] = Field(None, description="Quantity prescribed")
    route: Optional[str] = Field(None, description="Route of administration")


class Allergy(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(
        default=EntityType.ALLERGY, description="Entity type"
    )
    allergen: str = Field(..., description="Allergen (drug, food, substance)")
    allergy_type: Optional[AllergyType] = Field(None, description="Allergy type")
    reaction: Optional[str] = Field(None, description="Reaction description")
    onset_date: Optional[date] = Field(None, description="Onset date")


class VitalSign(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(
        default=EntityType.VITAL_SIGN, description="Entity type"
    )
    blood_pressure_systolic: Optional[float] = Field(
        None, description="Systolic BP (mmHg)"
    )
    blood_pressure_diastolic: Optional[float] = Field(
        None, description="Diastolic BP (mmHg)"
    )
    heart_rate: Optional[float] = Field(None, description="Heart rate (bpm)")
    temperature: Optional[float] = Field(None, description="Body temperature (°C)")
    respiratory_rate: Optional[float] = Field(
        None, description="Respiratory rate (/min)"
    )
    oxygen_saturation: Optional[float] = Field(None, description="SpO2 (%)")
    weight_kg: Optional[float] = Field(None, description="Weight (kg)")
    height_cm: Optional[float] = Field(None, description="Height (cm)")


class LabValue(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(
        default=EntityType.LAB_VALUE, description="Entity type"
    )
    test_name: str = Field(..., description="Name of the lab test")
    value: Optional[Union[str, float]] = Field(None, description="Test result value")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    reference_range: Optional[str] = Field(None, description="Normal reference range")
    abnormal_flag: Optional[str] = Field(
        None, description="Abnormality indicator: H, L, HH, LL"
    )


ENTITY_TYPE_MAPPING = {
    "disease": Disease,
    "symptom": Symptom,
    "drug": Drug,
    "food": Food,
    "department": Department,
    "producer": Producer,
    "treatment": Treatment,
    "check": Check,
    "surgery": Surgery,
    "patient": Patient,
    "physician": Physician,
    "diagnosis": Diagnosis,
    "lab_test": LabTest,
    "procedure": Procedure,
    "prescription": Prescription,
    "allergy": Allergy,
    "vital_sign": VitalSign,
    "lab_value": LabValue,
}


def get_entity_class(entity_type: Union[str, EntityType]) -> type[BaseEntity]:
    if isinstance(entity_type, EntityType):
        entity_type = entity_type.value
    return ENTITY_TYPE_MAPPING.get(entity_type, BaseEntity)


Disease.model_rebuild()
Department.model_rebuild()
Drug.model_rebuild()
LabTest.model_rebuild()
Procedure.model_rebuild()
Prescription.model_rebuild()
Allergy.model_rebuild()
VitalSign.model_rebuild()
LabValue.model_rebuild()
