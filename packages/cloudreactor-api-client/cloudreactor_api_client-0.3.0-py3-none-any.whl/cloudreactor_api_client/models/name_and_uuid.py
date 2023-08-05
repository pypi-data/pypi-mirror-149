from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NameAndUuid")


@attr.s(auto_attribs=True)
class NameAndUuid:
    """Identifies an entity in three ways: 1. UUID; 2. Name; and 3. URL.
    When used to indentify an entity in a request method body, only one of
    uuid and name needs to be specified. If both are present, they must
    refer to the same entity or else the response will be a 400 error.

        Attributes:
            uuid (Union[Unset, str]):
            url (Union[Unset, None, str]):
            name (Union[Unset, str]):
    """

    uuid: Union[Unset, str] = UNSET
    url: Union[Unset, None, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid
        url = self.url
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if url is not UNSET:
            field_dict["url"] = url
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        uuid = d.pop("uuid", UNSET)

        url = d.pop("url", UNSET)

        name = d.pop("name", UNSET)

        name_and_uuid = cls(
            uuid=uuid,
            url=url,
            name=name,
        )

        name_and_uuid.additional_properties = d
        return name_and_uuid

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
