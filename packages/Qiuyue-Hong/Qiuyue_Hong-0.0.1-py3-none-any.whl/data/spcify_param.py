# -*-coding:utf-8-*-

"""
The only file needed from the CD is "dat_01.001", which contains the
radar data as well as the chirp replica and auxiliary data for each range line.

@author:hqy
@create time:20220421
"""

import numpy as np


input_path = '/home/mdpi/hqy/simu_data/radar/scene01'  # Path of data
CD_data_file_name = 'DAT_01.001'  # File name of data saving
output_path = '/home/mdpi/hqy/simu_data/radar/EXTRACTED_DATA/py'  # Path saved after data processing
output_prefix = 'raw'  # prefix

"""Define area of interest of the radar data to be extracted"""
first_rg_cell = 1850  # Define the range limits
first_rg_line = 7657  # Define the azimuth limits  (19432 max)

Nrg_cells = 2048  # Suggest 2048 cells
Nrg_lines_blk = 6 * 256  # Suggest 1536, it should be larger than the size of the azimuth match filter (705)
                         # so that an image can be created.
Nrg_lines = 2 * Nrg_lines_blk  # 3072 = 2*6*256


"""Quantize the range line limits and block size, if necessary"""
# Move the first range line to the beginning of an 8-line block
first_rg_line = 8 * (np.ceil(first_rg_line / 8) - 1) + 1  # 7657 = 8*(ceil(7657/8)-1)+1
# Make 'Nrg_lines_blk' a multiple of 8, to get complete the 8-line blocks
DATA_aver = 8 * np.ceil(Nrg_lines_blk / 8)  # 1536 = 8*ceil(1536/8)
# Find the number of complete blocks required to cover the area of interest
Nblocks = np.ceil(Nrg_lines / Nrg_lines_blk)  # 2 = ceil(3072/1536)
# Make 'Nrg_lines' a multiple of 'Nblocks', to get complete blocks
Nrg_lines = Nrg_lines_blk * Nblocks  # 3072 =1536*2

"""These values are specific to the data set, DO NOT CHANGE for this CD"""
length_replica = 2880  # Total length (I&Q) of replica record
tot_Nrg_cells = 9288  # Total number of range cells per line
tot_Nrg_lines = 19432  # Total number of range lines (records)
first_replica = 7  # First record that contains the replica
PRF = 1256.98  # Pulse Reputation Frequency (Hz)
Fr = 32.317e+6  # Radar sampling rate (Hz)
f0 = 5.300e+9  # Radar center frequency (Hz)
c = 2.9979e+8  # Speed of light (m/s)
R0 = 0.0065956 * c / 2  # Slant range of first radar sample (m)
Nrepl = 1349  # No. of valid samples in the replica
Kr = 0.72135e+12  # FM rate of radar pulse (Hz/s)
Tr = 41.75e-6  # Chirp duration (s)

# usef = 1

replica_suffix = '_replica.bin'  # one replica per 8 - line
data_header_suffix = '_data_header.bin'  # header of each line
aux_suffix = '_aux.bin'  # auxiliary data from each line
data_suffix = '_data.bin'  # radar signal data
file_header_suffix = '_file_header.bin'  #