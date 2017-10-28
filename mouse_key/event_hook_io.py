'''
    鼠标键盘控制 驱动级控制 键盘控制鼠标
    by wooght 2014.08.15
'''
from ctypes import *
import win32con
import win32gui
import win32api
import time
import WOOGHTIO


#移动鼠标到制定坐标
def mouse_move(zb):
    uwin=windll.user32
    uwin.SetCursorPos(zb[0],zb[1])
#鼠标单击
def mouse_click(zb):
    mouse_move(zb)
    WOOGHTIO.MouseClick(1)

#鼠标双击
def mouse_dbclick(zb):
    mouse_move(zb)
    WOOGHTIO.MouseDoubleClick(1)

#键盘输入
def keyset(num_or_str):
        for i in num_or_str:
            WOOGHTIO.EnterKey(int(i))
#敲回车
def key_enter():
        #键盘按下
        win32api.keybd_event(13,0,0,0)
        #抬起
        win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)    

uwin=windll.user32
#获取颜色值 16进制
def get_color(zb):
        #获取句柄
    hdc = uwin.GetDC(None)
    #获取指定像素的颜色
    color = windll.gdi32.GetPixel(hdc,int(zb[0]),int(zb[1]))
    return hex(color)
