# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: WholeLandTokenData.proto
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
    'WholeLandTokenData.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18WholeLandTokenData.proto\x12\x04\x44\x61ta\"=\n\x15WholeLandTokenRequest\x12\x16\n\trequestId\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x0c\n\n_requestId\"Z\n\x16WholeLandTokenResponse\x12\x12\n\x05token\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x15\n\x08\x63onflict\x18\x02 \x01(\x08H\x01\x88\x01\x01\x42\x08\n\x06_tokenB\x0b\n\t_conflict\"2\n\x12\x44\x65leteTokenRequest\x12\x12\n\x05token\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x08\n\x06_token\"5\n\x13\x44\x65leteTokenResponse\x12\x13\n\x06result\x18\x01 \x01(\x08H\x00\x88\x01\x01\x42\t\n\x07_resultB\x16\n\x14\x63om.ea.simpsons.datab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'WholeLandTokenData_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\024com.ea.simpsons.data'
  _globals['_WHOLELANDTOKENREQUEST']._serialized_start=34
  _globals['_WHOLELANDTOKENREQUEST']._serialized_end=95
  _globals['_WHOLELANDTOKENRESPONSE']._serialized_start=97
  _globals['_WHOLELANDTOKENRESPONSE']._serialized_end=187
  _globals['_DELETETOKENREQUEST']._serialized_start=189
  _globals['_DELETETOKENREQUEST']._serialized_end=239
  _globals['_DELETETOKENRESPONSE']._serialized_start=241
  _globals['_DELETETOKENRESPONSE']._serialized_end=294
# @@protoc_insertion_point(module_scope)
