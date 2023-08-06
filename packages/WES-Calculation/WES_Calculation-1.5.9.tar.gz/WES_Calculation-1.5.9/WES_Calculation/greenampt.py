'''
Author: BDFD
Date: 2022-03-01 17:28:34
LastEditTime: 2022-04-24 08:09:55
LastEditors: BDFD
Description: 
FilePath: \5.2-PyPi-WES_Calculation\WES_Calculation\greenampt.py
'''

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter
import numpy as np
from numpy import *
# import statistics
import io
import base64

# Effective Rainfall Generation   
# # Primary Inputs (required)
# # thetar = float(request.form["thetar"]) # Residual soil moisture content (It can be assumed to be zero, if no actual value is avaiulable.)
# thetai = float(request.form["thetai"] )# Initial soil moisture content
# thetas = float(request.form["thetas"] )# Soil moisture content at saturation (i.e. porosity)
# Psi = float(request.form["psi"]) # Suction head (m)
# K = float(request.form["k"]) # Saturated hydraulic conductivity (cm/h)
# tol = 0.00001
# toln= 0.00001
# dti= float(request.form["dti"]) #6 time interval in the analysis, normally that used in hyetograph (min)
# nin= int(request.form["nin"])# The number of time intervals to be considered in the anlysis
# iyesno = int(request.form["iyesno"]) # Whether to generate an effective hyetograph (0: No; 1: Yes)
# # test1 = request.form["thetar"]
# test2 = request.form["thetai"]
# test3 = request.form["thetas"]
# test4 = request.form["psi"]
# test5 = request.form["k"]
# # test6 = request.form["tol"]
# test7 = request.form["dti"]
# test8 = request.form["nin"]
# test9 = None
# test10 = None
# yesono = request.form["iyesno"]
# if iyesno == 1:
#     test9 = request.form["dd"]
#     test10 = request.form["i"]
#     dd = float(request.form["dd"])# Depression depth used in generating an effective hyetograph (mm), which has to be zero when iyesno=0.
#     result = request.form["i"] # Hyetograph (mm/h) (The first value covers the period between time 0 and time 0+dti.)
#     res = result.split(",")
#     i = list(map(float, res))
#     #if sum(i)*dti/60<dd: # (20121226)
#         #print('说明：') # (20121226)
#         #print('1. 降雨量不足以蓄满地表的坑洼，故没有净雨产生，也不会有下渗产生。') # (20121226)
#         #sys.exit(0) # (20121226)
    
# if iyesno==0:
#     i=[0 for k in range(nin)]# Hyetograph (mm/h) (The first value covers the period between time 0 and time 0+dti.)
#     dd=0                


def greenampt(thetai, thetas, Psi, K, dti, nin, dd, i, iyesno, ss1, ss2, ss3):
# Secondary Inputs (default)
    tol=0.00001 # 0.00001Iteration tolerance in calculating infiltration quantity (F) (Note: iteration results are sensitive to tol, and a small tol value is preferred.)   
    Tpu=10000 # an imaginary ponding time when i = 0 or i<=K (min)
    toln=0.00001 # Numeric tolerance.(For example, a number will become zero if smaller then this toln, to prevent a very very small, negative rainfall intensity, such as -1.7763568394002505e-15) 2022.03.10   
    
    nini=len(i)
    if nin>nini:
        i=np.concatenate((i,[0 for k in range(nin-nini)])) # Extend i with zero intensities 

    fpo=[0 for k in range(len(i)+2)] # Theoretical potential infiltration rate (m/h)
    fpu=[0 for k in range(len(i)+1)] # Updated potential infiltration rate (m/h)
    f=[0 for k in range(len(i)+1)] # Actual infiltration rate (m/h)
    Fpo=[0 for k in range(len(i)+2)] # Theoretical potential infiltration quantity (m)
    F=[0 for k in range(len(i)+1)] # Actual infiltration quantity (m)
    
    dtheta=thetas-thetai
    if dtheta==0: # (20211227)  
        ddtheta=dtheta+toln # a dummy dtheta to be used as denominator when dtheta = 0 (20211227)  
        fpo[0]=K/100 # (20211227)  
        fpu[0]=fpo[0] # (20211227)  
    else:
        ddtheta=dtheta # simply dtheta to be used as denominator when dtheta is not equal to 0 (20211227) 
        fpo[0]='Inf' # (20211227)  
        fpu[0]='Inf' # (20211227)  
            
    #fpo[0]='Inf'
    #fpu[0]='Inf'

    # 1. Hyetograph

    t1=np.linspace(0,dti*(len(i)-1),len(i))
    ie=[0 for k in range(len(i))] # Effective hyetograph (mm/h)

    fig,ax1 = plt.subplots()
    if max(i)>0:
        #ax1.bar(t1,i,width=dti,label="Hyetograph",color="lightblue",align='edge')
        ax1.bar(t1,i,width=dti,label=u"降雨强度过程（整个柱状图）",color="aqua",align='edge',alpha=1,zorder=1)

    #ax1.set_xlabel("Time (min)")
    ax1.set_xlabel(u"时间 (minutes)")
    ax1.set_ylabel("雨强或入渗率 (mm/h)") 
    #ax1.set_ylabel("数值 (mm/h)") 

    # 2. Depression Storage
    j=0
    Td=0 # The time to meet the depression depth (min)
    dda=0 # An assumed depression depth (mm)#20220313

    if dd>0:
        while dda<dd:
            if j==0:
                #ax1.bar(t1[j],i[j],width=dti,label="Depression Rate",color="darkgrey",hatch='/',align='edge',alpha=1)
                ax1.bar(t1[j],i[j],width=dti,label="地表坑洼的充填速率",color="aqua",hatch='x',edgecolor='black',align='edge',alpha=0.2,linewidth=.0,zorder=2)
            else:
                ax1.bar(t1[j],i[j],width=dti,color="aqua",hatch='x',edgecolor='black',align='edge',alpha=0.2,linewidth=0.0,zorder=2)
                
            if dtheta==0: # (20211227)  
                fpo[j]=K/100 # (20211227)  
                fpu[j]=fpo[0] # (20211227)  
            else:
                fpo[j]='Inf' # (20211227)  
                fpu[j]='Inf' # (20211227)  

            Fpo[j]=0
            ie[j]=0
            dda=dda+i[j]*dti/60 # Updated dda (mm)
            j=j+1
        
        Td=dti*j-60*(dda-dd)/i[j-1] # Updated Td (min) (revised on 20211226)
        
        ax1.bar(Td,i[j-1],width=60*(dda-dd)/i[j-1],color="aqua",align='edge',alpha=1,zorder=3)
        ax1.axvline(Td,ls="--",color="black",linewidth=0.5,zorder=4)
        extraticks=[Td]
        plt.xticks(list(plt.xticks()[0]) + extraticks)

        if dda>dd:
            j=j-1 # Index will return to the beginning of the terminal period of the depression when Td is not at a time node
                # Otherwise, Index will stay at the time node when dd is met
            # Index will return to the beginning of the terminal period of the depression when Td is not at a time node
            # Otherwise, Index will stay at the time node when dd is met
            # If needed, both fpo[j] and fpu[j] at the time node corresponding to j will be used for the time moment of Td, which is later than the time node j. This way
            # will not cause any impact, for infiltration has not started, and both fpo and fpu keep their original state. (20220312)
        else:# (20220311)  
            if dtheta==0: # (20220311)  
                fpo[j]=K/100 # It simply equals K. (20220311)  
                fpu[j]=fpo[0] # It simply equals K. It keeps unchanged until i < K, different from fpo. (20220311)  
            else:
                fpo[j]='Inf' # It keeps unchanged until infiltration can start theoretically.(20220311)  
                fpu[j]='Inf' # It keeps unchanged until actual infiltration starts, different from fpo. (20220311)

    # 3. Infiltration  

    # 3.1 During the time interval where the depression terminates  

    Fa=K*0.01*(dti*(j+1)-Td)/60 # An assumed value for F (m)
    Fc=K*0.01*(dti*(j+1)-Td)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) # An iterated value for F (m) (revised on 20121226)

    while (abs(Fa-Fc)>tol):
        Fa=0.5*(Fa+Fc) # Updated Fa in iteration (m)
        Fc=K*0.01*(dti*(j+1)-Td)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) # Updated Fc in iteration (m) (revised on 20121226)
    
    Fpo[j+1]=Fc
    fpo[j+1]=K*0.01*(1+Psi*dtheta/Fc)

    if i[j]>0:#20220311
        #f[j]=(dtheta>0)*i[j]/1000+(dtheta==0)*K/100 #20220311
        f[j]=(dtheta>0)*i[j]/1000+(dtheta==0)*min(K/100,i[j]/1000) #20220312
    else:#20220311
        f[j]=0  #20220311

    # f[j]=(dtheta>0)*i[j]/1000+(dtheta==0)*K/100 #20211226  
    # Under the unbsaturated condition, since the initial infiltration rate is infinite, the first rainfall intensity is used as the actual infiltration rate.
    # Under the saturated condition, the actual infiltration rate simply equals the saturated hydraulic conductivity.
    # This f[j] is intended for the time node at Td, which may be later than the time node corresponding to j.
    F[j]=0#f[j-1]*(dti*j-Td)/60
    # Under the unbsaturated condition, since the initial infiltration rate is infinite, the first rainfall intensity is used as the actual infiltration rate.
    # Under the saturated condition, the actual infiltration rate equals the minimun of the saturated hydraulic conductivity and the actual rainfall intensity. (20220312)
    # The f[j] and F[j] here are intended for the time moment of Td, which may be later than the time node corresponding to j. (20220312)
    # The i[j] here is for the time node corresponding to j. 

    if i[j]>K*10:#20220312
        Tp=60*(K*10*Psi*1000*dtheta/(i[j]-K*10)-1000*F[j])/i[j] # Ponding time (min)
    else:
        Tp=Tpu
    
    if Tp>=(dti*(j+1)-Td):
        F[j+1]=f[j]*(dti*(j+1)-Td)/60
        if F[j+1]>0:
            fpu[j+1]=K*0.01*(1+Psi*dtheta/F[j+1])
        else:
            fpu[j+1]=fpu[j]#????20220311
            
    else:
        FTt=f[j]*Tp/60
        timertt=60*(FTt-Psi*dtheta*np.log(1+FTt/Psi/ddtheta))/K/0.01 # equivalent spent time to reach the turning point since the infiltration beginning (revised on 20121226)
        Fc=K*0.01*(timertt+dti-Tp)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) # An iterated value for F (m)(revised on 20121226)
        while (abs(Fa-Fc)>tol):
            Fa=0.5*(Fa+Fc) # Updated Fa in iteration (m)
            Fc=K*0.01*(timertt+dti-Tp)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) # Updated Fc in iteration (m) #20211226
        Fc=K*0.01*(timertt+dti*(j+1)-Td-Tp)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) # Updated Fc in iteration (m) #20220311
        # F[j+1]=Fc #?
        if 1000*(Fc-FTt)<i[j]*(dti*(j+1)-Td-Tp)/60:#20220311 
            F[j+1]=Fc#20220311
        else:#20220311
            F[j+1]=i[l]*(dti*(j+1)-Td-Tp)/60/1000+FTt#20220311  

        if dtheta>0: #2022.03.11     
            ietx,iety=[Td+Tp,dti*(j+1),dti*(j+1),Td+Tp],[i[j],i[j]-2*(dti*(j+1)-Td)*(i[j]-1000*60*(F[j+1]-F[j])/(dti*(j+1)-Td))/(dti*(j+1)-Td-Tp),i[j],i[j]]#A triangle for net rainfall (2022.03.10)
            if iety[0]>iety[1]:#20220311
                # plt.fill(ietx,iety,color="lightblue",linewidth=0.5,zorder=3)#2022.03.10   
                plt.fill(ietx,iety,color="aqua",linewidth=0,zorder=5,alpha=1)#2022.03.11
                ss2=1
        if F[j+1]>0:
            fpu[j+1]=K*0.01*(1+Psi*dtheta/F[j+1])
        else:
            # fpu[j+1]=fpo[j+1]
            fpu[j+1]=fpu[j]#20220313
    
    tin=60*(F[j+1]-Psi*dtheta*np.log(1+F[j+1]/Psi/ddtheta))/K/0.01 # a timer for subsequent infiltration calculation (min) (revised on 20121226)

    #ie[j]=i[j]-1000*f[j]
    ie[j]=i[j]-1000*60*(F[j+1]-F[j])/(dti*(j+1)-Td) 
    if abs(ie[j])<toln: # 2022.03.10
        ie[j]=0 # 2022.03.10

    if max(i)>0:
        #ax1.bar(Td,1000*f[j],width=(dti*(1+j)-Td),label="Actual Infiltration Rate",color="sandybrown",align='edge',alpha=.5)
        #ax1.bar(Td,1000*f[j],width=(dti*(1+j)-Td),label="实际入渗率",color="sandybrown",align='edge',alpha=.5)
        ax1.bar(Td,1000*f[j],width=(dti*(1+j)-Td),label="实际入渗率",color="steelblue",edgecolor='black',align='edge',alpha=0.75,linewidth=0.0,zorder=4)
    data=()
    
    if iyesno==1:
        if dd==0:
            data+=((str(j*dti),str(round(ie[j],2))),)
        else:
            data+=(('0','0'),)
            if dda>dd:   
                data+=((str(round(Td,1)),str(round(ie[j],2))),)
            else:  
                data+=((str(j*dti),str(round(ie[j],2))),)
    
    # 3.2 During every following time interval
    
    for l in range(j+1,len(i)):
        # f[l]=min(fpu[l],i[l]/1000)
        if fpu[l]=='Inf':#20220311
            #f[l]=i[l]/1000#20220311
            f[l]=(dtheta>0)*i[l]/1000+(dtheta==0)*min(K/100,i[l]/1000) #20220313
            dfpu=i[l]+toln #a dummy fpu for comparision purposes 20220311
        else:        #20220311
            f[l]=min(fpu[l],(dtheta>0)*i[l]/1000+(dtheta==0)*min(K/100,i[l]/1000))#20220313
            dfpu=fpu[l] #a dummy fpu for comparision purposes 20220311
        Fc=K*0.01*(dti*(l+1)-Td)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226)      
        while (abs(Fa-Fc)>tol):
            Fa=0.5*(Fa+Fc)
            Fc=K*0.01*(dti*(l+1)-Td)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226) 
        fc=K*0.01*(1+Psi*dtheta/Fc)
        # Fpo[l+1]=Fc
        # fpo[l+1]=fc #m/h
        Fpo[l+1]=Fc
        fpo[l+1]=K*0.01*(1+Psi*dtheta/Fc)#fc #m/h #20220313

        tin=tin+dti
        
        if dfpu<=i[l]/1000:##20211226   
            Fc=K*0.01*tin/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226)
            while (abs(Fa-Fc)>tol):
                Fa=0.5*(Fa+Fc)
                Fc=K*0.01*tin/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226)
            # fc=K*0.01*(1+Psi*dtheta/Fc)    
            F[l+1]=Fc
            # fpu[l+1]=fc
            fpu[l+1]=K*0.01*(1+Psi*dtheta/Fc) #fc#20220313
        else: 
    
            if i[l]>K*10:#20220313
                Tp=60*(K*10*Psi*1000*dtheta/(i[l]-K*10)-1000*F[l])/i[l]
                
            else:
                Tp=Tpu
        
            if Tp>=dti:
                F[l+1]=i[l]*dti/60/1000+F[l]
                
            else: # this part addresses the scenario where a rainfall intensity goes across the infiltration potential curve 
                
                FTt=i[l]*Tp/60/1000+F[l]
                timertt=60*(FTt-Psi*dtheta*np.log(1+FTt/Psi/ddtheta))/K/0.01 # equivalent spent time to reach the turning point since the infiltration beginning #(revised on 20121226)
                Fc=K*0.01*(timertt+dti-Tp)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) # An iterated value for F (m) #(revised on 20121226)
                while (abs(Fa-Fc)>tol):
                    Fa=0.5*(Fa+Fc) # Updated Fa in iteration (m)
                    Fc=K*0.01*(timertt+dti-Tp)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226)
                # F[l+1]=Fc  
                # ietx,iety=[dti*l+Tp,dti*(l+1),dti*(l+1),dti*l+Tp],[i[l],i[l]-2*dti*(i[l]-1000*60*(F[l+1]-F[l])/dti)/(dti-Tp),i[l],i[l]]#A triangle for net rainfall (2022.03.10)
                # plt.fill(ietx,iety,color="lightblue",linewidth=0.5,zorder=3)#2022.03.10         
                if 1000*(Fc-FTt)<i[l]*(dti-Tp)/60:#20220311 
                    F[l+1]=Fc#20220311
                else:#20220311
                    F[l+1]=i[l]*(dti-Tp)/60/1000+FTt#20220311            
                if dtheta>0: #20220311                 
                    ietx,iety=[dti*l+Tp,dti*(l+1),dti*(l+1),dti*l+Tp],[i[l],i[l]-2*60*(i[l]*(dti-Tp)/60-1000*(F[l+1]-FTt))/(dti-Tp),i[l],i[l]]#A triangle for net rainfall (2022.03.10)
                    if iety[0]>iety[1]:#20220311
                        plt.fill(ietx,iety,color="aqua",linewidth=0,zorder=5,alpha=1)#2022.03.11
                        ss2=1
            if F[l+1]>0:
                fpu[l+1]=K*0.01*(1+Psi*dtheta/F[l+1])
            else:
                # fpu[l+1]=fpo[l+1]
                fpu[l+1]=fpu[l]#20220311 
    
            tin=60*(F[l+1]-Psi*dtheta*np.log(1+F[l+1]/Psi/ddtheta))/K/0.01 # Uptated tin #(revised on 20121226)
    
        #ie[l]=i[l]-1000*f[l]
        ie[l]=i[l]-1000*60*(F[l+1]-F[l])/dti
        if abs(ie[l])<toln: # 2022.03.10
            ie[l]=0 # 2022.03.10

        if max(i)>0:
            ax1.bar(t1[l],1000*f[l],width=dti,color="steelblue",edgecolor='black',align='edge',alpha=0.75,linewidth=0.0,zorder=4)
        if iyesno==1:
            data += ((str(l*dti),str(round(ie[l],2))),)
        
    # Plotting

    Fc=K*0.01*(dti*(l+2)-Td)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226)     
    while (abs(Fa-Fc)>tol):
        Fa=0.5*(Fa+Fc)
        Fc=K*0.01*(dti*(l+2)-Td)/60+Psi*dtheta*np.log(1+Fa/Psi/ddtheta) #(revised on 20121226)
    fc=K*0.01*(1+Psi*dtheta/Fc)
    Fpo[l+2]=Fc
    fpo[l+2]=K*0.01*(1+Psi*dtheta/Fc)#fc  #20220313

    #ax1.plot(np.linspace(t1[j+1],dti*(l+1),l-j+1),1000*np.array(fpo[j+1:l+2]),label="Theoretical Infiltration Potential",ls="--",color="green",linewidth=1)
    ax1.plot(np.linspace(t1[j+1],dti*(l+1),l-j+1),1000*np.array(fpo[j+1:l+2]),label="理论入渗率",ls="--",color="orange",linewidth=1.5,zorder=5)
    
    if max(i)>0:
        for jj in range(j+1,l+2):#20220313      
            if fpu[jj]!='Inf' and F[jj]>0:#20220313
                #ax1.plot(np.linspace(t1[j+1],dti*(l+1),l-j+1),1000*np.array(fpu[j+1:l+2]),label="Updated Infiltration Potential",color="red",linewidth=1)
                ax1.plot(np.linspace(t1[jj],dti*(l+1),l-jj+2),1000*np.array(fpu[jj:l+2]),label="修正后的潜势入渗率",color="red",linewidth=1,zorder=5)
                break
    if dtheta==0: # (20211227)  
        ax1.hlines(1000*fpo[j],Td,t1[j+1],ls="--",color="orange",linewidth=1,zorder=5) # (20211227)  
        if max(i)>0 and F[j+1]>0:# (20211227)     
            ax1.hlines(1000*fpu[j],Td,t1[j+1],color="red",linewidth=1,zorder=5)# (20211227)
    
    plt.xlim(0,dti*len(i))
    ax1.legend()
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams["font.family"]="sans-serif"
    #plt.rcParams['axes.unicode_minus'] = False
    #mpl.rcParams['axes.unicode_minus'] = False
    #matplotlib.rc('font', family='FangSong')
    #mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei'] 
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    interval = str(dti)
    sminute = str(round(Td,1))
    eminute = str((j+1)*dti)
    #eff = "---Effective Rainfall Generated by Green-Ampt Infiltration Method---"
    eff = "---按Green-Ampt下渗模型生成的净雨过程---"
    #str1 = "2. Unless noted otherwise, an intensity lasts for a full time interval (= "+interval+" minutues), starting from the corresponding time moment."
    #note = ["Notes:","1. The lightblue portion in the figure shows the effective rainfall.",str1]
    note = [ ]
    note2 = [ ]
    if iyesno == 1:
        note_0 = "说明:"
        note_1 = "1. 在图中，降雨强度过程实为整个柱状图（原本为浅蓝色），但可能局部或全部被实际入渗率（深蓝色）或地表坑洼充填速率（带叉的浅蓝色）所覆盖。"
        # note_1 = "1. 为与降雨强度过程相比较，下渗率按柱状图表示，某时刻的下渗率会显示在接下来的整个时间步长内。"
        note_2 = "2. 无论是对于实际降雨还是净雨，除非特殊说明，一个雨强值从对应的时刻开始，会持续整个时间步长 (= "+interval+" minutes)。"
        # note_2 = "2. 除非特殊说明，一个降雨强度值从对应的时刻开始，会持续整个时间步长 (= "+interval+" minutes)。"
        note.append(note_0)
        note.append(note_1)
        note.append(note_2)
        
        if Td>0:
            #print(nn,'. The depression storage is completely filled at the',round(Td,1), 'th minute, and no effective rainfall has occurred prior to that moment.')
            note_3 = "3. 地表坑洼在第 "+sminute+" minute 被蓄满, 之前没有净雨产生。"
            note.append(note_3)

        if dtheta==0: # (20211227)
            #print(nn,'. Infiltration may occur after the',round(Td,1), 'th minute. The updated infiltration potential will be illustrated when infiltration occurs. In order to compare with the hyetograph, infiltration rates are plotted as a portion of the hyetograph histogram； if available, the remaining portion of the hyetograph represents effective rainfall (in light blue).')# (20220311)
            note_4 = "4. 下渗有可能在第 "+sminute+" minute 后发生。"# (20220311)
            note.append(note_4)  
        else:# (20211227)
            #print(nn,'. Infiltration may occur after the',round(Td,1), 'th minutes. Both theoretical and updated infiltration potentials are infinite at that time moment, but the updated infiltration potential will change only if infiltration occurs. In order to compare with the hyetograph, infiltration rates are plotted as a portion of the hyetograph histogram； if available, the remaining portion of the hyetograph represents effective rainfall (in light blue).')# (20211227)
            note_4 = "4. 下渗有可能在第 "+sminute+" minute 后发生。为便于比较，图中的理论入渗率和修正后的潜势入渗率曲线均从这一时刻起始。理论入渗率和修正后的潜势入渗率在这一时刻均为无限大，图中的曲线在这一时间点上不专门显示。之后，修正后的潜势入渗率仅仅在有实际下渗发生时会有所变化。"# (20211227)
            note.append(note_4)

        if ss2==0:#20220310
            #print(nn,'. In order to compare with the hyetograph, after the depression storage is completely filled, infiltration rates are plotted as a portion of the hyetograph histogram, while the remaining portion of the hyetograph represents effective rainfall intensities.')
            note_5 = "5. 为与降雨强度过程相比较，实际入渗率也按柱状图表示（深蓝色），某时刻的实际入渗率会显示在接下来的整个时间单元内。如果存在，实际入渗率柱状图顶边以上的残余降雨量即为净雨（浅蓝色）。"
            note.append(note_5)
        else:
            note_5 = "5. 为与降雨强度过程相比较，实际入渗率也按柱状图表示（深蓝色），某时刻的实际入渗率会显示在接下来的整个时间单元内。如果存在，实际入渗率柱状图顶边以上的残余降雨量即为净雨（浅蓝色）。当修正后的潜势入渗率曲线穿过某时段降雨强度柱状图顶边时，如果在这一时段产生净雨，净雨被近似绘制成一个三角形分布，其在这一时段内的均匀分布值见表格。"
            note.append(note_5)

        if dda>dd:
            #print(nn,'. If available, the effective rainfall intensity starting at the',round(Td,1), 'th minute ends at the', (j+1)*dti,'th minute.')
            note_6 = "6. 如果存在，起始于第 "+sminute+" minute 的净雨强度值会在第 "+eminute+" minute 结束。"
            note.append(note_6)
        if sum(f[j:l+2])==0:# (20220311)
            #print(nn,'. Because no actual infiltration occurs, the updated infiltration potential is not applicable here.')# (20220311)
            note_7 = "6. 由于没有实际下渗发生，修正后的潜势入渗率在此不适用."# (20220311)
            note.append(note_7)
        # if Td>0:
        #     #str2 = "3. The depression storage is completely filled at the "+ sminute +"th minute, and no effective rainfall has occurred prior to the moment"
        #     str2 = "3. 地表坑洼在第 "+ sminute +" minutes 被蓄满, 之前没有净雨产生。"
        #     if dtheta==0: # (20211227) 
        #         str4 = "4. 下渗在第 "+ sminute +" minutes 开始。"# (20211227) 
        #     else:# (20211227) 
        #         str4 = "4. 下渗在第 "+ sminute +" minutes 开始，理论入渗率和修正后的理论入渗率在这一时刻均为无限大。"
        #     note.append(str2)
        #     note.append(str4)
        #     if dda>dd:
        #         #str3 = " 4. If applicable, the intensity starting at the "+sminute+"th minute ends at the "+eminute+"th minute."
        #         str3 = " 5. 起始于第 "+sminute+" minutes 的净雨强度值在第 "+eminute+" minutes 结束。"
        #         note.append(str3)
    else:
        if dtheta==0:
            note2_0 = '说明:'
            note2_1 = '1. 理论入渗率等于土体的渗透系数。'
            note2.append(note2_0)
            note2.append(note2_1)
        else:     
            #note2 = ["Notes:","1. The theoretical infiltration potential is infinite at time zero."]
            # note2 = ["说明:","1. 理论入渗率在时间零点处为无限大，图中的理论入渗率曲线在这一时间点上不专门显示。"]
            note2_0 = '说明:'
            note2_1 = '1. 理论入渗率在时间零点处为无限大，图中的理论入渗率曲线在这一时间点上不专门显示。'
            note2.append(note2_0)
            note2.append(note2_1)
            #note2 = ["说明:","1. 在时间零点处理论入渗率为无限大。","2.????"]
        if ss1==1:#20220310
            note2_2 = '2. 由于降雨量不足以蓄满地表的坑洼，没有下渗产生，也不会有净雨产生。故图中仅绘出理论入渗率。' #20220310
            note2.append(note2_2)
            if dtheta>0:
                note2_3 = '3. 图中的理论入渗率曲线仅展示土体的基本下渗特性，不指定专门的时间零点。'
                note2.append(note2_3)
        if ss3==1:#20220310
            note2_2 = '2. 由于降雨量为零，没有下渗产生，也不会有净雨产生。故图中仅绘出理论入渗率。'#20220310
            note2.append(note2_2)

    return plot_url,data,eff,note,note2
