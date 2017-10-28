'''
    动作操作控制模块 东北亚
    by wooght 2014_11_28
'''
import time
from save_data import config
if config.wooght_data.PB_Xevent:
    from mouse_key import event_hook_io as hk
else:
    from mouse_key import event_hook as hk
    
class wooght_control:
    '''
    获取前台数据: 买口,买口,价差钩钩,委托确定,失败弹窗确定按钮,成功位置颜色,数量确认
    买口:open_zb
    卖口:pc_zb
    价差:dc_zb
    委托确认:queren 确认提交  ==>下单中确认
    数量确认:jl_pc_qr_zb ==>平单中确认
    失败弹窗确认:p_dc_zb  ==>下单中平差
    成功颜色位置:open_qr_zb ==>建立参数设置中坐标
    '''
    num_arr=[]#各坐标,数据存储数组
    cg=object#配置
    dc_num=0#点差
    dk=1#多空
    def __init__(self,num_arr):
        self.num_arr=num_arr
        self.cg=config.wooght_data()
        self.set_new_num_arr()
    #设置数据
    def set_new_num_arr(self):
        #基准坐标
        base_zb=[self.num_arr['dc_zb'][0],self.num_arr['dc_zb'][1]]
        self.base_zb=base_zb
        self.num_arr['shou_zb']=[base_zb[0]+62,base_zb[1]-88]#数量
        self.num_arr['sp_zb']=[base_zb[0]+282,base_zb[1]-178]#产品按钮
        self.num_arr['dk_zb']=[base_zb[0]+17,base_zb[1]-33]#买坐标
        self.num_arr['submit']=[base_zb[0]+12,base_zb[1]+47]#开仓坐标
        self.num_arr['pc_tj']=[base_zb[0]+232,base_zb[1]+47]#平仓坐标

        self.num_arr['jywt_zb']=[self.num_arr['open_zb'][0],self.num_arr['open_zb'][1]+16]
    #打开建仓单
    def open_jianc(self):
       #单击打开下拉框
        hk.mouse_click(self.num_arr['open_zb'])
        time.sleep(0.5)
        hk.mouse_click(self.num_arr['jywt_zb'])
        #判断是否打开
        is_open=False
        for i in range(20):
            time.sleep(0.2)
            if hk.get_color(self.num_arr['submit'])=='0xcacaca':
                is_open=True
                break
        if is_open:
            #多空点击
            hk.mouse_click(self.num_arr['dk_zb'])
            time.sleep(0.2)
            #商品
            hk.mouse_click(self.num_arr['sp_zb'])
            time.sleep(0.5)
            #选取千克
            xq_qk_zb=[self.num_arr['sp_zb'][0]-40,self.num_arr['sp_zb'][1]+16*self.num_arr['qk']]
            hk.mouse_click(xq_qk_zb)
            time.sleep(0.2)
            #手
            hk.mouse_dbclick(self.num_arr['shou_zb'])
            hk.keyset(self.num_arr['shou'])
            time.sleep(0.2)
            #点差
            self.set_diancha(int(self.num_arr['dc']))
            time.sleep(0.2)
            #下单前确认 0x0为已经选取,各系统演示不一样,目的:取消选取
            #到提交按钮
            #hk.mouse_move(self.num_arr['submit'])
            return True
        else:
            return False
    #打开平仓单
    def open_pingc(self):
        is_jc=False
        for i in range(15):
            #打开最长时间 3秒
            time.sleep(0.2)
            #双击打开平仓
            hk.mouse_dbclick(self.num_arr['pc_zb'])
            if(hk.get_color(self.num_arr['submit'])=='0xffffff'):
                is_jc=True
                break
        if is_jc:
            #点击打钩
            hk.mouse_click(self.base_zb)
            #双击准备输入
            hk.mouse_dbclick([self.base_zb[0]+140,self.base_zb[1]])
            if self.dc_num<8:
                hk.keyset(str(self.dc_num+2))
            else:
                hk.keyset(str(self.dc_num))
            return True
        else:
            return False
        
    #判断平仓,建仓是否成功 最多4秒时间
    def judge_cang(self):
        #判断确认按钮是否点击
        is_dj=False
        for i in range(40):
            #确认按钮 最多4秒
            qr_color=hk.get_color([int(self.num_arr['open_qr_zb'][0])-20,self.num_arr['open_qr_zb'][1]])
            loss_color=hk.get_color(self.num_arr['p_dc_zb'])
            if qr_color=='0xd1b499':
                #关闭成功确认框
                hk.mouse_click([int(self.num_arr['open_qr_zb'][0]),int(self.num_arr['open_qr_zb'][1])])
                is_dj=True
                break
            elif loss_color=='0xcacaca':
               #有失败信息提示
               #关闭失败确认框
               hk.mouse_click(self.num_arr['p_dc_zb'])
               is_dj=False
               break
            time.sleep(0.1)
        #已经点击弹窗
        if is_dj:
               return True
        else:
            #点击弹窗失败 或者弹窗等待中
            return False
        
    #执行建仓操作
    def jianc(self):
        #点击提交 建仓
        k=time.time()
        hk.mouse_click(self.num_arr['submit'])
        #判断是否建立成功
        if self.judge_cang():
            j=time.time()
            print('jc:',str(j-k))
            return True
        else:
            #建仓失败
            return False

    #执行平仓操作
    def pingc(self):
        #点击平仓
        hk.mouse_click(self.num_arr['pc_tj'])
        #判定是否平仓
        if self.judge_cang():
            return True
        else:
            #平仓失败,原因:点位偏差太大
            return False
    
    #多,空选择 num=[1,2] 1->多 2->空
    def jianc_dk(self,num):
        self.dk=num;
        if num==1:
            hk.mouse_click(self.num_arr['dk_zb'])
        elif num==2:
            #多空坐标相距55像素
            dk_zb=[self.num_arr['dk_zb'][0]+55,self.num_arr['dk_zb'][1]]
            hk.mouse_click(dk_zb)
    #设置点差
    def set_diancha(self,num):
        #保存系统点差
        self.dc_num=num
        #点击打钩
        hk.mouse_click(self.base_zb)
        #设置点差
        hk.mouse_dbclick([self.base_zb[0]+140,self.base_zb[1]])
        hk.keyset(str(num))
