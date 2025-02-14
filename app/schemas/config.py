from pydantic import BaseModel


class ConfigBase(BaseModel):
    key: str
    value: str


class ConfigCreate(ConfigBase):
    pass


class ConfigUpdate(ConfigBase):
    pass


class ConfigOut(ConfigBase):
    class Config:
        from_attributes = True
