'''
   外盘数据获取
   by wooght 2014-07-15
'''
from PIL import ImageGrab
from PIL import Image
import sys
import time

class number:
   #原始数字二进制代表
   out_list=['1101111011','0111001110','0001101110','0011100011','1111111111',
            '1100000011','1100011011','0011101110','1111111011','1101100011']
   #受4影响数字二进制代表
   out_list_by4=['','0111001111','0001101111','0011110011','',#0-4
            '1100010011','','0011101111','','1101110011',#5-9
            '','0111011110','0001111110','','',#0-4
            '','','0011111110','','',#5-9
            '','0111011111','0001111111','','',#0-4
            '','','0011111111','','']#5-9
   list4=''#4位置四
   list2=''#2位置二
   result_run_num=''#返回数字字符串
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
      #截图,截图失败返回false
      self.list4=''
      self.list2=''
      try:
         self.imw=ImageGrab.grab([self.x,self.y,self.x+28,self.y+7])
      except OSError:
         print('mt4截图错误:',self.save_time())
         return False
      for i in range(28):
         #取色 只判断有色和无色
          c4=self.imw.getpixel((i,4))
          c2=self.imw.getpixel((i,2))
          if c4==(0,0,0):
              self.list4+='0'
          else:
              self.list4+='1'
          if c2==(0,0,0):
              self.list2+='0'
          else:
              self.list2+='1'
      return True
              
   #编码分析
   def asc_analysis(self):
      out=[]#2,4组合 列表
      out_str=''#组合得到二进制字符串
      #每个数字5像素
      for i in range(0,5):
          if i>1:
              k=i*5+3
          else:
              #以小数点分开
              k=i*5
          out.append(self.list2[k:(k+5)]+self.list4[k:(k+5)])
          if out[i] in self.out_list:
             out_str+=str(self.out_list.index(out[i]))
          elif out[i] in self.out_list_by4:
             pd_key=self.out_list_by4.index(out[i])
             #受到4的影响
             if pd_key>19:
                pd_key-=20
             elif pd_key>9:
                pd_key-=10
             out_str+=str(pd_key)
          else:
             out_str+=''#缺省值 空
      #如果数字相同 如44444  则没获取到数据
      #判断获取的值是否正确
      if len(out_str)!=5:
         self.save_img()
         return False
      elif out_str[0]==out_str[1] and out_str[1]==out_str[2] and out_str[2]==out_str[3]:
         self.save_img()
         return False
      else:
         self.result_run_num=out_str
         return True

   #时间记录
   def save_time(self):
      return time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
   #保存图片
   def save_img(self):
      addr='run_error_pic'
      pic_name=self.save_time()
      pic_name=addr+'/'+pic_name+'.jpg'
      try:
         self.imw.save(pic_name,'jpeg')
      except PermissionError:
         return False
