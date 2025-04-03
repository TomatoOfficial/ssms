<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://img.picui.cn/free/2025/04/04/67eeb896601d0.jpg" alt=""></a>
</p>

<h3 align="center">Student Scores Management System</h3>

<p align="center"> "A Python Project." | For CG Middle Junior Middle School
    <br> 
</p>

## ✍️ Author <a name = "author"></a>

- [@TomatoOfficial](https://github.com/tomatoofficial) - Idea & Program

See also the list of [contributors](https://github.com/tomatoofficial/ssms/) who participated in this project.


## ⚠️ Before Use
- I do not recommend using this program, as it has
been customized for Class 5 of _Chenggong Junior Middle School_ in 2023.
- Of course, if you want to use it, you can also modify
the relevant list in the source code and customize
__in.csv__ to look like you want.
- Perhaps this is the charm of open source.


## ⌨️ How to Use
- There is a partial guide in the program, theoretically
you can use it based on the guide.
- Attention: __ssms__ is currently in the __development__ stage
and some features have not been implemented.


## 📝 Changelog (After 2025.03.27)
### ssms - v1.2.5 - 2025.03.27
+ 完善了选择班长的功能：
  - 不再选中 **in.csv** 中的空行。
  - **out.csv** 输出正常。

---

### ssms - v1.2.6 - 2025.03.28
+ 将输入输出 **csv** 中的 “红领巾” 替换为 “校徽” 。
+ 将输入 **csv** 中添加了 ”组长“ 列。当值为 **1** 时，判断该生为组长，反之不是。
+ 添加了 **settings.ini** 文件。用户可以通过修改 **[Multiplier]** 节中的相关内容控制组员扣分时组长扣分的倍率 (*不支持非int*)。
+ 修改了扣分系统:
  - 组员扣分: 按 **settings.ini** 中配置的倍数扣除组长分数（*如 纪律 = 2 时，学生扣 3 分 -> 组长扣 6 分*）。
  - 组长扣分: 仅扣除输入分数，不触发额外逻辑。
+ 清屏使用了更兼容的 **os.system**。

---

### ssms - v1.3.0 - 2025.03.31 (WORKING IN PROGRESS)
+ 修复了 **output** 文件夹未找到而崩溃的问题。
+ 完全重构了代码结构，史山已推倒。
+ 添加了简体中文适配 (**zh_CN.local**) ，同时改进了 **UI** 显示。
+ 增加了自动计算班长分数功能，不需要在最终表格中使用 **=sum**。
+ 选择班长时将跳过已为班长的学生，且将计算该表格中该生是否未被扣分。