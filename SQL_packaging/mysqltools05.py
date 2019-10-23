import MySQLdb
import pythoon_base.SQL_packaging.cp_loader as loader


class MySqlTools(object):

    #初始化方法
    def __init__(self,*,db,user,password,host='localhost',port=3306,charset='utf8'):
        '''
        第一个参数是*，后面的参数都要用关键值传参
        :param db: 数据库名
        :param user: 用户名
        :param password: 密码
        :param host: 主机IP
        :param port: 端口
        :param charset: 字符编码
        '''
        self.__db = db
        self.__user = user
        self.__password = password
        self.__host =host
        self.__port = port
        self.__charset = charset

    def _connection(self):
        '''
        只在文件内部使用，设置为受保护的
        :param self:
        :return:
        '''
        self.conn = MySQLdb.connect(db = self.__db,user = self.__user,password = self.__password,
                                    host = self.__host,port = self.__port,charset = self.__charset)

        #创建游标
        self.cursor = self.conn.cursor()

    def _close(self):
        '''
        内部使用的释放资源
        :return:
        '''
        self.cursor.close()
        self.conn.close()

    #增加
    def add(self,table,data):
        '''

        :param table:
        :param data:
        :return:
        '''
        keys = []
        values = []
        self._connection()
        try:
            for i in data.items():
                keys.append(i[0])
                values.append(self._deal_data(i[1]))

            sql='insert into {table} ({key}) values ({value})'.format(table=table,
                                                                  key=','.join(keys),
                                                                  value=','.join(values))
            print('ssssssssssssddddddddddddddd')
            print(sql)
            self.cursor.execute(sql)
            print('ddddddddddddddd')
            self.conn.commit()
        except Exception as error:
            print(error)
        finally:
            self._close()

    #处理数据方法
    def _deal_data(self,data):
        if isinstance(data,str):
            return "'{data}'".format(data = data)

        elif isinstance(data,dict):
            temp = []
            for key,value in data.items():
                value = self._deal_data(value)
                res = '{key}={value}'.format(key = key,value = value)
                temp.append(res)
            return temp
        else:
            return str(data)

    #删除
    def delete(self,table,condition):
        '''

        :param table: str
        :param condition: dict
        :return:
        '''
        self._connection()

        try:
            condition = ' and '.join(self._deal_data(condition))
            sql = 'delete from {table} where {condition}'.format(table = table,condition = condition)
            self.cursor.execute(sql)
            self.conn.commit()

        except:
            print('出错了！')

        finally:
            self._close()

    #修改
    def modify(self,table,data,condition = None):
        '''

        :param table: str
        :param data: dict
        :param condition: dict
        :return:
        '''
        self._connection()

        try:
            #处理数据
            data = ','.join(self._deal_data(data))
            if condition:
                condition = ' and '.join(self._deal_data(condition))
                sql = 'update {table} set {data} where {condition}}'.format(table = table, data = data, condition = condition)

            else:
                sql = 'update {table} set {data}'.format(table = table, data = data)
            self.cursor.execute(sql)
            self.conn.commit()

        except:
            print('出错了！')
        finally:
            self._close()

    #查询
    def get(self,table,data,condition=None,get_one=False):
        '''

        :param table: str
        :param data: list
        :param condition: dict
        :param get_one: boolean
        :return:
        '''
        self._connection()
        try:
            data = ','.join(data)
            if condition:
                condition = ' and '.join(self._deal_data(condition))
                sql = 'select {data} from {table} where {condition}'.format(table=table,
                                                                        data=data,
                                                                        condition = condition)
            else:
                sql = 'select {data} from {table}'.format(table = table, data = data)
            self.cursor.execute(sql)
            if get_one:
                r = self.cursor.fetchone()
            else:
                r = self.cursor.fetchall()

        except:
            print('出错了！')
        finally:
            self._close()
        return r

    #利用工厂函数，使用方法或函数创建对象 节省资源
    @classmethod
    def get_tool(cls):
        cp = loader.CPTools()
        data = {
            'db':cp.get_config('DATA','db'),
            'user':cp.get_config('DATA','user'),
            'password': cp.get_config('DATA', 'password'),
            'host': cp.get_config('DATA', 'host'),
            'port': int(cp.get_config('DATA', 'port')),
            'charset': cp.get_config('DATA', 'charset')
        }
        def check_connection():
            try:
                print('asdasdad')
                conn = MySQLdb.connect(**data)#把字典属性的data解开成赋值串，可以直接进行赋值
                print('ssssssssssssssss')
            except Exception as e:
                print(e)
                return False
            else:
                conn.close()
                return True

        if check_connection():
            return cls(**data)
        else:
            print('连接失败')

if __name__ == '__main__':
    #首先调用判断是否能成功连接的类方法，如果能连接，则返回类对象，用tool接受
    tool = MySqlTools.get_tool()
    print(tool.get('stu',['*']))
    tool.add('stu',{'name':'xiaoli','id':13,'age':28})

