'''
   内盘数据获取 截图 分析 西部银业
   by wooght 2014-09-23
'''
from PIL import ImageGrab
from PIL import Image
import sys
import time
import random

class number:
   #原始数字-二进制代表
   in_list=['11100000000111','00000001110000','00000000011110','00000111111000','00111000111000',
            '01111111111110','11111111111110','00000011110000','00011111111000','11110000001111']
   in_list_red=['11110000000111','00000001111000','','00000111111100','01111000111100',
                '','','','','']
   in_list_white=['11110000001111','','','','',
                  '','','','','']
   list9=''#4位置二
   result_run_num=''#返回数字字符串
   abc=1
   def __init__(self,x,y):
      self.x=x
      self.y=y
   #运行接口
   def get_number(self):
      if not self.get_asc():
         return False
      if self.asc_analysis():
         return self.result_run_num
      else:
         return False
   #获取编码
   def get_asc(self):
      self.list9=''
      try:
         self.im=ImageGrab.grab([self.x,self.y,self.x+62,self.y+21])
      except OSError:
         print('xbyy截图错误:',self.save_time())
         return False
      for i in range(62):
         #第9个位置
         c9=self.im.getpixel((i,9))
         if c9<(0,0,20):
            self.list9+='0'
         else:
            self.list9+='1'
      return True
   #编码分析
   def asc_analysis(self):
      out=[]#数字编码列表
      out_str=''
      for i in range(0,4):
         #每个文字,14像素
         if i>0:
            k=i*16
         else:
            k=i*14
         out.append(self.list9[k:(k+14)])
         if out[i] in self.in_list:
            #6,5区分
            if self.in_list.index(out[i])==6:
               pd_6=self.im.getpixel((k,8))
               if pd_6==(0,0,0):
                  out_str+='5'
               else:
                  out_str+='6'
            #白0,9区分
            elif self.in_list.index(out[i])==9:
               pd_12=self.im.getpixel((k,12))
               if pd_12==(0,0,0):
                  out_str+='9'
               else:
                  out_str+='0'
            else:
               out_str+=str(self.in_list.index(out[i]))
         elif out[i] in self.in_list_red:
            out_str+=str(self.in_list_red.index(out[i]))
         else:
            out_str+=''#缺省值为空
      if len(out_str)!=4:
         print(self.list9)
         self.save_img()
         return False
      else:
         self.result_run_num=out_str
         return True

   #时间记录
   def save_time(self):
      time_str=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
      return time_str
   #保存图片
   def save_img(self):
      addr='run_error_pic'
      pic_name=self.save_time()+str(random.randint(1,10000))
      pic_name=addr+'/'+pic_name+'.jpg'
      try:
         self.im.save(pic_name,'jpeg')
      except PermissionError:
         return False
