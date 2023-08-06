#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum
from typing import List
import struct

@dataclass
class VnirHeader: # 16 bytes
    it: int
    scans: int
    max_channel: int
    min_channel: int
    saturation: int
    shutter: int
    drift: int
    dark_substracted: int
    reserved: List[int] # len 8

@dataclass
class SwirHeader: # 16 bytes
    tec_status: int
    tec_current: int
    max_channel: int
    min_channel: int
    saturation: int
    a_scans: int
    b_scans: int
    dark_current: int
    gain: int
    offset: int
    scansize1: int
    scansize2: int
    dark_substracted: int
    reserved: List[int] # len 3

@dataclass
class SpectrumHeader: # 64 bytes
    header: int
    errbyte: int
    sample_count: int
    trigger: int
    voltage: int
    current: int
    temperature: int
    motor_current: int
    instrument_hours: int
    instrument_minutes: int
    instrument_type: int
    ab: int
    reserved: List[int] # len 4
    v_header: VnirHeader
    s1_header: SwirHeader
    s2_header: SwirHeader

@dataclass
class FRInterpSpec:
    fr_spectrum_header: SpectrumHeader
    spec_buffer: List[float] # len 2151

    def to_npl_format(self):
        drift = self.fr_spectrum_header.v_header.drift
        for i in range(350, 1001):
            self.spec_buffer[i] = abs(self.spec_buffer[i] - drift)

@dataclass
class OptimizeStruct:
    header: int
    errbyte: int
    itime: int
    gain_1: int
    gain_2: int
    offset_1: int
    offset_2: int

@dataclass
class InitStruct:
    header: int
    errbyte: int
    name: List[str] # len 200 str of len 30
    value: List[float] # len 200 doubles
    count: int
    verify: int

class ITimeEnum(Enum):
    ms8p5 = -1
    ms17 = 0
    ms34 = 1
    ms68 = 2
    ms136 = 3
    ms272 = 4
    ms544 = 5
    s109 = 6
    s218 = 7
    s435 = 8
    s870 = 9
    s1741 = 10
    s3482 = 11
    M116 = 12
    M232 = 13
    M464 = 14
    M928 = 15

def create_FRInterpSpec(data: bytes) -> FRInterpSpec:
    header_ints = []
    spec_buffer = []
    for i in range(0, 64*4, 4):
        val = struct.unpack('!i', data[i:i+4])[0]
        header_ints.append(val)
    for i in range(64*4, len(data)-3, 4):
        val = struct.unpack('!f', data[i:i+4])[0]
        spec_buffer.append(val)
    v_header = VnirHeader(*[*header_ints[16:24], header_ints[24:32]])
    s1_header = SwirHeader(*[*header_ints[32:45], header_ints[45:48]])
    s2_header = SwirHeader(*[*header_ints[48:61], header_ints[61:]])
    header_params = [*header_ints[:12], header_ints[12:16], v_header, s1_header, s2_header]
    header = SpectrumHeader(*header_params)
    return FRInterpSpec(header, spec_buffer)

def create_OptimizeStruct(data: bytes) -> OptimizeStruct:
    vals = []
    for i in range(0, len(data)-3, 4):
        val = struct.unpack('!i', data[i:i+4])[0]
        vals.append(val)
    return OptimizeStruct(*vals)

def create_InitStruct(data: bytes) -> InitStruct:
    ints_start = []
    names = []
    values = []
    ints_end = []
    pointer = 0
    for i in range(pointer, 2*4, 4):
        val = struct.unpack('!i', data[i:i+4])[0]
        ints_start.append(val)
    pointer = 2*4
    for i in range(200):
        name = data[pointer+i*30:pointer+(i+1)*30].decode("utf-8")
        names.append(name)
    pointer += 200*30
    for i in range(pointer, pointer+200*8, 8):
        val = struct.unpack('d', data[i:i+8])[0]
        values.append(val)
    pointer += 200*8
    for i in range(pointer, pointer+2*4, 4):
        val = struct.unpack('!i', data[i:i+4])[0]
        ints_end.append(val)
    params = [*ints_start, names, values, *ints_end]
    return InitStruct(*params)
