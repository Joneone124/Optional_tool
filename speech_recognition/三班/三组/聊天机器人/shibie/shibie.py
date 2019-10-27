#1.导aip包
#2.设置应用信息
#3.从文件中获取语音进行识别

from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '16658714'
API_KEY = 'Uf1b7CeHo7CmOWbKo5piuRRt'
SECRET_KEY = 'nzyo9aHfI4XKCuZKiTsq3HOwjVQtYGg9'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件
def sbyy(filePath):
    result = client.asr(get_file_content(filePath), 'pcm', 16000, {
        'dev_pid': 1536,
    })
    return result
