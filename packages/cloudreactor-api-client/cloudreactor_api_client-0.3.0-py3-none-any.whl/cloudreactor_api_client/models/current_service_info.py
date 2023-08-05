import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CurrentServiceInfo")


@attr.s(auto_attribs=True)
class CurrentServiceInfo:
    """
    Attributes:
        type (Union[Unset, str]):
        service_arn (Union[Unset, None, str]):
        service_infrastructure_website_url (Union[Unset, None, str]):
        service_arn_updated_at (Union[Unset, None, datetime.datetime]):
    """

    type: Union[Unset, str] = UNSET
    service_arn: Union[Unset, None, str] = UNSET
    service_infrastructure_website_url: Union[Unset, None, str] = UNSET
    service_arn_updated_at: Union[Unset, None, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        service_arn = self.service_arn
        service_infrastructure_website_url = self.service_infrastructure_website_url
        service_arn_updated_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.service_arn_updated_at, Unset):
            service_arn_updated_at = self.service_arn_updated_at.isoformat() if self.service_arn_updated_at else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if service_arn is not UNSET:
            field_dict["service_arn"] = service_arn
        if service_infrastructure_website_url is not UNSET:
            field_dict["service_infrastructure_website_url"] = service_infrastructure_website_url
        if service_arn_updated_at is not UNSET:
            field_dict["service_arn_updated_at"] = service_arn_updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        service_arn = d.pop("service_arn", UNSET)

        service_infrastructure_website_url = d.pop("service_infrastructure_website_url", UNSET)

        _service_arn_updated_at = d.pop("service_arn_updated_at", UNSET)
        service_arn_updated_at: Union[Unset, None, datetime.datetime]
        if _service_arn_updated_at is None:
            service_arn_updated_at = None
        elif isinstance(_service_arn_updated_at, Unset):
            service_arn_updated_at = UNSET
        else:
            service_arn_updated_at = isoparse(_service_arn_updated_at)

        current_service_info = cls(
            type=type,
            service_arn=service_arn,
            service_infrastructure_website_url=service_infrastructure_website_url,
            service_arn_updated_at=service_arn_updated_at,
        )

        current_service_info.additional_properties = d
        return current_service_info

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
