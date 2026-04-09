"""
医疗实体类型（中文场景下的字段说明；类型键仍为英文 snake_case）。
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

    entity_type: EntityType = Field(default=EntityType.DISEASE, description="实体类型")
    code: Optional[str] = Field(
        None, description="疾病编码（如 ICD-10/ICD-9，有则填）", examples=["I10", "E11.9"]
    )
    alias: Optional[str] = Field(None, description="别名/俗称")


class Symptom(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.SYMPTOM, description="实体类型")


class Drug(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    entity_type: EntityType = Field(default=EntityType.DRUG, description="实体类型")
    dosage_form: Optional[str] = Field(
        None, description="剂型", examples=["片剂", "胶囊", "注射液"]
    )
    strength: Optional[str] = Field(
        None, description="规格/浓度", examples=["500mg", "0.5g"]
    )
    atc_code: Optional[str] = Field(None, description="ATC 分类编码（有则填）")


class Food(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.FOOD, description="实体类型")


class Department(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.DEPARTMENT, description="实体类型")


class Producer(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.PRODUCER, description="实体类型")


class Treatment(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.TREATMENT, description="实体类型")


class Check(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.CHECK, description="实体类型")
    category: Optional[str] = Field(
        None, description="类别：如实验室检查、影像学检查等"
    )


class Surgery(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.SURGERY, description="实体类型")
    code: Optional[str] = Field(None, description="手术/操作编码（如 CPT、ICD-9-PCS）")


class Patient(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    entity_type: EntityType = Field(default=EntityType.PATIENT, description="实体类型")
    patient_id: str = Field(
        ...,
        description="患者唯一标识（病历号等；原文无则可用占位如“患者”+上下文）",
        examples=["MRN-2024001", "门诊-001"],
    )
    date_of_birth: Optional[date] = Field(None, description="出生日期")
    gender: Optional[str] = Field(None, description="性别")
    phone: Optional[str] = Field(None, description="联系电话")
    id_number: Optional[str] = Field(None, description="身份证号或医保号等")


class Physician(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    entity_type: EntityType = Field(default=EntityType.PHYSICIAN, description="实体类型")
    license_number: Optional[str] = Field(None, description="执业证书编号")
    title: Optional[str] = Field(None, description="职称")
    hospital: Optional[str] = Field(None, description="所在医院/机构")


class Diagnosis(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.DIAGNOSIS, description="实体类型")
    code: Optional[str] = Field(None, description="诊断编码（ICD 等）", examples=["I10"])
    severity: Optional[Severity] = Field(None, description="严重程度")
    is_primary: Optional[bool] = Field(None, description="是否主要诊断")


class LabTest(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.LAB_TEST, description="实体类型")
    test_code: Optional[str] = Field(None, description="检验项目编码（LOINC 或院内码）")
    category: Optional[str] = Field(None, description="检验大类")


class Procedure(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.PROCEDURE, description="实体类型")
    procedure_code: Optional[str] = Field(None, description="操作编码")
    procedure_type: Optional[str] = Field(
        None, description="操作类型：如手术、影像、检查等"
    )


class Prescription(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.PRESCRIPTION, description="实体类型")
    drug_name: str = Field(..., description="药品名称")
    dosage: Optional[str] = Field(None, description="用法用量说明")
    frequency: Optional[str] = Field(None, description="频次")
    duration: Optional[str] = Field(None, description="疗程")
    quantity: Optional[str] = Field(None, description="开药数量")
    route: Optional[str] = Field(None, description="给药途径")


class Allergy(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.ALLERGY, description="实体类型")
    allergen: str = Field(..., description="过敏原（药物、食物、物质等）")
    allergy_type: Optional[AllergyType] = Field(None, description="过敏类型")
    reaction: Optional[str] = Field(None, description="反应描述")
    onset_date: Optional[date] = Field(None, description="发生日期")


class VitalSign(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.VITAL_SIGN, description="实体类型")
    blood_pressure_systolic: Optional[float] = Field(
        None, description="收缩压（mmHg）"
    )
    blood_pressure_diastolic: Optional[float] = Field(
        None, description="舒张压（mmHg）"
    )
    heart_rate: Optional[float] = Field(None, description="心率（次/分）")
    temperature: Optional[float] = Field(None, description="体温（℃）")
    respiratory_rate: Optional[float] = Field(None, description="呼吸频率（次/分）")
    oxygen_saturation: Optional[float] = Field(None, description="血氧饱和度（%）")
    weight_kg: Optional[float] = Field(None, description="体重（kg）")
    height_cm: Optional[float] = Field(None, description="身高（cm）")


class LabValue(BaseEntity):
    model_config = ConfigDict(
        extra="ignore",
    )

    entity_type: EntityType = Field(default=EntityType.LAB_VALUE, description="实体类型")
    test_name: str = Field(..., description="检验项目名称")
    value: Optional[Union[str, float]] = Field(None, description="检验结果值")
    unit: Optional[str] = Field(None, description="单位")
    reference_range: Optional[str] = Field(None, description="参考范围")
    abnormal_flag: Optional[str] = Field(
        None, description="异常标识：如偏高 H、偏低 L 等"
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
