'''
   内盘数据获取 截图 分析
   by wooght 2014-11-27
'''
from PIL import ImageGrab
from PIL import Image
import sys
import time

class number:
   #原始数字-二进制代表
   in_list=['01110001111-11110000111','01111111100-00000111100','00000001111-00000111110','00000001111-00000001111','00001111110-00111011110',
            '01111000000-00000000111','01111000000-11111001111','00000011110-00001111000','01111001111-00111111110','11110001111-00111111111']
   list4=''#4位置二
   list8=''#8位置二
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
      self.list4=''
      self.list8=''
      try:
         self.im=ImageGrab.grab([self.x,self.y,self.x+48,self.y+14])
      except OSError:
         print('dby截图错误:',self.save_time())
         return False
      for i in range(48):
         #第4个位置
         c4=self.im.getpixel((i,4))
         #第8个位置
         c8=self.im.getpixel((i,8))
         
         if c4==(0,0,0):
            self.list4+='0'
         else:
            self.list4+='1'
         if c8==(0,0,0):
            self.list8+='0'
         else:
            self.list8+='1'
      return True
   #编码分析
   def asc_analysis(self):
      out=[]#数字编码列表
      out_str=''
      for i in range(0,4):
         #每个文字,11像素
         k=i*12
         out.append(self.list4[k:(k+11)]+'-'+self.list8[k:(k+11)])
         if out[i] in self.in_list:
               out_str+=str(self.in_list.index(out[i]))
         else:
            print("error:",out[i],'i:',i)
            out_str+=''#缺省值为空
      if len(out_str)!=4:
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
      pic_name=self.save_time()
      pic_name=addr+'/'+pic_name+'.jpg'
      try:
         self.im.save(pic_name,'jpeg')
      except PermissionError:
         return False
