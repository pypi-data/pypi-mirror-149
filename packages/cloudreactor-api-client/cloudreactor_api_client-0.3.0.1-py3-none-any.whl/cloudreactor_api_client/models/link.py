from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Link")


@attr.s(auto_attribs=True)
class Link:
    """Links represent a URL and associated metadata.

    Attributes:
        uuid (str):
        name (str):
        link_url_template (str):
        icon_url (str):
        rank (int):
        link_url (Union[Unset, str]):
        description (Union[Unset, str]):
    """

    uuid: str
    name: str
    link_url_template: str
    icon_url: str
    rank: int
    link_url: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid
        name = self.name
        link_url_template = self.link_url_template
        icon_url = self.icon_url
        rank = self.rank
        link_url = self.link_url
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "link_url_template": link_url_template,
                "icon_url": icon_url,
                "rank": rank,
            }
        )
        if link_url is not UNSET:
            field_dict["link_url"] = link_url
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        uuid = d.pop("uuid")

        name = d.pop("name")

        link_url_template = d.pop("link_url_template")

        icon_url = d.pop("icon_url")

        rank = d.pop("rank")

        link_url = d.pop("link_url", UNSET)

        description = d.pop("description", UNSET)

        link = cls(
            uuid=uuid,
            name=name,
            link_url_template=link_url_template,
            icon_url=icon_url,
            rank=rank,
            link_url=link_url,
            description=description,
        )

        link.additional_properties = d
        return link

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
