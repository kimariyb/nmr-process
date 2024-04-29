# -*- coding: utf-8 -*-
"""
process.py

This file contains some useful functions for NMR processing.

@author:
Kimariyb, Hsiun Ryan (kimariyb@163.com)

@address:
XiaMen University, School of electronic science and engineering

@license:
Licensed under the MIT License.
For details, see the LICENSE file.

@data:
2024-04-17
"""
import os
import numpy as np
import pandas as pd


def read_fid(fid_path: str, sw: float = 20833.0) -> pd.DataFrame:
    """
    Read FID file generated by SpinFlow for small nuclear magnetic resonance 
    (Oxford Instruments) and return the raw data in DataFrame format.
    
    Example
    ----------
    >>> data = read_fid('./data/1.fid')
    >>> print(data)
            xaxis     real     imag
    0      0.000000 -13879.0 -12209.0    
    1      0.000048   5624.0 -17174.0    
    2      0.000096  17569.0  -1997.0    
    3      0.000144  10059.0  16139.0    
    4      0.000192 -11691.0  17121.0    
    ...         ...      ...      ...    
    32763  1.572649   1368.0      0.0    
    32764  1.572697    514.0    -95.0    
    32765  1.572745   1442.0    658.0    
    32766  1.572793    352.0    362.0    
    32767  1.572841   -427.0    105.0 

    Parameters
    ----------
        fid_path : str
            Path to the FID file
        sw : float, optional
            Sampling frequency, default is 20833.0 Hz

    Returns
    -------
        pd.DataFrame
            FID Data in DataFrame format
    """
    
    # 如果没有提供 FID 文件路径，或者 FID 文件不存在，抛出异常
    if not os.path.exists(fid_path):
        raise FileNotFoundError(f"FID file not found: {fid_path}")

    # 用来存储 FID 数据的字典
    data_dict = {
        'xaxis': [],
        'real': [],
        'imag': []
    }
    
    # 读取 FID 二进制文件
    with open(fid_path, 'rb') as fid_file:
        raw_data = fid_file.read()
         
        # 使用 numpy 解析二进制数据，并将其转换为 float32 类型
        raw_data = np.frombuffer(raw_data, "<f")
        
        # raw_data 包含了 FID 数据，其前 259 个元素为头部信息，后面的元素为 FID 数据
        fid_data = raw_data[259: ]

        # 数据点数
        data_points = len(fid_data) / 2

        # 计算时间序列
        time = (data_points  - 1 )/ sw
        
        # 存入横轴时间
        data_dict['xaxis'] = np.linspace(0, time, int(data_points))
    
        # 存入实部和虚部数据
        data_dict['real'] = fid_data[::2]
        data_dict['imag'] = fid_data[1::2]
        
    # 将数据转换为 DataFrame 格式
    data = pd.DataFrame(data_dict)
    
    return data


def export_fid(data: pd.DataFrame, fid_path: str, freq: float = 56.17410278):
    """
    Export FID data in DataFrame format to a binary file for SpinFlow.
    
    Example
    ----------
    >>> data = read_fid('./data/1.fid')     
    >>> export_fid(data, './data/1.txt')
    
    Parameters
    ----------
        data : pd.DataFrame
            FID Data in DataFrame format
        fid_path : str
            Path to the output FID file
    """

    # 如果存在同名文件，则删除文件
    if os.path.exists(fid_path):
        os.remove(fid_path)
        
    # 文件头
    with open(fid_path, 'w') as f:
        f.write(f'Frequency\t{freq}\n')
        f.write('Nucleus\tUnknown\n')

    # 导出数据到文件
    data.to_csv(fid_path, sep='\t', header=None, index=False, mode='a')
    
