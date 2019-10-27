#顶层文件，用于调取所有其他文件
import 三班.三组.聊天机器人.reocrd as rTools
import 三班.三组.聊天机器人.shibie.shibie as sTools
FILE_PATH = r'D:\PyCharm\untitled\课程设计\三班\三组\聊天机器人\source\hehe.wav'
#1.录音


#2.存储到本地——source
rTools.record(4, FILE_PATH)

#3.取出音频，解析成中文
r = sTools.sbyy(FILE_PATH)

#4.打印解析出的结果

print(r['result'][0])