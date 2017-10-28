'''
    动作操作控制模块 西部银业
    by wooght 2014_09_23
'''
import time
from save_data import config
if config.wooght_data.PB_Xevent:
    from mouse_key import event_hook_io as hk
else:
    from mouse_key import event_hook as hk
    
class wooght_control:
    num_arr=[]#各坐标,数据存储数组
    cg=object#配置
    dc_num=0#点差
    def __init__(self,num_arr):
        self.num_arr=num_arr
        self.cg=config.wooght_data()
        self.set_new_num_arr()
    #设置数据
    def set_new_num_arr(self):
        bz_zb=[self.num_arr['dk_zb'][0]+69,self.num_arr['dk_zb'][1]]
        self.num_arr['shou_zb']=[bz_zb[0],bz_zb[1]-86]
        self.num_arr['sp_zb']=[bz_zb[0],bz_zb[1]-117]
        self.num_arr['dc_zb']=[bz_zb[0]-76,bz_zb[1]+100]
        self.num_arr['open_qr_zb']=[bz_zb[0]+42,bz_zb[1]+127]
        #建平仓确认坐标
        self.num_arr['jpc_qr_zb']=[bz_zb[0]+54,bz_zb[1]-15]
        self.num_arr['p_dc_zb']=[bz_zb[0]-69,bz_zb[1]+69]
        self.num_arr['submit']=[bz_zb[0]-35,bz_zb[1]+204]
        self.num_arr['pc_tj']=[bz_zb[0],bz_zb[1]+177]
    #打开建仓单
    def open_jianc(self):
        #单击/双击打开
        hk.mouse_dbclick(self.num_arr['open_zb'])
        #判断是否打开
        is_open=False
        for i in range(20):
            time.sleep(0.2)
            if(hk.get_color(self.num_arr['open_qr_zb'])==self.num_arr['open_qr_color']):
                is_open=True
                break
        if is_open:
            #多空点击
            hk.mouse_click(self.num_arr['dk_zb'])
            #商品
            hk.mouse_click(self.num_arr['sp_zb'])
            #选取千克
            xq_qk_zb=[self.num_arr['sp_zb'][0],self.num_arr['sp_zb'][1]+12*self.num_arr['qk']]
            hk.mouse_click(xq_qk_zb)
            time.sleep(0.5)
            #手
            hk.mouse_dbclick(self.num_arr['shou_zb'])
            hk.keyset(self.num_arr['shou'])
            time.sleep(0.5)
            #点差
            #self.set_diancha(int(self.num_arr['dc']))
            time.sleep(0.5)
            #下单前确认 0x0为已经选取,各系统演示不一样,目的:取消选取
            if hk.get_color(self.num_arr['queren'])==self.cg.GOU_COLOR:
                hk.mouse_click(self.num_arr['queren'])
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
            if(hk.get_color(self.num_arr['open_qr_zb'])==self.num_arr['open_qr_color']):
                is_jc=True
                break
        if is_jc:
            #设置平仓点差 判断点差处是否打钩
            if(hk.get_color(self.num_arr['p_dc_zb'])!=self.cg.GOU_COLOR):
                hk.mouse_click(self.num_arr['p_dc_zb'])
            return True
        else:
            return False
        
    #判断平仓,建仓是否成功 最多4秒时间
    def judge_cang(self,state):
        #判断确认按钮是否点击
        is_dj=False
        for i in range(30):
            #确认按钮 最多2秒
            qr_color=hk.get_color(self.num_arr['jpc_qr_zb'])
            if qr_color!=self.num_arr['open_qr_color']:
                #点击弹窗的确认
                if state==1:
                    hk.mouse_click(self.num_arr['submit'])
                elif state==2:
                    hk.mouse_click(self.num_arr['pc_tj'])
                is_dj=True
                break
        #已经点击弹窗
        if is_dj:
            pd_num=0
            for i in range(3):
                time.sleep(0.1)
                qr_color=hk.get_color(self.num_arr['open_qr_zb'])
                #判断是提交成功 还是提交失败返回
                if qr_color!=self.num_arr['open_qr_color']:
                    #提交成功
                    return True
                else:
                    pd_num+=1
                    if pd_num>=2:
                        #点位影响提交 需要再次提交
                        return False
        else:
            #点击弹窗失败 或者弹窗等待中
            return False
        
    #执行建仓操作
    def jianc(self):
        #点击提交 建仓
        k=time.time()
        hk.mouse_click(self.num_arr['submit'])
        #判断是否建立成功
        if self.judge_cang(1):
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
        if self.judge_cang(2):
            return True
        else:
            #平仓失败,原因:点位偏差太大
            return False
    
    #多,空选择 num=[1,2] 1->多 2->空
    def jianc_dk(self,num):
        if num==1:
            hk.mouse_click(self.num_arr['dk_zb'])
        elif num==2:
            #多空坐标相距72像素
            dk_zb=[self.num_arr['dk_zb'][0]+72,self.num_arr['dk_zb'][1]]
            hk.mouse_click(dk_zb)
    #设置点差
    def set_diancha(self,num):
        #保存系统点差
        self.dc_num=num
        #设置点差
        hk.mouse_dbclick(self.num_arr['dc_zb'])
        hk.keyset(str(num))
