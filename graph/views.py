import datetime
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Data
import pandas as pd
import matplotlib.pyplot as plt
import io
import urllib
import base64
import matplotlib
from statsmodels.tsa.seasonal import seasonal_decompose
matplotlib.use('Agg')
degree_sign = u'\N{DEGREE SIGN}'
labels = {
    'tempr': 'Temperature ('+degree_sign+'C)',
    'ap': 'Atmospheric Pressure (mbar)',
    'ws': 'Wind Speed (knots)',
    'rh': 'Relative Humidity (%)'
}
legend = {
    'tempr': 'Temperature',
    'ap': 'Atmospheric Pressure',
    'ws': 'Wind Speed',
    'rh': 'Relative Humidity'
}


def graph(request):
    plottype = request.POST.get('plottype')

    datafreq = request.POST.get('datafreq')

    paramaterArr = []
    if(request.POST.get('temp') != None):
        paramaterArr.append('tempr')
    if(request.POST.get('ap') != None):
        paramaterArr.append('ap')
    if(request.POST.get('ws') != None):
        paramaterArr.append('ws')
    if(request.POST.get('rh') != None):
        paramaterArr.append('rh')
    filteredData = Data.objects.all()
    df = pd.DataFrame(list(filteredData.values()))
    df.set_index('obstime', inplace=True)

    df = df[paramaterArr]

    if(plottype == "trend"):
        if(request.POST.get('start') == None):
            start = "2016-06-02"
        else:
            start = request.POST.get('start')
        if(request.POST.get('end') == None):
            end = "2019-06-19"
        else:
            end = request.POST.get('end')
        df = df[df.index >= start]
        df = df[df.index <= end]
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
        if(datafreq == 'hourly'):
            if(len(paramaterArr) > 1):
                fig = plt.figure(figsize=(15, 8))
                v = 0
                fig.subplots_adjust(hspace=0.4)
                for parameter in paramaterArr:
                    v = v+1
                    ax = fig.add_subplot(len(paramaterArr), 1, v)
                    ax.plot(df[[parameter]], label=legend[parameter])
                    ax.legend()
                    ax.set_ylabel(labels[parameter])
                    ax.set_xlabel('Observation Time')
            else:
                res = seasonal_decompose(
                    df[paramaterArr[0]].interpolate(), freq=(end-start).days, model='additive')
                fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(15, 8))
                fig.text(0.04, 0.5, labels[paramaterArr[0]],
                         va='center', rotation='vertical')
                res.observed.plot(ax=ax1)
                ax1.set(ylabel="Observed")
                res.trend.plot(ax=ax2)
                ax2.set(ylabel="Trend")
                res.seasonal.plot(ax=ax3)
                ax3.set(ylabel="Seasonal")
                res.resid.plot(ax=ax4)
                ax4.set(ylabel="Residual")
                plt.xlabel('Observation Time', fontsize=15)
        elif(datafreq == 'daily'):
            df['date'] = df.index.map(lambda x: str(x).split()[0])
            df_daily = df.pivot_table(index='date')
            df_daily.index = pd.to_datetime(df_daily.index, format="%Y-%m-%d")
            if(len(paramaterArr) > 1):
                fig = plt.figure(figsize=(15, 8))
                v = 0
                fig.subplots_adjust(hspace=0.4)
                for parameter in paramaterArr:
                    v = v+1
                    ax = fig.add_subplot(len(paramaterArr), 1, v)
                    ax.plot(df_daily[[parameter]], label=legend[parameter])
                    ax.legend()
                    ax.set_ylabel(labels[parameter])
                    ax.set_xlabel('Observation Time')
            else:
                res = seasonal_decompose(
                    df_daily[paramaterArr[0]].interpolate(), freq=24, model='additive')
                fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(15, 8))
                fig.text(0.04, 0.5, labels[paramaterArr[0]],
                         va='center', rotation='vertical')
                res.observed.plot(ax=ax1)
                ax1.set(ylabel="Observed")
                res.trend.plot(ax=ax2)
                ax2.set(ylabel="Trend")
                res.seasonal.plot(ax=ax3)
                ax3.set(ylabel="Seasonal")
                res.resid.plot(ax=ax4)
                ax4.set(ylabel="Residual")
                plt.xlabel('Observation Time', fontsize=15)
        elif(datafreq == 'monthly'):
            df['year-month'] = df.index.map(lambda x: str(x).split()
                                            [0].split('-')[0] + '-' + str(x).split()[0].split('-')[1])
            df_monthly = df.pivot_table(index='year-month')
            df_monthly.index = pd.to_datetime(df_monthly.index, format="%Y-%m")
            if(len(paramaterArr) > 1):
                fig = plt.figure(figsize=(15, 8))
                v = 0
                fig.subplots_adjust(hspace=0.4)
                for parameter in paramaterArr:
                    v = v+1
                    ax = fig.add_subplot(len(paramaterArr), 1, v)
                    ax.plot(df_monthly[[parameter]], label=legend[parameter])
                    ax.legend()
                    ax.set_ylabel(labels[parameter])
                    ax.set_xlabel('Observation Time')
            else:
                res = seasonal_decompose(
                    df_monthly[paramaterArr[0]].interpolate(), freq=12, model='additive')
                fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(15, 8))
                fig.text(0.04, 0.5, labels[paramaterArr[0]],
                         va='center', rotation='vertical')

                res.observed.plot(ax=ax1)
                ax1.set(ylabel="Observed")
                res.trend.plot(ax=ax2)
                ax2.set(ylabel="Trend")
                res.seasonal.plot(ax=ax3)
                ax3.set(ylabel="Seasonal")
                res.resid.plot(ax=ax4)
                ax4.set(ylabel="Residual")
                plt.xlabel('Observation Time', fontsize=15)
        else:
            print("Choose Something")
    elif(plottype == 'diurnal'):
        if(request.POST.get('diurnaldate') == None):
            t = '2019-06-19'
        else:
            t = request.POST.get('diurnaldate')
        df['date'] = df.index.map(lambda x: str(x).split()[0])
        df = df[df['date'] == t]
        fig = plt.figure(figsize=(15, 8))
        v = 0
        fig.subplots_adjust(hspace=0.4)
        for parameter in paramaterArr:
            v = v+1
            ax = fig.add_subplot(len(paramaterArr), 1, v)
            ax.plot(df[[parameter]], label=legend[parameter])
            ax.legend()
            ax.set_ylabel(labels[parameter])
            ax.set_xlabel('Observation Time')
    elif(plottype == 'seasonal'):
        df['date'] = df.index.map(lambda x: str(x).split()[0])
        df['year-month'] = df.date.map(lambda x: x.split('-')
                                       [0] + '-' + x.split('-')[1])
        df['date_only'] = df.date.map(lambda x: x.split('-')[2])
        if(request.POST.get('seasonal_year') == None):
            year = '2018'
        else:
            year = request.POST.get('seasonal_year')
        if(request.POST.get('season') == None):
            season = 'summer'
        else:
            season = request.POST.get('season')
        if(season == 'summer'):
            if(datafreq == 'daily'):
                dec = df[df['year-month'] == str(int(year)-1) + '-'+'12']
                jan = df[df['year-month'] == year+'-'+'01']
                feb = df[df['year-month'] == year+'-'+'02']
                dec_daily = dec.pivot_table(index='date_only')
                jan_daily = jan.pivot_table(index='date_only')
                feb_daily = feb.pivot_table(index='date_only')
                fig = plt.figure(figsize=(15, 8))
                v = 0

                for parameter in paramaterArr:
                    v = v+1
                    ax = fig.add_subplot(len(paramaterArr), 1, v)
                    ax.plot(dec_daily[[parameter]], label='Dec')
                    ax.plot(jan_daily[[parameter]], label='Jan')
                    ax.plot(feb_daily[[parameter]], label='Feb')
                    ax.legend()
                    ax.set_ylabel(labels[parameter])
                    ax.set_xlabel('Days')
        elif(season == 'fall'):
            if(datafreq == 'daily'):
                mar = df[df['year-month'] == year + '-'+'03']
                apr = df[df['year-month'] == year+'-'+'04']
                may = df[df['year-month'] == year+'-'+'05']
                mar_daily = mar.pivot_table(index='date_only')
                apr_daily = apr.pivot_table(index='date_only')
                may_daily = may.pivot_table(index='date_only')
                fig = plt.figure(figsize=(15, 8))
                v = 0

                for parameter in paramaterArr:
                    v = v+1
                    ax = fig.add_subplot(len(paramaterArr), 1, v)
                    ax.plot(mar_daily[[parameter]], label='Mar')
                    ax.plot(apr_daily[[parameter]], label='Apr')
                    ax.plot(may_daily[[parameter]], label='May')
                    ax.legend()
                    ax.set_ylabel(labels[parameter])
                    ax.set_xlabel('Days')
        elif(season == 'winter'):
            if(datafreq == 'daily'):
                jun = df[df['year-month'] == year+'-'+'06']
                jul = df[df['year-month'] == year+'-'+'07']
                aug = df[df['year-month'] == year+'-'+'08']
                jun_daily = jun.pivot_table(index='date_only')
                jul_daily = jul.pivot_table(index='date_only')
                aug_daily = aug.pivot_table(index='date_only')
                fig = plt.figure(figsize=(15, 8))
                v = 0

                for parameter in paramaterArr:
                    v = v+1
                    ax = fig.add_subplot(len(paramaterArr), 1, v)
                    ax.plot(jun_daily[[parameter]], label='Jun')
                    ax.plot(jul_daily[[parameter]], label='Jul')
                    ax.plot(aug_daily[[parameter]], label='Aug')
                    ax.legend()
                    ax.set_ylabel(labels[parameter])
                    ax.set_xlabel('Days')
        elif(season == 'spring'):
            if(datafreq == 'daily'):
                sep = df[df['year-month'] == year+'-'+'09']
                octo = df[df['year-month'] == year+'-'+'10']
                nov = df[df['year-month'] == year+'-'+'11']
                sep_daily = sep.pivot_table(index='date_only')
                oct_daily = octo.pivot_table(index='date_only')
                nov_daily = nov.pivot_table(index='date_only')
                fig = plt.figure(figsize=(10, 8))
                v = 0

                for parameter in paramaterArr:
                    v = v+1
                    ax = fig.add_subplot(len(paramaterArr), 1, v)
                    ax.plot(sep_daily[[parameter]], label='Sep')
                    ax.plot(oct_daily[[parameter]], label='Oct')
                    ax.plot(nov_daily[[parameter]], label='Nov')
                    ax.legend()
                    ax.set_ylabel(labels[parameter])
                    ax.set_xlabel('Days')
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'graph/index.html', {'data': uri})
