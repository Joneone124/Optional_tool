#!/usr/bin/python
# -*- encoding: utf-8

import numpy as np
import matplotlib as mpl
import pandas as pd
from sklearn.preprocessing import StandardScaler, minmax_scale
import matplotlib.pyplot as plt
from sklearn.linear_model import LassoCV, ElasticNetCV
import warnings
from sklearn.exceptions import ConvergenceWarning


if __name__ == "__main__":
    warnings.filterwarnings(action='ignore', category=ConvergenceWarning) #忽略ConvergenceWarning警告

    #显示画布中的汉字符号
    mpl.rcParams['font.sans-serif'] = [u'simHei']
    mpl.rcParams['axes.unicode_minus'] = False
    data = pd.read_excel('crim.xlsx', sheetname='Sheet1', header=0)  #读取excel文件；header=0即指定列名为第一行，从下一行开始读取数据
    ppq = pd.read_excel('crim.xlsx', sheetname='Sheet1', header=0)
    print('data.head() = \n', data.head()) #打印data全部数据
    columns = [c for c in data.columns]      # 列标题
    print(data.columns)
    data.sort_values(by=data.columns[1], inplace=True) #根据第二列盗窃案件数进行纵向升序，并用排序后的数据代替现有数据
    data = data.values
    x = data[:, 2:].astype(np.float) #将第三列到最后一列的所有行数据类型转为float
    y = data[:, 1].astype(np.int)  #将第二列所有值类型转为int
    columns = columns[2:]

    ss = StandardScaler()
    x = ss.fit_transform(x) #归一化训练数据

    # 增加一列全1
    t = np.ones(x.shape[0]).reshape((-1, 1))  #生成一行1（x的行数），将其变成一列1
    print (t.shape, x.shape)
    x = np.hstack((t, x))   #进行拼接

    # model = ElasticNetCV(alphas=np.logspace(-3, 2, 50), l1_ratio=[.1, .5, .7, .9, .95, .99, 1], fit_intercept=False)
    model = LassoCV(alphas=np.logspace(-3, 2, 50), fit_intercept=False)  #使用lasso回归，且无截距
    model.fit(x, y) #进行拟合，学习参数
    y_hat = model.predict(x) #进行预测
    # print('----------------------------',y_hat)
    y_hat[y_hat < 0] = 0 #将预测的犯罪数小于0的数全部置为0
    print ('model.alpha = \t', model.alpha_)
    # print 'model.l1_ratio = \t', model.l1_ratio_
    print ('model.coef_ = \n', model.coef_)   #输出权重
    print ('model.predict(x) = \n', y_hat) #输出预测结果
    print ('Acture = \n', y)
    print ('RMSE:\t', np.sqrt(np.mean((y_hat-y)**2)))
    print ('R2:\t', model.score(x, y)) #R2 =（1-u/v） u=((y_true - y_pred) ** 2).sum()     v=((y_true - y_true.mean()) ** 2).sum()
    for theta, col in zip(model.coef_[1:], columns):  #zip()将可迭代对象打包成元组的列表
        if theta > 0.01:
            print (col, theta)

    #画图
    plt.figure(facecolor='w')
    t = np.arange(len(y))
    plt.plot(t, y_hat, 'go', label=u'预测值')
    plt.plot(t, y, 'r-', lw=2, label=u'实际值')
    plt.grid(b=True) #增加网格
    plt.legend(loc='upper left')  #标签位置
    plt.title(u'北京市犯罪率与特征相关性回归分析', fontsize=18)
    plt.show()
