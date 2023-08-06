# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from google.protobuf.any_pb2 import Any
import time
import logging
import pkg_resources
from packaging import version
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import ErrorType
from cegalprizm.pythontool.exceptions import UnexpectedErrorException, UserErrorException

def _handle_petrel_error(response):
    petrel_error = response.error
    if petrel_error.type == ErrorType.NoError:
        return True
    elif petrel_error.type == ErrorType.UserError:
        raise UserErrorException(petrel_error.message, petrel_error.stack_trace)
    elif petrel_error.type == ErrorType.UnexpectedError:
        raise UnexpectedErrorException(petrel_error.message, petrel_error.stack_trace)

def handle_response_error(response):
    if _handle_petrel_error(response._response):
        return response

def handle_stream_error(response_stream):
    for response in response_stream:
        if _handle_petrel_error(response):
            yield response

class BaseHub(object):
    
    def __init__(self, ptp_hub_ctx):
        self._connector_id = "cegal.hub.petrel"
        self._ptp_hub_ctx = ptp_hub_ctx
        pkg_version = pkg_resources.get_distribution('cegalprizm-pythontoolpro').version
        version_obj = version.parse(pkg_version)
        self._majorversion = version_obj.major
        self._minorversion = version_obj.minor

    def _wrapper(self, wkt, out_type, msg):
        return self._unary_wrapper(wkt, out_type, msg) # type: ignore

    def _unary_wrapper(self, wkt, out_type, msg):
        payload = Any()
        payload.Pack(msg)
        start_time = time.time()
        (ok, packed_response, connector_id) = self._ptp_hub_ctx.channel.do_unary_request(wellknown_connector_identifier=self._connector_id, 
                                                                           wellknown_payload_identifier=wkt, 
                                                                           payload=payload,
                                                                           connector_filter=self._ptp_hub_ctx.connector_filter, 
                                                                           major_version=self._majorversion,
                                                                           minor_version=self._minorversion)
        end_time = time.time()
        logging.debug("Packet to '{}' took {} to complete".format(wkt, end_time - start_time))
        if ok:
            if packed_response.Is(out_type.DESCRIPTOR):
                unpacked_response = out_type()
                packed_response.Unpack(unpacked_response)
                if _handle_petrel_error(unpacked_response):
                    return unpacked_response
            else:
                logging.error("Client problem: {}".format(packed_response))
                raise Exception("Client problem: {} is not".format(out_type))
        else:
            logging.error("Hub problem: {}".format(packed_response))
            raise Exception("Hub problem: {}".format(packed_response))

    def _server_streaming_wrapper(self, wkt, out_type, msg):
        payload = Any()
        payload.Pack(msg)
        packed_response_stream = self._ptp_hub_ctx.channel.do_server_streaming(wellknown_connector_identifier=self._connector_id, 
                                                                               wellknown_payload_identifier=wkt, 
                                                                               payload=payload,
                                                                               connector_filter=self._ptp_hub_ctx.connector_filter,
                                                                               major_version=self._majorversion,
                                                                               minor_version=self._minorversion)
        for (ok, packed_response, connector_id) in packed_response_stream:
            if ok:
                if packed_response.type_url == '':
                    break
                if packed_response.Is(out_type.DESCRIPTOR):
                    unpacked_response = out_type()
                    packed_response.Unpack(unpacked_response)
                    if _handle_petrel_error(unpacked_response):
                        yield unpacked_response
                else:
                    logging.error("Client problem: {} is not {}".format(packed_response, out_type))
                    raise Exception("Client problem: {} is not {}".format(packed_response, out_type))
            else:
                logging.error("Hub problem: {}".format(packed_response))
                raise Exception("Hub problem: {}".format(packed_response))

    def _client_streaming_wrapper(self, wkt, out_type, iterable_requests):
        def pack_iterable_requests(rqs):
            for rq in rqs:
                payload = Any()
                payload.Pack(rq)
                yield payload
        (ok, packed_response, connector_id) = self._ptp_hub_ctx.channel.do_client_streaming(wellknown_connector_identifier=self._connector_id, 
                                                                              wellknown_payload_identifier=wkt, 
                                                                              iterable_payloads=pack_iterable_requests(iterable_requests),
                                                                              connector_filter=self._ptp_hub_ctx.connector_filter,
                                                                              major_version=self._majorversion,
                                                                              minor_version=self._minorversion)
        if ok:
            if packed_response.Is(out_type.DESCRIPTOR):
                unpacked_response = out_type()
                packed_response.Unpack(unpacked_response)
                if _handle_petrel_error(unpacked_response):
                    return unpacked_response
            else:
                logging.error("Client problem: {}".format(packed_response))
                raise Exception("Client problem: {} is not".format(out_type))
        else:
            logging.error("Hub problem: {}".format(packed_response))
            raise Exception("Hub problem: {}".format(packed_response))