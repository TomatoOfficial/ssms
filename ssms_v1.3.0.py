# Student Scores Management System (ssms) v1.3.0
# TomatoOfficial with Python 3.12.0
# Rebuild Time: 2025.03.31 23:22:24

# Import Library
import csv
import os
import datetime
import sys
from colorama import init, AnsiToWin32
import random
import configparser
import locale
import json

# 定义文件(夹)输入/输出目录
def init():
    # 初始化 colorams
    init(warp = False)
    stream = AnsiToWin32(sys.stderr).stream

    # 获取当前工作目录
    folder_dict = os.getcwd()
    
    # 输入文件路径
    in_file = os.path.join(folder_dict, 'in.csv')
    
    # 输出目录路径
    output_dict = os.path.join(folder_dict, 'output')
    os.makedirs(output_dict, exist_ok=True)  # 确保目录存在
    
    # 输出文件名
    output_version = 'outv130-'
    out_file_time = datetime.datetime.now().strftime('%Y.%m.%d %H.%M.%S')
    out_file = os.path.join(output_dict, output_version + out_file_time + '.csv')
    
    # 返回路径供其他函数使用
    return folder_dict, in_file, output_dict, out_file

# 读取的 data & 分数列表
student_data = []
score_types = [
    '语', '数', '英', '政史', '地生', '物', '音体美信', '出勤', '课间操', '午休',
    '眼操', '校徽', '路队', '卫生', '文明', '纪律', '发言', '班级', '校内'
]

# 读取in_file
def read_in_file(in_file):
    global student_data
    try:
        with open(in_file, 'r', encoding="utf-8-sig") as f:
            csv_r = csv.reader(f)
            headers = next(csv_r)
            student_data = []
            for row in csv_r:
                if not row or len(row) < 5: continue  # 跳过空行或列不足的行
                #if row[4] not in ('0', '1'):  # 组长列（第5列）必须为0/1
                    #print(f"Ignore Invalid Group Leader Identify: Number={row[0]}, Value={row[4]}")
                student_data.append(row)
    except FileNotFoundError:
        print(f"File {in_file} Not Found.")

# 保存out_file
def saveFile(out_file):
    with open(out_file, 'w+', newline='', encoding="utf-8-sig") as f:
        csv_w = csv.writer(f)
        headers = ['学号', '姓名', '缩写', '组', '组长', '语', '数', '英', '政史',
                   '地生', '物', '音体美信', '出勤', '课间操', '午休', '眼操',
                   '校徽', '路队', '卫生', '文明', '纪律', '发言', '班级', '校内']
        csv_w.writerow(headers)
        for row in student_data:
            if row:  # 确保行不为空
                # 将所有的0值替换为空字符串
                row = [item if item != '0' and item != 0 else '' for item in row]
                csv_w.writerow(row)

# 主函数
def main():
    folder_dict, in_file, output_dict, out_file = init()
    read_in_file(in_file)