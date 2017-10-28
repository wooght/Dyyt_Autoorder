'''
    白银数据分析
    内,外差分析
    做单操作
    逻辑分析
    by wooght 2014.07.25
'''
import threading
from threading import Timer
import time
import sys
import math
from socket import *
from model_number import *
from save_data import save_run_num
from save_data import save_data_sql as ssql
from save_data import config
from control import *

sys.setrecursionlimit(1000000) #设置递归深度为一百万
#是否开始
is_start=False
#开启线程
t=[]
'''
    数据分析及操作主体 实现类
    打开建仓,数据判断,建仓
    打开平仓,数据判断,平仓
'''
class fx_to_run:
    in_old_num=0#上一次in
    out_old_num=0#上一次out
    out_old_num_fuzu=0#上一次辅助out
    is_jc=False#是否已经建仓
    gao_di=False#做高还是做地 默认低
    ps_fn=False#默认做平时
    regis_state=False#注册状态
    jc_num=0#建仓次数
    is_continue_pc=True#当平仓事件达到设定值时,判断是否人为暂停
    dc_num=3#默认点差
    cg=object#配置
    w_c=object#动作控制
    to_server=False#服务器连接状态
    out_number_false=False#out数据是否出错
    in_number_false=False#in数据是否出错
    get_out_obj=object
    get_in_obj=object
    get_outfu_obj=object
    fuzu=False#是否辅助
    run_index=True#主判断是否开启
    fuzu_state=False#辅助状态
    qw_type=0#期望目标 1多 2空
    pc_time=0#平仓等待最长时间
    set_jc_num=1#设置建仓次数
    in_lx_num=0#内部数据连续相同次数
    in_lx_maxnum=0#内部数据连续相同最大次数
    is_start=False#开始标记
    now_money=0#当前金额
    last_innum=0#上一次成功建仓内部数据
    RADIO_NUM=0#系数
    RADIO_NUM_FUZU=0#辅助系数
    fuzu_bw_num=0#辅助本位
    zhu_bw_num=0#主本位
    #构造函数
    def __init__(self,xy1,xy2,num_arr):
        self.cg=config.wooght_data()
        self.in_zb=xy1
        self.out_zb=xy2
        self.get_out_obj=w_mt4.number(self.out_zb[0],self.out_zb[1])
        if len(self.out_zb)==4:
            self.fuzu=True
            self.get_outfu_obj=w_mt4.number(self.out_zb[2],self.out_zb[3])
        self.run_cs(num_arr)
        self.num_arr=num_arr
        self.about_num=self.cg.ABOUT_NUM
        self.name_id=self.cg.NAME_ID
        self.tk_good=self.cg.TK_GOOD
        self.zidong_pc=self.cg.ZIDONG_PC
        self.zidong_jc=self.cg.ZIDONG_JC
        self.pc_time=int(self.cg.PC_TIME/0.2)
        self.in_lx_maxnum=int(self.cg.IN_LX_TIME*(1/(len(self.cg.READ_OUT_NUM)*0.09)))
        self.RADIO_NUM=float(self.num_arr['zhu_xs'])
        self.RADIO_NUM_FUZU=float(self.num_arr['fu_xs'])
        if self.num_arr['qw_state']:
            self.qw_number=self.num_arr['qw_number']
            in_num=self.get_in()
            if in_num>self.qw_number:
                self.qw_type=1
            else:
                self.qw_type=2
            print(self.qw_type)

    #外部运行参数设置
    def run_cs(self,num_arr):
        #dyyt
        if self.cg.SILVER_BM=='dyyt':
            self.w_c=c_dyyt.wooght_control(num_arr)
            self.get_in_obj=w_dyyt.number(self.in_zb[0],self.in_zb[1])
        #xbyy
        elif self.cg.SILVER_BM=='xbyy':
            self.w_c=c_xbyy.wooght_control(num_arr)
            self.get_in_obj=w_xbyy.number(self.in_zb[0],self.in_zb[1])
        #dby
        elif self.cg.SILVER_BM=='dby':
            self.w_c=c_dby.wooght_control(num_arr)
            self.get_in_obj=w_dby.number(self.in_zb[0],self.in_zb[1])            
            
    
    ###运行接口
    #运行开始
    def run(self):
        #判断是否已经打开建仓单
        if not self.is_jc:
        #做单次数判断 如果第三次 等待给定时间
            if self.jc_num>1:
                if self.jc_num%2==0:
                    time.sleep(self.cg.THREE_TIME)
                    #重新获取外盘旧数据
                    self.set_out_old(self.get_out())
            #判断是否已经做期望单
            if self.num_arr['qw_state']=='ready1':
                self.qw_to_pc(self.qw_number,1)
                return
            elif self.num_arr['qw_state']=='ready2':
                self.qw_to_pc(self.qw_number,2)
                return
            else:
                #如果暂停 则返回
                if not self.is_start:
                    return
                #获取总金额数
                if self.now_money==0:
                    in_num=self.get_in()
                    self.now_money=math.floor(int(self.num_arr['shou'])*in_num*self.cg.BZJBL)
                    print("bzj:",self.now_money)
                if self.w_c.open_jianc():
                    self.is_jc=True
                else:
                    self.error('打开建仓失败,\n4秒后重新打开')
                    time.sleep(4)
                    return
        #获取in数据
        in_num=self.get_in()
        #连续判断N次外盘数据
        for i in self.cg.READ_OUT_NUM:
            out_num=self.get_out()
            #如果数据出错 不运行
            if not out_num or not in_num:
                return
            #in和out数据差异 判断是否空或多 满足最低值判断进入
            cha=abs(in_num-out_num)
            self.bw_control(in_num,out_num)#本位计算
            #判断主判断是否开启
            if not self.run_index:
                cha=-1
            #以常规最低差判断进入做单程序
            if cha>=self.about_num[0][3]:
                self.pdjc(in_num,out_num)
                self.fuzu=False#关闭辅助
                break
            else:
                self.out_old_num=out_num
                self.in_old_num=in_num
                #条件不满足,辅助再次获取与判断
                if self.fuzu:
                    #辅助状态
                    self.fuzu_state=True
                    self.about_num=self.cg.ABOUT_NUM_FUZU#辅助参数
                    out_num_fuzu=self.get_out()
                    if not out_num_fuzu:
                        self.fuzu_state=False
                        self.about_num=self.cg.ABOUT_NUM#还原主参数
                        continue
                    fuzu_cha=abs(in_num-out_num_fuzu)
                    self.bw_control(in_num,out_num_fuzu)#本位计算
                    if fuzu_cha>=self.about_num[0][3]:
                        self.pdjc(in_num,out_num_fuzu)
                        #关闭主判断
                        self.run_index=False
                        self.fuzu_state=False
                        break
                    else:
                        #辅助数据不满足 记录
                        self.set_out_old(out_num_fuzu)
                    #整个辅助过程判断完毕 关闭辅助状态
                    self.fuzu_state=False
                    self.about_num=self.cg.ABOUT_NUM#还原主参数
        if self.fuzu:
            if not self.run_index:
                self.error('o2:'+str(self.out_old_num_fuzu)+'['+str(self.out_old_num_fuzu-in_num)+']\nin:'+str(in_num))
            else:
                self.error('o1:'+str(out_num)+'['+str(out_num-in_num)+']\no2:'+str(self.out_old_num_fuzu)+'['+str(self.out_old_num_fuzu-in_num)+']\nin:'+str(in_num))
        else:
            self.error('o1:'+str(out_num)+'['+str(out_num-in_num)+']\nin:'+str(in_num))

    #获取内外差__根据做单方向判断
    def get_newcha(self,ctype,inum,onum):
        if ctype==1:
            rcha=onum-inum
        else:
            rcha=inum-onum
        return rcha

    #*******************************************************************************************************************************************************************
    #本位控制
    #本位计算
    def bw_control(self,in_num,out_num):
        if self.fuzu_state:
            if(abs(in_num-out_num)>=self.cg.BW_NUM):
                self.fuzu_bw_num+=1
            else:
                self.fuzu_bw_num=0
        else:
            if(abs(in_num-out_num)>=self.cg.BW_NUM):
                self.zhu_bw_num+=1
            else:
                self.zhu_bw_num=0
    #本位判断
    def bw_panduan(self):
        bw_time=0
        if self.fuzu_state:
            bw_time=self.fuzu_bw_num
        else:
            bw_time=self.zhu_bw_num
        if bw_time>=self.cg.BW_TIME:
            return True
        else:
            self.fuzu_bw_num=0
            self.zhu_bw_num=0
            return False          
            
        
    #建立判断,动作判断
    #数据再判断
    def pdjc(self,in_num,out_num):
        #如果暂停 不进行操作
        if not self.is_start:
            return
        #多空判断 前后两次一样才确定做单1多 2空
        if in_num>out_num:
            c_type=2
        elif out_num>in_num:
            c_type=1
        else:
            return
        #如果满足出本位时间 返回
        if self.bw_panduan():
            self.error('出本位')
            return
        #再一次获取out和in数据 判断是否继续满足条件
        #也等待out数据继续走动,达到更高的点位的可能
        new_in_num=self.get_in()
        new_out_num=self.get_out()
        #第二次判断 需与第一次判断相一致 不一致则返回 继续下次判断
        new_cha=self.get_newcha(c_type,new_in_num,new_out_num)
        if new_cha<self.about_num[0][3]:
            return
        #判断 外有相应的浮动才做
        out_cha=new_out_num-self.get_out_old()
        if c_type==2:
            out_cha=-out_cha
        if out_cha>self.cg.OUT_FLOAT:
            new_cha=abs(new_in_num-new_out_num)
            #保存做单前最新数据,后续判断使用
            self.set_out_old(new_out_num)
            self.in_old_num=new_in_num
            ###
            #判断顺序 先判断是否非农 不是就执行平时的判断
            #做非农 高
            if(new_cha>=self.about_num[1][4]):
                #调用做单
                self.gao_di=True
                self.jctopc(1,4,c_type)
            #做非农 低
            elif new_cha>=self.about_num[1][3]:
                self.gao_di=False
                self.jctopc(1,3,c_type)
            #做平时 高
            elif new_cha>=self.about_num[0][4]:
                self.gao_di=True
                self.jctopc(0,4,c_type)
            #做平时 低
            elif new_cha>=self.about_num[0][3]:
                #在非农的情况下 第一次进仓 低位数据再判断一次
                if self.cg.FEINONG and self.jc_num==0:
                    new_in_num=self.get_in()
                    new_out_num=self.get_out()
                    now_cha=self.get_newcha(c_type,new_in_num,new_out_num)
                    if now_cha<self.about_num[0][3]:
                        #当第三次判断与前两次不一样的时候,怀疑是外盘突然回去的情况 不做单
                        save_run_num.save_txt('in:'+in_num+' out:'+out_num+',最后一次判断不一致')
                        return
                self.gao_di=False
                self.jctopc(0,3,c_type)
            else:
                #out in无差异 不做 及in已经跟随out了
                self.error('跟得太紧')
                return
        else:
            print('in:',in_num,' out:',out_num,'不满足out浮动')
            self.error('不满足out浮动')

    ###
    #建立开始,动作开始
    #建仓及后续平仓判断
    def jctopc(self,about_key,key_num,c_type):
        #设置多空
        self.w_c.jianc_dk(c_type)
        #第一次建仓的时候才设置,偏差
        if self.set_jc_num==1:            
            #设置建仓偏差,只有在大于设置的偏差的时候才重新设定偏差
            if self.about_num[about_key][key_num-2]>int(self.num_arr['dc']):
                self.w_c.set_diancha(self.about_num[about_key][key_num-2])
        if not self.zidong_jc:
            self.error('等待人为\n建仓,平仓')
            self.zt()
            return
        #数据出错,停止当前活动
        if self.in_number_false or self.out_number_false:
            return
        #建仓成功,做平仓判断
        if self.jianc():
            self.error("建仓成功\n判断平仓中...")
            #判断数据 准备平仓 隔0.2秒
            result_num=self.about_num[about_key][key_num]#条件临界值/初始判断值
            result_pc=self.about_num[about_key][key_num-2]#条件对应偏差
            ddnum_1=0#低高成本徘徊周期次数
            ddnum_2=0#外盘满足 内盘大于最小偏差
            back_min_cost_num=0#回到低于最低成本周期次数
            tk_di=0#考虑低仓位次数
            max_cost_num=0#满足高成本周期次数
            tk_di_pc=0#最低偏差范围周期次数
            
            #开始平仓判断,一个判断周期大楷0.2秒
            for i in range(self.pc_time):
                #平仓等待超时
                if i==self.pc_time-1:
                    self.gao_di=False
                    #没暂停就平仓
                    if self.is_continue_pc:
                        if self.pingc(in_num):
                            #结束本次交易
                            break
                        else:
                            #平仓失败 继续判断
                            self.zt_error('平仓失败\n等待人为平仓')
                            self.zt()
                    else:
                        self.zt_error('未达到平仓条件\n等待人为平仓')
                        self.zt()
                        
                #获取新的内部数据
                in_num=self.get_in()
                #获取新的外部数据
                out_num=self.get_out()
                if c_type==1:
                    #多单
                    in_cha=in_num-self.in_old_num
                    out_cha=out_num-self.get_out_old()
                    inout_cha=out_num-in_num
                    out_oldin_cha=out_num-self.in_old_num
                elif c_type==2:
                    #空单
                    in_cha=self.in_old_num-in_num
                    out_cha=self.get_out_old()-out_num
                    inout_cha=in_num-out_num
                    out_oldin_cha=self.in_old_num-out_num

                ###数据分析,条件判断开始
                #达到设定点位,视情况考虑立即平仓
                if in_cha>=result_num:
                    #考虑高收益
                    if self.tk_good:
                        if inout_cha>self.cg.TK_GOOD_FLOAT:
                            continue
                        else:
                            if self.pingc(in_num):
                                self.gao_di=False
                                break
                            else:
                                continue
                    else:
                        #不考虑高收益 立即平仓
                        if self.pingc(in_num):
                            self.gao_di=False
                            break
                        else:
                            continue
                #达到止损点位,立即平仓
                elif in_cha<=-self.cg.LOSS_NUM:
                    if self.pingc(in_num):
                        self.gao_di=False
                        break
                    else:
                        continue
                #未达到设定盈利点位和止损点位
                else:
                    #如果外盘满足条件 视具体情况等待or平仓
                    if out_oldin_cha>=result_num:
                        #内盘大于最小偏差范围 等待5个周期
                        if in_cha>result_num-result_pc:
                            if ddnum_2<5:
                                ddnum_2+=1
                            else:
                                #当外盘仍然大于内盘超过偏差范围时 继续等待
                                if inout_cha>self.about_num[about_key][key_num-2]:
                                    continue
                                else:
                                    if self.pingc(in_num):
                                        self.gao_di=False
                                        break
                                    else:
                                        continue
                        else:
                            continue
                    #外盘反向走动超过设定点 立即止损
                    elif out_oldin_cha<=-self.cg.LOSS_OUT_NUM:
                        if self.pingc(in_num):
                            self.gao_di=False
                            break
                        else:
                            continue
                    #外盘不满足条件但不满足立即平仓 做降低盈利或者做亏损处理
                    else:
                        #徘徊在最低成本和最高成本之间达到10个周期,考虑平仓止损
                        if in_cha>=self.about_num[0][0] and in_cha<self.about_num[1][0]:
                            #设置回到成本次数为0
                            back_min_cost_num=0
                            if ddnum_1<10:
                                ddnum_1+=1
                            else:
                                #当外盘仍然大于内盘超过偏差范围时 继续等待
                                if inout_cha>self.about_num[about_key][key_num-2]:
                                    continue
                                else:
                                    #当外盘高于最小等待值时 等待
                                    if inout_cha>self.cg.TK_WRITE_FLOAT:
                                        continue
                                    else:
                                        if self.pingc(in_num):
                                            self.gao_di=False
                                            break
                                        else:
                                            continue
                        #没有继续增长而是回到最低成本以下的时候 考虑5个周期止损
                        elif in_cha<self.about_num[0][0]:
                            if back_min_cost_num<5:
                                back_min_cost_num+=1
                            else:
                                #当外盘仍然大于内盘超过偏差范围时 继续等待
                                if inout_cha>self.about_num[about_key][key_num-2]:
                                    continue
                                else:
                                    #当外盘高于最小等待值时 等待
                                    if inout_cha>self.cg.TK_WRITE_FLOAT:
                                        continue
                                    else:
                                        if self.pingc(in_num):
                                            self.gao_di=False
                                            break
                                        else:
                                            continue
                        #在没达到任何止损的条件下 考虑降低盈利
                        else:
                            #内盘大于最小偏差范围 外盘从满足条件到不满足条件的情况 立即平仓
                            if in_cha>result_num-result_pc:
                                if ddnum_2>0:
                                    if self.pingc(in_num):
                                        self.gao_di=False
                                        break

                            #高点位位进仓时,考虑低仓位是否满足
                            if self.gao_di:
                                #满足低仓位 等待5个周期
                                if in_cha>self.about_num[about_key][key_num-1]:
                                    if tk_di<5:
                                        tk_di+=1
                                    else:
                                        #达到周期数 立即平仓
                                        if self.pingc(in_num):
                                            self.gao_di=False
                                            break
                                        else:
                                            continue
                                #不满足低仓位 但满足最高成本5个周期
                                elif in_cha>=self.about_num[1][0]:
                                    if max_cost_num<5:
                                        max_cost_num+=1
                                    else:
                                        #当外盘仍然大于内盘超过偏差范围时 继续等待
                                        if inout_cha>self.about_num[about_key][key_num-2]:
                                            continue
                                        else:
                                            if self.pingc(in_num):
                                                self.gao_di=False
                                                break
                                            else:
                                                continue
                            #低点位进仓时,考虑偏差范围最低是否满足
                            else:
                                #满足偏差范围最低点位 5个周期
                                if in_cha>result_num-result_pc:
                                    if tk_di_pc<5:
                                        tk_di_pc+=1
                                    else:
                                        if self.pingc(in_num):
                                            self.gao_di=False
                                            break
                                        else:
                                            continue
                                #不满足偏差最低点位 但满足最高成本5个周期
                                elif in_cha>=self.about_num[1][0]:
                                    if max_cost_num<5:
                                        max_cost_num+=1
                                    else:
                                        #当外盘仍然大于内盘超过偏差范围时 继续等待
                                        if inout_cha>self.about_num[about_key][key_num-2]:
                                            continue
                                        else:
                                            if self.pingc(in_num):
                                                self.gao_di=False
                                                break
                                            else:
                                                continue
                #平仓判断,一个周期休息0.2秒
                time.sleep(0.2)
            #重新设总金额
            self.z_shou(c_type)
            self.set_jc_num=1#单次做单简单次数
            self.jc_num+=1#成功做单次数
        else:
            #建仓失败
            #再一次判定条件 是否可以继续建仓
            if not self.is_start:
                return
            new_out_num=self.get_out()
            new_in_num=self.get_in()
            if c_type==1:
                inout_cha=new_out_num-new_in_num
            elif c_type==2:
                inout_cha=new_in_num-new_out_num
            if inout_cha>=self.about_num[about_key][key_num]:
                #第二次及以上建仓,不再设置多空及偏差
                #如果已经建立两次失败 暂停2秒 等待人为操作
                if self.set_jc_num==2:
                    time.sleep(2)
                self.set_jc_num=2
                #继续做 如果条件一直满足 直到成功建仓为止
                self.jctopc(about_key,key_num,c_type)
            else:
                save_run_num.save_txt('建仓失败:in_'+str(new_in_num)+'_out_'+str(new_out_num)+'\n')
                self.set_jc_num==1
                

    #设置old_out数据
    def set_out_old(self,out_num):
        if self.fuzu_state:
            self.out_old_num_fuzu=out_num
        else:
            self.out_old_num=out_num
    #获取old_out数据
    def get_out_old(self):
        if self.fuzu_state:
            return self.out_old_num_fuzu
        else:
            return self.out_old_num
        
    #获取out数据
    def get_out(self):
        if self.fuzu_state:
            out_num=self.get_outfu_obj.get_number()
        else:
            out_num=self.get_out_obj.get_number()
        if out_num:
            if self.fuzu_state:
                radio_num=self.RADIO_NUM_FUZU
            else:
                radio_num=self.RADIO_NUM
            now_num=int(int(out_num)*radio_num/1000)
            if self.get_out_old()==0:
                self.set_out_old(now_num)
            old_num=self.get_out_old()
            if old_num==0:
                print(now_num,'--')
                return False
            #数据变化超过120 视为不正常
            elif abs(now_num-old_num)>120:
                self.out_number_false=True
                return old_num
            else:
                self.out_number_false=False
                return now_num
        else:
            self.error('out数据出错')
            self.out_number_false=True
            #数据出错 返回之前的正确数据
            if self.out_old_num==0:
                return False
            else:
                return self.get_out_old()
    #获取in数据
    def get_in(self):
        in_num=self.get_in_obj.get_number()
        if in_num:
            if self.in_old_num==0:
                self.in_old_num=int(in_num)
            #相同
            if self.in_old_num==int(in_num):
                self.in_lx_num+=1
            #变化
            else:
                self.in_lx_num=1
            #连续相同次数判断
            if self.in_lx_num>self.in_lx_maxnum:
                self.in_number_false=True
                self.error('内部掉线'+str(self.cg.IN_LX_TIME)+'秒\n或者卡住')
                time.sleep(1)
                return int(in_num)
            #处于变化状态
            else:
                self.in_number_false=False
                return int(in_num)
        else:
            self.error('in数据出错')
            self.in_number_false=True
            #数据出错 返回之前正确的数据
            if self.in_old_num==0:
                return False
            else:
                return self.in_old_num
    '''
        动作-->建仓,平仓,验证
    '''
    #执行建仓操作
    def jianc(self):
        #点击提交 建仓
        #判断是否建立成功
        if self.w_c.jianc():
            #保存建仓时内部数据 后续判断使用
            self.in_old_num=self.get_in()
            if self.w_c.open_pingc():
                #建立平仓成功
                return True
            else:
                while is_start:
                    #再一次建立平仓
                    #打开平仓失败 一直继续打开 每两次停顿4秒
                    if self.w_c.open_pingc():
                        return True
                    else:
                        self.zt_error('打开平仓失败\n尝试继续打开')
                        time.sleep(4)#两次共6秒打开失败后留取时间给人为操作
        else:
            #建仓失败
            #self.zt_error('建仓失败')
            return False

    #执行平仓操作
    def pingc(self,in_num):
        if not self.zidong_pc:
            self.zt_error('等待人为平仓')
            self.zt()
            return True
        #点击平仓
        #判定是否平仓
        if self.w_c.pingc():
            self.error('平仓成功')
            #记录数据
            save_str='建:IN_'+str(self.in_old_num)+' OUT_'+str(self.get_out_old())
            save_str+=' 平:'+str(in_num)+'\n'
            save_run_num.save_txt(save_str)
            #ssql.save_jl(self.in_old_num,self.get_out_old(),in_num,self.name_id)
            #保存最新的数据,以便于后续继续判断
            self.last_innum=self.in_old_num
            self.in_old_num=in_num
            self.set_out_old(self.get_out())
            #准备下次建仓
            self.is_jc=False
            #关闭期望
            self.num_arr['qw_state']='OFF'
            self.zt_error("平仓成功\n运行中...")
            return True
        else:
            #平仓失败,原因:点位偏差太大
            return False

    #总金额退出总手数
    def z_shou(self,c_type):
        before_money=self.now_money
        cha=self.in_old_num-self.last_innum
        if c_type==2:
            cha=-cha
        run_money=(cha-self.about_num[1][0])*int(self.num_arr['shou'])
        self.now_money=before_money+run_money
        shou=math.floor(self.now_money/(self.in_old_num*self.cg.BZJBL))
        #重新设置手数
        if shou<int(self.num_arr['shou']):
            #当亏钱的情况下,计算好手数后再减一,以免有手数差异导致建仓失败
            self.num_arr['shou']=str(shou-1)
        elif shou>int(self.num_arr['shou']):
            if self.cg.TO_HEIGHT:
                if shou<self.cg.HEIGHT_SHOU:
                    self.num_arr['shou']=str(shou)
                else:
                    self.num_arr['shou']=str(self.cg.HEIGHT_SHOU)
        self.run_cs(self.num_arr)
        
    #人为控制平仓
    def people_control_pc(self):
        self.zidong_pc=True
        in_num=self.get_in()
        if self.pingc(in_num):
            return True
        else:
            return False

    #普通错误,输出
    def error(self,instr):
        self.num_arr['display_yz'].set(instr)
    #状态输出
    def zt_error(self,instr):
        self.num_arr['display_zt'].set(instr)
    
    #初始数字验证验证
    def num_yz(self):
        return_result=True
        in_num=self.get_in()
        out_num=self.get_out()
        strr=""
        if not out_num:
            strr+="out:error"
            return_result=False
        else:
            strr+="out:"+str(out_num)
            if abs(in_num-out_num)>3:
                return_result=False
                strr+='(X)'
        if self.fuzu:
            #辅助状态
            self.fuzu_state=True
            fuzu_num=self.get_out()
            self.fuzu_state=False
            if not fuzu_num:
                strr+="\n out_fu:error";
                return_result=False
            else:
                strr+="\n out:fu:"+str(fuzu_num);
                if abs(in_num-fuzu_num)>3:
                    return_result=False
                    strr+='(X)'
        if not in_num:
            strr+="\n in:error"
        else:
            strr+="\n in:"+str(in_num)
        self.error(strr)
        return return_result

    #验证打开 值针对模拟盘
    def open_yz(self):
        if self.w_c.open_jianc():
            #设置空单
            self.w_c.jianc_dk(2)
            #再设置多单
            time.sleep(2)
            self.w_c.jianc_dk(1)
            if self.w_c.jianc():
                if self.w_c.open_pingc():
                    #模拟验证中 平仓暂停5秒
                    time.sleep(4)
                    if self.w_c.pingc():
                        self.error('平仓成功')
                    else:
                        self.error('平仓失败')
                else:
                    self.error('打开平仓失败')
            else:
                self.error('建仓失败')
        else:
            self.error('打开失败')
    #远程验证
    def registration(self):
        if ssql.registration(self.name_id):
            self.regis_state=True
            return True
        else:
            self.regis_state=False
            return False

    #内部暂停
    def zt(self):
        is_start=False
    '''
        分析,操作主体 类声明结束
    '''
        

'''
    分析,操作主体运行控制
    多线程控制
'''
wooght=object
class ThreadClass(threading.Thread):
    def run(self):
        global is_start
        #分析判断循环中 分析之间无时间停顿
        while is_start:
            #s=time.time()
            wooght.run()
            #z=time.time()
            #print(z-s)
    def fx_stop(self):
        global is_start
        self.thread_stop=True
        
#本地控制
def set_start():
    global is_start
    #开始运行 到时平仓开启
    wooght.is_continue_pc=wooght.cg.CONTINUE_PC
    wooght.zidong_jc=wooght.cg.ZIDONG_JC
    wooght.zidong_pc=wooght.cg.ZIDONG_PC
    wooght.is_start=True
    if not is_start:
        is_start=True
        t.append(ThreadClass())
        t[-1].start()
#停止线程
def stop_thread():
    global is_start
    is_start=False

    
def set_stop():
    #del t[i]
    wooght.zidong_jc=False
    wooght.zidong_pc=False
    wooght.error('暂停中...')
    wooght.is_start=False
    #暂停运行 会暂停到时平仓
    wooght.is_continue_pc=False
