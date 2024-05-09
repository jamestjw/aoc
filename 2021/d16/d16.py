import sys
from functools import reduce
from operator import add
from math import prod


class Packet:
    def version_sum(self):
        raise NotImplementedError()

    def eval(self):
        raise NotImplementedError()


class Literal(Packet):
    def __init__(self, version, val):
        self.version = version
        self.val = val

    def version_sum(self):
        return self.version

    def eval(self):
        return self.val


class Operator(Packet):
    def __init__(self, version, subpackets: list[Packet], type_id):
        self.version = version
        self.subpackets = subpackets
        self.type_id = type_id

    def version_sum(self):
        return self.version + sum(s.version_sum() for s in self.subpackets)

    def eval(self):
        subvals = [s.eval() for s in self.subpackets]
        match self.type_id:
            case 0:
                return reduce(add, subvals)
            case 1:
                return prod(subvals)
            case 2:
                return reduce(min, subvals)
            case 3:
                return reduce(max, subvals)
            case 5:
                assert len(subvals) == 2
                return 1 if subvals[0] > subvals[1] else 0
            case 6:
                assert len(subvals) == 2
                return 1 if subvals[0] < subvals[1] else 0
            case 7:
                assert len(subvals) == 2
                return 1 if subvals[0] == subvals[1] else 0
            case _:
                raise Exception


def hex2bin(s):
    return (bin(int(s, 16))[2:]).zfill(len(s) * 4)


def transmission2packet(t: str):
    version = int(t[:3], 2)
    type_id = int(t[3:6], 2)
    other_bits = t[6:]

    if type_id == 4:
        # Handle literal
        acc = ""
        done = False
        while not done:
            prefix = other_bits[0]
            data = other_bits[1:5]
            if prefix == "0":
                done = True
            assert len(data) == 4
            acc += data
            other_bits = other_bits[5:]
        return Literal(version, int(acc, 2)), other_bits
    else:
        # Handle operator
        length = other_bits[0]
        if length == "0":
            num_bits = int(other_bits[1:16], 2)
            other_bits = other_bits[16:]

            use_now, others = other_bits[:num_bits], other_bits[num_bits:]

            packets = []

            while len(use_now) != 0:
                packet, use_now = transmission2packet(use_now)
                packets.append(packet)

            return Operator(version, packets, type_id), others
        else:
            num_packets = int(other_bits[1:12], 2)
            other_bits = other_bits[12:]

            packets = []
            for _ in range(num_packets):
                packet, other_bits = transmission2packet(other_bits)
                packets.append(packet)
            return Operator(version, packets, type_id), other_bits


transmissions = list(map(hex2bin, open(sys.argv[1]).read().splitlines()))
packets = [p for p, _ in map(transmission2packet, transmissions)]
print([p.version_sum() for p in packets])
print([p.eval() for p in packets])
