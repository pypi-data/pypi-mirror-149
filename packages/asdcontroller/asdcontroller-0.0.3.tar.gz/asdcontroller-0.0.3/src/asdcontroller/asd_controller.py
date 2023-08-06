#!/usr/bin/env python3

import socket
import time
from typing import Callable

from .asd_types import FRInterpSpec, InitStruct, OptimizeStruct, ITimeEnum, \
    create_FRInterpSpec, create_InitStruct, create_OptimizeStruct

MAX_WLEN = 2500
MIN_WLEN = 350
INITIAL_MESSAGE_BASE_LEN = 47
ACQUIRE_HEADER_SIZE = 64
OPT_SIZE = 7
RESTORE_SIZE = 1904

class ASDController:

    def __init__(self, ip: str = "10.1.1.11", port: int = 8080):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.sock.settimeout(15)
        self.sock.connect((ip, port))
        self.hello = True

    def __del__(self):
        self.close()
    
    def _recv(self, data_bytes: int) -> bytes:
        initial_msg_len = 0
        if self.hello:
            initial_msg_len = len(self.ip) + len(str(self.port)) + INITIAL_MESSAGE_BASE_LEN
            self.hello = False
        msg: bytes = b''
        total_bytes = initial_msg_len + data_bytes
        try:
            while len(msg) < total_bytes:
                rec = self.sock.recv(16384)
                msg += rec
                time.sleep(0.1)
        except socket.timeout:
            raise Exception("Timeout error receiving data. Received {}, expected {} ({} + {})".format(
                len(msg), total_bytes, data_bytes, initial_msg_len))
        return msg[initial_msg_len:]

    
    def _restore(self) -> InitStruct:
        self.sock.settimeout(60)
        self.sock.sendall(bytes("RESTORE,1", "utf-8"))
        data = self._recv(RESTORE_SIZE*4)
        return create_InitStruct(data)

    def _optimize(self) -> OptimizeStruct:
        self.sock.settimeout(60)
        self.sock.sendall(bytes("OPT,7", "utf-8"))
        data = self._recv(OPT_SIZE*4)
        return create_OptimizeStruct(data)
    
    def _acquire(self, n_averages: int) -> FRInterpSpec:
        self.sock.settimeout(5 + 1*n_averages)
        self.sock.sendall(bytes("A,1,{}".format(n_averages), "utf-8"))
        data = self._recv((MAX_WLEN - MIN_WLEN)*4 + ACQUIRE_HEADER_SIZE*4)
        return create_FRInterpSpec(data)
    
    def _set_itime(self, itime: ITimeEnum) -> FRInterpSpec:
        self.sock.settimeout(5)
        self.sock.sendall(bytes("A,2,{}".format(itime.value), "utf-8"))
        data = self._recv((MAX_WLEN - MIN_WLEN)*4 + ACQUIRE_HEADER_SIZE*4)
        return create_FRInterpSpec(data)
    
    def send_cmd(self, f: Callable, args: list = []):
        try:
            return f(*args)
        except (ConnectionResetError, BrokenPipeError):
            self.close()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
            self.hello = True
            self._optimize() # This might be wrong
            return f(*args)

    def restore(self) -> OptimizeStruct:
        return self.send_cmd(self._restore)

    def optimize(self) -> OptimizeStruct:
        return self.send_cmd(self._optimize)

    def acquire(self, n_averages: int) -> FRInterpSpec:
        return self.send_cmd(self._acquire, [n_averages])

    def set_itime(self, itime: ITimeEnum) -> FRInterpSpec:
        return self.send_cmd(self._set_itime, [itime])

    def close(self):
        self.sock.close()
