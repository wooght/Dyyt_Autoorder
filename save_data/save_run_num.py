###
#保存文本,追加文本,写入文本
import time
def save_txt(txt):
    time_str=time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))
    spath='save_data/save.wooght'
    f=open(spath,'a')
    f.write(time_str+"-"+txt)
    f.close()
