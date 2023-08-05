from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.main_arg_signature_args_item_typ import MainArgSignatureArgsItemTyp
from ..types import UNSET, Unset

T = TypeVar("T", bound="MainArgSignatureArgsItem")


@attr.s(auto_attribs=True)
class MainArgSignatureArgsItem:
    """
    Attributes:
        name (str):
        typ (MainArgSignatureArgsItemTyp):
        has_default (Union[Unset, bool]):
        default (Union[Unset, Any]):
    """

    name: str
    typ: MainArgSignatureArgsItemTyp
    has_default: Union[Unset, bool] = UNSET
    default: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        typ = self.typ.value

        has_default = self.has_default
        default = self.default

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "typ": typ,
            }
        )
        if has_default is not UNSET:
            field_dict["has_default"] = has_default
        if default is not UNSET:
            field_dict["default"] = default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        typ = MainArgSignatureArgsItemTyp(d.pop("typ"))

        has_default = d.pop("has_default", UNSET)

        default = d.pop("default", UNSET)

        main_arg_signature_args_item = cls(
            name=name,
            typ=typ,
            has_default=has_default,
            default=default,
        )

        main_arg_signature_args_item.additional_properties = d
        return main_arg_signature_args_item

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
