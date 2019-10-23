import configparser,os

class CPTools:
    def get_config(self,section,option,path=r'.\config.ini',encoding='utf-8'):
        '''

        :param section: 注释，通过注释找到注释下的内容
        :param option: 操作内容，其对应的就是需要的值
        :param path:文本存放路径
        :param encoding:编码格式
        :return:
        '''
        cp = configparser.ConfigParser()
        cp.read(path,encoding = encoding)
        return cp.get(section,option)

if __name__ == '__main__':
    path = r'.\config.ini'
    print(CPTools().get_config('DATA','user'))
