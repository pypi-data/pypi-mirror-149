# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import numpy as np
from cegalprizm.pythontool.grpc import petrelinterface_pb2

def subchunk_stream_to_np_array(po_guid, get_subchunk_stream_func, plink, chunk_type, irange, jrange, krange):
    ''' Creates and returns a numpy Array that mirrors the provided protobuf type object

    @src: A single or a list of petrelinterface_pb2.Chunk objects

    @Returns: numpy Array with dtype matching src's element type, and identical dimensions with content that matches the provided protobuf type object
    '''
    if plink._array_transfer_mode == petrelinterface_pb2.STREAM:
        request = petrelinterface_pb2.GetChunk_Request(
            guid = po_guid, 
            range_i = irange, 
            range_j = jrange,
            range_k = krange,
            chunk_type = chunk_type,
            array_transfer_mode = plink._array_transfer_mode
        )
        return _subchunk_stream_to_np_array(get_subchunk_stream_func(request))

def _subchunk_stream_to_np_array(subchunk_stream):
    ''' Creates and returns a numpy Array that mirrors the provided protobuf type object

    @src: A single or a list of petrelinterface_pb2.subchunk objects

    @Returns: numpy Array with dtype matching src's element type, and identical dimensions with content that matches the provided protobuf type object
    '''
    nparray = None
    
    for subchunk in subchunk_stream:
        nparray = _fill(nparray, subchunk)

    return _shape_array(subchunk, nparray)

def _get_nptype(subchunk):
    if subchunk.element_type == 'Single':
        return np.float32
    elif subchunk.element_type == 'Double':
        return np.float64
    elif subchunk.element_type == 'Int32':
        return np.int32
    elif subchunk.element_type == 'Int64':
        return np.int64
    elif subchunk.element_type == 'Boolean':
        return np.bool
    else:
        raise ValueError("Unknown dotnet array type")

def _get_data_array(subchunk):
    data = subchunk.data

    dtype = _get_nptype(subchunk)

    array = np.frombuffer(data, dtype=dtype)
    return array

def _get_subarray(subchunk):
    if subchunk.array_transfer_mode == petrelinterface_pb2.STREAM:
        nparray_chunk = _get_data_array(subchunk)
        return nparray_chunk

def _fill(nparray, subchunk):
    if nparray is None:
        nparray = _create_flat_nparray(subchunk)

    nparray_chunk = _get_subarray(subchunk)
    nparray[subchunk.local_start: subchunk.local_start + len(nparray_chunk)] = nparray_chunk[:]

    return nparray

def _create_flat_nparray(subchunk):
    nptype = _get_nptype(subchunk)

    nparray = np.zeros(subchunk.global_size, dtype=nptype)

    return nparray

def _shape_array(subchunk, nparray):
    si = subchunk.global_dimensions.i
    sj = subchunk.global_dimensions.j
    sk = subchunk.global_dimensions.k
    
    if subchunk.type == petrelinterface_pb2.SPANNING_IJ:
        return nparray.reshape((si,sj))
    elif subchunk.type == petrelinterface_pb2.SPANNING_I or subchunk.type == petrelinterface_pb2.SPANNING_J or subchunk.type == petrelinterface_pb2.SPANNING_K:
        return nparray.reshape(si*sj*sk)
    else:
        return nparray.reshape((si, sj, sk))
