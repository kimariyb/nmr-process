# -*- coding: utf-8 -*-
"""
draw.py

@author:
Kimariyb, Hsiun Ryan (kimariyb@163.com)

@address:
XiaMen University, School of electronic science and engineering

@license:
Licensed under the MIT License.
For details, see the LICENSE file.

@data:
2024-04-15
"""

import glob
import pandas as pd
import proplot as pplt

from proplot import rc


def get_data_from_csv(file_path: str):
    """
    从 csv 文件中读取数据，并返回 pandas DataFrame 对象
    
    Args:
        file_path (str): csv 文件路径
    
    Returns:
        pandas DataFrame: 包含 csv 文件中数据的 DataFrame 对象
    """
    data = pd.read_csv(file_path, header=0, sep=',')
    return data


def get_data_from_csv_folder(folder_path: str):
    """
    从文件夹中读取 csv 文件，并返回包含所有 csv 文件数据的 pandas DataFrame 对象
    
    Args:
        folder_path (str): 文件夹路径
    
    Returns:
        pandas DataFrame: 包含所有 csv 文件数据的 DataFrame 对象
    """
    file_list = glob.glob(folder_path + '/*.csv')
    data_list = []
    for file in file_list:
        data = get_data_from_csv(file)
        data = data.dropna(axis=1, how='all')
        data_list.append(data)

    return data_list

# 读取数据，在这里修改读取的文件夹
datas = get_data_from_csv_folder('./data')


# 设置绘图的默认参数，如字体、字号等
rc['font.name'] = 'Arial'
rc['title.size'] = 14
rc['label.size'] = 12
rc['font.size'] = 10.5
rc['tick.width'] = 1.3
rc['meta.width'] = 1.3
rc['label.weight'] = 'bold'
rc['tick.labelweight'] = 'bold'
rc['ytick.major.size'] = 4.6
rc['ytick.minor.size'] = 2.5
rc['xtick.major.size'] = 4.6
rc['xtick.minor.size'] = 2.5

# 颜色设置，在这里修改颜色
colors = [
    '#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728'
]

# 标签设置，在这里修改标签
labels = [
    '4096 Acquisition Points', 
    '8192 Acquisition Points', 
    '16384 Acquisition Points', 
    '32768 Acquisition Points'
]

# 创建子图和坐标轴
fig = pplt.figure(figsize=(7, 9), dpi=300, span=True, share=True)
axs = fig.subplots(nrows=4, ncols=1)

for ax, data, color, label in zip(axs, datas, colors, labels):
    # 绘制数据，第一列作为 x 值，第二列作为 y 值
    x = data.iloc[:, 0]
    y = data.iloc[:, 1]
    ax.plot(x, y, color=color, label=label)
    
    ax.format(
        xlabel='Chemical Shift (ppm)', ylabel='Intensity (a.u.)',
        xlim=(-60, -70), ylim=(-50, 200),
        xlocator=2, ylocator=50,
        xminorlocator=1, yminorlocator=25
    )
    
    ax.legend(loc='ur', ncols=1, fontweight='bold', fontsize=14, frame=False)

axs.format(grid=False, abc='(a)', abcloc="ul", fontsize=14)

fig.savefig('./plot.png', dpi=300, bbox_inches="tight")

