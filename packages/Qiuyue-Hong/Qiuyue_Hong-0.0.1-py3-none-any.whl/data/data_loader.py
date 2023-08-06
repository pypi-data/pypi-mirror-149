# -*-coding:utf-8-*-
"""
@author:hqy
@create time:20220421
"""

import numpy as np
import os
import matplotlib.pyplot as plt

from scripts.data.spcify_param import *
from scripts.utils.btools import *


def extract_AGC(file_in, Nlines):
    """

    This program reads the RADARSAT aux data and calculates the AGC settings

    The parameters encoded in the auxilary data bits are defined in RSI-D6
    also known as RSCSA-IC0009 (X-band ICD)
    -------------------------------------------------------------------------
    PARAMETER NAME                          LOCATION         LENGTH   ID
    -------------------------------------------------------------------------
    aux_sync_marker         = aux_bits (:,   1:  32);     % 32 bit -  1
    image_ref_id            = aux_bits (:,  33:  64);     % 32 bit -  2
    payload_status          = aux_bits (:,  65:  80);     % 16 bit -  3
    replica_AGC             = aux_bits (:,  81:  86);     %  6 bit -  4
    CALN_atten_LPT_pow_set  = aux_bits (:,  89:  96);     %  8 bit -  6
    pulse_waveform_number   = aux_bits (:,  97: 100);     %  4 bit -  7
    temperature             = aux_bits (:, 113: 144);     % 32 bit -  9
    beam_sequence           = aux_bits (:, 145: 160);     % 16 bit - 10
    ephemeris               = aux_bits (:, 161: 176);     % 16 bit - 11
    number_of_beams         = aux_bits (:, 177: 178);     %  2 bit - 12
    ADC_rate                = aux_bits (:, 179: 180);     %  2 bit - 13
    pulse_count_1           = aux_bits (:, 185: 192);     %  8 bit - 15
    pulse_count_2           = aux_bits (:, 193: 200);     %  8 bit - 16
    PRF_beam                = aux_bits (:, 201: 213);     % 13 bit - 17
    beam_select             = aux_bits (:, 214: 215);     %  2 bit - 18
    Rx_window_start_time    = aux_bits (:, 217: 228);     % 12 bit - 20
    Rx_window_duration      = aux_bits (:, 233: 244);     % 12 bit - 22
    altitude                = aux_bits (:, 249: 344);     % 96 bit - 24
    time                    = aux_bits (:, 345: 392);     % 48 bit - 25
    SC_T02_defaults         = aux_bits (:, 393: 393);     %  1 bit - 26
    first_replica           = aux_bits (:, 394: 394);     %  1 bit - 27
    Rx_AGC_setting          = aux_bits (:, 395: 400);     %  6 bit - 28
    -------------------------------------------------------------------------
                                       Total  => 50 bytes (400 bits)

    :param file_in: input file name including it's path
    :param Nlines: number of azimuth lines
    :return: Receiver attenuation in dB for each range line
    """
    fid_aux = open(file_in, 'rb')

    aux_bytes = np.fromfile(fid_aux, np.uint8, count=50 * int(Nlines)).reshape((50, int(Nlines))).T  # 1536*50

    fid_aux.close()

    b8f = b8func()
    b2i = b2ifunc()
    byte = 50
    # aux_bit = np.zeros([int(Nlines),400]) # 1536
    # aux_bit[:,8*(byte-1):8*byte] = np.asarray([list(ch) for ch in b8f(aux_bytes[:,byte-1])])
    aux_bit = np.asarray([ch[2:] for ch in b8f(aux_bytes[:, byte - 1])])

    # convert 50 bytes to 400 bits in general (it is only done for 50th byte)
    d_Rx_AGC = b2i(aux_bit)

    """
      For values greater than 31, the binary representation defined in the 
      documentation is different and there is the need to substract 24 from 
      decimal values to get the AGC setting in dB
    """
    comput_atten_dB = np.vectorize(lambda i: i - (24 * int(i > 31)))
    AGC_atten_dB = comput_atten_dB(d_Rx_AGC)
    return AGC_atten_dB


def load_AGC_block(file_pre,  Nrg_lines_blk, block,plo=False):
    """

    This program returns the RADARSAT-1 receiver attenuation values for
    one block.  They are integers from 2 to 17, in 1 dB steps.

    :param file_pre: File prefix ( path + prefix + block number)
    # :param first_rg_line: First range line for the extracted data
    :param Nrg_lines_blk: Number of range lines in a block
    :param block: the current block number
    :param usef:
    :return:
    """
    file_in = file_pre + aux_suffix
    # print(file_in)
    AGC_atten_dB = extract_AGC(file_in, Nrg_lines_blk)
    if plo:
        plt.figure(num=201)
        font_dict = dict(fontsize=8,
                         color='k',
                         family='SimHei',
                         weight='light',
                         style='italic',
                         )
        plt.title("AGC attenuation values for %d block of data"%block)
        plt.xlabel("Azimuth (sample no. within this block)", loc='center', fontdict=font_dict)
        plt.ylabel("Magnitude  (dB)", loc='center', fontdict=font_dict)
        plt.plot(AGC_atten_dB)
        plt.show()
    return AGC_atten_dB


def load_DATA_block(file_pre,   Nrg_lines_blk, Nrg_cells, AGC_atten_dB, block):
    """

     This program - reads /loads data for a block
              - converts to floating point
              - compansates for the receiver attenuation

    :param file_pre: File prefix (path + prefix + block number)
    #:param output_path: Path where the SAR data MAT files are stored
    :param Nrg_lines_blk: Number of range lines in a block
    :param Nrg_cells: Number of range cells
    :param AGC_atten_dB: Nominal attenuation (Rx_AGC_setting) for each line (dB)
    :param block: block number
    :return:
    """
    file_in = file_pre + data_suffix
    # print(file_in)
    fid2 = open(file_in, 'rb')
    try:
        data = np.fromfile(fid2,np.uint8).reshape(
            (int(2*Nrg_cells), int(Nrg_lines_blk))).T  # (1536 4096)

        #  Compensate for packed data format --> convert to signed numbers
        data = 2 * (data - 16 * (data > 7)) + 1
        data =  data[:, 0:2*Nrg_cells:2] +np.complex('j')*data[:,1:2*Nrg_cells:2]
        source_data = data
        """
         Apply gain correction to the data.  The attenuation varies from 2 to 17
         dB for this CD, so the linear gain factor varies from 1.26 to 7.08.
         If you want to store the decoded data in one byte arrays, use an additional 
         factor of 1.5, so that the maximum abs value is less than 127.
        """
        fact = 1.5
        linear_gain_factor = fact * np.power(10,(AGC_atten_dB/20))
        linear_gain_factor = linear_gain_factor.reshape(int(Nrg_lines_blk),1)
        one_array = np.ones((1,int(Nrg_cells)))

        data = np.multiply(np.dot(linear_gain_factor , one_array) , data)

        return data, source_data
    finally:
        fid2.close()


def load_source_data(b):
    """

    The total data partition is 2.\n
    You can extract them separately or together, so parameter "b" must be one of "1-3" \n
    if b == 1:
        return data1,source_data1
    elif b == 2:
        return data2,source_data2
    elif b == 3:
        return [data1,data2],[source_data1,source_data2]
    :param b: Partition to extract
    :return: AGC gain compensated data, and original data
    """

    if b not in [1,2,3]:
        raise Exception('The total data partition is 2. \n You can extract them separately or together, so parameter "b" must be one of "1-3"')

    if b <3 :
        file_pre = os.path.join(output_path, output_prefix + '_' + str(b))
        print('Load or Extract AGC setting and Data for block %d .' % b)
        # Load a block of 'AGC_values'
        AGC_values = load_AGC_block(file_pre, Nrg_lines_blk, b)
        # Load a block of raw SAR data
        data, source_data = load_DATA_block(file_pre, Nrg_lines_blk, Nrg_cells, AGC_values, b)
        return data,source_data
    else:
        data1 ,source_data1 = load_source_data(1)
        data2, source_data2 = load_source_data(2)
        return np.concatenate([data1,data2],axis=1),\
               np.concatenate([source_data1,source_data2],axis=1)
        # return [data1,data2],[source_data1,source_data2]
