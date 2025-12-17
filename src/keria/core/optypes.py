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
    AnchoringEvent,
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
    DRT_V_1,
    DRT_V_2,
)
from keria.app.aiding import (
    KeyStateRecord,
    RPY_V_1,
    RPY_V_2,
)
from keria.peer.exchanging import EXN_V_1, EXN_V_2
from keria.core.longrunning import (
    OperationStatus,
    PendingOperation,
    CompletedOperation,
    FailedOperation,
)


@dataclass
class OOBIMetadata:
    oobi: str


@dataclass
class PendingOOBIOperation(PendingOperation):
    metadata: OOBIMetadata = field(
        default_factory=OOBIMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OOBIMetadata), required=False
            )
        },
    )


@dataclass
class CompletedOOBIOperation(CompletedOperation):
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
class FailedOOBIOperation(FailedOperation):
    metadata: OOBIMetadata = field(
        default_factory=OOBIMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OOBIMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


OOBIOperation = Union[PendingOOBIOperation, CompletedOOBIOperation, FailedOOBIOperation]


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
class PendingQueryOperation(PendingOperation):
    metadata: QueryMetadata = field(
        default_factory=QueryMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(QueryMetadata), required=False
            )
        },
    )


@dataclass
class CompletedQueryOperation(CompletedOperation):
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
class FailedQueryOperation(FailedOperation):
    metadata: QueryMetadata = field(
        default_factory=QueryMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(QueryMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


QueryOperation = Union[
    PendingQueryOperation, CompletedQueryOperation, FailedQueryOperation
]


@dataclass
class WitnessMetadata:
    pre: str
    sn: int


@dataclass
class PendingWitnessOperation(PendingOperation):
    metadata: WitnessMetadata = field(
        default_factory=WitnessMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(WitnessMetadata), required=False
            )
        },
    )


@dataclass
class CompletedWitnessOperation(CompletedOperation):
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
class FailedWitnessOperation(FailedOperation):
    metadata: WitnessMetadata = field(
        default_factory=WitnessMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(WitnessMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


WitnessOperation = Union[
    PendingWitnessOperation, CompletedWitnessOperation, FailedWitnessOperation
]


@dataclass
class DelegationMetadata:
    pre: str
    sn: int


@dataclass
class PendingDelegationOperation(PendingOperation):
    metadata: DelegationMetadata = field(
        default_factory=DelegationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(DelegationMetadata), required=False
            )
        },
    )


@dataclass
class CompletedDelegationOperation(CompletedOperation):
    metadata: DelegationMetadata = field(
        default_factory=DelegationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(DelegationMetadata), required=False
            )
        },
    )
    response: Union[DIP_V_1, DIP_V_2, DRT_V_1, DRT_V_2] = None  # type: ignore


@dataclass
class FailedDelegationOperation(FailedOperation):
    metadata: DelegationMetadata = field(
        default_factory=DelegationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(DelegationMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


DelegationOperation = Union[
    PendingDelegationOperation, CompletedDelegationOperation, FailedDelegationOperation
]


@dataclass
class DoneOperationMetadata:
    response: Union[ICP_V_1, ICP_V_2, ROT_V_1, ROT_V_2, EXN_V_1, EXN_V_2]  # type: ignore
    pre: str = None


@dataclass
class PendingDoneOperation(PendingOperation):
    metadata: DoneOperationMetadata = field(
        default_factory=DoneOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(DoneOperationMetadata), required=False
            )
        },
    )


@dataclass
class CompletedDoneOperation(CompletedOperation):
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
class FailedDoneOperation(FailedOperation):
    metadata: DoneOperationMetadata = field(
        default_factory=DoneOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(DoneOperationMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


DoneOperation = Union[PendingDoneOperation, CompletedDoneOperation, FailedDoneOperation]


@dataclass
class GroupOperationMetadata:
    pre: str
    sn: int


@dataclass
class PendingGroupOperation(PendingOperation):
    metadata: GroupOperationMetadata = field(
        default_factory=GroupOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(GroupOperationMetadata), required=False
            )
        },
    )


@dataclass
class CompletedGroupOperation(CompletedOperation):
    metadata: GroupOperationMetadata = field(
        default_factory=GroupOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(GroupOperationMetadata), required=False
            )
        },
    )
    response: AnchoringEvent = None  # type: ignore


@dataclass
class FailedGroupOperation(FailedOperation):
    metadata: GroupOperationMetadata = field(
        default_factory=GroupOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(GroupOperationMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


GroupOperation = Union[
    PendingGroupOperation, CompletedGroupOperation, FailedGroupOperation
]


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
class PendingDelegatorOperation(PendingOperation):
    metadata: DelegatorOperationMetadata = field(
        default_factory=DelegatorOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(DelegatorOperationMetadata), required=False
            )
        },
    )


@dataclass
class CompletedDelegatorOperation(CompletedOperation):
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
class FailedDelegatorOperation(FailedOperation):
    metadata: DelegatorOperationMetadata = field(
        default_factory=DelegatorOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(DelegatorOperationMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


DelegatorOperation = Union[
    PendingDelegatorOperation, CompletedDelegatorOperation, FailedDelegatorOperation
]


@dataclass
class SubmitOperationMetadata:
    pre: str
    sn: int


@dataclass
class PendingSubmitOperation(PendingOperation):
    metadata: SubmitOperationMetadata = field(
        default_factory=SubmitOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(SubmitOperationMetadata), required=False
            )
        },
    )


@dataclass
class CompletedSubmitOperation(CompletedOperation):
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
class FailedSubmitOperation(FailedOperation):
    metadata: SubmitOperationMetadata = field(
        default_factory=SubmitOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(SubmitOperationMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


SubmitOperation = Union[
    PendingSubmitOperation, CompletedSubmitOperation, FailedSubmitOperation
]


@dataclass
class EndRoleMetadata:
    cid: str
    role: str
    eid: str


@dataclass
class PendingEndRoleOperation(PendingOperation):
    metadata: EndRoleMetadata = field(
        default_factory=EndRoleMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(EndRoleMetadata), required=False
            )
        },
    )


@dataclass
class CompletedEndRoleOperation(CompletedOperation):
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
class FailedEndRoleOperation(FailedOperation):
    metadata: EndRoleMetadata = field(
        default_factory=EndRoleMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(EndRoleMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


EndRoleOperation = Union[
    PendingEndRoleOperation, CompletedEndRoleOperation, FailedEndRoleOperation
]


@dataclass
class LocSchemeMetadata:
    eid: str
    scheme: str
    url: str


@dataclass
class PendingLocSchemeOperation(PendingOperation):
    metadata: LocSchemeMetadata = field(
        default_factory=LocSchemeMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(LocSchemeMetadata), required=False
            )
        },
    )


@dataclass
class CompletedLocSchemeOperation(CompletedOperation):
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
class FailedLocSchemeOperation(FailedOperation):
    metadata: LocSchemeMetadata = field(
        default_factory=LocSchemeMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(LocSchemeMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


LocSchemeOperation = Union[
    PendingLocSchemeOperation, CompletedLocSchemeOperation, FailedLocSchemeOperation
]


@dataclass
class ChallengeOperationMetadata:
    words: list[str]


@dataclass
class ChallengeOperationResponse:
    exn: Union[EXN_V_1, EXN_V_2]  # type: ignore


@dataclass
class PendingChallengeOperation(PendingOperation):
    metadata: ChallengeOperationMetadata = field(
        default_factory=ChallengeOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(ChallengeOperationMetadata), required=False
            )
        },
    )


@dataclass
class CompletedChallengeOperation(CompletedOperation):
    metadata: ChallengeOperationMetadata = field(
        default_factory=ChallengeOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(ChallengeOperationMetadata), required=False
            )
        },
    )
    response: ChallengeOperationResponse = field(
        default_factory=ChallengeOperationResponse,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(ChallengeOperationResponse), required=False
            )
        },
    )


@dataclass
class FailedChallengeOperation(FailedOperation):
    metadata: ChallengeOperationMetadata = field(
        default_factory=ChallengeOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(ChallengeOperationMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


ChallengeOperation = Union[
    PendingChallengeOperation, CompletedChallengeOperation, FailedChallengeOperation
]


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
class PendingRegistryOperation(PendingOperation):
    metadata: RegistryOperationMetadata = field(
        default_factory=RegistryOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(RegistryOperationMetadata), required=False
            )
        },
    )


@dataclass
class CompletedRegistryOperation(CompletedOperation):
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
class FailedRegistryOperation(FailedOperation):
    metadata: RegistryOperationMetadata = field(
        default_factory=RegistryOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(RegistryOperationMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


RegistryOperation = Union[
    PendingRegistryOperation, CompletedRegistryOperation, FailedRegistryOperation
]


@dataclass
class CredentialOperationMetadata:
    ced: Union[ACDC_V_1, ACDC_V_2]  # type: ignore
    depends: Union[ROT_V_1, ROT_V_2, DRT_V_1, DRT_V_2, IXN_V_1, IXN_V_2] = None  # type: ignore


@dataclass
class CredentialOperationResponse:
    ced: Union[ACDC_V_1, ACDC_V_2] = None  # type: ignore


@dataclass
class PendingCredentialOperation(PendingOperation):
    metadata: CredentialOperationMetadata = field(
        default_factory=CredentialOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(CredentialOperationMetadata), required=False
            )
        },
    )


@dataclass
class CompletedCredentialOperation(CompletedOperation):
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
class FailedCredentialOperation(FailedOperation):
    metadata: CredentialOperationMetadata = field(
        default_factory=CredentialOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(CredentialOperationMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


CredentialOperation = Union[
    PendingCredentialOperation, CompletedCredentialOperation, FailedCredentialOperation
]


@dataclass
class ExchangeOperationMetadata:
    said: str


@dataclass
class PendingExchangeOperation(PendingOperation):
    metadata: ExchangeOperationMetadata = field(
        default_factory=ExchangeOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(ExchangeOperationMetadata), required=False
            )
        },
    )


@dataclass
class CompletedExchangeOperation(CompletedOperation):
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


@dataclass
class FailedExchangeOperation(FailedOperation):
    metadata: ExchangeOperationMetadata = field(
        default_factory=ExchangeOperationMetadata,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(ExchangeOperationMetadata), required=False
            )
        },
    )
    error: Optional[OperationStatus] = field(
        default=None,
        metadata={
            "marshmallow_field": fields.Nested(
                class_schema(OperationStatus), required=False
            )
        },
    )


ExchangeOperation = Union[
    PendingExchangeOperation, CompletedExchangeOperation, FailedExchangeOperation
]
