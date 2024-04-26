# -*- coding: utf-8 -*-
"""
utils.py

This file contains some useful functions for NMR processing.

@author:
Kimariyb, Hsiun Ryan (kimariyb@163.com)

@address:
XiaMen University, School of electronic science and engineering

@license:
Licensed under the MIT License.
For details, see the LICENSE file.

@data:
2024-04-16
"""

import os
import pathlib
import glob
import shutil
import pandas as pd



def change_file_ext(folder_path: str, old_ext: str, new_ext: str):
    """
    批量修改文件夹中的文件扩展名

    Args:
        folder_path (str): 文件夹路径
        old_ext (str): 旧扩展名
        new_ext (str): 新扩展名
    """
    # 获取目录下所有符合条件的文件
    file_list = glob.glob(os.path.join(folder_path, f"*.{old_ext}"))
    
    # 遍历文件列表，修改文件扩展名
    for file_path in file_list:
        # 获取文件名和扩展名
        file_name, _ = os.path.splitext(os.path.basename(file_path))
        # 构造新的文件名
        new_file_name = file_name + "." + new_ext
        # 构造新的文件路径
        new_file_path = os.path.join(folder_path, new_file_name)
        # 修改文件后缀
        os.rename(file_path, new_file_path)
        print('successfully changed file extension of', file_path, 'to', new_file_path)
   

def scan_folder(folder_path: str, scan_sub: bool = False) -> list:
    """
    扫描文件夹并返回文件夹名称列表. 如果 scan_sub 为 True, 则继续扫描其子文件夹.

    Args:
        folder_path (str): 文件夹路径
        scan_sub (bool, optional): 是否扫描子文件夹. Defaults to False.

    Returns:
        list: Path 对象组成的列表
    """
    folder_name_list = []
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            folder_name_list.append(os.path.join(root, dir))
        if not scan_sub:
            break
    return folder_name_list


def build_file_name(src_path: str) -> str:
    """
    根据源文件路径构建文件名
    
    Args:
        src_path (str): 源文件路径

    Returns:    
        str: 新的文件名
    """
    # 分割源文件路径
    # D:/study/SABRE/20240117/7-900uM-SABRE-90/2024.01.17/5/average/fid/avg3.fid       
    # ['D:', 'study', 'SABRE', '20240117', '7-900uM-SABRE-90', '2024.01.17', '5', 'average', 'fid', 'avg3.fid']
    # 取 '7-900uM-SABRE-90-20240117-5-avg3.fid' 作为文件名
    path_parts = src_path.split('/')
    
    # 提取日期部分
    date_part = path_parts[5].replace(".", "")

    # 拼接为新的文件名
    file_name = "-".join(path_parts[4:5] + [date_part] + path_parts[6:8] + [path_parts[-1][:-4]])
    
    return file_name + ".fid"


def move_files(src: str, dst: str):
    """
    移动文件到指定文件夹（保留源文件）

    Args:
        src (str): 源文件路径
        dst (str): 目标文件夹路径
    """
    try:
        shutil.copy2(src, dst)
        print(f"Successfully moved {src} to {dst}.")
    except Exception as e:
        print(f"Failed to move {src} to {dst}. Error: {str(e)}")

        
def delete_files(folder_path: str, file_ext: str):
    """
    删除文件夹下指定扩展名的文件

    Args:
        folder_path (str): 文件夹路径
        file_ext (str): 文件扩展名
    """
    file_list = glob.glob(os.path.join(folder_path, f"*.{file_ext}"))
    for file_path in file_list:
        os.remove(file_path)
        print(f"Successfully deleted {file_path}.")


def process_fid_files(target_folder: str, destination_folder: str):
    """
    处理 fid 文件，将其移动到指定文件夹并重命名

    Args:
        target_folder (str): 源文件路径
        destination_folder (str): 目标文件夹路径  
    """
    # 第一次遍历目标文件夹，获取文件夹列表
    folder_list = scan_folder(target_folder)

    # 第二次遍历第一次遍历的所有文件夹，找到符合条件的文件夹 (average 文件夹)
    fid_folder_list = []
    for folder in folder_list:
        for root, dirs, files in os.walk(folder):
            folder_path = pathlib.Path(root)
            if "average" in folder_path.name:
                # 符合条件的文件夹
                fid_folder_list.append(folder_path)

    # 第三次遍历符合条件的文件夹，获取文件列表
    for fid_folder in fid_folder_list:
        fid_file_list = glob.glob(fid_folder.as_posix() + "/fid/*.fid")

        # 第四次遍历 list 列表，将 fid 文件移动到目标文件夹，同时修改名字
        for fid_file in fid_file_list:
            source_path = pathlib.Path(fid_file)
            # 构造目标文件路径和新文件名
            move_path = pathlib.Path(destination_folder) / source_path.name
            new_name = build_file_name(source_path.as_posix())

            # 移动文件并修改文件名
            move_files(source_path.as_posix(), move_path)
            os.replace(move_path.as_posix(), move_path.with_name(new_name).as_posix())


def process_csv_files(csv_directory: str, output_directory: str):
    """
    处理 csv 文件，将其移动到指定文件夹并重命名    
    
    Args:
        csv_directory (str): csv 文件夹路径
        output_directory (str): 输出文件夹路径
    """
     # 获取目录下的所有 CSV 文件
    csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]

    # 循环处理每个 CSV 文件
    for file in csv_files:
        # 构建文件的完整路径
        file_path = os.path.join(csv_directory, file)
        
        # 构建输出文件的完整路径
        output_file_path = os.path.join(output_directory, file)

        # 使用 pandas 读取 CSV 文件
        df = pd.read_csv(file_path, header=None, sep='\t')
        
        # 分列操作
        df.rename(columns={0: 'x (ppm)', 1: 'real', 2: 'imag'}, inplace=True)

        # 保存为新的 CSV 文件
        df.to_csv(output_file_path, index=False, header=False, float_format='%.7f')

        # 打印 success 信息
        print(f'{file} processed successfully.')
        
