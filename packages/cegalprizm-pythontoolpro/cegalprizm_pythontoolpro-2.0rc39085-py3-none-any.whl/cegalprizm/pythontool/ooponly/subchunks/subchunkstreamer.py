# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc import petrelinterface_pb2
import math
import numpy as np

def np_array_to_subchunk_stream(po_guid, plink, stream_set_chunk_func, nparray, shift_start_i, shift_start_j, shift_start_k):
    ''' Creates and returns a ProtobufChunk object that mirrors the provided numpy array

    @nparray: numpy array

    @Returns: A petrelinterface_pb2.Chunk object matching nparray.dtype and identical dimensions with content that matches the provided numpy array
    '''
    global_origin = [shift_start_i, shift_start_j, shift_start_k]
    if plink._array_transfer_mode == petrelinterface_pb2.STREAM:
        sub_chunk_size_bytes = plink._preferred_streamed_unit_bytes

        iterable_requests = map(
            lambda subchunk: _subchunk_upload_request(po_guid, subchunk),
                _yield_subchunk_array(nparray, sub_chunk_size_bytes, global_origin)
        )
    
        plink._set_report(stream_set_chunk_func(iterable_requests))
    else:
        raise NotImplementedError()

def _subchunk_upload_request(po_guid, subchunk):
    return petrelinterface_pb2.SetSubchunk_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = po_guid),
            subchunk = subchunk
        )

def _get_element_type(sub_nparray):
    if sub_nparray.dtype == np.float32:
        return 'Single'
    elif sub_nparray.dtype == np.float64:
        return 'Double'
    elif sub_nparray.dtype == np.int32:
        return 'Int32'
    elif sub_nparray.dtype == np.int64:
        return 'Int64'
    elif sub_nparray.dtype == np.bool:
        return 'Boolean'
    else:
         raise ValueError("_get_element_type does not handle nparrays of type " + str(sub_nparray.dtype))

def _split(nparray, split_n):
    for i in range(0, len(nparray), split_n):
        yield i, nparray[i:i+split_n]


def _yield_subchunk_array(nparray, sub_chunk_size_bytes, global_origin):
    global_size = _get_global_size(nparray)

    for local_start, subarray in _split(nparray.ravel(), sub_chunk_size_bytes//nparray.dtype.itemsize):
        sub_chunk = petrelinterface_pb2.Subchunk(
            array_transfer_mode = petrelinterface_pb2.STREAM,
            global_size = nparray.size,
            global_dimensions = petrelinterface_pb2.Primitives.Indices3(
                i = global_size[0],
                j = global_size[1],
                k = global_size[2]
            ),
            global_origin = petrelinterface_pb2.Primitives.Indices3(
                i = global_origin[0],
                j = global_origin[1],
                k = global_origin[2]
            ),
            element_type = _get_element_type(nparray),
            local_start = local_start,
            data = subarray.tobytes()
        )
        yield sub_chunk

def _get_global_size(nparray):
    s = nparray.shape
    n = len(s)
    global_size = [
        s[0],
        s[1] if n > 1 else 1,
        s[2] if n > 2 else 1]
    
    if n == 1:
        global_size[2] = global_size[0] * global_size[1]
        global_size[0] = 1
        global_size[1] = 1

    return global_size
