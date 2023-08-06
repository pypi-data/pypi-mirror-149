import sys
from platform import python_version
from time import sleep
from os import system
from rich.console import Console
"""colorful_output.py"""
"""
此.py文件名为colorful_outputlib.py（31849字符，上上次小更新增加2404字符）
这个是python-colorful-font-output的主代码，
其辅助文件为：
python.py（7929字符，与此.py同一目录下）
__init__.py（32字符，与此.py文件同一目录下）
setup.py（804字符，位于pythonProject6文件夹目录下的唯一一个文件）
setup_information.txt（54字符，与此.py文件同一目录下）
要改动：
038~216：更新0.0.9的Help功能（现16187字符）
240~153：更新(defined function)print_rgb
254~264：更新(defined function)print_colorful_256
265~269：更新(defined function)show
"""
def print_256(width=32):
    print("")
    print("\033[38;2;147;112;219m                                                   现在是背景颜色\033[0m")
    for i in range(256):
        if (i+1) % width == 0 and i != 0:
            if 240 <= i <= 255:
                if len(list(str(i))) == 3:
                    print("\033[48;5;" + str(i) + ";38;2;0;0;128m" + str(i) + "\033[0m")
                elif len(list(str(i))) == 2:
                    print("\033[48;5;{0};38;2;0;0;128m{0} \033[0m".format(i))
                else:
                    print("\033[48;5;{0}38;2;0;0;128m {0} \033[0m".format(i))
            else:
                if len(list(str(i))) == 3:
                    print("\033[48;5;"+str(i)+"m"+str(i)+"\033[0m")
                elif len(list(str(i))) == 2:
                    print("\033[48;5;{0};38;2;0;0;128m{0} \033[0m".format(i))
                else:
                    print("\033[48;5;{0};38;2;0;0;128m {0} \033[0m".format(i))
        else:
            if 240 <= i <= 255:
                if len(list(str(i))) == 3:
                    print("\033[48;5;" + str(i) + ";38;2;0;0;128m" + str(i) + "\033[0m",end=' ')
                elif len(list(str(i))) == 2:
                    print("\033[48;5;{0};38;2;0;0;128m{0} \033[0m".format(i),end=' ')
                else:
                    print("\033[48;5;{0};38;2;0;0;128m {0} \033[0m".format(i),end=' ')
            else:
                if len(list(str(i))) == 3:
                    print("\033[48;5;" + str(i) + "m" + str(i) + "\033[0m",end=' ')
                elif len(list(str(i))) == 2:
                    print("\033[48;5;{0};38;2;0;0;128m{0} \033[0m".format(i),end=' ')
                else:
                    print("\033[48;5;{0};38;2;0;0;128m {0} \033[0m".format(i),end=' ')
    print("")
    print("\033[38;2;147;112;219m                                                 接下来是字体颜色\033[0m")
    for i in range(256):
        if (i+1) % width == 0 and i != 0:
            if 240 <= i <= 255:
                if len(list(str(i))) == 3:
                    print("\033[38;5;" + str(i) + "m" + str(i) + "\033[0m")
                elif len(list(str(i))) == 2:
                    print("\033[38;5;{0}m{0}\033[0m".format(i))
                else:
                    print("\033[38;5;{0}m{0}\033[0m".format(i))
            else:
                if len(list(str(i))) == 3:
                    print("\033[38;5;"+str(i)+"m"+str(i)+"\033[0m")
                elif len(list(str(i))) == 2:
                    print("\033[38;5;{0}m{0}\033[0m".format(i))
                else:
                    print("\033[38;5;{0}m {0}\033[0m".format(i))
        else:
            if 240 <= i <= 255:
                if len(list(str(i))) == 3:
                    print("\033[38;5;" + str(i) + "m" + str(i) + "\033[0m",end=' ')
                elif len(list(str(i))) == 2:
                    print("\033[38;5;{0}m{0} \033[0m".format(i),end=' ')
                else:
                    print("\033[38;5;{0}m {0} \033[0m".format(i),end=' ')
            else:
                if len(list(str(i))) == 3:
                    print("\033[38;5;" + str(i) + "m" + str(i) + "\033[0m",end=' ')
                elif len(list(str(i))) == 2:
                    print("\033[38;5;{0}m{0} \033[0m".format(i),end=' ')
                else:
                    print("\033[38;5;{0}m {0} \033[0m".format(i),end=' ')
def print_256_diff(width=6):
    print("")
    print("\033[38;2;147;112;219m                                                   现在是背景颜色\033[0m")
    for i in range(256):
        if (i+1) % width == 0 and i != 0:
            if 240 <= i <= 255:
                if len(list(str(i))) == 3:
                    print("\033[48;5;" + str(i) + ";38;2;0;0;128m" + str(i) + "\033[0m")
                elif len(list(str(i))) == 2:
                    print("\033[48;5;{0};38;2;0;0;128m{0}\033[0m".format(i))
                else:
                    print("\033[48;5;{0}38;2;0;0;128m {0}\033[0m".format(i))
            else:
                if len(list(str(i))) == 3:
                    print("\033[48;5;"+str(i)+"m"+str(i)+"\033[0m")
                elif len(list(str(i))) == 2:
                    print("\033[48;5;{0};38;2;0;0;128m{0}\033[0m".format(i))
                else:
                    print("\033[48;5;{0};38;2;0;0;128m {0}\033[0m".format(i))
        else:
            if 240 <= i <= 255:
                if len(list(str(i))) == 3:
                    print("\033[48;5;" + str(i) + ";38;2;0;0;128m" + str(i) + "\033[0m",end=' ')
                elif len(list(str(i))) == 2:
                    print("\033[48;5;{0};38;2;0;0;128m{0}\033[0m".format(i),end=' ')
                else:
                    print("\033[48;5;{0};38;2;0;0;128m {0}\033[0m".format(i),end=' ')
            else:
                if len(list(str(i))) == 3:
                    print("\033[48;5;" + str(i) + "m" + str(i) + "\033[0m",end=' ')
                elif len(list(str(i))) == 2:
                    print("\033[48;5;{0};38;2;0;0;128m{0}\033[0m".format(i),end=' ')
                else:
                    print("\033[48;5;{0};38;2;0;0;128m {0}\033[0m".format(i),end=' ')
    print("")
    print("\033[38;2;147;112;219m                                                 接下来是字体颜色\033[0m")
    for i in range(256):
        if (i+1) % width == 0 and i != 0:
            if 240 <= i <= 255:
                if len(list(str(i))) == 3:
                    print("\033[38;5;" + str(i) + "m" + str(i) + "\033[0m")
                elif len(list(str(i))) == 2:
                    print("\033[38;5;{0}m{0} \033[0m".format(i))
                else:
                    print("\033[38;5;{0}m{0} \033[0m".format(i))
            else:
                if len(list(str(i))) == 3:
                    print("\033[38;5;"+str(i)+"m"+str(i)+"\033[0m")
                elif len(list(str(i))) == 2:
                    print("\033[38;5;{0}m{0} \033[0m".format(i))
                else:
                    print("\033[38;5;{0}m {0} \033[0m".format(i))
        else:
            if 240 <= i <= 255:
                if len(list(str(i))) == 3:
                    print("\033[38;5;" + str(i) + "m" + str(i) + "\033[0m",end=' ')
                elif len(list(str(i))) == 2:
                    print("\033[38;5;{0}m{0}\033[0m".format(i),end=' ')
                else:
                    print("\033[38;5;{0}m {0}\033[0m".format(i),end=' ')
            else:
                if len(list(str(i))) == 3:
                    print("\033[38;5;" + str(i) + "m" + str(i) + "\033[0m",end=' ')
                elif len(list(str(i))) == 2:
                    print("\033[38;5;{0}m{0}\033[0m".format(i),end=' ')
                else:
                    print("\033[38;5;{0}m {0}\033[0m".format(i),end=' ')
def print_16(width=8, language='Chinese'):
    dict = {'1': "加粗", '3': "斜体", '4': "划线", '7': "白底", '9': "划去", '21': "粗划线", '51': "加方框",
            '30': "黑色", '31': "红色", '32': "绿色", '33': "黄色", '34': "蓝色", '35': "紫色", '36': "淡蓝",
            '37': "灰色", '41': "红底", '42': "绿底", '43': "黄底", '44': "蓝底", '45': "紫底", '46': "淡蓝底",
            '47': "灰底", '40': "黑底"}
    if language=='Chinese':
        pass
    x=0
    for k,v in dict.items():
        if x % width == 0:
            print("\033[{}m{}\033[0m".format(k,v))
        else:
            print("\033[{}m{}\033[0m".format(k,v), end=' ')
def print_input_rgb(input_rgb, background=0, return_01=1):
    if background == 0:
        print("\033[38;5;{};{};{}mRGB: {}\033[0m".format(input_rgb[0],input_rgb[1],input_rgb[2],','.join(input_rgb[:])))
        if return_01 == 1:
            return 0
        else:
            return 'well'
    elif background == 1:
        print("\033[48;5;{};{};{}mRGB: {}\033[0m".format(input_rgb[0], input_rgb[1], input_rgb[2],','.join(input_rgb[:])))
        if return_01 ==1:
            return 0
        else:
            return 'well'
    else:
        if return_01 == 1:
            return 1
        else:
            return 'error'
try:
    import traceback
except:
    import traceback2
m_list = []
m_time = []
rgb = []
class WindowsUpdateOwnColor:
    def __init__(self, color_name='1', update_color='0'):
        self.colorname=color_name
        self.update_color=update_color
    def chinese_control_colors(self):
        dict = {'1': "加粗", '3': "斜体", '4': "划线", '7': "白底", '9': "划去", '21': "粗划线", '51': "加方框",
                '30': "黑色", '31': "红色", '32': "绿色", '33': "黄色", '34': "蓝色", '35': "紫色", '36': "淡蓝",
                '37': "灰色",'41': "红底", '42': "绿底", '43': "黄底", '44': "蓝底", '45': "紫底", '46': "淡蓝底",
                '47': "灰底",'40': "黑底"}
        for k,v in dict.items():
            if self.colorname == v:
                the_color = k
        return the_color
    def update_to_default_colors(self):
        print("\033[0m\033[0m")
    def update_to_input_color(self):
        print("\033["+self.update_color+"m\033[0m")
class Help:
    def __init__(self):
        self.version = sys.version
        self.version_info = sys.version_info
    def ask_the_module_questions(self):
        print("This is <python-colorful-font-output-0.0.9>'s Help.")
        print("There are some classes to make your terminal more colorful and beautiful! (Writer:Yuli Wang;作者：王俞励)")
        print("""What do you want to ask? Please answer 'Run the module's tips', 'Dependency Libraries', 'All functions',
        'Editions' or 'Information':""",end='')
        answer=input()
        if answer == "Run the module's tips":
            print("""These are some tips for the module(I know):
            No.1 If you use the module in PyCharm, please set something,because it doesn't supported
                 the default color space. So, do:
                 1.find your program. Right click it. And choose 'Edit run configuration'.
                 2.find 'run', click 'terminal in analog output console' and determine it.
                 3.Now you can run the module successfully.(Because library 'rich' is the module's dependency Library)
                 But, you don't run about rgb output, if your computer monitor does not support it. It will print,but
                 you can't read it right.
            No.2 If you want to import the module, please write on your program: from python_colorful_font_output import ...
                 It's '_', not '-'. But install the module with pip want: pip install python-colorful-font-output==0.0.9
            """)
        elif answer == 'Dependency Library':
            print("""The module need these Dependency Libraries:
            No.1 sys
            No.2 rich
            No.3 rich.console
            No.4 traceback/traceback2
            No.5 os
            No.6 time
            No.7 platform
            If you don't install these six libraries before you run the program, it will return a trace back.""")
        elif answer == 'All functions':
            print("""These are all of the module functions:
            (class)WindowsUpdateOwnOutput
            |      |____(defined function)control_colors(Only support Chinese color-name.)
            |      |    |____(Use method)control_colors(color-name's str) -> (return) the color-name's own color number in Windows.
            |      |    |    |____(Example)WindowsUpdateOwnOutput.control_colors("红底") -> (return) 41 (Because in
            |      |    |                                                   WindowsOwnColors 41 -> red-background)
            |      |    |____(function)Control letter's color(Only control colors with Windows's Own color).
            |      |____(defined function)update_to_default_colors
            |      |    |____(Use method)update_to_default_colors() -> Update to your terminal's default color.
            |      |    |____(function)It will update the word's color to your PC/Python's default color.
            |      |____(defined function)update_to_input_color
            |           |____(Use method)update_to_input_color("32") -> (change)The word's color will update to the input color.
            |           |    |____(Example)WindowsUpdateOwnOutput.update_to_input_color("32") -> Same with ↑.
            |           |____(function)It will update to a input color.
            (class)Help
            |      |____(defined function)the_module_questions
            |      |    |____(Use method)the_module_questions() -> (print)It will print some help-tips.
            |      |    |    |____(Example)Help.the_module_questions() -> (print)It will print some help-tips.
            |      |    |____(function)tell you about the module's information.
            |      |    |____(function)tell you how to use the module well.
            |      |____(defined function)the_pc_information
            |           |____(Use method)the_pc_information() -> (print)It will print some help of your PC information.
            |           |    |____(Example)Help.the_pc_information() -> Same with ↑.
            |           |____(function)tell you about your PC/Python version.
            |           |____(function)tell you about the module needs what PC/Python version to run the module successfully.
            |           |____(function)tell you your PC/Python version are/aren't qualified.
            (class)RichColorfulOutput
            |      |____(defined function)output_object
            |      |    |____(Use method)output_object(objects, rgb_list, wait_time_list)
            |      |    |    |____(Example)RichColorfulOutput.output_object('Hello,world', -> str
            |      |    |             ['rgb(123,23,234)', ...]->list, each are str.When it's only 1, all word's color same.
            |      |    |             [0.3, ...])->list,each are float.When it's only 1 number,all word's color same.
            |      |    |____(function)print letter one by one with color-RGB same, wait time same.
            |      |    |____(function)print letter one by one with color-RGB same, wait time different.
            |      |    |____(function)print letter one by one with color-RGB different, wait time same.
            |      |    |____(function)print letter one by one with color-RGB different, wait time different.
            |      |____(defined function)english_description_output
            |      |    |____(Use method)english_description_output(objects, color_description_list, wait_time_list)
            |      |    |    |____(Example)RichColorfulOutput.english_description_output('Hello World', -> str
            |      |    |       ['red on white', ...] -> list, each str.When it's only 1, all word's color same.
            |      |    |       [0.3, ...] -> list, each float.When it's only 1, all word's color same.
            |      |    |____(function)print letter one by one with english-color same, wait time same.
            |      |    |____(function)print letter one by one with english-color same, wait time different.
            |      |    |____(function)print letter one by one with english-color different, wait time same.
            |      |    |____(function)print letter one by one with english-color different, wait time different.
            |____(class)PyPrintOutput
            |    |____(defined function)print_rgb
            |    |    |____(Use method)print_rgb(object, rgb, wait_time_secs, output_256)
            |    |    |    |____(Example)print_rgb('Hello World!', -> (str)A OBJECT, it's output thing.
            |    |    |       [(123,234,12), ...], -> tuple in list, it can be only 1, if there only 1, color-RGB same.
            |    |    |      [0.1, ...], -> wait time(s) a list.(Can be 1,if there only 1,wait time same.
            |    |    |      29347) -> If you only use this function, it can be anything.
            |    |    |____(function)print one by one with color-RGB, wait time same, color different.
            |    |    |____(function)print one by one with color-RGB, wait time different, color same.
            |    |    |____(function)print one by one with color-RGB, wait time same, color same.
            |    |    |____(function)print one by one with color-RGB, wait time different, color different.
            |    |____(defined function)print_colorful_256
            |    |    |____(Use method)PyPrintOutput(object, rgbs, time=0.2).print_colorful_256(
            |    |    |    |                          ft=1, width=32, ft_2=0)
            |    |    |    |____(Example)PyPrintOutput(...).print_colorful_256(
            |    |    |             ft=1, -> (bool)Yes/No show color-256 I can print.(Can omit, omit will default show) ↓ too.
            |    |    |           width=32, -> (int)means show color-256 I can print how many colors' width.(32 is default)
            |    |    |             ft_2=1) -> (bool)means use (defined function)print_256
            |    |    |____(function)
            |    |____(defined function)show
            |         |____(Use method)show(inputs_rgb, background=0, width=8, print_16_ft=1) 1~3 numbers is default.
            |         |    |____(Example)show((123,234,12), -> tuple, means color-RGB numbers.
            |         |                  background=0, -> (bool)Is/isn't print color background-color
            |         |                       width=8, -> (int)output width, can't be 0.
            |         |             print_16_ft=1 -> (bool)Is/isn't print 16 colors,if there 0, will print color with inputs_rgb
            |         |             return_01=1) -> (bool)if it's 1, show() will return 1/0,else return 'well' or 'error'. 
            |         |   Warning: if the function show()'s 4th number 0, it will return a message, if return_01=1,return 0/1,
            |         |  else if return =1, return 'well'(means all right) or 'error'(means has a error)
            |         (function)show colors with the numbers.(16/a rgb)Different width you can choose.
            (class)WindowsOwnColorOutput
            |      |____(defined function)colorful_output
            |      |    |____(Use method)colorful_output(object,color_true_or_false,wait_time_list,
            |      |    |    |      color_m_list_or_dict, is_each_word_write_all_t_or_f, default_color)
            |      |    |    |____(Example)colorful_output('win',  -> (all str)You want to print's str
            |      |    |  1,   ->(bool) 1:colorful print; 0: default color print(if it was 0, 3th number please write down, too.
            |      |    | [0.2], -> (all float)If there 1 float, each word's wait time same.
            |      |    | 1, -> (bool) 1:Omit default color numbers 0: No omit default color numbers
            |      |    | [(3,4,5),(3,4,5)]) -> (list or dict both ok)list: 1~len(list)word's color numbers
            |      |    | dict: {(int)word's index : (int,can be tuple)word's color , ...}
            |      |    |           ↑   If word's color = default color, can omit it.   ↑
            |      |    |____(function)print letter one by one(white/black, the color change with your terminal background-color.)
            |      |    |____(function)print letter one by one, each word's color same with function1, wait time different.
            |      |    |____(function)print letter one by one, each word's color are same, wait time is same.
            |      |    |____(function)print letter one by one, each word's color are same, wait time is different.
            |      |    |____(function)print letter one by one, each word's color are different, wait time is same.
            |      |    |____(function)print letter one by one, each word's color are different, wait time is different.
            |      |    |____(function)print letter one by one, each word's color can be a tuple, each number in tuple means a
            |      |                   color argument.(Applies all of the functions in WindowsOwnColorOutput.colorful_output)
            |      |____(defined function)update_the_color(link to: WindowsUpdateOwnColor.control_colors)
            |           |____(Use method)update_the_color(update_color) -> Same with ↑.
            |           |    |____(Example)WindowsOwnColorOutput.update_the_color('36') ->Update the color to your input color.
            |           |____(function)Same defined function 'control_colors'
            (class)WindowsUpdateModule
                  |____(defined function)windows_update
                       |____(Use method)WindowsUpdateModule.windows_update()
                       |    |____(Example)WindowsUpdateModule.windows_update()
                       |____(function)You can use the function to update the module in any http.
            """)
        elif answer == "Editions":
            print("""These are the module's all editions.
            python-colorful-font-output               0.0.1
            python-colorful-font-output               0.0.2
            python-colorful-font-output               0.0.3(Big grow)
            python-colorful-font-output               0.0.4
            python-colorful-font-output               0.0.5
            python-colorful-font-output               0.0.6
            python-colorful-font-output               0.0.7
            python-colorful-font-output               0.0.8
            python-colorful-font-output               0.0.9(Big grow, This version)
            <python-colorful-font-output-0.0.4> add/update/remove-error items:
            No.1 Update class 'Help' to show some information.
            N0.2 Remove main file, change to some classes and defined functions to do more complex than
                        <python-colorful-font-output-0.0.8>.
            No.3 Add class PyPrintOutput, to print with python's print(), but it can print very beautiful, too.
            No.4 Update many defined functions to help you use the module well, and add many functions to give the module's
                 functions more powerful and large-scale to envoy your terminal more beautiful.
            No.5 Add english_description_output to print colorful words without color-RGB.
            No.6 Remove errors, for example: In the module '.' writes to ','.
            No.7 Add show(...),print_rgb(...),print_colorful_256(...) in class PyPrintOutput.
            """)
        elif answer == "information":
            print("""This is the module's version information.(name, time, version)
                        Name                Time                Version
            python-colorful-font-output   2022.04.29 19:25       0.0.1
            python-colorful-font-output   2022.04.29 20:30       0.0.2
            python-colorful-font-output   2022.05.03 19:45       0.0.3(Big grow)
            python-colorful-font-output   2022.05.04 10:12       0.0.4
            python-colorful-font-output   2022.05.04 13:51       0.0.5
            python-colorful-font-output   2022.05.05 13:59       0.0.6
            python-colorful-font-output   2022.05.05 20:21       0.0.7
            python-colorful-font-output   2022.05.05 20:50       0.0.8
            python-colorful-font-output   2022.05.07 19:40       0.0.9(Big grow,This version)
            ps:This version is a very big progress, but maybe there are some bug in the module yet.
            ps:And the module's some functions only support Chinese, (Because I'm Chinese) sorry.
            """)
    def the_pc_information(self):
        print("""You want to know the questions of your PC information? Yeah, you're right.Now I ask you some questions:
        Do you want to know 'My PC/Python's version', 'The program want PC/Python version' or 'It is/isn't qualified'?""",end='')
        answer1 = input()
        if answer1 == "My PC/Python's version":
            print("""Your PC/Python's version is:
            Your PC version:{0}
            Your Python version:{1}
            Your Python information:"""+sys.version_info+""".""".format(sys.getwindowsversion(), sys.version))
        elif answer1 == "The program want PC/Python version":
            print("""The program wants' PC/Python version is:
            1. computer system: Linux, Windows, Windows 10/11 is the best, because the module write in them.
              But, I don't know Linux system will return a trace back or not.
            2. Python version: Python 3.x, Python 3.10 is the best(because the module write in Python 3.10)
              And,you can't use Python 2.7/2.6, because Python 2.7/2.6 and Python 3.x, they are fundamentally different.
            3. Python libraries version:
              1.sys----------------------Latest version is the best
              2.time---------------------Latest version is the best
              3.os-----------------------Latest version is the best
              4.traceback/traceback2-----the best version to run: 1.4.0
              5.rich---------------------the best version to run: 12.3.0
              6.rich.console-------------it's in library: rich
              7.platform-----------------Latest version is the best
              8.python-output-show-------You can't install in all of apps, because it write down by me!
            """)
        elif answer1 == "It is/isn't qualified":
            print("""You want to check your PC/Python's version is qualified? These are the answers.""")
            print("""Your PC/Python's version is:
            Your windows version:{0}
            Your Python version: Python {1}
            """.format(sys.getwindowsversion(), python_version()))
            print("""The program wants:
            PC version: Linux, windows, windows 10/11 is the best, because the module write on them.
            Python version: Python 3.x, Python 3.10 is the best, because the module write on it.
            Warning:Python 2.6/2.7 isn't qualified,because they and Python 3.x are fundamentally different.
                    And, I don't know Linux system will return a trace back or not, because I never try on
                    it.(But I think it's will run very well, too.)
            """)
        else:
            print("You only can answer the option!")
class RichColorfulOutput:
    def __init__(self, object, rgbs, time=0.2):
        self.object=object
        self.rgbs=rgbs
        self.time=time
        self.console = Console()
    def rgb_colorful_output(self):
        x=0
        self.object=list(self.object)
        for i in self.object:
            if len(rgb) != 1:
                self.console.print(i,end='',style=self.rgbs[x])
            else:
                self.console.print(i,end='',style=self.rgbs[0])
            if len(self.time) == 1:
                sleep(self.time[0])
            else:
                sleep(self.time[x])
            x+=1
    def english_description_output(self, color_description):
        x=0
        self.object=list(self.object)
        for i in self.object:
            self.console.print(i,end='',style=color_description[(len(color_description)!=1)*x])
            sleep(self.time[(len(self.time)==1)*x])
class PyPrintOutput:
    def __init__(self, object, rgb, times, output_256):
        self.object=object
        self.rgb=rgb
        self.times=times
        self.output_256=output_256
    def print_rgb(self):
        x=0
        self.object=list(self.object)
        for i in self.object:
            print("\033[38;2;{};{};{}m{}\033[0m".format(self.rgb[x][0],self.rgb[x][1],self.rgb[x][2],i), end='')
            sleep(self.times[(len(self.times)==1)*x])
            x+=1
    def print_colorful_256(self, ft=1, width=32, ft_2=0):
        x=0
        if ft == 1:
            if ft_2 == 0:
                print_256(width)
            else:
                print_256_diff(width)
        self.object=list(self.object)
        for i in self.object:
            print("\033[38;5;{}m{}\033[0m".format(self.output_256[x],i),end='')
            x+=1
    def show(self, inputs_rgb, background=0, width=8, print_16_ft=1, return_01=1):
        if print_16_ft == 1:
            print_16(width=width, language='Chinese')
        else:
            print_input_rgb(input_rgb=inputs_rgb, background=background, return_01=return_01)
class WindowsOwnColorOutput:
    def __init__(self, object, color_t_or_f, m_time, words_color_ft, words_color, default_color='0'):
        self.object=object
        self.colorful_ft=color_t_or_f
        self.time_m=m_time
        self.times=int(m_time[0])
        self.words_color_ft=words_color_ft
        self.words_color=words_color
        self.default_color=default_color
    def colorful_output(self):
        x=0
        color_list=[]
        words_colors={}
        self.object = list(self.object)
        for i in range(len(self.object)):
            words_colors[i]=self.default_color
        if type(self.words_color) == list:
            for i in self.words_color:
                words_colors[x]=i
                x+=1
        elif type(self.words_color) == dict:
            words_colors = self.words_color
        x=0
        for k,v in words_colors.items():
            if k != x:
                append_value=self.default_color
            else:
                append_value=v
            color_list.append(append_value)
            x+=1
        x=0
        if self.colorful_ft == 0:
            for i in self.object:
                print(i, end='')
                if self.times == -1:
                    sleep(float(self.time_m[x]))
                    x += 1
                else:
                    sleep(self.times)
        elif self.colorful_ft == 1:
            if len(color_list) == 1:
                x = 0
                for i in self.object:
                    print("\033[" + str(color_list[0]) + "m" + i + "\033[0m", end='')
                    if self.times == -1:
                        sleep(float(self.time_m[x]))
                        x += 1
                    else:
                        sleep(self.times)
                        x += 1
            elif len(color_list) != 1:
                x = 0
                for i in self.object:
                    if type(color_list[0]) == tuple:
                        if len(color_list[x]) == 3:
                            print("\033[{};{};{}m{}".format(str(color_list[x][0]), str(color_list[x][1]),
                                                            str(color_list[x][2]), i))
                        elif len(color_list[x]) == 2:
                            print("\033[{};{}m{}".format(str(color_list[x][0]), str(color_list[x][1]), i))
                    else:
                        print("\033[" + str(color_list[x]) + "m" + i + "\033[0m", end='')
                    if self.times == -1:
                        sleep(float(self.time_m[x]))
                        x += 1
                    else:
                        sleep(self.times)
                        x += 1
            else:
                print("\033[31mWarning: Don't answer without numbers.\033[0m")
        else:
            print("\033[31mWarning: Don't answer without 1/0, please run again.\033[0m")
    def update_the_color(self, color):
        print("\033["+color+"m\033[0m",end='')
class WindowsUpdateModule:
    def __init__(self, update_url="https://upload.pypi.org/legacy/"):
        self.cmd_save_info="python setup.py sdist"
        self.cmd_update="python3 -m twine upload --repository-url "+update_url+" dist/*"
    def windows_update(self):
        system(self.cmd_save_info)
        system(self.cmd_update)