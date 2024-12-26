# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: PurchaseData.proto
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
    'PurchaseData.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12PurchaseData.proto\x12\x04\x44\x61ta\"S\n\x11PurchasedItemData\x12\x11\n\tproductId\x18\x01 \x01(\t\x12\x15\n\rpurchasePrice\x18\x02 \x01(\t\x12\x14\n\x0cpurchaseDate\x18\x03 \x01(\x03\"\x99\x01\n\x0c\x43urrencyData\x12\n\n\x02id\x18\x01 \x01(\t\x12\x18\n\x10vcTotalPurchased\x18\x02 \x01(\x05\x12\x16\n\x0evcTotalAwarded\x18\x03 \x01(\x05\x12\x11\n\tvcBalance\x18\x04 \x01(\x05\x12\x11\n\tcreatedAt\x18\x05 \x01(\x03\x12\x11\n\tupdatedAt\x18\x06 \x01(\x03\x12\x12\n\nunverified\x18\x07 \x01(\x05\"/\n\x11PurchaseErrorData\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0c\n\x04type\x18\x02 \x01(\t\"\xe6\x01\n\x17PurchaseResponseMessage\x12$\n\x08\x63urrency\x18\x01 \x01(\x0b\x32\x12.Data.CurrencyData\x12*\n\tpurchases\x18\x02 \x03(\x0b\x32\x17.Data.PurchasedItemData\x12&\n\x05\x65rror\x18\x03 \x01(\x0b\x32\x17.Data.PurchaseErrorData\x12\"\n\torderData\x18\x04 \x03(\x0b\x32\x0f.Data.OrderData\x12-\n\rsubscriptions\x18\x05 \x03(\x0b\x32\x16.Data.SubscriptionData\"\xb1\x07\n\x16PurchaseRequestMessage\x12\x0f\n\x07receipt\x18\x01 \x01(\t\x12\x12\n\nsignedData\x18\x02 \x01(\t\x12\x11\n\tsignature\x18\x03 \x01(\t\x12(\n\x08platform\x18\x04 \x01(\x0e\x32\x16.Data.PurchasePlatform\x12\x15\n\rpurchaseToken\x18\x05 \x01(\t\x12\x14\n\x0c\x61mazonUserId\x18\x06 \x01(\t\x12=\n\x0bpaymentInfo\x18\x07 \x03(\x0b\x32(.Data.PurchaseRequestMessage.PaymentInfo\x12\x39\n\tdeviceIds\x18\x08 \x03(\x0b\x32&.Data.PurchaseRequestMessage.DeviceIds\x12\x45\n\x0f\x61pplicationInfo\x18\t \x01(\x0b\x32,.Data.PurchaseRequestMessage.ApplicationInfo\x12;\n\ndeviceInfo\x18\n \x01(\x0b\x32\'.Data.PurchaseRequestMessage.DeviceInfo\x12\x1c\n\x14synergySystemVersion\x18\x0b \x01(\t\x12\x16\n\x0eisSubscription\x18\x0c \x01(\x08\x1aQ\n\x0bPaymentInfo\x12\x15\n\rtransactionId\x18\x01 \x01(\t\x12\x15\n\rpurchasePrice\x18\x02 \x01(\t\x12\x14\n\x0c\x63urrencyCode\x18\x03 \x01(\t\x1a\x35\n\tDeviceIds\x12\x1c\n\x04type\x18\x01 \x01(\x0e\x32\x0e.Data.DeviceId\x12\n\n\x02id\x18\x02 \x01(\t\x1a\xbb\x01\n\x0f\x41pplicationInfo\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\x10\n\x08\x62undleId\x18\x02 \x01(\t\x12\x0f\n\x07\x61ppName\x18\x03 \x01(\t\x12\x12\n\nappVersion\x18\x04 \x01(\t\x12\x13\n\x0b\x61ppLanguage\x18\x05 \x01(\t\x12\x13\n\x0b\x63ountryCode\x18\x06 \x01(\t\x12\x15\n\rfacebookAppId\x18\x07 \x01(\t\x12\x1d\n\x15\x66\x61\x63\x65\x62ookAttributionId\x18\x08 \x01(\t\x1a\x8b\x01\n\nDeviceInfo\x12\x12\n\nsystemName\x18\x01 \x01(\t\x12\x17\n\x0flimitAdTracking\x18\x02 \x01(\x08\x12\x16\n\x0e\x64\x65viceNativeId\x18\x03 \x01(\t\x12\x12\n\ndeviceType\x18\x04 \x01(\t\x12\x16\n\x0eiadAttribution\x18\x05 \x01(\x08\x12\x0c\n\x04imei\x18\x06 \x01(\t\"\xef\x01\n\tOrderData\x12\x16\n\x0enotificationId\x18\x01 \x01(\t\x12\x0f\n\x07orderId\x18\x02 \x01(\t\x12\x32\n\x05state\x18\x03 \x01(\x0e\x32\x1a.Data.OrderData.OrderState:\x07IGNORED\x12(\n\x08platform\x18\x04 \x01(\x0e\x32\x16.Data.PurchasePlatform\x12\x15\n\rpurchaseToken\x18\x05 \x01(\t\x12\x12\n\nsignedData\x18\x06 \x01(\t\"0\n\nOrderState\x12\t\n\x05VALID\x10\x00\x12\x0b\n\x07IGNORED\x10\x01\x12\n\n\x06\x46\x41ILED\x10\x02\"\x96\x01\n\x10SubscriptionData\x12\x16\n\x0esubscriptionId\x18\x01 \x01(\t\x12\x12\n\npurchaseId\x18\x02 \x01(\t\x12(\n\x08platform\x18\x03 \x01(\x0e\x32\x16.Data.PurchasePlatform\x12\x14\n\x0cpurchaseDate\x18\x04 \x01(\x03\x12\x16\n\x0evalidationDate\x18\x05 \x01(\x03*\x95\x01\n\x10PurchasePlatform\x12\n\n\x06ITUNES\x10\x00\x12\x11\n\rGOOGLEPLAY_V2\x10\x01\x12\x11\n\rGOOGLEPLAY_V3\x10\x02\x12\n\n\x06\x41MAZON\x10\x03\x12 \n\x1cITUNES_GRAND_UNIFIED_RECEIPT\x10\x04\x12\x12\n\x0eNOKIA_NORMANDY\x10\x05\x12\r\n\tAMAZON_V2\x10\x06*e\n\x08\x44\x65viceId\x12\x10\n\x0c\x45\x41_DEVICE_ID\x10\x00\x12\x07\n\x03\x41UT\x10\x01\x12\x11\n\rADVERTISER_ID\x10\x02\x12\r\n\tVENDOR_ID\x10\x03\x12\x0e\n\nANDROID_ID\x10\x04\x12\x0c\n\x08MAC_HASH\x10\x05\x42\x16\n\x14\x63om.ea.simpsons.data')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'PurchaseData_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\024com.ea.simpsons.data'
  _globals['_PURCHASEPLATFORM']._serialized_start=1895
  _globals['_PURCHASEPLATFORM']._serialized_end=2044
  _globals['_DEVICEID']._serialized_start=2046
  _globals['_DEVICEID']._serialized_end=2147
  _globals['_PURCHASEDITEMDATA']._serialized_start=28
  _globals['_PURCHASEDITEMDATA']._serialized_end=111
  _globals['_CURRENCYDATA']._serialized_start=114
  _globals['_CURRENCYDATA']._serialized_end=267
  _globals['_PURCHASEERRORDATA']._serialized_start=269
  _globals['_PURCHASEERRORDATA']._serialized_end=316
  _globals['_PURCHASERESPONSEMESSAGE']._serialized_start=319
  _globals['_PURCHASERESPONSEMESSAGE']._serialized_end=549
  _globals['_PURCHASEREQUESTMESSAGE']._serialized_start=552
  _globals['_PURCHASEREQUESTMESSAGE']._serialized_end=1497
  _globals['_PURCHASEREQUESTMESSAGE_PAYMENTINFO']._serialized_start=1029
  _globals['_PURCHASEREQUESTMESSAGE_PAYMENTINFO']._serialized_end=1110
  _globals['_PURCHASEREQUESTMESSAGE_DEVICEIDS']._serialized_start=1112
  _globals['_PURCHASEREQUESTMESSAGE_DEVICEIDS']._serialized_end=1165
  _globals['_PURCHASEREQUESTMESSAGE_APPLICATIONINFO']._serialized_start=1168
  _globals['_PURCHASEREQUESTMESSAGE_APPLICATIONINFO']._serialized_end=1355
  _globals['_PURCHASEREQUESTMESSAGE_DEVICEINFO']._serialized_start=1358
  _globals['_PURCHASEREQUESTMESSAGE_DEVICEINFO']._serialized_end=1497
  _globals['_ORDERDATA']._serialized_start=1500
  _globals['_ORDERDATA']._serialized_end=1739
  _globals['_ORDERDATA_ORDERSTATE']._serialized_start=1691
  _globals['_ORDERDATA_ORDERSTATE']._serialized_end=1739
  _globals['_SUBSCRIPTIONDATA']._serialized_start=1742
  _globals['_SUBSCRIPTIONDATA']._serialized_end=1892
# @@protoc_insertion_point(module_scope)