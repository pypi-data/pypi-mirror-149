import logging
import os

import grpc

from apeman.dal.tsdb import tsdb_pb2
from apeman.dal.tsdb import tsdb_pb2_grpc

logger = logging.getLogger("apeman.tsdb.client")


class ApemanDalTsdbClient(object):

    def __init__(self):
        apeman_dal_server_addr = os.getenv("apeman_dal_server_addr")
        if apeman_dal_server_addr is None:
            raise RuntimeError('Invalid value of apeman_dal_server_addr')

        logging.info('Connect to APEMAN DAL server %s', apeman_dal_server_addr)
        channel = grpc.insecure_channel(apeman_dal_server_addr)
        self.__stub = tsdb_pb2_grpc.TsdbServiceStub(channel)

    def create_datafeed(self, request=None):
        self.__stub.createDatafeed(request=request)

    def delete_datafeed(self, datafeed=''):
        request = tsdb_pb2.DeleteDatafeedRequest(datafeed=datafeed)
        self.__stub.deleteDatafeed(request=request)

    def get_datafeed(self, datafeed=''):
        request = tsdb_pb2.GetDatafeedRequest(datafeed=datafeed)
        return self.__stub.getDatafeed(request=request)

    def list_datafeed(self, query_filter=''):
        request = tsdb_pb2.ListDatafeedRequest(filter=query_filter)
        return self.__stub.listDatafeed(request=request)

    def put_data(self, datafeed='', data=None):
        request = tsdb_pb2.PutDataRequest(datafeed=datafeed, data=data)
        self.__stub.putData(request=request)

    def get_data(self, request=None):
        return self.__stub.getData(request=request)
