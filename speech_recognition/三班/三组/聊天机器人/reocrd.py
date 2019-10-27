import pyaudio
import wave

#封装一个函数：seconds:录音时长 filename:录好的音的文件名
def record(seconds, filename):
    #采样率 每秒钟截取多少样本，把声音分成多少段
    RATE = 8000
    #采样管道数 两个管道同时采样，即每秒一共8000*2=16000段
    CHANNELS = 2
    #量化位数 用多少位录音,用16位
    FORMAT = pyaudio.paInt16
    #录音时长
    SECONDS = seconds

    #创建音频对象
    p = pyaudio.PyAudio()
    #开启 数据流
    stream  = p.open(rate=RATE, channels=CHANNELS, format=FORMAT, input=True)
    #创建数据仓库 用常用的可存储多种数据的容器：列表
    frames = []
    #打印提示语句
    print('开始录音，您还有'+str(SECONDS)+'秒时间')
    #开始录音
    data = stream.read(RATE*SECONDS)
    #存储数据
    frames.append(data)
    #停止录音
    stream.stop_stream()
    #释放资源
    stream.close()
    #关闭会话
    p.terminate()
    print('录音结束')

    #将录好的音频数据存储到本地文件中（wav格式）
    wf = wave.open(filename, 'wb')
    #设置管道
    wf.setnchannels(CHANNELS)
    #设置采样率
    wf.setframerate(RATE)
    #设置量化位数
    wf.setsampwidth(p.get_sample_size(FORMAT))
    #将数据存储起来
    wf.writeframes(b''.join(frames))#frames是数据,用b''将后面的字符串转化为二进制，用write方法写道文件里
    #关闭资源
    wf.close()
    return filename

if __name__ == '__main__':
    record(4, 'hehe.wav')