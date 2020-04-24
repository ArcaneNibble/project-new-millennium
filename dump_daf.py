#!/usr/bin/env python3

from collections import namedtuple
import struct
import sys

mainblock_fields = namedtuple('daf_mainblock', 'total_bits wl_offset pia_wl_offset pt_offset mc_pt_offset lab_offset pia_offset lab_pia_wls pia_wls pt_wls arch1_bits arch2_bits n_pins n_mcs n_labs n_data_bits n_default_groups n_jedec_groups n_vpterms n_jedec_bits pterms_per_mc exp_per_lab exp_per_mc lab_clocks lab_clears initial_arr_val first_pia_addr por_wl_1 por_wl_2 assemble_mux assemble_por jedec_defined bit_matches_jed bit_shift bit_mask')
arch_hdr_fields = namedtuple('daf_arch_hdr', 'arch_type arch_value num_bits offset index num_vpterm addr_rows addr_columns num_select')
arch_vpterm_fields = namedtuple('daf_arch_vpterm', 'input_eq_type vpterm condition setting')
default_group_fields = namedtuple('daf_default_group', 'start_addr num_bits offset value')
jedec_group_fields = namedtuple('daf_jedec_group', 'bit_array_baseaddr jed_array_baseaddr bit_array_offset jed_array_offset num_bits bit_strand_offset jed_strand_offset num_strands')
vpterm_fields = namedtuple('daf_vpterm', 'input_eq_type pterm_offset')

def main():
    infn = sys.argv[1]
    with open(infn, 'rb') as f:
        indata = f.read()
    # print(indata)

    filehdr = indata[:8]
    indata = indata[8:]
    print(filehdr)
    assert filehdr == b'DAF\x00\x00\x00\x0e\x00'

    mainblock = indata[:0x8c]
    indata = indata[0x8c:]
    # print(mainblock)
    # print(indata)
    mainblock = mainblock_fields._make(struct.unpack("<iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", mainblock))
    print(mainblock)

    for i in range(mainblock.arch1_bits + 1):
        print("***** arch_hdr1[{}] *****".format(i))
        arch_hdr = indata[:0x24]
        indata = indata[0x24:]
        # print(arch_hdr)
        arch_hdr = arch_hdr_fields._make(struct.unpack("<iiiiiiiii", arch_hdr))
        print(arch_hdr)

        for j in range(arch_hdr.num_select + 1):
            select = indata[:4]
            indata = indata[4:]
            select = struct.unpack("<i", select)[0]
            print("select[{}] = {}".format(j, select))

        for _ in range(arch_hdr.num_vpterm + 1):
            arch_vpterm = indata[:0x10]
            indata = indata[0x10:]
            arch_vpterm = arch_vpterm_fields._make(struct.unpack("<iiii", arch_vpterm))
            print(arch_vpterm)

        for _ in range(arch_hdr.addr_rows + 1):
            for _ in range(arch_hdr.addr_columns + 1):
                arch_addr = indata[:4]
                indata = indata[4:]
                arch_addr = struct.unpack("<i", arch_addr)[0]
                print(arch_addr, end='')
                print("\t", end='')
            print()

    for i in range(mainblock.arch2_bits + 1):
        print("***** arch_hdr2[{}] *****".format(i))
        arch_hdr = indata[:0x24]
        indata = indata[0x24:]
        # print(arch_hdr)
        arch_hdr = arch_hdr_fields._make(struct.unpack("<iiiiiiiii", arch_hdr))
        print(arch_hdr)

        for j in range(arch_hdr.num_select + 1):
            select = indata[:4]
            indata = indata[4:]
            select = struct.unpack("<i", select)[0]
            print("select[{}] = {}".format(j, select))

        for _ in range(arch_hdr.num_vpterm + 1):
            arch_vpterm = indata[:0x10]
            indata = indata[0x10:]
            arch_vpterm = arch_vpterm_fields._make(struct.unpack("<iiii", arch_vpterm))
            print(arch_vpterm)

        for _ in range(arch_hdr.addr_rows + 1):
            for _ in range(arch_hdr.addr_columns + 1):
                arch_addr = indata[:4]
                indata = indata[4:]
                arch_addr = struct.unpack("<i", arch_addr)[0]
                print(arch_addr, end='')
                print("\t", end='')
            print()

    for i in range(mainblock.n_default_groups + 1):
        print("***** default_group[{}] *****".format(i))
        default_group = indata[:0x10]
        indata = indata[0x10:]
        default_group = default_group_fields._make(struct.unpack("<iiii", default_group))
        print(default_group)

    for i in range(mainblock.n_jedec_groups + 1):
        print("***** bit_jed_conv[{}] *****".format(i))
        bit_jed_conv = indata[:0x20]
        indata = indata[0x20:]
        bit_jed_conv = jedec_group_fields._make(struct.unpack("<iiiiiiii", bit_jed_conv))
        print(bit_jed_conv)

    for i in range(2):
        print("***** oe_pin[{}] *****".format(i))
        oe_pin = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(oe_pin)

    for i in range(mainblock.n_pins + 1):
        print("***** io_wl[{}] *****".format(i))
        io_wl = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(io_wl)

    for i in range(mainblock.n_mcs + 1):
        print("***** mc_wl[{}] *****".format(i))
        mc_wl = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(mc_wl)

    for i in range(mainblock.exp_per_lab + 1):
        print("***** exp_wl[{}] *****".format(i))
        exp_wl = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(exp_wl)

    for i in range(mainblock.lab_pia_wls + 1):
        print("***** pia_wl[{}] *****".format(i))
        pia_wl = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(pia_wl)

    for i in range(mainblock.n_pins + 1):
        print("***** io_pia_wl[{}] *****".format(i))
        io_pia_wl = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(io_pia_wl)

    for i in range(mainblock.n_mcs + 1):
        print("***** mc_pia_wl[{}] *****".format(i))
        mc_pia_wl = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(mc_pia_wl)

    for i in range(mainblock.n_mcs + 1):
        print("***** mc_lab[{}] *****".format(i))
        mc_lab = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(mc_lab)

    for i in range(mainblock.n_mcs + 1):
        print("***** mc_data_bit[{}] *****".format(i))
        mc_data_bit = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(mc_data_bit)

    for i in range(mainblock.n_labs + 1):
        print("***** pia_data_bit[{}] *****".format(i))
        pia_data_bit = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(pia_data_bit)

    for i in range(mainblock.lab_pia_wls + 1):
        print("***** pia_addr[{}] *****".format(i))
        pia_addr = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(pia_addr)

    for i in range(mainblock.pia_wls):
        print("***** pia_wl_polarity[{}] *****".format(i))
        pia_wl_polarity = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(pia_wl_polarity)

    for i in range(mainblock.n_vpterms + 1):
        print("***** vpterm[{}] *****".format(i))
        vpterm = indata[:8]
        indata = indata[8:]
        vpterm = vpterm_fields._make(struct.unpack("<ii", vpterm))
        print(vpterm)

    for i in range(mainblock.n_mcs + 1):
        print("***** mc_pterm[{}] *****".format(i))
        mc_pterm = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(mc_pterm)

    for i in range(mainblock.exp_per_lab + 1):
        print("***** exp_pterm[{}] *****".format(i))
        exp_pterm = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(exp_pterm)

    for i in range(mainblock.exp_per_lab + 1):
        print("***** exp_data_bit[{}] *****".format(i))
        exp_data_bit = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(exp_data_bit)

    for i in range(mainblock.n_pins + 1):
        print("***** pin_mc[{}] *****".format(i))
        pin_mc = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(pin_mc)

    for i in range(mainblock.n_mcs + 1):
        print("***** output_mc[{}] *****".format(i))
        output_mc = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(output_mc)

    for i in range(mainblock.n_data_bits):
        print("***** bit_tab[{}] *****".format(i))
        bit_tab = struct.unpack("<i", indata[:4])[0]
        indata = indata[4:]
        print(bit_tab)

    print(indata)
    assert len(indata) == 0

if __name__ == '__main__':
    main()
