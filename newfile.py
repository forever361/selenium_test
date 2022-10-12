#!/usr/bin/python3

import subprocess

#启一个子线程等待生后再继续
#处理文件
p = subprocess.Popen('cat -v main2.py | sed -e "s/\^M//g" > newfile2.py', shell=True)
while True:
    #没有生成文件的时候是p.poll()为None
    if p.poll() == 0:
        with open('/home/kundwang/newfile2.py', 'r') as f:
            print("the file is exit!")
            print("*" * 50)
            print(f.read())
            print("*" * 50)
        break
#校验^M是否还存在
with open('/home/kundwang/newfile2.py', 'r') as f:
    #不包含指定字符串或不在指定范围内时，返回-1
    if f.read().find('^M') == -1:
        print("替换成功！")
    else:
        print("替换失败！")







