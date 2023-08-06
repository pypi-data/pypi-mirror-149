# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc import petrelinterface_pb2
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import Primitives as ProtobufPrimitives
from .subchunks import streamsubchunkcollector
from .subchunks import subchunkstreamer

import collections
import numpy as np
import typing

class Utils:
    
    sub_chunk_size_bytes = 2*1024*1024

    @classmethod
    def protobuf_map_to_dict(cls, protobuf_map: typing.Mapping[str, str], out_dict: typing.Optional[typing.Dict[str, str]] = None) -> typing.Dict[str, str]:
        if out_dict is None:
            out_dict = {}
        keys_list = [ key for key in protobuf_map ]
        for k in keys_list:
            out_dict[k] = protobuf_map[k]
        
        return out_dict

    @classmethod
    def dict_to_string(cls, dictionary, separator = ':\t', sort_by_value = True):
        if sort_by_value:
            sorted_pairs = sorted(dictionary.items(), key = lambda pair: (pair[1], pair[0]))
        else:
            sorted_pairs = sorted(dictionary.items(), key = lambda pair: (pair[0], pair[1]))

        a_list = []
        for pair in sorted_pairs:
            a_list.append(f"'{pair[0]}'{separator}'{pair[1]}'")

        return '\n'.join(a_list)


    @classmethod
    def grpc_get_subchunk(cls, po, get_chunk_stream_func, plink, chunk_type, range_i, range_j, range_k):
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = po._guid, sub_type = po._sub_type)
        if plink._array_transfer_mode == petrelinterface_pb2.STREAM:
            irange = ProtobufPrimitives.PairInt(value1 = range_i[0], value2 = range_i[1]) if range_i else None
            jrange = ProtobufPrimitives.PairInt(value1 = range_j[0], value2 = range_j[1]) if range_j else None
            krange = ProtobufPrimitives.PairInt(value1 = range_k[0], value2 = range_k[1]) if range_k else None
            return streamsubchunkcollector.subchunk_stream_to_np_array(
                po_guid, 
                get_chunk_stream_func, 
                plink, 
                chunk_type, 
                irange, 
                jrange, 
                krange
            )

    @classmethod
    def grpc_set_subchunk(cls, po_guid, plink, np_array, stream_set_chunk_func, shift_start_i, shift_start_j, shift_start_k):
        subchunkstreamer.np_array_to_subchunk_stream(
            po_guid,
            plink,
            stream_set_chunk_func,
            np_array, 
            shift_start_i, 
            shift_start_j, 
            shift_start_k
        )

class System:
    Minmax = collections.namedtuple('Minmax', ['MinValue', 'MaxValue'])
    Int32 = Minmax(int(-2147483648), int(2147483647))
    
    Nan = collections.namedtuple('Nan', 'NaN')
    Double = Nan(np.nan)
