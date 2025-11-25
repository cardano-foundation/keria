# -*- encoding: utf-8 -*-
"""
KERIA
keria.core.operation module

"""

from dataclasses import dataclass, field
from marshmallow import fields
from typing import Optional, Union
from marshmallow_dataclass import class_schema
from keria.app import aiding, credentialing
from keria.app.credentialing import (
    Anchor,
    ACDC_V_1,
    ACDC_V_2,
    ICP_V_1,
    ICP_V_2,
    ROT_V_1,
    ROT_V_2,
    DIP_V_1,
    DIP_V_2,
    IXN_V_1,
    IXN_V_2,
)
from keria.app.aiding import (
    KeyStateRecord,
    EXN_V_1,
    EXN_V_2,
    RPY_V_1,
    RPY_V_2,
)
from keria.core.longrunning import Operation


@dataclass
class OOBIMetadata:
    oobi: str


@dataclass
class OOBIOperation(Operation):
    metadata: OOBIMetadata = field(
        default_factory=OOBIMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OOBIMetadata), required=False
            )
        },
    )
    response: aiding.KeyStateRecord = field(
        default_factory=aiding.KeyStateRecord,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(aiding.KeyStateRecord), required=False
            )
        },
    )


@dataclass
class QueryMetadata:
    pre: str
    sn: int
    anchor: credentialing.Anchor = field(
        default_factory=credentialing.Anchor,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(credentialing.Anchor), required=False
            )
        },
    )


@dataclass
class QueryOperation(Operation):
    metadata: QueryMetadata = field(
        default_factory=QueryMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(QueryMetadata), required=False
            )
        },
    )
    response: aiding.KeyStateRecord = field(
        default_factory=aiding.KeyStateRecord,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(aiding.KeyStateRecord), required=False
            )
        },
    )


@dataclass
class WitnessMetadata:
    pre: str
    sn: int


@dataclass
class WitnessOperation(Operation):
    metadata: WitnessMetadata = field(
        default_factory=WitnessMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(WitnessMetadata), required=False
            )
        },
    )
    response: Union[ICP_V_1, ICP_V_2, ROT_V_1, ROT_V_2, IXN_V_1, IXN_V_2] = None  # type: ignore


@dataclass
class DelegationMetadata:
    pre: str
    sn: int


@dataclass
class DelegationOperation(Operation):
    metadata: DelegationMetadata = field(
        default_factory=DelegationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(DelegationMetadata), required=False
            )
        },
    )
    response: Union[DIP_V_1, DIP_V_2] = None  # type: ignore


@dataclass
class DoneOperationMetadata:
    response: Union[ICP_V_1, ICP_V_2, ROT_V_1, ROT_V_2, EXN_V_1, EXN_V_2]  # type: ignore
    pre: str = None


@dataclass
class DoneOperation(Operation):
    metadata: DoneOperationMetadata = field(
        default_factory=DoneOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(DoneOperationMetadata), required=False
            )
        },
    )
    response: Union[ICP_V_1, ICP_V_2, ROT_V_1, ROT_V_2, EXN_V_1, EXN_V_2] = None  # type: ignore


@dataclass
class GroupOperationMetadata:
    pre: str
    sn: int


@dataclass
class GroupOperation(Operation):
    metadata: GroupOperationMetadata = field(
        default_factory=GroupOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(GroupOperationMetadata), required=False
            )
        },
    )
    response: Union[ICP_V_1, ICP_V_2, ROT_V_1, ROT_V_2, IXN_V_1, IXN_V_2] = None  # type: ignore


@dataclass
class DelegatorOperationMetadata:
    pre: str
    teepre: str
    anchor: credentialing.Anchor = field(
        default_factory=credentialing.Anchor,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(credentialing.Anchor), required=False
            )
        },
    )
    depends: Union["GroupOperation", "WitnessOperation", "DoneOperation"] = None  # type: ignore


@dataclass
class DelegatorOperation(Operation):
    metadata: DelegatorOperationMetadata = field(
        default_factory=DelegatorOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(DelegatorOperationMetadata), required=False
            )
        },
    )
    response: Optional[str] = field(
        default=None, metadata={"marshmallow_field": fields.String(allow_none=False)}
    )


@dataclass
class SubmitOperationMetadata:
    pre: str
    sn: int


@dataclass
class SubmitOperation(Operation):
    metadata: SubmitOperationMetadata = field(
        default_factory=SubmitOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(SubmitOperationMetadata), required=False
            )
        },
    )
    response: KeyStateRecord = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(KeyStateRecord), required=False
            )
        },
    )


@dataclass
class EndRoleMetadata:
    cid: str
    role: str
    eid: str


@dataclass
class EndRoleOperation(Operation):
    metadata: EndRoleMetadata = field(
        default_factory=EndRoleMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(EndRoleMetadata), required=False
            )
        },
    )
    response: Union[RPY_V_1, RPY_V_2]  # type: ignore


@dataclass
class LocSchemeMetadata:
    eid: str
    scheme: str
    url: str


@dataclass
class LocSchemeOperation(Operation):
    metadata: LocSchemeMetadata = field(
        default_factory=LocSchemeMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(LocSchemeMetadata), required=False
            )
        },
    )
    response: LocSchemeMetadata = field(
        default_factory=LocSchemeMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(LocSchemeMetadata), required=False
            )
        },
    )


@dataclass
class ChallengeMetadata:
    words: list[str]


@dataclass
class ChallengeOperation(Operation):
    metadata: ChallengeMetadata = field(
        default_factory=ChallengeMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(ChallengeMetadata), required=False
            )
        },
    )
    response: Union[EXN_V_1, EXN_V_2] = None  # type: ignore


@dataclass
class RegistryOperationMetadata:
    pre: str
    depends: Union[
        "GroupOperation", "WitnessOperation", "DoneOperation", "DelegationOperation"
    ]
    anchor: Anchor = field(
        default_factory=Anchor,
        metadata={
            "marshmallow_field": fields.Nested(class_schema(Anchor), required=True)
        },
    )


@dataclass
class RegistryOperationResponse:
    anchor: Anchor = field(
        default_factory=Anchor,
        metadata={
            "marshmallow_field": fields.Nested(class_schema(Anchor), required=True)
        },
    )


@dataclass
class RegistryOperation(Operation):
    metadata: RegistryOperationMetadata = field(
        default_factory=RegistryOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(RegistryOperationMetadata), required=False
            )
        },
    )
    response: RegistryOperationResponse = field(
        default_factory=RegistryOperationResponse,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(RegistryOperationResponse), required=False
            )
        },
    )


@dataclass
class CredentialOperationMetadata:
    ced: Union[ACDC_V_1, ACDC_V_2]  # type: ignore
    depends: Union[ROT_V_1, ROT_V_2, EXN_V_1, EXN_V_2] = None  # type: ignore


@dataclass
class CredentialOperationResponse:
    ced: Union[ACDC_V_1, ACDC_V_2] = None  # type: ignore


@dataclass
class CredentialOperation(Operation):
    metadata: CredentialOperationMetadata = field(
        default_factory=CredentialOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(CredentialOperationMetadata), required=False
            )
        },
    )
    response: CredentialOperationResponse = field(
        default_factory=CredentialOperationResponse,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(CredentialOperationResponse), required=False
            )
        },
    )


@dataclass
class ExchangeOperationMetadata:
    said: str


@dataclass
class ExchangeOperation(Operation):
    metadata: ExchangeOperationMetadata = field(
        default_factory=ExchangeOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(ExchangeOperationMetadata), required=False
            )
        },
    )
    response: ExchangeOperationMetadata = field(
        default_factory=ExchangeOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(ExchangeOperationMetadata), required=False
            )
        },
    )
