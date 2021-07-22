from datetime import datetime
from enum import Enum
from typing import Optional, Union, List, Dict, Any

from pydantic import BaseModel, Field, validator
from pydantic.fields import ModelField

from .utils import validate_url


class Error(BaseModel):
    status: int
    timestamp: Optional[datetime]
    error: Optional[str]
    message: Optional[str]
    path: Optional[str]

    @validator('timestamp', pre=True, always=True)
    def timestamp_validator(cls, v: Optional[datetime]):
        return v or datetime.now()


class Result(BaseModel):
    result: Union[str, List]


class Domain(str, Enum):
    IN_SV = 'in.sv'
    VK_SV = 'vk.sv'
    TG_SV = 'tg.sv'
    YT_SV = 'yt.sv'
    FB_SV = 'fb.sv'
    GO_SV = 'go.sv'
    TO_SV = 'to.sv'
    TW_SV = 'dl.sv'
    MY_SV = 'my.sv'
    DL_SV = 'dl.sv'
    IT_SV = 'it.sv'
    AI_SV = 'ai.sv'
    BD_SV = 'bd.sv'
    DO_SV = 'do.sv'
    FL_SV = 'fl.sv'
    LC_SV = 'lc.sv'
    ID_SV = 'id.sv'
    ME_SV = 'me.sv'
    OK_SV = 'ok.sv'
    ON_SV = 'on.sv'
    QQ_SV = 'qq.sv'
    RT_SV = 'rt.sv'
    SA_SV = 'sa.sv'
    TT_SV = 'tt.sv'
    WA_SV = 'wa.sv'
    WC_SV = 'wc.sv'
    YA_SV = 'ya.sv'
    CLI_CO = 'cli.co'
    TWO_UA = '2.ua'
    FOUR_FO = '4.fo'
    LINK_SV = 'link.sv'


class Integration(BaseModel):
    callback_uri: str
    redirect_uri: Optional[str]
    user_data: Optional[Dict[str, str]]
    token: Optional[str]


class Link(BaseModel):
    target_url: str
    domain: Domain = Field(default=Domain.CLI_CO)
    is_deep: bool = Field(default=False)
    id_campaign: Optional[str]
    right_side: Optional[str]
    utm_phone: Optional[str]
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_campaign: Optional[str]
    utm_content: Optional[str]
    utm_term: Optional[str]
    callback_url: Optional[str]
    short_link: Optional[str]

    class Config:
        anystr_strip_whitespace = True

    def __str__(self):
        return self.short_link or self.target_url

    def __eq__(self, other):
        if self.short_link and other.short_link:
            return self.short_link == other.short_link
        return False

    @property
    def full_target_url(self) -> str:
        utm = '&'.join(tuple(f'{k}={v}' for k, v in self.dict().items() if 'utm_' in k and v))
        return f'{self.target_url}?{utm}' if len(utm) else self.target_url

    @property
    def link_id(self) -> Optional[str]:
        if self.short_link:
            return self.short_link.split('/')[-1]

    @validator('*', pre=True)
    def prepare_str(cls, v, **kwargs):
        if isinstance(v, str):
            field = kwargs.get('field', None)
            if isinstance(field, ModelField):
                if 'utm_' in field.name:
                    return v.replace(' ', '+')
            return v.replace(' ', '')
        return v

    @validator('target_url', 'callback_url')
    def url_validator(cls, v: Optional[str]):
        if v:
            _ = v.split('?')[0]
            return validate_url(s=_)
