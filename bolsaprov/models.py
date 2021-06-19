from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List

from bolsaprov.constants import (
    ASSET_EVENT_TYPE_MAPPER,
    ASSET_ESPECIF_TYPE_MAPPER,
    BrokerAssetExtractEspecif,
    BrokerAssetExtractEventType
)


@dataclass
class BrokerParseExtraData():
    data: str


@dataclass
class Broker():
    value: str
    name: str
    parse_extra_data: BrokerParseExtraData
    accounts: List = field(default_factory=lambda: [])


@dataclass
class BrokerAccountParseExtraData():
    """ Essential data to do other requests using account information. """

    view_state: str
    view_state_generator: str
    event_validation: str


@dataclass
class BrokerAccount():
    id: str
    parse_extra_data: BrokerAccountParseExtraData


@dataclass
class BrokerAssetExtract():
    raw_negotiation_name: str
    asset_specification: str
    raw_negotiation_code: str
    operation_date: datetime
    event_type: str
    unit_amount: Decimal
    quotation_factor: int
    bruto_price: Decimal
    liquido_price: Decimal


    @classmethod
    def create_from_response_fields(
        cls,
        raw_negotiation_name,
        asset_specification,
        raw_negotiation_code,
        operation_date,
        event_type,
        unit_amount,
        quotation_factor,
        bruto_price,
        liquido_price,
    ):
        operation_date = datetime.strptime(operation_date, '%d/%m/%Y').date()
        # asset_specification = ASSET_ESPECIF_TYPE_MAPPER[asset_specification]
        # event_type = ASSET_EVENT_TYPE_MAPPER[event_type]
        unit_amount = cls._format_string_to_decimal(unit_amount)
        quotation_factor = int(quotation_factor)
        bruto_price = cls._format_string_to_decimal(bruto_price)
        liquido_price = cls._format_string_to_decimal(liquido_price)

        return cls(
            raw_negotiation_name=raw_negotiation_name,
            asset_specification=asset_specification,
            raw_negotiation_code=raw_negotiation_code,
            operation_date=operation_date,
            event_type=event_type,
            unit_amount=unit_amount,
            quotation_factor=quotation_factor,
            bruto_price=bruto_price,
            liquido_price=liquido_price
        )

    @staticmethod
    def _format_string_to_decimal(value):
        value = value.replace(',', '').replace('.', '')
        value = f'{value[:-2]}.{value[-2:]}'
        return Decimal(value)
