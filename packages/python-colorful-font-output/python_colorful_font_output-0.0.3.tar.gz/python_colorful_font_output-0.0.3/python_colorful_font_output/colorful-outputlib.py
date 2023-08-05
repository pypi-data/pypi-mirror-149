from time import sleep
from os import system
from rich import print as rich_print
from rich.console import Console
import sys
import python_colorful_font_output
from platform import python_version
try:
    import traceback
except:
    import traceback2
m_list = []
m_time = []
rgbs = []
console = Console()
class WindowsUpdateOwnColor:
    def __init__(self, color_name='1', update_color='0'):
        self.colorname=color_name
        self.update_color=update_color
    def control_colors(self):
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
        print("There are some classes to make your terminal more colorful and beautiful! ")
        print("""What do you want to ask? Please answer 'Run the module's tips', 'Dependency Libraries', 'All functions',
        'Editions' or 'Information':""",end='')
        answer=input()
        if answer == "Run the module's tips":
            print("""These are some tips for the module(I know):
            If you use the module in PyCharm, please set something,because it doesn't supported
            the default color space. So, do:
            1.find your program. Right click it. And choose 'Edit run configuration'.
            2.find 'run', click 'terminal in analog output console' and determine it.
            3.Now you can run the module successfully.(Because library 'rich' is the module's dependency Library)
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
            (class)RichRgbOutput
            |      |____(defined function)output_object
            |           |____(Use method)output_object(object, rgb_list, wait_time_list)
            |           |    |____(Example)RichRgbOutput.output_object('Hello,world' -> str
            |           |                                    ['rgb(123,23,234)', ...]->list, each are str(Can be only 1)
            |           |                                    [0.3, ...])->list,each are float(Can be only 1 number)
            |           |____(function)print letter one by one with color-RGB same, wait time same.
            |           |____(function)print letter one by one with color-RGB same, wait time different.
            |           |____(function)print letter one by one with color-RGB different, wait time same.
            |           |____(function)print letter one by one with color-RGB different, wait time different.
            (class)WindowsOwnColorOutput
                   |____(defined function)colorful_output
                   |    |____(Use method)colorful_output(object,color_true_or_false,wait_time_list,color_m_list)
                   |    |    |____(Example)colorful_output('win',     -> (all str)You want to print's str
                   |    |                               1,   ->(1/0) 1:colorful print; 0: default color print
                   |    |                             [0.2], -> (all float)If there 1 float, each word's wait time same
                   |    |                              [36]) -> (all int)If there 1 int, each word's color same
                   |    |        Warning: If wait time list or color(m)list's len() isn't 1, please write all word's
                   |    |        information(number).
                   |    |____(function)print letter one by one(white/black, the color change with your terminal background-color.)
                   |    |____(function)print letter one by one, each word's color same with function1, wait time different.
                   |    |____(function)print letter one by one, each word's color are same, wait time is same.
                   |    |____(function)print letter one by one, each word's color are same, wait time is different.
                   |    |____(function)print letter one by one, each word's color are different, wait time is same.
                   |    |____(function)print letter one by one, each word's color are different, wait time is different.
                   |____(defined function)update_the_color(link to: WindowsUpdateOwnColor.control_colors)
                        |____(Use method)update_the_color(update_color) -> Same with ↑.
                        |    |____(Example)WindowsOwnColorOutput.update_the_color('36') ->Update the color to your input color.
                        |____(function)Same defined function 'control_colors'
            """)
        elif answer == "Editions":
            print("""These are the module's all editions.
            python-colorful-font-output               0.0.1
            python-colorful-font-output               0.0.2
            python-colorful-font-output               0.0.3(This version)
            <python-colorful-font-output-0.0.3> add items:
            No.1 Add class 'Help' to show some information.
            N0.2 remove main file, change to some classes and defined functions to do more complex than <python-colorful
                 -font-output-0.0.1> and <python-colorful-font-output-0.0.2>.
            No.3 Add class 'RichRgbOutput' to output colorful words with R-G-B.(R-G-B is RED-GREEN-BLUE's concentration.
            No.4 Add many defined functions to help you use the module well, and add many functions to give the module's
                 functions more powerful and large-scale to envoy your terminal more beautiful.
            No.5 
            """)
        elif answer == "information":
            print("""This is the module's version information.(name, time, version)
                        Name                Time                Version
            python-colorful-font-output   2022.04.29 19:25       0.0.1
            python-colorful-font-output   2022.04.29 20:30       0.0.2
            python-colorful-font-output   2022.05.03 19:45       0.0.3(This version)
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
            Your Python information:"""+sys.version_info+""".""", format(sys.getwindowsversion(), sys.version))
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
            """)
        elif answer1 == "It is/isn't qualified":
            print("""You want to check your PC/Python's version is qualified? These are the answers.""")
            print("""Your PC/Python's version is:
            Your windows version:{0}
            Your Python version: Python {1}
            """, format(sys.getwindowsversion(), python_version()))
            print("""The program wants:
            PC version: Linux, windows, windows 10/11 is the best, because the module write on them.
            Python version: Python 3.x, Python 3.10 is the best, because the module write on it.
            Warning:Python 2.6/2.7 isn't qualified,because they and Python 3.x are fundamentally different.
                    And, I don't know Linux system will return a trace back or not, because I never try on
                    it.(But I think it's will run very well, too.)
            """)
        else:
            print("You only can answer the option!")
class RichRgbOutput:
    def __init__(self, object, rgbs, time):
        self.object=object
        self.rgbs=rgbs
        self.time=time
    def output_object(self):
        x=0
        self.object=list(self.object)
        for i in self.object:
            if len(rgbs) != 1:
                console.print(i,end='',style=self.rgbs[x])
            else:
                console.print(i,end='',style=self.rgbs[0])
            if len(self.time) == 1:
                sleep(self.time[0])
            else:
                sleep(self.time[i])
            x+=1
class WindowsOwnColorOutput:
    def __init__(self, object, color_t_or_f, m_time, m_list):
        self.object=object
        self.colorful_ft=color_t_or_f
        self.time_m=m_time
        self.times=int(time[0])
        self.list_m=m_list
    def colorful_output(self):
        x = 0
        self.object = list(self.object)
        if self.colorful_ft == 0:
            for i in self.object:
                print(i, end='')
                if self.times == -1:
                    sleep(float(self.time_m[x]))
                    x += 1
                else:
                    sleep(self.times)
        elif self.colorful_ft == 1:
            if len(self.list_m) == 1:
                x = 0
                for i in self.object:
                    print("\033[" + str(self.list_m[0]) + "m" + i + "\033[0m", end='')
                    if self.times == -1:
                        sleep(float(self.time_m[x]))
                        x += 1
                    else:
                        sleep(self.times)
                        x += 1
            elif len(self.list_m) != 1:
                x = 0
                for i in self.object:
                    print("\033[" + str(self.list_m[x]) + "m" + i + "\033[0m", end='')
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