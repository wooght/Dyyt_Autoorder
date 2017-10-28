'''
   内盘数据获取 截图 分析
   by wooght 2014-07-15
'''
from PIL import ImageGrab
from PIL import Image
import sys
import time

class number:
   #原始数字-二进制代表
   in_list=['11000110','00011001','00001101','01111000','11101100',
            '00001110','11101110','00011101','00111000','11101111']
   #特殊或影响数字-二进制代表
   in_list_ts=['','00111001','00011101','','01101100',
              '00001100','','00011001','01111100','']
   list4=''#4位置二
   list5=''#5位置二
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
      self.list5=''
      try:
         self.im=ImageGrab.grab([self.x,self.y,self.x+28,self.y+9])
      except OSError:
         print('dyyt截图错误:',self.save_time())
         return False
      for i in range(28):
         #第4个位置
         c4=self.im.getpixel((i,4))
         #单独第5个位置
         if (i+4)%7==0:
            c5=self.im.getpixel((i,5))
            if c5==(0,0,0):
               self.list5+='0'
            else:
               self.list5+='1'
         if c4==(0,0,0):
            self.list4+='0'
         else:
            self.list4+='1'
      return True
   #编码分析
   def asc_analysis(self):
      out=[]#数字编码列表
      out_str=''
      for i in range(0,4):
         #每个文字,7像素
         k=i*7
         out.append(self.list4[k:(k+7)]+self.list5[i])
         if out[i] in self.in_list:
            #如果是1或者7或者2
            if self.in_list.index(out[i])==1:
               pd_8=self.im.getpixel(((i*7)+4,8))
               #7
               if pd_8==(0,0,0):
                  out_str+=str(self.in_list_ts.index(out[i]))
               #1
               else:
                  out_str+=str(self.in_list.index(out[i]))
            elif self.in_list.index(out[i])==7:
               pd_8=self.im.getpixel(((i*7)+4,8))
               if pd_8==(0,0,0):
                  out_str+=str(self.in_list.index(out[i]))
               #2
               else:
                  out_str+=str(self.in_list_ts.index(out[i]))
            elif self.in_list.index(out[i])==3:
               pd_8=self.im.getpixel(((i*7)+1,3))
               if pd_8==(0,0,0):
                  out_str+="3"
               else:
                  out_str+="8"
            else:
               out_str+=str(self.in_list.index(out[i]))
         elif out[i] in self.in_list_ts:
            out_str+=str(self.in_list_ts.index(out[i]))
         else:
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
