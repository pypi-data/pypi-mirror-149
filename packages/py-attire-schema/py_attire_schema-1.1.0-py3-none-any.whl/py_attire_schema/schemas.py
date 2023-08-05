from typing import List
from pydantic import BaseModel, Field, validator, IPvAnyAddress
from typing import Optional
import re

class ExecutionCategory(BaseModel):
    name: str
    abbreviation: str


class ProcedureId(BaseModel):
    type: str
    id: str


class AttireTarget(BaseModel):
    host: Optional[str]
    ip: IPvAnyAddress = None

    class Config:
        validate_assignment = True


class ExecutionData(BaseModel):
    command: str = Field(alias="execution-command")
    execution_id: str = Field(alias="execution-id")
    source: str = Field(alias="execution-source")
    category: Optional[ExecutionCategory] = Field(alias="execution-category")
    target: Optional[AttireTarget]
    time_generated: Optional[str] = Field(alias="time-generated")

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True


class OutputItem(BaseModel):
    content: Optional[str]
    level: Optional[str]
    type: Optional[str]


class ProcedureId(BaseModel):
    type: str
    id: str

    class Config:
        validate_assignment = True


class Step(BaseModel):
    command: Optional[str]
    executor: Optional[str]
    order: Optional[int]
    output: Optional[List[OutputItem]]
    time_start: Optional[str] = Field(alias="time-start")
    time_stop: Optional[str] = Field(alias="time-stop")

    class Config:
        allow_population_by_field_name = True

class Procedure(BaseModel):
    procedure_name: Optional[str] = Field(alias="procedure-name")
    procedure_description: Optional[str] = Field(alias="procedure-description")
    procedure_id: Optional[ProcedureId] = Field(alias="procedure-id")
    mitre_technique_id: Optional[str] = Field(alias="mitre-technique-id")
    order: Optional[int]
    steps: List[Step] = [str]

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

    @validator('mitre_technique_id')
    def mitre_id_format(cls, v):
        mitre_id = ("^(T\d{4})(\.\d{3})?$")
        if not re.match(mitre_id, v):
            return ValueError("Mitre Technique ID format unrecognized")
        return v.title()


class AttireLog(BaseModel):
    attire_version: Optional[str] = Field(alias="attire-version")
    execution_data: Optional[ExecutionData] = Field(alias="execution-data")
    procedures: List[Procedure] = []

    class Config:
        allow_population_by_field_name = True
