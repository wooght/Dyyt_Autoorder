'''
    白银数据分析
    操作界面
    数据界面
    展示界面
    by wooght 2014.07.25
'''
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from ctypes import *
import win32api
import win32con
import win32gui
import os
import pickle
import wmodel as run
import threading
from threading import Timer
from socket import *
from save_data import config as cg
fm =Tk()
fm.title(cg.wooght_data.SILVER_NAME)
#fm.minsize(cg.wooght_data.BOX_XY[0],cg.wooght_data.BOX_XY[1])
#fm.maxsize(cg.wooght_data.BOX_XY[0],cg.wooght_data.BOX_XY[2])
#默认大小
fm.geometry(str(cg.wooght_data.BOX_XY[0])+"x"+str(cg.wooght_data.BOX_XY[1]))
#禁止手动改变窗口大小
fm.resizable(False,False)


#获取颜色 判断是否打开
uwin=windll.user32
#获取句柄
hdc = uwin.GetDC(None)
def get_color():
    zb_str=js_is_zb_entry.get()
    zb=zb_str.split(',')
    #获取指定像素的颜色
    color = windll.gdi32.GetPixel(hdc,int(zb[0]),int(zb[1]))
    display.set(str(hex(color)))
def get_pc_color():
    zb_str=pc_zb_entry.get()
    zb=get_zb(zb_str)
    color=windll.gdi32.GetPixel(hdc,int(zb[0]),int(zb[1]))
    pc_pd_rgb_display.set(str(hex(color)))

'''
    验证程序
    依次获取数据
    存放数组中
'''
#xy1 in数据
#xy2 out数据
xy1=[]
xy2=[]

#获取数据坐标
def get_num_zb():
    #获取数据
    global xy1,xy2
    innum=in_entry.get()
    xy1=get_zb(innum)
    outnum=out_entry.get()
    xy2=get_zb(outnum)
#获取数据坐标外的数据
#num_arr 表单数据
num_arr={}
#pickle_num 需要序列化的数据
pickle_num={}
#pick_name 保存序列化文件名
pick_name='save_data/'+cg.wooght_data.SILVER_BM+'.wooght'
#主窗口显示设置驱动变量
display_yz=StringVar()
display_zt=StringVar()

#获取数据
def get_num():
    global num_arr
    #建立按钮
    open_zb_a=jl_button_entry.get()
    str_zb=open_zb_a.split(',')
    open_zb=[int(str_zb[0]),int(str_zb[1])]
    #建立确认
    open_qr_a=js_is_zb_entry.get()
    open_qr_zb=open_qr_a.split(',')
    open_qr_color=js_is_ys_entry.get()
    #多空
    dk_zb_a=dk_entry.get()
    dk_zb_b=dk_zb_a.split(',')
    dk_zb=[int(dk_zb_b[0]),int(dk_zb_b[1])]
    #手
    shou=jl_shou_entry.get()
    shou_zb=get_zb(jl_shou_zb.get())
    #下单前确认
    queren=get_zb(xd_qian_entry.get())
    #提交按钮
    submit=get_zb(xd_ok_entry.get())
    #点差
    dc_zb=get_zb(dc_zb_entry.get())
    #平仓点差
    p_dc_zb=get_zb(dc_pc_zb_entry.get())
    #商品
    sp_zb=get_zb(sp_entry.get())
    #千克
    qk=int(qk_entry.get())
    #平仓坐标
    pc_zb=get_zb(pc_zb_entry.get())
    #平仓颜色
    pc_rgb=pc_pd_rgb.get()
    #平仓提交
    pc_tj=get_zb(pc_tj_entry.get())
    #建立,平 确认
    jl_pc_qr_zb=get_zb(jl_pc_qr.get())
    #期望考虑
    qw_selected=qw_combobox.get()
    if qw_selected=='ON':
        qw_number=int(qw_entry.get())
        qw_state='ON'
    elif qw_selected=='ready1' or qw_selected=='ready2':
        qw_number=int(qw_entry.get())
        qw_state=qw_selected
    else:
        qw_number=0
        qw_state=False
    #系数
    zhu_xs=xs_zhu_entry.get()
    fu_xs=xs_fu_entry.get()
    #运行参数
    num_arr={'open_zb':open_zb,'open_qr_zb':open_qr_zb,'open_qr_color':open_qr_color,
             'display_yz':display_yz,'display_zt':display_zt,'dk_zb':dk_zb,'shou':shou,'shou_zb':shou_zb,
             'queren':queren,'submit':submit,'dc_zb':dc_zb,'p_dc_zb':p_dc_zb,'dc':dc_entry.get(),
             'sp_zb':sp_zb,'qk':qk,'pc_tj':pc_tj,'pc_zb':pc_zb,'pc_rgb':pc_rgb,'jl_pc':jl_pc_qr_zb,
             'qw_state':qw_state,'qw_number':qw_number,'zhu_xs':zhu_xs,'fu_xs':fu_xs}
    #序列化参数
    global pickle_num
    pickle_num={'jl_button_entry':jl_button_entry.get(),'js_is_zb_entry':js_is_zb_entry.get(),
                'js_is_ys_entry':js_is_ys_entry.get(),'dk_entry':dk_entry.get(),'jl_shou_entry':jl_shou_entry.get(),
                'jl_shou_zb':jl_shou_zb.get(),'xd_qian_entry':xd_qian_entry.get(),'xd_ok_entry':xd_ok_entry.get(),
                'dc_zb_entry':dc_zb_entry.get(),'p_dc_zb':dc_pc_zb_entry.get(),'dc':dc_entry.get(),'sp_entry':sp_entry.get(),
                'qk_entry':qk_entry.get(),'pc_zb_entry':pc_zb_entry.get(),'pc_pd_rgb':pc_pd_rgb.get(),
                'pc_tj_entry':pc_tj_entry.get(),'jl_pc_qr':jl_pc_qr.get(),'in_entry':in_entry.get(),'out_entry':out_entry.get(),
                'xs_zhu_entry':xs_zhu_entry.get(),'xs_fu_entry':xs_fu_entry.get()}

cg_data=cg.wooght_data()
#服务器控制
class server_constrol():
    server_connect=False
    def __init__(self):
        #注册
        self.sockobj=socket(AF_INET,SOCK_STREAM)
    def CnectToServer(self,display_view):
        try:
            self.sockobj.connect((cg_data.SERVER_HOST,8001))
            self.server_connect=True
        except ConnectionRefusedError:
            self.server_connect=False
            display_view.set('服务器未连接')
        if self.server_connect:
            self.SendToServer(1010)
            return True
        else:
            return False
    def receive_server(self):
        while True:
            if not self.server_connect:
                break
            try:
                d=self.sockobj.recv(64)
            except ConnectionResetError:
                break
            if int(d)==1111:
                #开始
                set_start()
                self.SendToServer(1111)
            elif int(d)==2222:
                #暂停
                run.set_stop()
                self.SendToServer(2222)
            elif int(d)==3333:
                #平仓
                if run.wooght.people_control_pc():
                    self.SendToServer(3333)
                else:
                    self.SendToServer(-3333)
    def SendToServer(self,num):
        self.sockobj.send(str(num).encode())
#实例化服务器控制
sv_ctrl=server_constrol()
#接收信息线程开启
class ThreadSocket(threading.Thread):
    def run(self):
        sv_ctrl.receive_server()
if sv_ctrl.CnectToServer(display_yz):
    s=ThreadSocket()
    s.start()

is_yz=False
#验证数据坐标
def num_yz():
    global is_yz
    try:
        get_num()
        get_num_zb()
    except ValueError or TypeError:
        display_yz.set('数据填写不完整')
        return
    if not is_yz:
        is_yz=True
    run.is_start=False
    run.wooght=run.fx_to_run(xy1,xy2,num_arr)
    display_zt.set('数据如右:')
    return run.wooght.num_yz()
#开始
def set_start():
    global is_yz
    if not is_yz:
        root_jg('数据尚未验证,请验证')
        return
    if not run.wooght.registration():
            display_yz.set('注册失败!')
    else:
        save_pick()
        if not num_yz():
            root_jg('内外数据差异太大,开始失败!')
        else:
            if ask_result('请确认数据确认框中数据是否正常?\n如不正常,请点击取消'):
                is_yz=False
                display_zt.set('运行中...')
                run.set_start()
#暂停
def set_stop():
    display_zt.set('暂停中...')
    run.set_stop()
#验证
def yz():
    try:
        get_num()
        get_num_zb()
    except ValueError or TypeError:
        display_yz.set('数据填写不完整')
        return
    num_arr['shou']='1'#将手数设置为1
    wooght_yz=run.fx_to_run(xy1,xy2,num_arr)
    #验证
    wooght_yz.registration()
    if ask_result('请确认是模拟盘?'):
        wooght_yz.open_yz()

#提取坐标 返回整数数组
def get_zb(zb_str):
    zb=zb_str.split(',')
    #当传入三个坐标时 返回三个坐标
    if len(zb)==4:
        return [int(zb[0]),int(zb[1]),int(zb[2]),int(zb[3])]
    return [int(zb[0]),int(zb[1])]

#执行保存序列化数据
def save_pick():
    with open(pick_name,'wb') as f:
        pickle.dump(pickle_num,f)

#当前窗口状态1为默认 2为最大
now_size_state=1
#设置窗口尺寸
def setfmsize():
    global now_size_state
    if now_size_state==1:
        fm.geometry(str(cg.wooght_data.BOX_XY[0])+"x"+str(cg.wooght_data.BOX_XY[2]))
        now_size_state=2
    elif now_size_state==2:
        fm.geometry(str(cg.wooght_data.BOX_XY[0])+"x"+str(cg.wooght_data.BOX_XY[1]))
        now_size_state=1

#弹窗警告
def root_jg(s):
    showinfo('警告',s)
#询问结果
def ask_result(s):
    ask= askokcancel('Ask',s)
    if ask:
        return True
    else:
        return False

#数据获取坐标
num_label=Label(fm,text='数据坐标,要求精确到1像素',width=45,bg="#FF9999")
num_label.grid(row=0,column=0,columnspan=8,sticky="NW")

#数据坐标文字提醒
num_in_label=Label(fm,text='IN:')
num_in_label.grid(row=1,column=0)
num_out_label=Label(fm,text='OUT:')
num_out_label.grid(row=1,column=2)

#数据坐标输入框
in_entry=Entry(fm,width=9)
in_entry.grid(row=1,column=1)
out_entry=Entry(fm,width=9)
out_entry.grid(row=1,column=3)
#验证
num_inout_yz=Button(fm,width=5,text='验证',comman=num_yz)
num_inout_yz.grid(row=1,column=4)

#建立文字提醒
jl=Label(fm,text='建平打开坐标',width=45,bg="#FF9999")
jl.grid(row=3,column=0,columnspan=5,sticky='NW')
#建单
jl_button=Label(fm,text='买口')
jl_button.grid(row=4,column=0)
jl_button_entry=Entry(fm,width=9)
jl_button_entry.grid(row=4,column=1)
#平单
pc_zb_label=Label(fm,text='卖口')
pc_zb_label.grid(row=4,column=2)
pc_zb_entry=Entry(fm,width=9)
pc_zb_entry.grid(row=4,column=3)
#显示参数按钮
cs_button=Button(fm,text="↓",comman=setfmsize)
cs_button.grid(row=4,column=4)

#系数设定
xs_label=Label(fm,text='系数')
xs_label.grid(row=5,column=0)
#主系数
xs_zhu_entry=Entry(fm,width=9)
xs_zhu_entry.grid(row=5,column=1)
#辅助系数
xs_fu_entry=Entry(fm,width=5)
xs_fu_entry.grid(row=5,column=2)

#控制按钮
###
#开始按钮
start_button=Button(fm,text='开始',width=5,bg="#FF6666",comman=set_start)
start_button.grid(row=5,column=3)
#暂停按钮
stop_button=Button(fm,text='暂停',width=5,bg="#66FF66",comman=set_stop)
stop_button.grid(row=5,column=4)

#运行显示
yz_label=Label(fm,borderwidth=4,height=3,anchor=SE,bg='white',width=14,relief='sunken',font = ("Arial, 16 bold"))
yz_label['textvariable']=display_yz
yz_label.grid(row=6,column=2,columnspan=4)
#状态显示
zt_label=Label(fm,borderwidth=4,height=3,anchor=SE,bg='white',width=10,relief='sunken',font = ("Arial, 16 bold"))
zt_label['textvariable']=display_zt
zt_label.grid(row=6,column=0,columnspan=2)

'''
    重要数据设置
    建立文字提醒
'''
jl=Label(fm,text='建立参数设置',bg="#FF9999")
jl.grid(row=7,column=0,columnspan=5,sticky='NW')
jl_shou=Label(fm,text='手数:')
jl_shou.grid(row=8,column=0)
jl_shou_entry=Entry(fm,width=3,textvariable='20')
jl_shou_entry.grid(row=8,column=2)
jl_shou_zb=Entry(fm,width=9)
jl_shou_zb.grid(row=8,column=1)
#验证按钮
jy_button=Button(fm,text="!**!",comman=yz)
jy_button.grid(row=8,column=4)

#建仓打开确认
jl_is_zb_label=Label(fm,text='坐标')
jl_is_zb_label.grid(row=9,column=0)
js_is_zb_entry=Entry(fm,width=9)
#js_is_zb_entry.insert(INSERT,'680,425')
js_is_zb_entry.grid(row=9,column=1)
js_is_ys_label=Label(fm,text='RGB')
js_is_ys_label.grid(row=9,column=2)

js_is_ys_entry=Entry(fm,width=9)
display=StringVar()
js_is_ys_entry['textvariable']=display
#js_is_ys_entry.insert(INSERT,'0xeecaae')
js_is_ys_entry.grid(row=9,column=3)
#获取颜色
get_ys_zb=Button(fm,text="获取",width=5,comman=get_color)
get_ys_zb.grid(row=9,column=4)


#多空选项
dk_label=Label(fm,text='多空,商品,以多为准',bg="#FF9999")
dk_label.grid(row=10,column=0,sticky='NW',columnspan=5)
dk_zb_label=Label(fm,text='坐标')
dk_zb_label.grid(row=11,column=0)
dk_entry=Entry(fm,width=9)
#dk_entry.insert(INSERT,'660,399')
dk_entry.grid(row=11,column=1)
#商品
sp_label=Label(fm,text='商品')
sp_label.grid(row=11,column=2)
sp_entry=Entry(fm,width=9)
#sp_entry.insert(INSERT,'800,266')
sp_entry.grid(row=11,column=3)
#千克
qk_entry=Entry(fm,width=3,textvariable='1')
qk_entry.grid(row=11,column=4)


#下单操作
xd=Label(fm,text='下单操作',bg="#FF9999")
xd.grid(row=12,column=0,columnspan=5,sticky="NW")
#下单前确认
xd_qian_label=Label(fm,text='确认')
xd_qian_label.grid(row=13,column=0)
xd_qian_entry=Entry(fm,width=9)
#xd_qian_entry.insert(INSERT,'624,619')
xd_qian_entry.grid(row=13,column=1)
#提交
xd_ok_label=Label(fm,text="提交")
xd_ok_label.grid(row=13,column=2)
xd_ok_entry=Entry(fm,width=9)
#xd_ok_entry.insert(INSERT,'736,646')
xd_ok_entry.grid(row=13,column=3)

#偏差
dc_entry=Entry(fm,width=3)
dc_entry.grid(row=14,column=4)
#坐标
dc_zb_label=Label(fm,text='建差')
dc_zb_label.grid(row=14,column=0)
dc_zb_entry=Entry(fm,width=9)
#dc_zb_entry.insert(INSERT,'860,538')
dc_zb_entry.grid(row=14,column=1)
dc_pc_zb_label=Label(fm,text='平差')
dc_pc_zb_label.grid(row=14,column=2)
dc_pc_zb_entry=Entry(fm,width=9)
dc_pc_zb_entry.grid(row=14,column=3)


#平仓
pc_label=Label(fm,text='平单操作',bg="#FF9999")
pc_label.grid(row=15,column=0,columnspan=5,sticky="NW")

#判断
pc_rgb_label=Label(fm,text='RGB')
pc_rgb_label.grid(row=16,column=2)
pc_pd_rgb=Entry(fm,width=9)
pc_pd_rgb_display=StringVar()
pc_pd_rgb['textvariable']=pc_pd_rgb_display
#pc_pd_rgb.insert(INSERT,'0xff9933')
pc_pd_rgb.grid(row=16,column=3)
get_pc_rgb=Button(fm,text="获取",width=5,comman=get_pc_color)
get_pc_rgb.grid(row=16,column=4)
#提交
pc_tj_label=Label(fm,text='提交')
pc_tj_label.grid(row=17,column=0)
pc_tj_entry=Entry(fm,width=9)
#pc_tj_entry.insert(INSERT,'732,630')
pc_tj_entry.grid(row=17,column=1)
#建立 平仓后确认
jl_pc_qr_label=Label(fm,text='确认')
jl_pc_qr_label.grid(row=16,column=0)
jl_pc_qr=Entry(fm,width=9)
#jl_pc_qr.insert(INSERT,'802,482')
jl_pc_qr.grid(row=16,column=1)

#期望设置
qw_label=Label(fm,text='期望设置',bg="#FF9999")
qw_label.grid(row=18,column=0,columnspan=5,sticky="NW")
qw_entry_label=Label(fm,text='点位')
qw_entry_label.grid(row=19,column=0)
qw_entry=Entry(fm,width=9)
qw_entry.grid(row=19,column=1)
qw_combobox_label=Label(fm,text='方式')
qw_combobox_label.grid(row=19,column=2)
qw_combobox=ttk.Combobox(fm,values=['OFF','ON','ready1','ready2'],width=6)
qw_combobox.grid(row=19,column=3)

#设置某列最小的宽度
#fm.columnconfigure(0,minsize = 20)

#设置数据
def set_num():
    if os.path.exists(pick_name):
        with open(pick_name,'rb') as f:
            pick_old_num=pickle.load(f)
        #设置数据
        pc_pd_rgb.insert(INSERT,pick_old_num['pc_pd_rgb'])
        dc_zb_entry.insert(INSERT,pick_old_num['dc_zb_entry'])
        dc_pc_zb_entry.insert(INSERT,pick_old_num['p_dc_zb'])
        dc_entry.insert(INSERT,pick_old_num['dc'])
        jl_button_entry.insert(INSERT,pick_old_num['jl_button_entry'])
        pc_tj_entry.insert(INSERT,pick_old_num['pc_tj_entry'])
        xd_ok_entry.insert(INSERT,pick_old_num['xd_ok_entry'])
        qk_entry.insert(INSERT,pick_old_num['qk_entry'])
        js_is_zb_entry.insert(INSERT,pick_old_num['js_is_zb_entry'])
        jl_shou_entry.insert(INSERT,pick_old_num['jl_shou_entry'])
        js_is_ys_entry.insert(INSERT,pick_old_num['js_is_ys_entry'])
        jl_shou_zb.insert(INSERT,pick_old_num['jl_shou_zb'])
        pc_zb_entry.insert(INSERT,pick_old_num['pc_zb_entry'])
        sp_entry.insert(INSERT,pick_old_num['sp_entry'])
        dk_entry.insert(INSERT,pick_old_num['dk_entry'])
        xd_qian_entry.insert(INSERT,pick_old_num['xd_qian_entry'])
        jl_pc_qr.insert(INSERT,pick_old_num['jl_pc_qr'])
        xs_zhu_entry.insert(INSERT,pick_old_num['xs_zhu_entry'])
        xs_fu_entry.insert(INSERT,pick_old_num['xs_fu_entry'])
        #数据坐标
        in_entry.insert(INSERT,pick_old_num['in_entry'])
        out_entry.insert(INSERT,pick_old_num['out_entry'])
set_num()
#运行界面 作为主界面
fm.mainloop()
