# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: OffersData.proto
# Protobuf Python Version: 5.28.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    3,
    '',
    'OffersData.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import Error_pb2 as Error__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10OffersData.proto\x12\x04\x44\x61ta\x1a\x0b\x45rror.proto\"\xd6\x0c\n\x15OffersResponseMessage\x12\x39\n\nofferItems\x18\x01 \x03(\x0b\x32%.Data.OffersResponseMessage.OfferItem\x12K\n\x13popularityRangeList\x18\x02 \x03(\x0b\x32..Data.OffersResponseMessage.ItemPopularityList\x12!\n\x05\x65rror\x18\x03 \x01(\x0b\x32\x12.Data.ErrorMessage\x12\x43\n\x0flevelUpXpOffers\x18\x04 \x03(\x0b\x32*.Data.OffersResponseMessage.LevelUpXpOffer\x12J\n\x12priceOverrideOffer\x18\x05 \x03(\x0b\x32..Data.OffersResponseMessage.PriceOverrideOffer\x1a\xc7\x02\n\tOfferItem\x12\x42\n\tofferType\x18\x01 \x01(\x0e\x32/.Data.OffersResponseMessage.OfferItem.OfferType\x12\x11\n\tproductId\x18\x02 \x01(\t\x12T\n\x12recommendationType\x18\x03 \x01(\x0e\x32\x38.Data.OffersResponseMessage.OfferItem.RecommendationType\"N\n\tOfferType\x12\x07\n\x03MTX\x10\x01\x12\x0b\n\x07PREMIUM\x10\x02\x12\r\n\tCHARACTER\x10\x03\x12\x0c\n\x08\x42UILDING\x10\x04\x12\x0e\n\nCONSUMABLE\x10\x05\"=\n\x12RecommendationType\x12\r\n\tRECOMMEND\x10\x01\x12\t\n\x05WATCH\x10\x02\x12\r\n\tNOCONVERT\x10\x03\x1a\xd1\x02\n\x12ItemPopularityList\x12\x13\n\x0b\x64isplayName\x18\x01 \x01(\t\x12V\n\x12popularityItemList\x18\x03 \x03(\x0b\x32:.Data.OffersResponseMessage.ItemPopularityList.PopularItem\x1a\xcd\x01\n\x0bPopularItem\x12W\n\x0epopularityType\x18\x01 \x01(\x0e\x32?.Data.OffersResponseMessage.ItemPopularityList.PopularItem.Type\x12\n\n\x02id\x18\x02 \x01(\x05\x12\r\n\x05\x63ount\x18\x03 \x01(\x05\"J\n\x04Type\x12\x0c\n\x08\x42UILDING\x10\x01\x12\r\n\tCHARACTER\x10\x02\x12\x0e\n\nCONSUMABLE\x10\x03\x12\x08\n\x04SKIN\x10\x04\x12\x0b\n\x07UNKNOWN\x10\x05\x1a\xfa\x01\n\x0eLevelUpXpOffer\x12\r\n\x05level\x18\x01 \x01(\x05\x12\x16\n\x0expForNextLevel\x18\x02 \x01(\x05\x12\x18\n\x10\x64onutAwardAmount\x18\x03 \x01(\x05\x12\x18\n\x10moneyAwardAmount\x18\x04 \x01(\x05\x12W\n\x11levelUpRecordType\x18\x05 \x01(\x0e\x32<.Data.OffersResponseMessage.LevelUpXpOffer.LevelUpRecordType\"4\n\x11LevelUpRecordType\x12\t\n\x05OFFER\x10\x01\x12\x14\n\x10\x43ONVERSION_EVENT\x10\x02\x1a\xe5\x02\n\x12PriceOverrideOffer\x12Y\n\x10overrideItemType\x18\x01 \x01(\x0e\x32?.Data.OffersResponseMessage.PriceOverrideOffer.OverrideItemType\x12\x11\n\tproductId\x18\x02 \x01(\t\x12[\n\x11\x63urrencyPriceType\x18\x03 \x01(\x0e\x32@.Data.OffersResponseMessage.PriceOverrideOffer.CurrencyPriceType\x12\x16\n\x0e\x63urrencyAmount\x18\x04 \x01(\x05\"?\n\x10OverrideItemType\x12\r\n\tCHARACTER\x10\x01\x12\x0c\n\x08\x42UILDING\x10\x02\x12\x0e\n\nCONSUMABLE\x10\x03\"+\n\x11\x43urrencyPriceType\x12\t\n\x05GRIND\x10\x01\x12\x0b\n\x07PREMIUM\x10\x02\x42\x16\n\x14\x63om.ea.simpsons.data')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'OffersData_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\024com.ea.simpsons.data'
  _globals['_OFFERSRESPONSEMESSAGE']._serialized_start=40
  _globals['_OFFERSRESPONSEMESSAGE']._serialized_end=1662
  _globals['_OFFERSRESPONSEMESSAGE_OFFERITEM']._serialized_start=382
  _globals['_OFFERSRESPONSEMESSAGE_OFFERITEM']._serialized_end=709
  _globals['_OFFERSRESPONSEMESSAGE_OFFERITEM_OFFERTYPE']._serialized_start=568
  _globals['_OFFERSRESPONSEMESSAGE_OFFERITEM_OFFERTYPE']._serialized_end=646
  _globals['_OFFERSRESPONSEMESSAGE_OFFERITEM_RECOMMENDATIONTYPE']._serialized_start=648
  _globals['_OFFERSRESPONSEMESSAGE_OFFERITEM_RECOMMENDATIONTYPE']._serialized_end=709
  _globals['_OFFERSRESPONSEMESSAGE_ITEMPOPULARITYLIST']._serialized_start=712
  _globals['_OFFERSRESPONSEMESSAGE_ITEMPOPULARITYLIST']._serialized_end=1049
  _globals['_OFFERSRESPONSEMESSAGE_ITEMPOPULARITYLIST_POPULARITEM']._serialized_start=844
  _globals['_OFFERSRESPONSEMESSAGE_ITEMPOPULARITYLIST_POPULARITEM']._serialized_end=1049
  _globals['_OFFERSRESPONSEMESSAGE_ITEMPOPULARITYLIST_POPULARITEM_TYPE']._serialized_start=975
  _globals['_OFFERSRESPONSEMESSAGE_ITEMPOPULARITYLIST_POPULARITEM_TYPE']._serialized_end=1049
  _globals['_OFFERSRESPONSEMESSAGE_LEVELUPXPOFFER']._serialized_start=1052
  _globals['_OFFERSRESPONSEMESSAGE_LEVELUPXPOFFER']._serialized_end=1302
  _globals['_OFFERSRESPONSEMESSAGE_LEVELUPXPOFFER_LEVELUPRECORDTYPE']._serialized_start=1250
  _globals['_OFFERSRESPONSEMESSAGE_LEVELUPXPOFFER_LEVELUPRECORDTYPE']._serialized_end=1302
  _globals['_OFFERSRESPONSEMESSAGE_PRICEOVERRIDEOFFER']._serialized_start=1305
  _globals['_OFFERSRESPONSEMESSAGE_PRICEOVERRIDEOFFER']._serialized_end=1662
  _globals['_OFFERSRESPONSEMESSAGE_PRICEOVERRIDEOFFER_OVERRIDEITEMTYPE']._serialized_start=1554
  _globals['_OFFERSRESPONSEMESSAGE_PRICEOVERRIDEOFFER_OVERRIDEITEMTYPE']._serialized_end=1617
  _globals['_OFFERSRESPONSEMESSAGE_PRICEOVERRIDEOFFER_CURRENCYPRICETYPE']._serialized_start=1619
  _globals['_OFFERSRESPONSEMESSAGE_PRICEOVERRIDEOFFER_CURRENCYPRICETYPE']._serialized_end=1662
# @@protoc_insertion_point(module_scope)