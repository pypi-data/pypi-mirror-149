import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.group import Group
from ..models.name_and_uuid import NameAndUuid
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedEmailNotificationProfile")


@attr.s(auto_attribs=True)
class PatchedEmailNotificationProfile:
    """An EmailProfile contains settings for emailing notifications.

    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, str]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        dashboard_url (Union[Unset, str]):
        created_by_user (Union[Unset, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
        created_by_group (Union[Unset, Group]):
        run_environment (Union[Unset, None, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and 3.
            URL.
            When used to indentify an entity in a request method body, only one of
            uuid and name needs to be specified. If both are present, they must
            refer to the same entity or else the response will be a 400 error.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        to_addresses (Union[Unset, None, List[str]]):
        cc_addresses (Union[Unset, None, List[str]]):
        bcc_addresses (Union[Unset, None, List[str]]):
        subject_template (Union[Unset, str]):
        body_template (Union[Unset, str]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    dashboard_url: Union[Unset, str] = UNSET
    created_by_user: Union[Unset, str] = UNSET
    created_by_group: Union[Unset, Group] = UNSET
    run_environment: Union[Unset, None, NameAndUuid] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    to_addresses: Union[Unset, None, List[str]] = UNSET
    cc_addresses: Union[Unset, None, List[str]] = UNSET
    bcc_addresses: Union[Unset, None, List[str]] = UNSET
    subject_template: Union[Unset, str] = UNSET
    body_template: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        uuid = self.uuid
        name = self.name
        description = self.description
        dashboard_url = self.dashboard_url
        created_by_user = self.created_by_user
        created_by_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.created_by_group, Unset):
            created_by_group = self.created_by_group.to_dict()

        run_environment: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.run_environment, Unset):
            run_environment = self.run_environment.to_dict() if self.run_environment else None

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        to_addresses: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.to_addresses, Unset):
            if self.to_addresses is None:
                to_addresses = None
            else:
                to_addresses = self.to_addresses

        cc_addresses: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.cc_addresses, Unset):
            if self.cc_addresses is None:
                cc_addresses = None
            else:
                cc_addresses = self.cc_addresses

        bcc_addresses: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.bcc_addresses, Unset):
            if self.bcc_addresses is None:
                bcc_addresses = None
            else:
                bcc_addresses = self.bcc_addresses

        subject_template = self.subject_template
        body_template = self.body_template

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if dashboard_url is not UNSET:
            field_dict["dashboard_url"] = dashboard_url
        if created_by_user is not UNSET:
            field_dict["created_by_user"] = created_by_user
        if created_by_group is not UNSET:
            field_dict["created_by_group"] = created_by_group
        if run_environment is not UNSET:
            field_dict["run_environment"] = run_environment
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if to_addresses is not UNSET:
            field_dict["to_addresses"] = to_addresses
        if cc_addresses is not UNSET:
            field_dict["cc_addresses"] = cc_addresses
        if bcc_addresses is not UNSET:
            field_dict["bcc_addresses"] = bcc_addresses
        if subject_template is not UNSET:
            field_dict["subject_template"] = subject_template
        if body_template is not UNSET:
            field_dict["body_template"] = body_template

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url", UNSET)

        uuid = d.pop("uuid", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        dashboard_url = d.pop("dashboard_url", UNSET)

        created_by_user = d.pop("created_by_user", UNSET)

        _created_by_group = d.pop("created_by_group", UNSET)
        created_by_group: Union[Unset, Group]
        if isinstance(_created_by_group, Unset):
            created_by_group = UNSET
        else:
            created_by_group = Group.from_dict(_created_by_group)

        _run_environment = d.pop("run_environment", UNSET)
        run_environment: Union[Unset, None, NameAndUuid]
        if _run_environment is None:
            run_environment = None
        elif isinstance(_run_environment, Unset):
            run_environment = UNSET
        else:
            run_environment = NameAndUuid.from_dict(_run_environment)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        to_addresses = cast(List[str], d.pop("to_addresses", UNSET))

        cc_addresses = cast(List[str], d.pop("cc_addresses", UNSET))

        bcc_addresses = cast(List[str], d.pop("bcc_addresses", UNSET))

        subject_template = d.pop("subject_template", UNSET)

        body_template = d.pop("body_template", UNSET)

        patched_email_notification_profile = cls(
            url=url,
            uuid=uuid,
            name=name,
            description=description,
            dashboard_url=dashboard_url,
            created_by_user=created_by_user,
            created_by_group=created_by_group,
            run_environment=run_environment,
            created_at=created_at,
            updated_at=updated_at,
            to_addresses=to_addresses,
            cc_addresses=cc_addresses,
            bcc_addresses=bcc_addresses,
            subject_template=subject_template,
            body_template=body_template,
        )

        patched_email_notification_profile.additional_properties = d
        return patched_email_notification_profile

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
