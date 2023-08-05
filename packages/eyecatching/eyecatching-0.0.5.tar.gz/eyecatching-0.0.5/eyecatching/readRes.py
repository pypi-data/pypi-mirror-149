# -*- coding: utf-8 -*-
# Author: Jimei Shen

import datetime
import matplotlib.pyplot as plt
import math
from math import pi
import pandas as pd
import pickle
from random import sample
from eyecatching.settings import *
from io import BytesIO
import base64


def cal_area(vertices): #Gauss's area formula 高斯面积计算
    A = 0.0
    point_p = vertices[-1]
    for point in vertices:
        A += (point[1]*point_p[0] - point[0]*point_p[1])
        point_p = point
    return abs(A)/2

def cal_centroid(points):
    A = cal_area(points)
    c_x, c_y = 0.0, 0.0
    point_p = points[-1]
    for point in points:
        c_x +=((point[0] + point_p[0]) * (point[1]*point_p[0] - point_p[1]*point[0]))
        c_y +=((point[1] + point_p[1]) * (point[1]*point_p[0] - point_p[1]*point[0]))
        point_p = point

    return c_x / (6*A), c_y / (6*A)

def outlier(data, deviation):
    mean = np.mean(data)
    standard_deviation = np.std(data)
    distance_from_mean = abs(data - mean)
    max_deviations = deviation
    not_outlier = distance_from_mean < max_deviations * standard_deviation
    return not_outlier, mean, standard_deviation


def plot(user_input, pointPerPlot):
    with open('pupilOffsetXYList.pkl', 'rb') as f:
        res = pickle.load(f)
        f.close()
    pointPerPlot = int(pointPerPlot)
    res.time = pd.to_datetime(res.time)
    res = res[res.time > res.time[0]+datetime.timedelta(seconds=initTime)].reset_index(drop=True)

    xnot_outlier, xallmean, xallstd = outlier(res.x, 3)
    res = res[xnot_outlier]
    ynot_outlier, yallmean, yallstd = outlier(res.y, 3)
    res = res[ynot_outlier]

    xMax = max(list(res.x))
    xMin = min(list(res.x))
    yMax = max(list(res.y))
    yMin = min(list(res.y))

    res.x = [(j-xMin)/(xMax-xMin) for j in res.x]
    res.y = [(j-yMin)/(yMax-yMin) for j in res.y]

    timeDelta = (res.time[len(res.time)-1] - res.time[0]).seconds
    print(timeDelta)
    plotTimeDelta = int(timeDelta/plotNumber)
    print(plotTimeDelta)

    img = plt.imread("./static/%s"%user_input)
    plt.figure(figsize=(30, 25))
    xAll = []
    yAll = []

    for i in range(plotNumber):
        tStart = res.time[0] + datetime.timedelta(seconds=i*plotTimeDelta)
        tEnd = res.time[0] + datetime.timedelta(seconds=(i+1)*plotTimeDelta)
        dataTemp = res[(res.time >= tStart) & (res.time < tEnd)].dropna().reset_index(drop=True)
        xnot_outlier, xmean, xstd = outlier(dataTemp.x, 1)
        dataTemp = dataTemp[xnot_outlier]
        ynot_outlier, ymean, ystd = outlier(dataTemp.y, 1)
        dataTemp = dataTemp[ynot_outlier]

        # x_centroid, y_centroid = cal_centroid([[xTemp[j], yTemp[j]] for j in range(len(xTemp))])
        x = sample(list(dataTemp.x), pointPerPlot)
        y = sample(list(dataTemp.y), pointPerPlot)

        xAll.append(x)
        yAll.append(y)

        plt.subplot(plotNColumn, math.ceil(plotNumber / plotNColumn), i+1)
        if i == 0:
            plt.imshow(img, extent=[0, 1, 0, 1], alpha=1)
        else:
            plt.imshow(img, extent=[0, 1, 0, 1], alpha=0.5)
        # ax = plt.gca()

        # ellipse = Ellipse(xy=(xmean, ymean), width=xstd, height=ystd, alpha=0.5)
        # ax.add_patch(ellipse)
        #
        # ellipse = Ellipse(xy=(xmean, ymean), width=xstd*3, height=ystd*3, alpha=0.2)
        # ax.add_patch(ellipse)

        t = np.linspace(0, 2 * pi, 100)
        plt.fill(xmean + 1.5*xstd * np.cos(t), ymean + 1.5*ystd * np.sin(t), alpha=.5, color='#BEB8DC')
        # plt.fill(xmean + 3*xstd * np.cos(t), ymean + 3*ystd * np.sin(t), alpha=0.3, color='#E7DAD2')

        for j in range(i+1):
            if j != i:
                plt.scatter(xAll[j], yAll[j], s=200, alpha=0.1, label='%s'%j, color='blue')
            else:
                plt.scatter(xAll[j], yAll[j], s=200, alpha=1, label='%s' % j, color='blue')
            plt.legend()
        plt.title('From Time %s to Time %s, Initialization Time %s'%(i*plotTimeDelta, (i+1)*plotTimeDelta,initTime))
    # plt.savefig('./res%s.png'%user_input)
    plt.plot()
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    plt.close()

    return data

# def pointsCalulator(data, pointPerPlot, plotNumber):
#
#     timeDelta = (data.time[len(data.time)-1] - data.time[0]).seconds
#     print(timeDelta)
#     plotTimeDelta = int(timeDelta/plotNumber)
#     print(plotTimeDelta)
#     xRaw = []
#     yRaw = []
#     x = []
#     y = []
#
#     for i in range(plotNumber):
#         tStart = data.time[0] + datetime.timedelta(seconds=i*plotTimeDelta+initTime)
#         tEnd = data.time[0] + datetime.timedelta(seconds=(i+1)*plotTimeDelta+initTime)
#         dataTemp = data[(data.time >= tStart) & (data.time < tEnd)].dropna().reset_index(drop=True)
#         dataTempSample = dataTemp.sample(n=pointPerPlot).reset_index(drop=True)
#         xRaw.append(dataTempSample.x)
#         yRaw.append(dataTempSample.y)
#
#     xMax = max([max(i) for i in xRaw])
#     xMin = min([min(i) for i in xRaw])
#     yMax = max([max(i) for i in yRaw])
#     yMin = min([min(i) for i in yRaw])
#
#     for i in range(plotNumber):
#         x.append([(j-xMin)/(xMax-xMin) for j in xRaw[i]])
#         y.append([(j-yMin) /(yMax-yMin) for j in yRaw[i]])
#
#     return x, y, plotTimeDelta

# def pointsAllCalulator(data, plotNumber, plotTimeDelta):
#
#     xRaw = []
#     yRaw = []
#     x = []
#     y = []
#
#     for i in range(plotNumber):
#         tStart = data.time[0] + datetime.timedelta(seconds=i*plotTimeDelta+initTime)
#         tEnd = data.time[0] + datetime.timedelta(seconds=(i+1)*plotTimeDelta+initTime)
#         dataTemp = data[(data.time >= tStart) & (data.time < tEnd)].dropna().reset_index(drop=True)
#         xRaw.append(dataTemp.x)
#         yRaw.append(dataTemp.y)
#
#     xMax = max([max(i) for i in xRaw])
#     xMin = min([min(i) for i in xRaw])
#     yMax = max([max(i) for i in yRaw])
#     yMin = min([min(i) for i in yRaw])
#
#     for i in range(plotNumber):
#         x.append([(j-xMin)/(xMax-xMin) for j in xRaw[i]])
#         y.append([(j-yMin) /(yMax-yMin) for j in yRaw[i]])
#
#     return x, y

# def plot(user_input):
#     with open('./result/pupilOffsetXYList.pkl', 'rb') as f:
#         res = pickle.load(f)
#         f.close()
#
#     for i in ['x', 'y']:
#         mean = np.mean(res[i])
#         print(mean)
#         standard_deviation = np.std(res[i])
#         print(standard_deviation)
#         distance_from_mean = abs(res[i] - mean)
#         max_deviations = 3
#         not_outlier = distance_from_mean < max_deviations * standard_deviation
#         res[i] = res[i][not_outlier]
#
#     res = res.reset_index(drop=True)
#     res.time = pd.to_datetime(res.time)
#
#     x, y, plotTimeDelta = pointsCalulator(res, pointPerPlot, plotNumber)
#
#     img = plt.imread("./static/%s"%user_input)
#     plt.figure(figsize=(30, 25))
#     for i in range(len(x)):
#         plt.subplot(plotNColumn, math.ceil(plotNumber / plotNColumn), i+1)
#         if i == 0:
#             plt.imshow(img, extent=[0, 1, 0, 1], alpha=1)
#         else:
#             plt.imshow(img, extent=[0, 1, 0, 1], alpha=0.5)
#         for j in range(i+1):
#             if j != i:
#                 plt.scatter(x[j], y[j], s=200, alpha=0.2, label = '%s'%j)
#             else:
#                 plt.scatter(x[j], y[j], s=200, alpha=1, label='%s' % j)
#             plt.legend()
#         plt.title('From Time %s to Time %s, Initialization Time %s'%(i*plotTimeDelta, (i+1)*plotTimeDelta,initTime))
#     plt.savefig('./result/res%s.png'%user_input)
#
#     sio = BytesIO()
#     plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
#     data = base64.encodebytes(sio.getvalue()).decode()
#     plt.close()
#
#     return data


# def plotall(user_input):
#
#     with open('./result/pupilOffsetXYList.pkl', 'rb') as f:
#         res = pickle.load(f)
#         f.close()
#
#     for i in ['x', 'y']:
#         mean = np.mean(res[i])
#         print(mean)
#         standard_deviation = np.std(res[i])
#         print(standard_deviation)
#         distance_from_mean = abs(res[i] - mean)
#         max_deviations = 3
#         not_outlier = distance_from_mean < max_deviations * standard_deviation
#         res[i] = res[i][not_outlier]
#
#     res = res.reset_index(drop=True)
#     res.time = pd.to_datetime(res.time)
#
#     x, y, plotTimeDelta = pointsCalulator(res, pointPerPlot, plotNumber)
#     x_all, y_all = pointsAllCalulator(res, plotNumber, plotTimeDelta)
#     img = plt.imread("./static/%s" % user_input)
#     plt.figure(figsize=(30, 25))
#     fig, ax = plt.subplots()
#     alpha_ratio = 1/len(x_all)
#     for i in range(len(x_all)):
#         ax.imshow(img, extent = [0, 1, 0, 1])
#         plt.plot(x_all[i], y_all[i], label = i, alpha = min(alpha_ratio*(i+1), 1), color = 'blue')
#         plt.legend()
#     plt.savefig('./result/res_all%s.png'%user_input)
#     sio = BytesIO()
#     plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
#     data = base64.encodebytes(sio.getvalue()).decode()
#     plt.close()
#
#     return data

if __name__ == "__main__":
    plot('Picture1.png', 5)