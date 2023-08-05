from fast_micro.utils import camelize
from pydantic import BaseModel


class CamelCaseModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True
        frozen = True
