#配置文件
class wooght_data:
    SILVER_NAME='刷单系统'
    SILVER_BM='dyyt'
    NAME_ID='10001'#注册号
    
    RADIO_NUM=197.67#内外系数
    RADIO_NUM_FUZU=199.82#辅助内外系数
    ABOUT_NUM=[[5,3,5,13,20],[9,8,10,30,45]]#执行参数
    ABOUT_NUM_FUZU=[[5,3,5,14,20],[9,8,10,30,45]]#辅助执行参数
    QW_ABOUT_NUM=[3,18,35]#期望参数
    BZJBL=0.03#保证金比例
    
    LOSS_NUM=8#止损点位
    LOSS_OUT_NUM=8#外部反转点位
    FEINONG=False#非农是否开启

    BW_NUM=5#本位范围
    BW_TIME=10#本位次数
    
    TK_GOOD=True#考虑高收益
    TK_GOOD_FLOAT=3#高收益浮动
    TK_WRITE_FLOAT=3#考虑最小等待外内差
    THREE_TIME=1#第三次运行等待时间 秒
    TO_HEIGHT=True#做单手数是否增长
    HEIGHT_SHOU=50#最高做单手数
    
    CONTINUE_PC=False#到时平仓
    ZIDONG_PC=True#自动平仓
    ZIDONG_JC=True#自动建仓
    PB_Xevent=False#屏蔽环境
    PC_TIME=36000#平仓等待最长时间 按秒计算
    OUT_FLOAT=100#外浮动幅度 此数加一
    
    #本地
    #SQL_ROOT={'user':'1yy3','passwd':'6yyqr3!@!$!&','host':'AB$*.*.*A','dbname':'6yyqr3'}
    #远程
    SQL_ROOT={'user':'6yyqr3A','passwd':'6yyqr3!@!$!&','host':'20v*6A.&*5ry23qy*cyw','dbname':'6yyqr3A'}
    #控制服务器地址
    SERVER_HOST='127.0.0.1'
    
    GOU_COLOR='0x0'#选取框打钩颜色
    BOX_XY=[316,207,580]#界面尺寸
    
    READ_OUT_NUM=[0,1]#连续读取外盘次数
    IN_LX_TIME=300#内部连续相同最大时间 单位秒
