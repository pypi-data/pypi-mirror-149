# -*-coding:utf-8-*-

"""
@author:hqy
@create time:20220421
"""

import os
import sys
dir  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, dir)

from  read_CEOS_raw import read_ceos_raw1
from scripts.data.spcify_param import *

"""Check the dimensions of the selected area to be processed."""
if first_rg_line <=0 or ((first_rg_line+Nrg_lines-1) > tot_Nrg_lines):
    raise Exception('ERROR: Check the limits of the range lines !')
if first_rg_cell <= 0 or ((first_rg_cell + Nrg_cells -1) > tot_Nrg_cells):
    raise Exception('ERROR: Check the limits of the range cells !')

"""EXTRACT DATA from the area of interest and write data files """

for blk in range(1,int(Nblocks)+1):
    # find the first range line of block 'blk'
    start_line_blk = Nrg_lines_blk*(blk-1)+first_rg_line # 9288*(blk-1)+7657
    print('Extracting block number %d, RC1 = %d ,RL1 = %d \n'%(blk,first_rg_cell,start_line_blk))
    # create the output file name for block 'blk'
    output_file_pre = os.path.join(output_path,output_prefix+'_'+str(blk))
    #Call 'read_ceos_raw' function to extract the data for block 'blk'
    read_ceos_raw1(output_file_pre, start_line_blk, blk)