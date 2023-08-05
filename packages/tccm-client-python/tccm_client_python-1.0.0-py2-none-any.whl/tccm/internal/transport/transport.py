# coding:utf-8
# -*- coding:utf-8 -*-
import httplib
import logging
import socket


class DefaultConfig(object):
    # net/http库会有连接池，连接池的大小，是可以打开的最大连接数
    defaultHttpConn = 4
    # http连接超时时间
    defaultHttpTimeout = 3
    # 默认的tcp的拨号时间
    defaultTcpConnTimeout = 1
    # 默认的长连接时间
    defaultKeepAliveTimeout = 30
    # 默认的空闲连接的超时时间
    defaultIdleConnTimeout = 10


class TranSport(object):
    UDPTransportMode = 1
    HTTPTransportMode = 2
    UnSupportTransportMode = 3

    def __init__(self, transport_mode, addr, port):
        super(TranSport, self).__init__()
        if transport_mode == TranSport.UDPTransportMode:
            self.udp_writer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.send_addr = (addr, port)
        if transport_mode == TranSport.HTTPTransportMode:
            self.http_writer = httplib.HTTPConnection(addr, port, timeout=DefaultConfig.defaultHttpTimeout)
            self.send_addr = None
        self.transport_mode = transport_mode

    def new_writer(self, transport_mode, addr, port):
        if transport_mode == TranSport.UDPTransportMode:
            self.udp_writer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.transport_mode = transport_mode
            return self
        # http协议, 暂不检测http的端口agent是否有监听, 不会使业务进程失败
        if transport_mode == TranSport.HTTPTransportMode:
            self.http_writer = httplib.HTTPConnection(addr, port, timeout=DefaultConfig.defaultHttpTimeout)
            self.transport_mode = transport_mode
            return self

    def write(self, data):
        if self.transport_mode == TranSport.UDPTransportMode:
            try:
                self.udp_writer.sendto(data, self.send_addr)
            except IOError:
                logging.error("Fail to udp request,error:", IOError)
                print("Fail to udp request,error:", IOError)
        elif self.transport_mode == TranSport.HTTPTransportMode:
            try:
                headers = {"Connection": "keep-alive"}
                self.http_writer.request('POST', '/api/v2', data, headers)
                response = self.http_writer.getresponse()
                response.read()
            except IOError:
                logging.error("Fail to http request,error:", IOError)
                print("Fail to http request,error:", IOError)
        else:
            logging.error("transport protocol just support http or udp.")
            raise NotImplementedError(u"transport protocol just support http or udp.")

    def close(self):
        if self.transport_mode == TranSport.UDPTransportMode:
            self.udp_writer.close()
        if self.transport_mode == TranSport.HTTPTransportMode:
            self.http_writer.close()
