#! /usr/bin/env/python
# _*_ encoding : utf-8 _*_

from ctypes import *
import numpy as np
import os

ai = cdll.LoadLibrary(os.getcwd()+ "/temp.so")
ai.argtypes=[POINTER(c_char)]    #传入参数为字符指针
STR=(c_char * 100)(*bytes("283104765",'utf-8')) #把一组100个的字符定义为STR
cast(STR, POINTER(c_char))


ai._main.restype = c_char_p
res = ai._main(STR)
print(res)

# ai._main(STR)


#########################参数的回传存在问题########2020/10.03/23.37################
#########################complete it #############2020/10.04/15.30################


