import csv
import os
import datetime

# 定义csv输入输出文件（夹）
folderPath = os.getcwd()
fullinPath = folderPath + '\\' + 'in.csv'
fileoutName = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
fulloutPath = folderPath + '\\' + 'output\\' + 'debug-' + fileoutName + '.csv'
stuData = []

# 读取in.csv
def readFile():
    global stuData
    try:
        with open(fullinPath, 'r', encoding="utf-8-sig") as f:
            csv_r = csv.reader(f)
            next(csv_r)  # 跳过表头
            stuData = list(csv_r)  # 读取所有数据到stuData
    except FileNotFoundError:
        print(f"File {fullinPath} Not Found.")

# 保存out.csv
def saveFile():
    with open(fulloutPath, 'w+', newline='', encoding="utf-8-sig") as f:
        csv_w = csv.writer(f)
        csv_w.writerow(['学号', '姓名', '缩写', '组', '语', '数', '英', '政史', '地生', '物', '音体美信', '出勤', '课间操', '午休', '眼操', '红领巾', '路队', '卫生', '文明', '纪律', '发言', '班级', '校内'])  # 写入表头
        for row in stuData:
            csv_w.writerow(row)

# 输入学生ID或姓名缩写
def getStuIdOrInit():
    searchOption = input("Choose StuID(1), Initials(2) or type 'exit' to quit: ")
    if searchOption == '1':
        return getStuId(), None
    elif searchOption == '2':
        return None, getStuInit()
    elif searchOption.lower() == 'exit':
        return None, None
    else:
        print("Invalid Option.")
        return None, None

# 输入学生ID
def getStuId():
    while True:
        stuId = input("Input StuID (or type 'exit' to quit): ")
        if stuId.lower() == 'exit':
            return None
        if stuId.isdigit():  # StuID应为数字
            return stuId
        print("Invalid StuID. Please enter a numeric StuID.")

# 输入学生姓名缩写
def getStuInit():
    while True:
        stuInit = input("Input Initials (or type 'exit' to quit): ")
        if stuInit.lower() == 'exit':
            return None
        if stuInit.isalpha() and len(stuInit) > 0:  # StuInit应为字母
            return stuInit.upper()  # 返回大写字母
        print("\nInvalid Initials. Please enter alphabetical Initials.")

# 搜索学生
def searchStudent(stuId, stuInit):
    for row in stuData:
        if (stuId and str(row[0]).strip() == stuId) or \
           (stuInit and str(row[2]).strip().upper() == stuInit.upper()):
#            print(f"Found student: {row[1]} {row[0]}")
            print(f"Found student: {row}")
            return row
    print("No matching student found.")
    return None

# 输入学生分数主函数
def insertStudentScore():
    while True:
#        readFile()  # 读取学生数据
        stuId, stuInit = getStuIdOrInit()
        if stuId is None and stuInit is None:
            break
        while True:
            student = searchStudent(stuId, stuInit)
            if student:
                insertScoreForStudent(student)

            # 询问用户是否继续录入
            continue_input = input("Continue Entering This Student's Scores? (y/n): ")
            if continue_input.lower() != 'y':
                break
        break

# 更新分数csv
def updateStudentScore(student, score_type_index, score):
    # 找到学生在stuData中的位置并更新分数
    for i, row in enumerate(stuData):
        if row[0] == student[0] and row[1] == student[1]:  # 假设第一列是ID，第二列是姓名
            # 更新分数，分数类型索引从4开始（因为前四列是学号、姓名、缩写、组）
            stuData[i][score_type_index + 4] = score  # 更新分数
            break  # 更新后退出循环

# 输入学生分数
def insertScoreForStudent(student):
    # 选择要录入的分数类型
    print("\nChoose Insert Score's Type")
    score_types = ['语', '数', '英', '政史', '地生', '物', '音体美信', '出勤', '课间操', '午休', '眼操', '红领巾', '路队', '卫生', '文明', '纪律', '发言', '班级', '校内']
    for index, score_type in enumerate(score_types, start=1):
        print(f"{index}. {score_type}")

    choice = input("Choose the Serial Number: ")
    if choice.isdigit() and 1 <= int(choice) <= len(score_types):
        score_type_index = int(choice) - 1  # 用户输入的索引从1开始，所以我们减1来匹配列表索引
        score_type = score_types[score_type_index]

        # 输入分数
        try:
            score = int(input(f"Please Insert {score_type}'s Score: "))
            # 更新学生分数，分数类型索引从4开始
            updateStudentScore(student, score_type_index, score)  # 将用户输入的索引加上4来匹配CSV文件中的列索引
            print("Score inserted successfully.\n")
        except ValueError:
            print("Invalid Type. Input Must Be Int.")
    else:
        print("Invalid Number.")
    saveFile()

# 打印menu
def menu():
    print('''
    ╔═════─ Student Scores Management System ─═════╗
    ║                                              ║
    ║   ─══════════─ Function Menu ─═══════════─   ║
    ║                                              ║
    ║   ## 1  Input Student Data                   ║
    ║   ## 2  Search Student Data                  ║
    ║   ## 3  Delete Student Data                  ║
    ║   ## 4  Change Student Data                  ║
    ║   ## 5  Input Student Score                  ║
    ║   ## 6  Verify Score File                    ║
    ║   ## 7  Show All Student Data                ║
    ║   ## 0  Exit System                          ║
    ║  ------------------------------------------  ║
    ║   TomatoOfficial | Made with Python 3.12.0   ║
    ╚══════════════════════════════════════════════╝
    ''')
    
    # 什么 你问我为什么全英文ui+注释翻译ui？
    # 因为ascii字符方便做ui啊（雾
    
    # ╔═════─ 学生分数管理系统 ─═════╗
    # ║                                              ║
    # ║   ─══════════─ 功能菜单 ─═══════════─   ║
    # ║                                              ║
    # ║   ## 1  录入学生信息                       ║
    # ║   ## 2  搜索学生信息                      ║
    # ║   ## 3  删除学生信息                      ║
    # ║   ## 4  修改学生信息                      ║
    # ║   ## 5  录入学生分数                      ║
    # ║   ## 6  核实分数文件                      ║
    # ║   ## 7  显示所有学生信息                    ║
    # ║   ## 0  退出系统                          ║
    # ║  ------------------------------------------  ║
    # ║   TomatoOfficial | 使用 Python 3.12.0 制作  ║
    # ╚==============================================╝
    # 你看这中文字符加ascii 乱得跟一锅粥一样

# 核实csv
def verifyCsv(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        headers = next(reader)  # 读取表头
        expected_headers = ['学号', '姓名', '缩写', '组', '语', '数', '英', '政史', '地生', '物', '音体美信', '出勤', '课间操', '午休', '眼操', '红领巾', '路队', '卫生', '文明', '纪律', '发言', '班级', '校内']
        if headers != expected_headers:
            print("Header mismatch.")
            return

#        print("Verifying data...")
        row_count = 0
        for row in reader:
            if len(row) != len(expected_headers):
                print(f"Row {row_count+2} has incorrect number of columns.")
            row_count += 1

        print("\nCSV File '" + 'debug-' + fileoutName + '.csv' + f"' has been verified. Total rows: {row_count+1}\n({fulloutPath})\n\n")

# 主函数
def main():
    readFile()
    while True:
        menu()
#        readFile()
#        print(stuData)
        
        mainOption = input("system@ubuntu:~$ ssms ") # This is ubuntu!
        
        if mainOption == '0':  # exit system
            print("System exited.\n")
            os.system( 'pause ')
            break

        elif mainOption == '1':  # wip
            print("This Option is Work in Progress.")

        elif mainOption == '2':  # search stu data
            stuId, stuInit = getStuIdOrInit()
            if stuId is None and stuInit is None:
                break
            searchStudent(stuId, stuInit)
        
        elif mainOption == '3':  # wip
            print("This Option is Work in Progress.")
        
        elif mainOption == '4':  # wip
            print("This Option is Work in Progress.")

        elif mainOption == '5':  # search stu data
            insertStudentScore()
            saveFile()
            print(f"\nCSV File 'out.csv' has been saved(updated).\n({fulloutPath})\n\n")
        
        elif mainOption == '6':  # save file
            verifyCsv(fulloutPath)

        elif mainOption == '7':  # wip
            print("This Option is Work in Progress.")
        
        else:  # ? command
            print("Invaild Command.\n\n")

if __name__ == "__main__":
    main()
