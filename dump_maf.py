#!/usr/bin/env python3

from collections import namedtuple
import struct
import sys

mainblock_fields = namedtuple('maf_mainblock', 'rows columns location_types element_types elements UNKNOWN')
location_type_fields = namedtuple('maf_location_type', 'name type num') # num is guessed
element_type_fields = namedtuple('maf_element_type', 'name type num UNK_2 UNK_3 num_locations loc0 loc1') # num is guessed
element_fields = namedtuple('maf_element', 'elem_type elem_idx UNK_2 num_thing3 num_thing4')
UNKNOWN_fields = namedtuple('maf_UNKNOWN', 'UNK_0 UNK_1')

def main():
    infn = sys.argv[1]
    with open(infn, 'rb') as f:
        indata = f.read()
    # print(indata)

    filehdr = indata[:8]
    indata = indata[8:]
    print(filehdr)
    assert filehdr == b'MAF\x00\x00\x00\x09\x00'

    mainblock = indata[:0x18]
    indata = indata[0x18:]
    # print(mainblock)
    # print(indata)
    mainblock = mainblock_fields._make(struct.unpack("<iiiiii", mainblock))
    print(mainblock)

    for i in range(mainblock.location_types):
        print("***** location_type[{}] *****".format(i))
        location_type = indata[:0x28]
        indata = indata[0x28:]
        location_type = location_type_fields._make(struct.unpack("<32sii", location_type))
        print(location_type)

    for i in range(mainblock.element_types):
        print("***** element_type[{}] *****".format(i))
        element_type = indata[:0x3C]
        indata = indata[0x3C:]
        element_type = element_type_fields._make(struct.unpack("<32siiiiiii", element_type))
        print(element_type)

    for i in range(mainblock.columns):
        print("***** column[{}] *****".format(i))
        column = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(column)

    for i in range(mainblock.elements):
        print("***** element[{}] *****".format(i))
        element = indata[:0x14]
        indata = indata[0x14:]
        element = element_fields._make(struct.unpack("<iiiii", element))
        print(element)
        assert element.num_thing3 >= 0
        assert element.num_thing4 >= 0

        for j in range(element.num_thing3):
            element_thing3 = struct.unpack("<i", indata[:4])[0]
            indata = indata[4:]
            print("element[{}].thing3[{}] = {}".format(i, j, element_thing3))

        for j in range(element.num_thing4):
            element_thing4 = struct.unpack("<iI", indata[:8])
            indata = indata[8:]
            print("element[{}].thing4[{}] = ({}, 0x{:08X})".format(i, j, element_thing4[0], element_thing4[1]))

    for i in range(mainblock.UNKNOWN):
        print("***** UNKNOWN[{}] *****".format(i))
        UNKNOWN = indata[:8]
        indata = indata[8:]
        UNKNOWN = UNKNOWN_fields._make(struct.unpack("<ii", UNKNOWN))
        print(UNKNOWN)
        assert UNKNOWN.UNK_1 >= 0

        for j in range(UNKNOWN.UNK_1):
            UNKNOWN_thing1 = struct.unpack("<i", indata[:4])[0]
            indata = indata[4:]
            print("UNKNOWN[{}].UNK_1[{}] = {}".format(i, j, UNKNOWN_thing1))

    print(indata)
    assert len(indata) == 0

if __name__ == '__main__':
    main()
