# -*-coding:utf-8-*-
"""
@author:hqy
@create time:20220421
"""

import os
import sys

dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, dir)

from scripts.utils.btools import *
from scripts.data.spcify_param import *


def read_ceos_raw1(output_file_pre, start_line_blk, blk, usemf=False):
    """
    This function reads the CEOS format RSAT-1 RAW data from the CD
    :param output_file_pre: output file prefix ( path + prefix + block number)
    :param start_line_blk: extract data starting from row number 'start_line_blk'
    :param blk:the block number
    :return:
    """

    global file_replica
    num_aux = 50  # RSI - D4 Pg.32
    num_header = 192  # RSI - D4 Pg.32
    file_header_length = 16252  # RSI - D4 Pg.103

    # Specify input data file path and open to read
    file_in = os.path.join(input_path, CD_data_file_name)
    fid = open(file_in, 'rb')
    # Create output file names and open to write if MAT files not used
    if not usemf:
        # file_replica = '_replica.bin'  # one replica per 8 - line
        # file_data_header = '_data_header.bin'  # header of each line
        # file_aux = '_aux.bin'  # auxiliary data from each line
        # file_data = '_data.bin'  # radar signal data
        # file_file_header = '_file_header.bin'  # header of file 'dat_01.001'

        file_replica = output_file_pre + replica_suffix
        file_data_header = output_file_pre + data_header_suffix
        file_aux = output_file_pre + aux_suffix
        file_data = output_file_pre + data_suffix
        file_file_header = output_file_pre + file_header_suffix

        replica_buffer = []
        aux_buffer = []
        data_header_buffer = []
        data_buffer = []
        # Read file header
        file_header = np.fromfile(fid, np.uint8, count=file_header_length).reshape((1, file_header_length)).T
        # np.save(file_file_header, file_header)
        file_header.tofile(file_file_header)
    num_pixel_data = 2 * tot_Nrg_cells  # 18576 = 2*9288
    h = num_header  # 192
    ha = num_header + num_aux  # 242  =192+50
    hpa = num_header + num_aux + num_pixel_data  # 18818

    rep_block_length = length_replica + 8 * hpa  # 153424 = 2880 + 242*8

    start_rep = (first_replica - 1) * hpa + num_header + num_aux + 1  # (7-1)*18818 + 192+50+1
    end_rep = start_rep + length_replica - 1

    start_col = ha + 2 * (first_rg_cell - 1) + 1
    end_col = start_col + 2 * Nrg_cells - 1

    Nrep_blks_row1 = np.ceil(start_line_blk / 8) - 1
    Nbytes_blocks = Nrep_blks_row1 * rep_block_length
    Nbytes_skip = file_header_length + Nbytes_blocks

    # go to start of the 1st data block
    fid.seek(int(Nbytes_skip), 0)
    # Allocate data array
    data = np.zeros((int(Nrg_lines_blk), 2 * int(Nrg_cells)), dtype=np.int8)

    N_8line_blocks = np.ceil(Nrg_lines_blk / 8)
    print('\nReading %d small 8-line blocks from range line %d\n' % (N_8line_blocks, start_line_blk))

    # Read and decode 8 lines at a time
    for kb in range(1, int(N_8line_blocks + 1)):
        # read one 8-line block of radar data and replica
        temp = np.fromfile(fid, np.uint8, count=rep_block_length).reshape((1, rep_block_length)).T

        # separate the replica and 8 lines of [header, aux and data]
        # replica = temp[start_rep-1:end_rep].T
        replica = temp.reshape([-1])[start_rep - 1:end_rep]
        replica = replica.reshape([1, -1])

        temp_part1 = temp.reshape([-1])[0: start_rep - 1].reshape([1, -1])
        temp_part2 = temp.reshape([-1])[end_rep: rep_block_length].reshape([1, -1])

        temp = np.concatenate([temp_part1, temp_part2], axis=1)

        temp = temp.reshape((8, hpa))  # Shape array as 8 rows by all columns

        # Extract the desired set of range cells
        data[8 * (kb - 1):8 * (kb), :] = temp[:, start_col - 1: end_col]

        # Write replica, header, aux and data in a binary file
        if not usemf:
            header = temp[:, 0: h].T
            aux = temp[:, h: ha].T  # 192 :242 -> aux shape = (50,8)
            # print(aux)
            # exit(0)
            header.tofile(file_data_header)  # 8 - bit
            replica_buffer.append(replica)
            aux_buffer.append(aux)
            data_header_buffer.append(header)
            data_buffer.append(data[8 * (kb - 1):8 * kb, :].T)

    data = 2 * (data.astype(np.float) - 16 * (data > 7).astype(np.float)) + 1

    data = data[:, 0:2 * Nrg_cells:2] + np.complex('j') * data[:, 1:2 * Nrg_cells:2]

    datasavef = output_path + '/' + 'CDdata%d.bin' % (blk)
    data.tofile(datasavef)
    # np.save(datasavef,data)
    fid.close()
    if not usemf:
        npa2file(replica_buffer, file_replica)
        npa2file(aux_buffer, file_aux)
        npa2file(data_header_buffer, file_data_header)
        npa2file(data_buffer, file_data)

    return data
