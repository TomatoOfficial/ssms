import csv
import os
import datetime
import sys
from colorama import init, AnsiToWin32
import random
import configparser

# 初始化 colorama
init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream

# 定义csv 输入输出文件（夹）
folderPath = os.getcwd()
fullinPath = os.path.join(folderPath, 'in.csv')
dirPath = os.path.join(folderPath, 'output')
versionName = 'outv126-'
fileoutName = datetime.datetime.now().strftime('%Y.%m.%d %H.%M.%S')
fulloutPath = folderPath + '\\' + 'output\\' + versionName + fileoutName + '.csv'
stuData = []
score_types = ['语', '数', '英', '政史', '地生', '物', '音体美信', '出勤', '课间操', '午休', '眼操', '校徽', '路队', '卫生', '文明', '纪律', '发言', '班级', '校内']

# 读取in.csv
def readFile():
    global stuData
    try:
        with open(fullinPath, 'r', encoding="utf-8-sig") as f:
            csv_r = csv.reader(f)
            headers = next(csv_r)
            stuData = []
            for row in csv_r:
                if not row or len(row) < 5: continue  # 跳过空行或列不足的行
                #if row[4] not in ('0', '1'):  # 组长列（第5列）必须为0/1
                    #print(f"Ignore Invalid Group Leader Identify: Number={row[0]}, Value={row[4]}")
                stuData.append(row)
    except FileNotFoundError:
        print(f"File {fullinPath} Not Found.")

# 保存out.csv
def saveFile():
    with open(fulloutPath, 'w+', newline='', encoding="utf-8-sig") as f:
        csv_w = csv.writer(f)
        headers = ['学号', '姓名', '缩写', '组', '组长', '语', '数', '英', '政史', '地生', '物', '音体美信', '出勤', '课间操', '午休', '眼操', '校徽', '路队', '卫生', '文明', '纪律', '发言', '班级', '校内']
        csv_w.writerow(headers)
        for row in stuData:
            if row:  # 确保行不为空
                # 将所有的0值替换为空字符串
                row = [item if item != '0' and item != 0 else '' for item in row]
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
                deleteLines()
                break
            deleteLines()
        break

def insertScoreForStudent(student):
    # 选择要录入的分数类型
    print("\nChoose Insert Score's Type\n")
    for index, score_type in enumerate(score_types, start=1):
        print(f"{index}. {score_type}")

    choice = input("Choose the Serial Number: ")
    if choice.isdigit() and 1 <= int(choice) <= len(score_types):
        score_type_index = int(choice) - 1  # 用户输入的索引从1开始，所以减1来匹配列表索引

        # 输入分数
        try:
            score = int(input(f"Please Insert {score_types[score_type_index]}'s Score: "))
            # 更新学生分数
            updateStudentScore(student, score_type_index, score)  # 直接传递分数
            print("Score inserted successfully.")
        except ValueError:
            print("Invalid Type. Input Must Be Int.")
    else:
        print("Invalid Number.")
    saveFile()

def updateStudentScore(student, score_type_index, score):
    multiplier_rules = read_settings()
    category = score_types[score_type_index]
    group = student[3]          # 当前学生所属组号
    is_leader = student[4] == '1' # 当前学生是否为组长

    # 更新当前学生分数
    for i, row in enumerate(stuData):
        if row[0] == student[0]:
            current_score_index = score_type_index + 5  # 分数列索引
            current_score = int(row[current_score_index]) if row[current_score_index] else 0
            new_score = current_score - int(score)
            stuData[i][current_score_index] = str(new_score)
            print(f"学生 {row[1]} 扣除 {score} 分（{category}）")

    # 仅在扣分对象是组员时触发组长倍数扣分
    if not is_leader and category in multiplier_rules:
        # 查找该组的组长
        leader = None
        for row in stuData:
            if row[3] == group and row[4] == '1':
                leader = row
                break
        if leader:
            multiplier = multiplier_rules[category]
            leader_penalty = int(score) * multiplier
            # 更新组长分数
            for i, row in enumerate(stuData):
                if row[0] == leader[0]:
                    current_score_index = score_type_index + 5
                    current_leader_score = int(row[current_score_index]) if row[current_score_index] else 0
                    new_leader_score = current_leader_score - leader_penalty
                    stuData[i][current_score_index] = str(new_leader_score)
                    print(f"组长 {leader[1]} 扣除 {leader_penalty} 分（{category}，倍数={multiplier}）")

# 打印menu
def menu():
    print('''
    ╔═════─ Student Scores Management System ─═════╗
    ║                                              ║
    ║   ─══════════─ Function Menu ─═══════════─   ║
    ║                                              ║
    ║   ## 1  Input Student Data(WIP)              ║
    ║   ## 2  Search Student Data(Current File)    ║
    ║   ## 3  Delete Student Data(WIP)             ║
    ║   ## 4  Change Student Data(WIP)             ║
    ║   ## 5  Input Student Score                  ║
    ║   ## 6  Verify Score File                    ║
    ║   ## 7  Choose Monitor(PureRandom)           ║
    ║   ## 0  Exit System                          ║
    ║  ------------------------------------------  ║
    ║   TomatoOfficial | Made with Python 3.12.0   ║
    ╚══════════════════════════════════════════════╝
    ''')

# 核实csv
def verifyCsv(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        headers = next(reader)  # 读取表头
        expected_headers = ['学号', '姓名', '缩写', '组', '组长', '语', '数', '英', '政史', '地生', '物', '音体美信', '出勤', '课间操', '午休', '眼操', '校徽', '路队', '卫生', '文明', '纪律', '发言', '班级', '校内']
        if headers != expected_headers:
            print("Header mismatch.")
            return

#        print("Verifying data...")
        row_count = 0
        for row in reader:
            if len(row) != len(expected_headers):
                print(f"Row {row_count+2} has incorrect number of columns.")
            row_count += 1

        print("\nCSV File '" + versionName + fileoutName + '.csv' + f"' has been verified. Total rows: {row_count+1}\n({fulloutPath})\n\n")

def select_file(dirPath):
    global selected_file_path
    # 列出指定目录下的所有文件
    files = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]
    
    if not files:
        print("File(s) Not Found | 404")
        return None

    # 打印文件列表并编号
    for index, file_name in enumerate(files, start=1):
        print(f"{index}. {file_name}")

    # 获取用户输入并选择文件
    while True:
        try:
            choice = int(input("Choose a File (number): "))
            if 1 <= choice <= len(files):
                selected_file = files[choice - 1]  # 用户输入的编号减1得到列表索引
                selected_file_path = os.path.join(dirPath, selected_file)
                print(f"You chose: {selected_file_path}")
                return selected_file_path
            else:
                print("Invalid Number")
        except ValueError:
            print("Invalid Number")

def monitor_read_file():
    global monitorData
    try:
        with open(selected_file_path, 'r', encoding="utf-8-sig") as f:
            csv_r = csv.reader(f)
            next(csv_r)  # 跳过表头
            monitorData = list(csv_r)  # 读取所有数据到stuData
    except FileNotFoundError:
        print(f"File {selected_file_path} Not Found.")

def select_random_students(num):
    if not monitorData:
        print("No students available to select.")
        return []
    valid_students = [stu for stu in monitorData if stu and stu[0].strip() != '']
    if len(valid_students) < num:
        print(f"Not enough students (only {len(valid_students)} available).")
        return []
    return random.sample(valid_students, num)


# 删除行
def OLD_deleteLines(n):
    if n == 'menu': # deleteMenu
        for i in range(19):
            stream.write('\x1b[1A')  # 光标上移一行
            stream.write('\x1b[2K')  # 删除当前行

    if n == 'all': # deleteAll(40lines)
        for i in range(40):
            stream.write('\x1b[1A')  # 光标上移一行
            stream.write('\x1b[2K')  # 删除当前行

def deleteLines():
    os.system('cls' if os.name == 'nt' else 'clear')

# 读取settings.ini
def read_settings():
    settings_path = os.path.join(os.getcwd(), 'settings.ini')
    multiplier_rules = {}
    config = configparser.ConfigParser()
    try:
        config.read(settings_path, encoding='utf-8')
        if 'Multiplier' in config:
            for key in config['Multiplier']:
                try:
                    multiplier = int(config['Multiplier'][key])
                    if multiplier < 0:
                        raise ValueError
                    multiplier_rules[key.strip()] = multiplier
                except ValueError:
                    print(f"忽略无效倍数：{key}={config['Multiplier'][key]}")
    except FileNotFoundError:
        print(f"警告：未找到配置文件 {settings_path}，组长倍数扣分功能已禁用。")
    return multiplier_rules
        #print(f"WARNING: settings.ini Not Found in {settings_path}, Disabled Extra Deduction of Points.")

            
# 主函数
def main():
    readFile()
    while True:
        menu()
#        readFile()
#        print(stuData)
        
        mainOption = input("system@ubuntu:~$ ssms ") # Ubuntu欢迎您！
        
        if mainOption == '0':  # :wq
            deleteLines()
            print("System exited.\n")
            os.system( 'pause ')
            break

        elif mainOption == '1':  # wip
            deleteLines()
            print("No.")
#            os.system("chcp 437")

        elif mainOption == '2':  # Search data
            deleteLines()
            stuId, stuInit = getStuIdOrInit()
            if stuId is None and stuInit is None:
                break
            deleteLines()
            searchStudent(stuId, stuInit)
        
        elif mainOption == '3':  # wip
            deleteLines()
            print("No.")
        
        elif mainOption == '4':  # wip
            deleteLines()
            print("No.")

        elif mainOption == '5':  # 输入学生分数
            deleteLines()
            insertStudentScore()  # 输入分数
            saveFile()  # 保存文件
            deleteLines()
            print(f"\nCSV File 'out.csv' has been saved(updated).\n({fulloutPath})\n\n")
        
        elif mainOption == '6':
            deleteLines()
            verifyCsv(fulloutPath)

        elif mainOption == '7':  # random.Monitor
            deleteLines()
            select_file(dirPath)
            monitor_read_file()
            print("Randomly Selected 3:")
            selected_students = select_random_students(3)
            if selected_students:
                for i, student in enumerate(selected_students, 1):
                    print(i, ":", student)
        
        else:  # Invalid
            deleteLines()
            print("Invalid Command.\n\n")

if __name__ == "__main__":
    main()
