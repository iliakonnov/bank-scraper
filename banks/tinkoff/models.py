# generated by datamodel-codegen:
#   filename:  sample.json
#   timestamp: 2024-12-26T19:16:05+00:00

from __future__ import annotations

from typing import NotRequired, TypedDict


class Subgroup(TypedDict):
    id: str
    name: str


class Amount(TypedDict):
    value: int
    loyaltyProgramId: str
    loyalty: str
    name: str
    loyaltySteps: int
    loyaltyPointsId: int
    loyaltyPointsName: str
    loyaltyImagine: bool
    partialCompensation: bool


class LoyaltyBonu(TypedDict):
    description: str
    icon: str
    loyaltyType: str
    amount: Amount
    compensationType: str


class Currency(TypedDict):
    code: int
    name: str
    strCode: str


class CashbackAmount(TypedDict):
    currency: Currency
    value: int


class DebitingTime(TypedDict):
    milliseconds: int


class RubAmount(TypedDict):
    currency: Currency
    value: float


class Category(TypedDict):
    id: str
    name: str


class OperationId(TypedDict):
    value: str
    source: str


class Amount1(TypedDict):
    currency: Currency
    value: float


class OperationTime(TypedDict):
    milliseconds: int


class SpendingCategory(TypedDict):
    name: str
    icon: str
    id: str
    baseColor: str


class AdditionalInfoItem(TypedDict):
    fieldName: str
    fieldValue: str


class AccountAmount(TypedDict):
    currency: Currency
    value: float


class LoyaltyBonusSummary(TypedDict):
    amount: int


class FeeAmount(TypedDict):
    currency: Currency
    value: int


class FieldsValues(TypedDict):
    vbxlCurrency: NotRequired[str]
    vbxlAccount: NotRequired[str]
    bankContract: NotRequired[str]
    description: NotRequired[str]
    qrId: NotRequired[str]
    merchantDisplayName: NotRequired[str]
    mcc: NotRequired[str]
    merchantName: NotRequired[str]
    transactionId: NotRequired[str]
    confirmationCode: NotRequired[str]
    orderId: NotRequired[str]
    uid: NotRequired[str]
    phone: NotRequired[str]
    operationId: NotRequired[str]
    messageId: NotRequired[str]
    bankMemberId: NotRequired[str]
    receiverBankName: NotRequired[str]
    maskedFIO: NotRequired[str]
    pointer: NotRequired[str]
    card_number: NotRequired[str]
    pointerType: NotRequired[str]
    workflowType: NotRequired[str]
    pointerLinkId: NotRequired[str]
    extLegalId: NotRequired[str]
    bankAcnt: NotRequired[str]
    lastName: NotRequired[str]
    firstName: NotRequired[str]
    comment: NotRequired[str]
    bankBik: NotRequired[str]
    bankName: NotRequired[str]
    middleName: NotRequired[str]
    pointerCard: NotRequired[str]
    maskedPAN: NotRequired[str]
    acquiring_part_price: NotRequired[str]
    order_id: NotRequired[str]
    auto_cancel_time: NotRequired[str]
    departure_time: NotRequired[str]
    booking_number: NotRequired[str]
    ip_check: NotRequired[str]
    email: NotRequired[str]
    acquiring_part_currency: NotRequired[str]


class Payment(TypedDict):
    paymentId: str
    providerGroupId: str
    paymentType: str
    feeAmount: FeeAmount
    providerId: str
    hasPaymentOrder: bool
    comment: str
    repeatable: bool
    cardNumber: str
    sourceIsQr: bool
    bankAccountId: str
    isQrPayment: bool
    fieldsValues: FieldsValues
    templateId: NotRequired[str]
    templateIsFavorite: NotRequired[bool]


class Brand(TypedDict):
    name: str
    id: str
    roundedLogo: bool
    link: NotRequired[str]
    baseTextColor: NotRequired[str]
    fileLink: NotRequired[str]
    baseColor: NotRequired[str]
    logoFile: NotRequired[str]
    logo: NotRequired[str]


class Region(TypedDict):
    country: str
    city: NotRequired[str]
    address: NotRequired[str]
    zip: NotRequired[str]


class Merchant(TypedDict):
    name: str
    region: NotRequired[Region]


class PayloadItem(TypedDict):
    isOffline: bool
    icon: str
    isInner: bool
    type: str
    isAuto: bool
    subgroup: NotRequired[Subgroup]
    analyticsStatus: str
    hasStatement: bool
    isSuspicious: bool
    id: str
    status: str
    operationTransferred: bool
    idSourceType: str
    loyaltyBonus: list[LoyaltyBonu]
    cashbackAmount: CashbackAmount
    description: str
    debitingTime: NotRequired[DebitingTime]
    isTemplatable: bool
    rubAmount: NotRequired[RubAmount]
    mcc: int
    category: Category
    mccString: str
    locations: list
    cashback: int
    operationId: OperationId
    amount: Amount1
    operationTime: OperationTime
    spendingCategory: SpendingCategory
    offers: list
    isHce: bool
    additionalInfo: list[AdditionalInfoItem]
    account: str
    loyaltyPayment: list
    trancheCreationAllowed: bool
    cardPresent: bool
    accountAmount: AccountAmount
    isExternalCard: bool
    loyaltyBonusSummary: NotRequired[LoyaltyBonusSummary]
    isDispute: NotRequired[bool]
    typeSerno: NotRequired[int]
    authorizationId: NotRequired[str]
    payment: NotRequired[Payment]
    operationPaymentType: NotRequired[str]
    ucid: NotRequired[str]
    group: NotRequired[str]
    brand: NotRequired[Brand]
    posId: NotRequired[str]
    subcategory: NotRequired[str]
    merchantKey: NotRequired[str]
    virtualPaymentType: NotRequired[int]
    merchant: NotRequired[Merchant]
    cardNumber: NotRequired[str]
    senderAgreement: NotRequired[str]
    card: NotRequired[str]
    pointOfSaleId: NotRequired[int]
    hasShoppingReceipt: NotRequired[bool]
    compensation: NotRequired[str]
    message: NotRequired[str]
    senderDetails: NotRequired[str]
    installmentStatus: NotRequired[str]
    authMessage: NotRequired[str]


class Model(TypedDict):
    payload: list[PayloadItem]
