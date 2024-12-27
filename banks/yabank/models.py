# generated by datamodel-codegen:
#   filename:  sample.json
#   timestamp: 2024-12-27T08:31:40+00:00

from __future__ import annotations

from typing import TypedDict


class Title(TypedDict):
    compound: None
    plain: str
    field__typename: str


class Money(TypedDict):
    amount: float
    currency: str
    field__typename: str


class Amount(TypedDict):
    money: Money | None
    plus: str | None
    field__typename: str


class FirstImage(TypedDict):
    light: str
    dark: str
    field__typename: str


class Image(TypedDict):
    firstImage: FirstImage
    secondImage: None
    field__typename: str


class Item(TypedDict):
    id: str
    date: str
    statusCode: str
    title: Title
    amount: Amount
    directionV2: str | None
    image: Image
    comment: None
    field__typename: str
    isMultipleCashback: None
    summaryCashback: None
    rightSubTitle: None
    rightSubTitleImage: None
    description: str


class GetTransactionsFeedView(TypedDict):
    items: list[Item]


class Data(TypedDict):
    getTransactionsFeedView: GetTransactionsFeedView


class Model(TypedDict):
    data: Data
