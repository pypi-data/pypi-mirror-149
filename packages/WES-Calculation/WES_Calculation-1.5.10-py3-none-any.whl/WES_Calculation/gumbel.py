'''
Author: BDFD
Date: 2022-02-24 15:23:11
LastEditTime: 2022-04-27 23:52:07
LastEditors: BDFD
Description: 
FilePath: \5.2-PyPi-WES_Calculation\WES_Calculation\gumbel.py
'''
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter
import numpy as np
# from numpy import *
import math
import statistics
import io
import base64

# Reference Usage
# if request.method == "POST":
#     i1 = int(request.form["i1"])
#     i2 = int(request.form["i2"])
#     i3 = int(request.form["i3"])
#     unitt = request.form["unitt"]
#     unitx = request.form["unitx"]
#     result = request.form["datao"]  
#     test1 = result
#     test2 = unitt
#     test3 = unitx
#     plot_url,data,test4,test5,test6,test7,test8,test10 = wes.gumbel(result, unitt, unitx, i1, i2, i3)
#     return render_template("Gumbel.html",plot_url=plot_url,data=data,test1=test1,test2=test2,test3=test3,test4=test4,test5=test5,test6=test6,test7=test7,test8=test8,test10=test10)
# else:
#     return render_template("Gumbel.html")

def gumbel(pq, unitt, unitx, i1, i2, i3, meanx, sdx, n, dataolist):
    plt.rcParams['axes.unicode_minus']=False
    # return pq, unitt, unitx, i1, i2, i3, meanx, sdx, n, datao    
    # print('res is ', res,'and type is ', type(res))
    unitt = unitt
    # print('unitt is ', unitt,'and type is ', type(unitt))
    unitx = unitx
    # print('unitx is ', unitx,'and type is ', type(unitx))
    Tt=[2,5,10,20,25,50,100,200] # Typical return periods used in the output report  
    Tti=[1.005,2,3,4,5,10,20,30,40,50,60,70,80,90,100,200,500] # Return periods for plotting
    Tmat=[1.005,2,5,10,50,100,200] # major ticks (Note:Tmat + Tmit must = Tti.)
    Tmit=[3,4,20,30,40,60,70,80,90,500] # minor ticks (Note:Tmat + Tmit must = Tti.)
    zp=1.645 #1.96# Quantile of standard normal distribution used for confidence interval (1.645 for 90% confidence interval,1.96 for 95%) 2022.02.07
    nbin=10 # number of bins in histogram
    nlC2=20 # The minimum required sample size for Chi-Squared Test (2022.02.09)
    npl=5 # The minimum required expected number in each bin for Chi-Squared Test (2022.02.09)
    nmin=10 # The minimum sample size required for frequancy analysis (2022.02.09)
    
    if i2 == 2:
        res = dataolist.split(",")
        datao = list(map(float,res))
        datao=sorted(datao,reverse=True) # re-ordered X data series in a descending order.
        n=len(datao) # number of the observed data, or record length
        meanx=np.average(datao)
        sdx=statistics.stdev(datao) # standard deviation of X data series
        Csx=n*sum((np.array(datao)-meanx)**3)/(n-1)/(n-2)/sdx**3 # Skew Coefficient of X data series

        if i3==1:
            a=0 # a: a coefficient in plotting position equation:
        if i3==2:
            a=0.3175
        if i3==3:
            a=0.44

        Go=[0 for j in range(n)] # Empirical exceedance Probabilities of observed data
        Fo=[0 for j in range(n)] # Empirical CDF of observed data
        To=[0 for j in range(n)] # Empirical return periods of observed data
        
        Go[0]=(1-a)/(n+1-2*a)
        for i in range(1,n-1):
            if datao[i]!=datao[i+1]:
                Go[i]=(1+i-a)/(1+n-2*a)          
            else:
                Go[i]=(1+i+1-a)/(1+n-2*a)         
            if datao[i]==datao[i-1]:
                Go[i-1]=Go[i]         
        Go[n-1]=(n-a)/(1+n-2*a)
        if datao[n-1]==datao[n-2]:
            Go[n-2]=Go[n-1]  
        Fo=1-np.array(Go)

        if i1==1:
            To=1/np.array(Go)
        else:
            To=1/np.array(Fo)    

        o,bedge=np.histogram(datao,bins=nbin) # histogram
        F1bc=[0 for j in range(nbin)] # probability of each bin in Theoretical Distribution 1
        npn1=[0 for j in range(nbin)] # Expected numbers in regrouped bins (2022.02.09)
        on1=[0 for j in range(nbin)] # Observed numbers in regrouped bins (2022.02.09)
        F2bc=[0 for j in range(nbin)] # probability of each bin in Theoretical Distribution 2
        npn2=[0 for j in range(nbin)] # Expected numbers in regrouped bins (2022.02.09)
        on2=[0 for j in range(nbin)] # Observed numbers in regrouped bins (2022.02.09) 
        bc=[0 for j in range(nbin)] # bin centers

    # 2) Various y (reduced variate) values
    Tt=np.array(Tt)

    if i2==2:
        Tti[0]=min(Tti[0],To[n-1])
        Tti[len(Tti)-1]=max(Tti[len(Tti)-1],To[0])
    Tmat[0]=Tti[0]

    Tr=[Tti[0],Tti[len(Tti)-1]] # range of return periods for plotting

    if i1==1:
        if i2==2:
            yo=-np.log(np.log(np.array(To)/(np.array(To)-1))) # emperical y of observed data
        yTt=-np.log(np.log(Tt/(Tt-1)))
        yTti=-np.log(np.log(np.array(Tti)/(np.array(Tti)-1)))
        yTmat=-np.log(np.log(np.array(Tmat)/(np.array(Tmat)-1)))
        yTmit=-np.log(np.log(np.array(Tmit)/(np.array(Tmit)-1)))
        yr=-np.log(np.log(np.array(Tr)/(np.array(Tr)-1))) # range of y for plotting   
    if i1==2:
        if i2==2:
            yo=np.log(np.log(np.array(To)/(np.array(To)-1))) # emperical y of observed data
        yTt=np.log(np.log(Tt/(Tt-1)))
        yTti=np.log(np.log(np.array(Tti)/(np.array(Tti)-1)))
        yTmat=np.log(np.log(np.array(Tmat)/(np.array(Tmat)-1)))
        yTmit=np.log(np.log(np.array(Tmit)/(np.array(Tmit)-1)))
        yr=np.log(np.log(np.array(Tr)/(np.array(Tr)-1))) # range of y for plotting   
        
    yTmatl = FixedLocator(yTmat)
    yTmitl = FixedLocator(yTmit)

    PTmat=1/np.array(Tmat) # Probability corresponding to T in plotting 
    PTmat[0]=round(PTmat[0],4)  

    # 3) A limiting distribution with an infinite n
    scale1=sdx*np.sqrt(6)/math.pi
    if i1==1:
        mode1=meanx-sdx*0.5772*np.sqrt(6)/math.pi
    if i1==2:
        mode1=meanx+sdx*0.5772*np.sqrt(6)/math.pi

    xr1=np.array(yr)*scale1+mode1 # range of x for plotting
    xTt1=yTt*scale1+mode1 # really needed? Can it be read from xr1?

    Var=scale1**2*(1.11+0.52*yTt+0.61*yTt**2)/n # This is for maxima analysis. Still applicable to the minimum?
    #Var=scale**2*((1.1128-0.9066/n)-(0.4574-1.1722/n)*yTt+(0.8046-0.1855/n)*yTt**2)/(n-1) 
    xTt1u=xTt1+zp*np.sqrt(Var) # confidence limit
    xTt1l=xTt1-zp*np.sqrt(Var) # confidence limit

    if i2==2:
        x1o=(xr1[1]-xr1[0])*(np.array(yo)-yr[0])/(yr[1]-yr[0])+xr1[0] # theoretical values at To
        cm1=np.corrcoef(datao,x1o) # Correlation matrix between observed data and theoretical values 
        R1=cm1[0,1] # Correlation coefficient between observed data and theoretical values

    # 4) A distribution with the actual n
    if i1==1:
        Kr=(np.array(yr)-0.5775/n**(0.66/n))*n**(1.268/n)/1.2811
        KTt=(yTt-0.5775/n**(0.66/n))*n**(1.268/n)/1.2811 # really needed?
    if i1==2:
        Kr=(np.array(yr)+0.5775/n**(0.66/n))*n**(1.268/n)/1.2811
        KTt=(yTt+0.5775/n**(0.66/n))*n**(1.268/n)/1.2811 #  
    xr2=meanx+np.array(Kr)*sdx   
    xTt2=meanx+KTt*sdx 

    scale2=sdx*n**(1.268/n)/1.2811 # 20220204
    if i1==1:
        mode2=meanx-scale2*0.5775/n**(0.66/n)
    if i1==2:
        mode2=meanx+scale2*0.5775/n**(0.66/n)

    Var=scale2**2*(1.11+0.52*yTt+0.61*yTt**2)/n # 20220204
    xTt2u=xTt2+zp*np.sqrt(Var) # confidence limit
    xTt2l=xTt2-zp*np.sqrt(Var) # confidence limit

    if i2==2:         
        x2o=(xr2[1]-xr2[0])*(np.array(yo)-yr[0])/(yr[1]-yr[0])+xr2[0] # theoretical values at To
        cm2=np.corrcoef(datao,x2o) # Correlation matrix between observed data and theoretical values 
        R2=cm2[0,1] # Correlation coefficient between observed data and theoretical values 

    # 5) Goodness of Fit 
    if i2==2:
        # Kolmogorov-Smirnov Test
        if i1==1:
            F1o=1/np.exp(np.exp(-np.array((yr[0]+(yr[1]-yr[0])*(np.array(datao)-xr1[0])/(xr1[1]-xr1[0]))))) # Theoretical CDF at observed values (the limiting distribution)
            F2o=1/np.exp(np.exp(-np.array((yr[0]+(yr[1]-yr[0])*(np.array(datao)-xr2[0])/(xr2[1]-xr2[0]))))) # Theoretical CDF at observed values (the distribution with the actual n)
        if i1==2:
            F1o=1-1/np.exp(np.exp(np.array((yr[0]+(yr[1]-yr[0])*(np.array(datao)-xr1[0])/(xr1[1]-xr1[0]))))) # Theoretical CDF at observed values (the limiting distribution)
            F2o=1-1/np.exp(np.exp(np.array((yr[0]+(yr[1]-yr[0])*(np.array(datao)-xr2[0])/(xr2[1]-xr2[0]))))) # Theoretical CDF at observed values (the distribution with the actual n)
        KS1=max(abs(np.array(Fo-F1o))) # Kolmogorov-Smirnov Test Statistic the limiting distribution
        KS2=max(abs(np.array(Fo-F2o))) # Kolmogorov-Smirnov Test Statistic for the distribution with the actual n

        # Chi-Squared Test  
        if n>=nlC2:
            for i in range(1,nbin+1): 
                if i1==1:
                    F1bc[i-1]=1/np.exp(np.exp((mode1-bedge[i])/scale1))-1/np.exp(np.exp((mode1-bedge[i-1])/scale1)) #2022.02.08
                    npn1[i-1]=F1bc[i-1]*n# 2022.02.09             
                    F2bc[i-1]=1/np.exp(np.exp((mode2-bedge[i])/scale2))-1/np.exp(np.exp((mode2-bedge[i-1])/scale2)) #2022.02.08
                    npn2[i-1]=F2bc[i-1]*n# 2022.02.09             
                if i1==2:
                    F1bc[i-1]=1/np.exp(np.exp((bedge[i-1]-mode1)/scale1))-1/np.exp(np.exp((bedge[i]-mode1)/scale1)) #2022.02.08
                    npn1[i-1]=F1bc[i-1]*n# 2022.02.09
                    F2bc[i-1]=1/np.exp(np.exp((bedge[i-1]-mode2)/scale2))-1/np.exp(np.exp((bedge[i]-mode2)/scale2)) #2022.02.08
                    npn2[i-1]=F2bc[i-1]*n# 2022.02.09
                on1[i-1]=o[i-1]#
                on2[i-1]=o[i-1]# 2022.02.09
        
            for i in range(1,nbin+1):# 2022.02.09
                ii=1 # 2022.02.09
                if npn1[i-1]>0:# 2022.02.09
                    while npn1[i-1]<npl:# 2022.02.09
                        if i-1+ii>nbin-1:# 2022.02.09
                            break# 2022.02.09
                        npn1[i-1]=npn1[i-1]+npn1[i-1+ii]# 2022.02.09
                        on1[i-1]=on1[i-1]+on1[i-1+ii]# 2022.02.09
                        npn1[i-1+ii]=0# 2022.02.09
                        on1[i-1+ii]=0# 2022.02.09
                        ii=ii+1# 2022.02.09
                    
                ii=1 # 2022.02.09
                if npn2[i-1]>0:# 2022.02.09
                    while npn2[i-1]<npl:# 2022.02.09
                        if i-1+ii>nbin-1:# 2022.02.09
                            break# 2022.02.09
                        npn2[i-1]=npn2[i-1]+npn2[i-1+ii]# 2022.02.09
                        on2[i-1]=on2[i-1]+on2[i-1+ii]# 2022.02.09
                        npn2[i-1+ii]=0# 2022.02.09
                        on2[i-1+ii]=0# 2022.02.09
                        ii=ii+1# 2022.02.09
                    
            for i in range(1,nbin+1):# 2022.02.09
                ii=1 
                if npn1[nbin-i]>0:# 2022.02.09
                    while npn1[nbin-i]<npl:# 2022.02.09
                        if nbin-i-ii<0:# 2022.02.09
                            break# 2022.02.09
                        npn1[nbin-i]=npn1[nbin-i]+npn1[nbin-i-ii]# 2022.02.09
                        on1[nbin-i]=on1[nbin-i]+on1[nbin-i-ii]# 2022.02.09
                        npn1[nbin-i-ii]=0# 2022.02.09
                        on1[nbin-i-ii]=0# 2022.02.09
                        ii=ii+1# 2022.02.09
        
                ii=1 
                if npn2[nbin-i]>0:# 2022.02.09
                    while npn2[nbin-i]<npl:# 2022.02.09
                        if nbin-i-ii<0:# 2022.02.09
                            break# 2022.02.09
                        npn2[nbin-i]=npn2[nbin-i]+npn2[nbin-i-ii]# 2022.02.09
                        on2[nbin-i]=on2[nbin-i]+on2[nbin-i-ii]# 2022.02.09
                        npn2[nbin-i-ii]=0# 2022.02.09
                        on2[nbin-i-ii]=0# 2022.02.09
                        ii=ii+1# 2022.02.09
            
            C21=0# Chi-Squared Test Statistic (2022.02.09)
            C22=0# Chi-Squared Test Statistic (2022.02.09)
            for i in range(1,nbin+1):# 2022.02.09
                if npn1[i-1]>0:# 2022.02.09
                    C21=C21+(on1[i-1]-npn1[i-1])**2/npn1[i-1] # 2022.02.09
                if npn2[i-1]>0:# 2022.02.09
                    C22=C22+(on2[i-1]-npn2[i-1])**2/npn2[i-1] # 2022.02.09            

    # Result Illustrations
    note1 =[]
    note2 = []
    note3 = []
    note4 = []
    note5 = []
    data3 = ()
    data4 = ()
    data5 = ()
    heading1 = ''
    heading2 = ''
    ending = ''
    plot_url = ''
    # test4 = 'Return Period '
    # test5 =  'Value '+'('+unitx+')'
    # test6 = '---Frequency Analysis by Gumbel Distribution---'
    # test7 = 'By the limiting distribution'
    # test8 = 'By a distribution based on a finite record length'
    # test10 = '('+unitt+')'
    # print('Return Period (',unitt,')','                 Value (',unitx,')')
    #print('                     ',' 1)By the limiting distribution,','  2)By a distribution based on a finite record length')
    if n<nmin:
        if i1==1:
            note_1_1 = '--- Gumbel分布频率分析（最大值模式）---'
        if i1==2:
            note_1_1 = '--- Gumbel分布频率分析（最小值模式）---'
        note_1_2 = ''    
        note_1_3 = '说明：由于样本容量小于'+str(nmin)+'，频率分析未进行。'
        note_1_4 = ''
        note1.append(note_1_1)
        note1.append(note_1_2)
        note1.append(note_1_3)
        note1.append(note_1_4)
    else:
        if i2==1:
            note_2_1 = '--------- 所提供的样本基本统计特征 ---------'
            note2.append(note_2_1)     
        if i2==2:
            note_2_1 = '-------- 样本统计(基于整个样本序列）---------'
            note2.append(note_2_1)        
        note_2_2 = '均值 = '+str(round(meanx,2))+' '+str(unitx)
        note_2_3 = '均方差 = '+str(round(sdx,2))+' '+str(unitx)
        note2.append(note_2_2)
        note2.append(note_2_3)   
        if i2==2:
            note_2_4 = ' 偏态系数 = '+str(round(Csx,2))
            note2.append(note_2_4)
        note_2_5 = ' 样本容量 = '+str(n)
        note2.append(note_2_5) 
        
        if i1==1:
            note_3_1 = '------ Gumbel分布频率分析（最大值模式）------'
            note3.append(note_3_1)
        if i1==2:
            note_3_1 = '------ Gumbel分布频率分析（最小值模式）------'
            note3.append(note_3_1)
        
        heading1 = '极限理论Gumbel分布'
        heading2 = '基于样本容量的理论Gumbel分布'

        note_3_2 = '1) 不同回归期下的取值'
        note_3_3 = '回归期'+' '+'('+str(unitt)+')'
        note_3_4 = str(pq)+' '+'('+str(unitx)+')'
        note3.append(note_3_2)
        note3.append(note_3_3)
        note3.append(note_3_4)
        # for i in range(1,len(Tt)+1):
        #     print(Tt[i-1],'                                 ',round(xTt1[i-1],2),'                         ',round(xTt2[i-1],2))
        # print(' ')
        for i in range(1,len(Tt)+1):
            data3 += ((str(Tt[i-1]),str(round(xTt1[i-1],2)),str(round(xTt2[i-1],2))),)
        
        note_4_1 = '2) 分布参数'
        note4.append(note_4_1)
        data4 += (('位置系数',str(round(mode1,3)),str(round(mode2,3))),)
        data4 += (('尺度系数',str(round(scale1,3)),str(round(scale2,3))),)
        # print(' ') 

        if i2==2:  
            note_5_1 = '3) 拟合检验'
            note5.append(note_5_1)
            data5 += (('Kolmogorov-Smirnov 检验值',str(round(KS1,3)),str(round(KS2,3))),)
            if n>=nlC2:
                data5 += (('Chi-Squared 检验值',str(round(C21,3)),str(round(C22,3))),)
            else:
                data5 += (('Chi-Squared 检验值','无 (因为样本容量小于'+str(nlC2)+')','无'),)
            # print('')#20220310
        ending ='---结果展示结束---'#20220310
            # data=()
            # for i in range(1,len(Tt)+1):
            #     data+=((str(Tt[i-1]),str(round(xTt1[i-1],2)),str(round(xTt2[i-1],2))),)

        ax=plt.axes()
        ax.xaxis.set_major_locator(yTmatl)
        yTmatf = FixedFormatter(Tmat)
        ax.xaxis.set_major_formatter(yTmatf)

        ax.xaxis.set_minor_locator(yTmitl)
        ax.xaxis.set_minor_formatter(plt.NullFormatter())

        plt.xlabel('回归期 ('+str(unitt)+')')
        plt.ylabel(str(pq)+' ('+str(unitx)+')')
        plt.plot(yr,xr1,label="极限理论Gumbel分布",color="red",linewidth=2)
        plt.plot(yTt,xTt1u,label="极限理论分布90%置信限",color="red",linewidth=1.5,linestyle=":")
        plt.plot(yTt,xTt1l,color="red",linewidth=1.5,linestyle=":")
        plt.plot(yr,xr2,label="基于样本容量的理论Gumbel分布",color="blue",linewidth=2,linestyle="--")
        plt.plot(yTt,xTt2u,label="基于样本容量的理论分布90%置信限",color="blue",linewidth=1.5,linestyle=":")
        plt.plot(yTt,xTt2l,color="blue",linewidth=1.5,linestyle=":")
        if i2==2:
            plt.scatter(yo,datao,c="white",marker="o",s=20,edgecolors="black",label="样本值 ")
            if i1==1:
                plt.scatter(-np.log(np.log(2.3276/(2.3276-1))),meanx,c="red",marker="o",s=20,edgecolors="red",label="样本均值")# (return period = 2.33 at the limiting distribution)")
            else:
                plt.scatter(np.log(np.log(2.3276/(2.3276-1))),meanx,c="red",marker="o",s=20,edgecolors="red",label="样本均值")# (return period = 2.33 at the limiting distribution)")

        plt.xlim([yr[0], yr[1]])
        plt.tick_params(labelbottom=True,labelright=True,direction="in")
        plt.grid(color="black",alpha=.8,linewidth=1,linestyle="--")
        ax.tick_params(which="minor", axis="x", direction="in")
        plt.grid(which="minor", axis="x",color="black",alpha=.4,linewidth=1,linestyle="--")

        secax = ax.secondary_xaxis('top')
        if i1==1:
            secax.set_xlabel('超越概率')
        if i1==2:
            secax.set_xlabel('累积分布函数')
            
        secax.xaxis.set_major_locator(yTmatl)
        PTmatl = FixedFormatter(PTmat)
        secax.xaxis.set_major_formatter(PTmatl)
        secax.tick_params(direction="in")

        plt.legend()
        plt.rcParams['font.sans-serif'] = ['KaiTi']#FangSong
        # plt.show()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close("all")
        # return plot_url
    return plot_url, note1, note2, note3, data3, note4, data4, note5, data5, heading1, heading2, ending