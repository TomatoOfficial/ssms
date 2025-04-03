import csv
import os

# 定义csv输入输出文件（夹）
folderPath = os.getcwd()
fullinPath = folderPath + '\\' + 'in.csv'
fulloutPath = folderPath + '\\' + 'out.csv'
stuData = []

score_types = [
    '语', '数', '英', '政史', '地生', '物', '音体美信',
    '出勤', '课间操', '午休', '眼操', '红领巾', '路队',
    '卫生', '文明', '纪律', '发言', '班级', '校内'
]

# 读取in.csv
def readFile():
    global stuData
    try:
        with open(fullinPath, 'r', encoding="utf-8") as f:
            csv_r = csv.reader(f)
            next(csv_r)  # 跳过表头
            stuData = list(csv_r)  # 读取所有数据到stuData
    except FileNotFoundError:
        print(f"File {fullinPath} Not Found.")

# 保存out.csv（读写，如果文件存在则打开，且原有内容会删除/如果文件不存在则创建新文件）
def saveFile():
    with open(fulloutPath, 'w+', newline='', encoding="utf-8") as f:
        csv_w = csv.writer(f)
        csv_w.writerow(['学号', '姓名', '缩写', '组', '语', '数', '英', '政史', '地生', '物', '音体美信','出勤', '课间操', '午休', '眼操', '红领巾', '路队', '卫生', '文明', '纪律', '发言', '班级', '校内'])  # 写入表头
        for row in stuData:
            csv_w.writerow(row)

# 输入学生分数
def insertStudentScore():
    while True:
        readFile()
        searchOption = input("Choose StuID(1),  Initials(2) or type 'exit' to quit: ")
        
        if searchOption == '1':
            stuId = getStuId()
            if stuId is not None:
                searchStudent(stuId, None)
        
        elif searchOption == '2':
            stuInit = getStuInit()
            if stuInit is not None:  # 确保只有在输入有效时才进行搜索
                searchStudent(None, stuInit)

        # 选择要录入的分数类型
        print("Choose Insert Score's Type\n")
        for index, score_type in enumerate(score_types, start=1):
            print(f"{index}. {score_type}")

        choice = input("Choose the Serial Number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(score_types):
            score_type = score_types[int(choice) - 1]

        else:
            print("Invaild Number.")
            continue

        # 输入分数
        try:
            score = int(input(f"Please Insert {score_type}'s Score: "))
        except ValueError:
            print("Invaild Type. Input Must Be Int.")
            continue

        # 更新学生分数
        if student[0] == stuData:  # 如果是通过ID找到的学生
            stuData[stuData.index(student)] = student[:2] + [score] + student[3:]
        else:  # 如果是通过姓名缩写找到的学生
            for s in stuData:
                if s[1] == student_id:
                    index = stuData.index(s)
                    stuData[index] = s[:2] + [score] + s[3:]
                    break

        # 选择是否继续录入
        continue_input = input("是否继续录入其他学生分数？（y/n）：")
        if continue_input.lower() != 'y':
            break

    print("学生分数录入完毕。")

# 保存学生分数到CSV
def saveStudentScores():
    with open('out.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['学号', '姓名'] + score_types)  # 写入表头
        writer.writerows(stuData)  # 写入学生数据

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
    ║   ## 6  Save Score File                      ║
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
    # ║   ## 6  保存分数文件                      ║
    # ║   ## 7  显示所有学生信息                    ║
    # ║   ## 0  退出系统                          ║
    # ║  ------------------------------------------  ║
    # ║   TomatoOfficial | 使用 Python 3.12.0 制作  ║
    # ╚==============================================╝
    # 你看这中文字符加ascii 乱得跟一锅粥一样

# 主函数
def main():
    while True:
        menu()
        readFile()
#       print(stuData)
        
        mainOption = input("system@ubuntu:~ $ ssms ") # This is ubuntu!
        
        if mainOption == '0':  # exit system
            print("System exited.\n")
            os.system( 'pause ')
            break

        elif mainOption == '2':  # search stu data
            searchData()
                
        elif mainOption == '6':  # save file
            saveFile()
            print(f"\nCSV File 'out.csv' has been saved(updated).\n({fulloutPath})\n\n")
        
        else:  # invaild command
            print("Invaild Command.\n\n")

# 搜索学生data主函数
def searchData():
    stuId = None
    stuInit = None
    isSearchInput = False
    
    while True:
        readFile()
        searchOption = input("Choose StuID(1),  Initials(2) or type 'exit' to quit: ")
        
        if searchOption == '1':
            stuId = getStuId()
            if stuId is not None:
#                isSearchInput = True
                searchStudent(stuId, None)
                print(row)
            
        elif searchOption == '2':
            stuInit = getStuInit()
            if stuInit is not None:  # 确保只有在输入有效时才进行搜索
                searchStudent(None, stuInit)
                print(row)

        elif searchOption == '0':
            if isSearchInput:
                print(stuId)
                print(stuInit) 
            break
        
#        else:
#            print("Invaild Command.\n\n")
#        if isSearchInput:
#            print("StuID:", stuId)
#            print("Initials:", stuInit)
            break

# 输入学生id 
def getStuId():
    while True:
        stuId = input("\nInput StuID (or type 'exit' to quit): ")
        
        if stuId.lower() == 'exit':
            return None
        
        if stuId.isdigit():  # StuID应为数字
            return stuId
        
        print("\nInvalid StuID. Please enter a numeric StuID.")

# 输入学生init
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
        # 打印调试信息，检查缩写列的内容
#        print(f"Searching for {stuInit} in {row[2]}")
        # 检查学号，学号在第二列，索引为1
        # 检查缩写，缩写在第三列，索引为2
        if (stuId and str(row[0]).strip() == stuId) or \
           (stuInit and str(row[2]).strip().upper() == stuInit.upper()):
            return row  # 返回row
    print("\nNo matching student found.")  # 如果没有找到匹配的学生

if __name__ == "__main__":
    main()