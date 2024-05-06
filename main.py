from spinflow.process import *
from utils.file import *

import glob


print(read_fid('./data/1.fid'))

# 获取需要扫描的文件夹
# target_folder_list = scan_folder('D:/study/SABRE/', False)

# 循环遍历每个文件夹，调用 process_fid_file 函数处理
# for folder in target_folder_list:
#   process_fid_files(folder, 'D:\Data\Source FID')

# 将 csv 文件转移到 D:\Data\Processed FID 文件夹下
# csv_files = glob.glob('D:\Data\Source FID\*csv')
# for file in csv_files:
#     move_files(file, 'D:\Data\Processed FID')

# 删除 D:\Data\Source FID 文件夹下的所有 csv 文件
# delete_files('D:\Data\Source FID', 'csv')

# 给所有 csv 文件按照 \t 分割符分割，并保存为 csv 文件
# csv_dir = 'D:\\Data\\2024_04_18\\Source FID\\Source CSV'
# output_dir = 'D:\\Data\\2024_04_18\\Processed FID'
# process_csv_files(csv_dir, output_dir)



