from enum import Enum, unique


@unique
class BrokerAssetExtractEspecif(Enum):
    PN = 'pn'
    ON = 'on'
    CI = 'ci'
    REC = 'rec'


@unique
class BrokerAssetExtractEventType(Enum):
    JUROS = 'juros'
    REND = 'rendimentos'
    PROV = 'proventos'


ASSET_ESPECIF_TYPE_MAPPER = {
    'ON NM': BrokerAssetExtractEspecif.ON.value,
    'CI': BrokerAssetExtractEspecif.CI.value,
    'REC': BrokerAssetExtractEspecif.REC.value,
}

ASSET_EVENT_TYPE_MAPPER = {
    'JUROS SOBRE CAPITAL PRÓPRIO': BrokerAssetExtractEventType.JUROS.value,
    'RENDIMENTO': BrokerAssetExtractEventType.REND.value,
    'PROVENTOS': BrokerAssetExtractEventType.PROV.value
}
