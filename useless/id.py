import csv

def read_student_ids(filename):
    student_ids = {}
    try:
        with open(filename, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            print("列标题：", reader.fieldnames)  # 打印列标题以检查
            for row in reader:
                student_ids[row['姓名']] = row['学号']
    except FileNotFoundError:
        print(f"文件 {filename} 未找到。")
    except KeyError as e:
        print(f"CSV文件中缺少列：{e}")
    return student_ids

def add_student_ids_to_group(group_filename, ids_filename):
    student_ids = read_student_ids(ids_filename)
    if not student_ids:
        print("没有读取到学生ID数据。")
        return

    try:
        with open(group_filename, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            print("小组文件列标题：", reader.fieldnames)  # 打印列标题以检查
            with open('updated_group.csv', 'w+', newline='', encoding='utf-8-sig') as outfile:
                fieldnames = reader.fieldnames + ['学号']
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    row['学号'] = student_ids.get(row['姓名'], '未找到')
                    writer.writerow(row)
                print("数据已更新到 updated_group.csv 文件中。")
    except FileNotFoundError:
        print(f"文件 {group_filename} 未找到。")
        
# 调用函数
group_filename = 'in.csv'  # 分好小组的CSV文件
ids_filename = 'id.csv'  # 全班同学的姓名和学号CSV文件
add_student_ids_to_group(group_filename, ids_filename)

def main():
    read_student_ids()
    dd_student_ids_to_group()
