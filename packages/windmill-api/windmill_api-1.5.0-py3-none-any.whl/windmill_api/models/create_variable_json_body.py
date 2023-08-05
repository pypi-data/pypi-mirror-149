from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="CreateVariableJsonBody")


@attr.s(auto_attribs=True)
class CreateVariableJsonBody:
    """
    Attributes:
        path (str):
        value (str):
        is_secret (bool):
        description (str):
    """

    path: str
    value: str
    is_secret: bool
    description: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        value = self.value
        is_secret = self.is_secret
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "value": value,
                "is_secret": is_secret,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        value = d.pop("value")

        is_secret = d.pop("is_secret")

        description = d.pop("description")

        create_variable_json_body = cls(
            path=path,
            value=value,
            is_secret=is_secret,
            description=description,
        )

        create_variable_json_body.additional_properties = d
        return create_variable_json_body

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
