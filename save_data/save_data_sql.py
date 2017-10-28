import pymysql as mysql
from save_data import config
import time
#数据库资料
cg=config.wooght_data
#链接配置
sql_root=cg.SQL_ROOT
def connect_sql():
    cnx=mysql.connect(port=3306,user=jiemi(sql_root['user']),passwd=jiemi(sql_root['passwd']),host=jiemi(sql_root['host']),db=jiemi(sql_root['dbname']))
    return cnx
#保存操作记录
def save_jl(j_in,j_out,p_in,vip_id):
    cnx=connect_sql()
    cursor=cnx.cursor()
    time_str=time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))
    sql_str="insert into dyyt_jl set j_in="+str(j_in)+",j_out="+str(j_out)+",p_in="+str(p_in)+",p_time='"+time_str+"',vip_id="+vip_id+"";
    cursor.execute(sql_str)
    cnx.commit()#执行事物处理操作
    cnx.close()
    cursor.close()
#注册判断
def registration(num_id):
    cnx=connect_sql()
    cursor=cnx.cursor()
    sql_str="select vip_name from dyyt_vip where vip_id='"+str(num_id)+"'";
    if cursor.execute(sql_str):
        cnx.close()
        cursor.close()
        return True
    else:
        cnx.close()
        cursor.close()
        return False

#加密字节
jiami_char=['a','b','c','d','e','f','g','h','i','j','k',
           'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
          '0','1','2','3','4','5','6','7','8','9','.',
          'A','B','C','D','!','@','$','&','_','*','E']
#加密算法
def jiami(jiami_str):
    new_str=''
    len_str=len(jiami_str)
    for i in range(len_str):
        cha_index=jiami_char.index(jiami_str[i])
        if cha_index<5:
            new_str+=jiami_str[i]
        else:
            new_str+=jiami_char[jiami_char.index(jiami_str[i])+10]
    return new_str
#解密算法
def jiemi(mima_str):
    new_str=''
    len_str=len(mima_str)
    for i in range(len_str):
        char_index=jiami_char.index(mima_str[i])
        if char_index<5:
            new_str+=mima_str[i]
        else:
            new_str+=jiami_char[char_index-10]
    return new_str
if __name__=='__main__':
    print(jiami('sql.w108.vhostgo.com..wooght565758'))
