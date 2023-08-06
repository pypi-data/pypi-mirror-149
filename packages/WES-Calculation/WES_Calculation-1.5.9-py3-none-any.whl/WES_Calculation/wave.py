'''
Author: BDFD
Date: 2022-04-20 13:16:40
LastEditTime: 2022-05-04 13:13:44
LastEditors: BDFD
Description: 
FilePath: \5.2-PyPi-WES_Calculation\WES_Calculation\wave.py
'''
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter
import numpy as np
import math
import statistics
import io
import base64
import PyQt5
import seaborn as sns
from decimal import Decimal


def data_conv(data):
    if data == '':
        data = None
    else:
        data = float(data)
    return data


def data_conv_int(data):
    if data == '':
        data = None
    else:
        data = int(data)*1000
    return data

def return_img_stream(img_local_path):
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream

# if request.method == "POST":
# note = []
# # Generation of Ocean Wave Point Spectra
# # Inputs
# # Primary
# c1 = int(request.form["c1"])
# if c1 == 1:
#     d = float(request.form["d"])   # water depth (m)    
#     X = request.form["X"]
#     X = data_service.data_conv_int(X)            
#     U = float(request.form["U"])  # wind speed (m/s)
#     el = float(request.form["el"])   # the elevation of the wind speed (m)      
#     gamma = float(request.form["gamma"])   # peakedness parameter for JONSWAP (between 1 and 7, but 3.30 is normally recommended)
#     Hs = float(request.form["Hs"])   # significant wave height (m)
#     Tz = float(request.form["Tz"])  # average zero-crossing period from data (s)
#     Ts = request.form["Ts"] # significant wave period (s)
#     Ts = data_service.data_conv(Ts)
#     Tp = None

# # If c1=2, please input the following paramaters:
# if c1 == 2:
#     X = request.form["X"]
#     X = data_service.data_conv_int(X)   # fetch length (m)
#     U = float(request.form["U"])   # wind speed m/s).             
#     el = request.form["el"]  # the elevation of the wind speed (m). 
#     el = data_service.data_conv(el)            
#     gamma = float(request.form["gamma"])   # peakedness parameter in JONSWAP (between 1 and 7, but 3.30 is normally recommended). Optional
#     Hs = float(request.form["Hs"])   # 5 # significant wave height (m)  
#     Tz = request.form["Tz"]  # measured average zero-crossing period (s)
#     Tz = data_service.data_conv(Tz)
#     Ts = float(request.form["Ts"])   # measured significant period (s)
#     Tp = request.form["Tp"]  # Tz: period of spectral peak (s)
#     Tp = data_service.data_conv(Tp)
#     d = None       

def wave(c1, d, X, U, el, gamma, Hs, Tz, Ts, Tp):
    note = []
    content = []
    data1 = []
    data2 = []
    # Secondary
    fl = 0.02  # lower bound of f (Hz) (f: cyclic frequency)
    fu = 0.8  # upper bound of f (Hz)
    df = 0.001  # computational step of f (Hz)
    tol = 0.0001  # Iteration tolerance for wave dispersion relation (m)

    if U != None and el != None:  # 20220327
        U10 = U * (10 / el) ** (1 / 7)  # wind speed at 10 m elevation (m/s)
        U19m5 = U10 * (19.5 / 10) ** (1 / 7)  # wind speed at 19.5 m elevation (m/s)

    if c1 == 2:  # 20220327
        if Tp == None:  # 20220328
            if Tz != None:  # 20220328
                Tp = 1.2 * 1.05 * Tz  # 20220328
            if Ts != None:  # 20220328
                Tp = 1.05 * Ts  # 20220328
            if Tz == None and Ts == None:  # 20220328
                Tp = None  # 20220328

    f = np.arange(fl, fu, df)  # the range of f

    # note.extend([''])
    # print('---Generation of Ocean Wave Spectra---')
    heading = '---经验波浪频率谱---'
    data1_heading = "m\u208b\u2081 (m\u00b2s)","m\u2080 (m\u00b2)","m\u2081 (m\u00b2/s)","m\u2082 (m\u00b2/s\u00b2)","m\u2084 (m\u00b2/s\u2074)","\u03BD ","\u03B5 ","Hsm\u2080 (m)"
    # data1_heading1 = "m\u208b\u2081","m\u2080","m\u2081","m\u2082","m\u2084","\u03BD","\u03B5","Hsm\u2080"
    # data1_heading2 = "(m\u00b2s)","(m\u00b2)","(m\u00b2/s)","(m\u00b2/s\u00b2)","(m\u00b2/s\u2074)"," "," ","(m)"

    # Basic Bretschneider Type
    if c1 == 2:
        if Ts == None and Tz != None:
            Ts = Tz * 0.952 / 0.7104
        if Ts != None:
            fp1 = 0.946 / Ts  # fp for Basic Bretschneider Type
            fpBM=0.952/Ts # fp for B-M
            fpMBM=1/Ts/1.1353 # fp for M B-M
            
    if c1 == 2 and Ts != None and Hs !=None:  # 20220327
        # Bretschneider-Mitsuyasu (B-M) Spectrum             
        SfBM = 0.257 * Hs ** 2 * np.exp(
            -1.03 / (Ts * f) ** 4) / f ** 5 / Ts ** 4  # S(f): spectral energy density (m^2s)
        SfBMmax = 0.257 * Hs ** 2 * np.exp(-1.03 / (Ts * fpBM) ** 4) / fpBM ** 5 / Ts ** 4  # maximum of S(f)
        ABM = 0.257 * Hs ** 2 / Ts ** 4
        BBM = 1.03 / Ts ** 4
        mn1BM = 0.2266 * ABM/BBM**1.25 # m-1  
        m0BM = 0.25 * ABM / BBM
        m1BM = 0.306 * ABM / BBM ** 0.75
        m2BM = math.pi ** 0.5 * ABM / BBM ** 0.5 / 4
        m4BMn= sum(df*f**4*SfBM) # m4 (a numerical solution.)
        vBM=(m0BM*m2BM/m1BM**2-1)**0.5 # spectral width
        epBM=(1-m2BM**2/m0BM/m4BMn)**0.5 # spectral bandwidth
        feBM=m0BM/mn1BM # energy frequency 
        Tm01BM = m0BM / m1BM  # Tm01: mean period based on m0 and m1
        Tm02BM = (m0BM / m2BM) ** 0.5  # Tm02: mean period based on m0 and m2        

        data1 += (("B-M ",str(round(mn1BM,2)),str(round(m0BM, 2)),str(round(m1BM, 2)),str(round(m2BM, 2)),str(round(m4BMn,3)),str(round(vBM,2)),str(round(epBM,2)),str(round(4.004 * m0BM ** 0.5, 3))),)
        # note.append(str6)
        plt.plot(f, SfBM, label="B-M", color='darkblue', linewidth=1)

        # Modified Bretschneider-Mitsuyasu (M B-M) Spectrum 
        SfMBM=0.2056*Hs**2*np.exp(-0.7523/(Ts*f)**4)/f**5/Ts**4 # S(f): spectral energy density (m^2s)
        SfMBMmax=0.2056*Hs**2*np.exp(-0.7523/(Ts*fpMBM)**4)/fpMBM**5/Ts**4 # maximum of S(f)
        AMBM=0.2056*Hs**2/Ts**4
        BMBM=0.7523/Ts**4
        mn1MBM=0.2266*AMBM/BMBM**1.25  
        m0MBM=0.25*AMBM/BMBM
        m1MBM=0.306*AMBM/BMBM**0.75
        m2MBM=math.pi**0.5*AMBM/BMBM**0.5/4  
        m4MBMn=sum(df*f**4*SfMBM)# m4 (a numerical solution.)
        vMBM=(m0MBM*m2MBM/m1MBM**2-1)**0.5
        epMBM=(1-m2MBM**2/m0MBM/m4MBMn)**0.5
        feMBM=m0MBM/mn1MBM
        Tm01MBM=m0MBM/m1MBM # Tm01: mean period based on m0 and m1
        Tm02MBM=(m0MBM/m2MBM)**0.5 # Tm02: mean period based on m0 and m2
        
        data1 += (('M B-M',str(round(mn1MBM,2)),str(round(m0MBM,2)),str(round(m1MBM,2)),str(round(m2MBM,2)),str(round(m4MBMn,3)),str(round(vMBM,2)),str(round(epMBM,2)),str(round(3.832*m0MBM**0.5,3))),)
        # note.append(str17)
        plt.plot(f,SfMBM,label="M B-M",color='cyan',linewidth=2)

    if c1 == 2:
        # Pierson-Moskowitz (P-M) Spectrum
        if U != None and el != None:  # 20220327
            HsPM = 0.21 * U19m5 ** 2 / 9.81
        else:
            if Hs != None:
                HsPM = Hs
            else:
                HsPM = None
        if HsPM != None:
            fpPM = 0.5 * 0.4014 * (9.81 / HsPM) ** 0.5 / math.pi  # peak (or modal) frequency in P-M Spectrum (Hz)
            SfPM = 0.0081 * 9.81 ** 2 * np.exp(-1.25 * (fpPM / f) ** 4) / f ** 5 / (
                        2 * math.pi) ** 4  # S(f): spectral energy density (m^2s)
            SfPMmax = 0.0081 * 9.81 ** 2 * np.exp(-1.25 * (fpPM / fpPM) ** 4) / fpPM ** 5 / (
                        2 * math.pi) ** 4  # S(f): spectral energy density (m^2s)
            APM = 0.0081 * 9.81 ** 2 / (2 * math.pi) ** 4
            BPM = 1.25 * fpPM ** 4
            mn1PM=0.2266*APM/BPM**1.25 
            m0PM = 0.25 * APM / BPM
            m1PM = 0.306 * APM / BPM ** 0.75
            m2PM = math.pi ** 0.5 * APM / BPM ** 0.5 / 4
            m4PMn=sum(df*f**4*SfPM)# m4 (a numerical solution.)
            vPM=(m0PM*m2PM/m1PM**2-1)**0.5
            epPM=(1-m2PM**2/m0PM/m4PMn)**0.5  
            fePM=m0PM/mn1PM   
            Tm01PM = m0PM / m1PM  # Tm01: mean period based on m0 and m1
            Tm02PM = (m0PM / m2PM) ** 0.5  # Tm02: mean period based on m0 and m2
            
            data1 += (("P-M",str(round(mn1PM, 2)),str(round(m0PM, 2)),str(round(m1PM, 2)),str(round(m2PM, 2)),str(round(m4PMn,3)),str(round(vPM,2)),str(round(epPM,2)),str(round(4.004 * m0PM ** 0.5, 3))),)                
            # note.append(str7)
            plt.plot(f, SfPM, label="P-M", marker='o', color='darkblue', markersize=2, linewidth=0.5)

    if c1 == 2 and Hs != None:  # 20220327
        # Ochi-Hubble (O-H) Spectrum (Most Probable One)
        Hs1 = 0.84 * Hs
        Hs2 = 0.54 * Hs
        fp1OH = 0.7 / np.exp(0.046 * Hs) / 2 / math.pi
        fp2OH = 1.15 / np.exp(0.039 * Hs) / 2 / math.pi
        lamda1 = 3
        lamda2 = 1.54 / np.exp(0.062 * Hs)
        SfOH = math.pi * 0.5 * ((lamda1 + 0.25) ** lamda1 * Hs1 ** 2 * (fp1OH / f) ** (4 * lamda1) / np.exp(
            (lamda1 + 0.25) * (fp1OH / f) ** 4) / math.gamma(lamda1) / (f * 2 * math.pi) + \
                                (lamda2 + 0.25) ** lamda2 * Hs2 ** 2 * (fp2OH / f) ** (4 * lamda2) / np.exp(
                    (lamda2 + 0.25) * (fp2OH / f) ** 4) / math.gamma(lamda2) / (
                                            f * 2 * math.pi))  # SfOH: Spectral energy density of O-H (m^2s)
        SfOHmax1 = math.pi * 0.5 * ((lamda1 + 0.25) ** lamda1 * Hs1 ** 2 * (fp1OH / fp1OH) ** (4 * lamda1) / np.exp(
            (lamda1 + 0.25) * (fp1OH / fp1OH) ** 4) / math.gamma(lamda1) / (fp1OH * 2 * math.pi) + \
                                    (lamda2 + 0.25) ** lamda2 * Hs2 ** 2 * (fp2OH / fp1OH) ** (4 * lamda2) / np.exp(
                    (lamda2 + 0.25) * (fp2OH / fp1OH) ** 4) / math.gamma(lamda2) / (
                                                fp1OH * 2 * math.pi))  # SfOH: Spectral energy density of O-H (m^2s)
        mn1OHn=sum(df*SfOH/f)# m-1 (a numerical solution)
        m0OHn = sum(df * SfOH)  # m0 
        m1OHn = sum(df * f * SfOH)  # m1 
        m2OHn = sum(df * f ** 2 * SfOH)  # m2 
        m4OHn=sum(df*f**4*SfOH)# m4 (a numerical solution.)
        vOH=(m0OHn*m2OHn/m1OHn**2-1)**0.5
        epOH=(1-m2OHn**2/m0OHn/m4OHn)**0.5  
        feOH=m0OHn/mn1OHn  
        Tm01OH = m0OHn / m1OHn  # Tm01: mean period based on m0 and m1
        Tm02OH = (m0OHn / m2OHn) ** 0.5  # Tm02: mean period based on m0 and m2
            
        data1 += (("O-H",str(round(mn1OHn,2)),str(round(m0OHn, 2)),str(round(m1OHn, 2)),str(round(m2OHn, 2)),str(round(m4OHn, 3)),str(round(vOH,2)),str(round(epOH,2)),str(round(4.004 * m0OHn ** 0.5, 3))),)            
        # note.append(str8)
        plt.plot(f, SfOH, label="O-H(最可能谱型)", ls=":", color="black", )

    # Simplified Torsethaugen (Torsethaugen-S) Spectrum
    if c1 == 2 and X != None and Hs != None and Tp != None:  # 20220327
        
        if X==370000:
            Tf=6.6*Hs**(1/3)
        if X==100000:
            Tf=5.3*Hs**(1/3)
                                
        G0 = 3.26
        A2 = 1
        gamma2 = 1
        gammaF2 = 1

        el = (Tf - Tp) / (Tf - 2 * Hs ** 0.5)
        eu = (Tf - Tp) / (Tf - 25)
        rpw = 0.7 + 0.3 / np.exp((2 * el) ** 2)
        rps = 0.6 + 0.4 / np.exp((eu / 0.3) ** 2)

        fn1 = [0 for j in range(round((fu - fl) / df))]
        GF1 = [0 for j in range(round((fu - fl) / df))]
        fn2 = [0 for j in range(round((fu - fl) / df))]
        GF2 = [0 for j in range(round((fu - fl) / df))]
        gammaF1 = [0 for j in range(round((fu - fl) / df))]
        SfST = [0 for j in range(round((fu - fl) / df))]  # SfST: Spectral energy density of Torsethaugen-S(m^2s)

        if Tp <= Tf:
            Hsw = rpw * Hs
            Tpw = Tp
            gamma1 = 35 * (2 * math.pi * Hsw / 9.81 / Tp ** 2) ** 0.857
            A1 = (1 + 1.1 * (math.log(gamma1)) ** 1.19) / gamma1
            E1 = Hsw ** 2 * Tpw / 16

            Hss = (1 - rpw ** 2) ** 0.5 * Hs
            Tps = Tf + 2
            E2 = Hss ** 2 * Tps / 16

            for i in range(round((fu - fl) / df)):
                fn1[i] = f[i] * Tpw
                GF1[i] = 1 / fn1[i] ** 4 / np.exp(fn1[i] ** (-4))

                fn2[i] = f[i] * Tps
                GF2[i] = 1 / fn2[i] ** 4 / np.exp(fn2[i] ** (-4))

                if fn1[i] < 1:
                    sigma1 = 0.07
                else:
                    sigma1 = 0.06

                if fn2[i] < 1:
                    sigma2 = 0.07
                else:
                    sigma2 = 0.06
                
                gammaF1[i] = gamma1 ** np.exp(-0.5*(fn1[i]-1) ** 2 / sigma1 ** 2)
                SfST[i] = E1 * G0 * A1 * GF1[i] * gammaF1[i] + E2 * G0 * A2 * GF2[i] * gammaF2

        else:
            Hss = rps * Hs
            Tps = Tp          
            gamma1= 35 * (2 * math.pi * Hs / 9.81 / Tf ** 2) ** 0.857 * (1+6*eu)
            A1 = (1 + 1.1 * (math.log(gamma1)) ** 1.19) / gamma1
            E1 = Hss ** 2 * Tps / 16

            Hsw = (1 - rps ** 2) ** 0.5 * Hs
            Tpw = 6.6 * Hsw ** (1 / 3)
            E2 = Hsw ** 2 * Tpw / 16

            for i in range(round((fu - fl) / df)):
                fn1[i] = f[i] * Tps
                GF1[i] = 1 / fn1[i] ** 4 / np.exp(fn1[i] ** (-4))

                fn2[i] = f[i] * Tpw
                GF2[i] = 1 / fn2[i] ** 4 / np.exp(fn2[i] ** (-4))

                if fn1[i] < 1:
                    sigma1 = 0.07
                else:
                    sigma1 = 0.09

                if fn2[i] < 1:
                    sigma2 = 0.07
                else:
                    sigma2 = 0.09
        
                gammaF1[i] = gamma1 ** np.exp(-0.5*(fn1[i]-1) ** 2 / sigma1 ** 2)
                SfST[i] = E1 * G0 * A1 * GF1[i] * gammaF1[i] + E2 * G0 * A2 * GF2[i] * gammaF2

        mn1STn=df*sum(SfST/f)# m-1 (a numerical solution)
        m0STn = df * sum(SfST) # m0 
        m1STn = df * sum(f * SfST) # m1
        m2STn = df * sum(f ** 2 * SfST) # m2
        m4STn=sum(df*f**4*SfST)# m4 (a numerical solution.)
        vST=(m0STn*m2STn/m1STn**2-1)**0.5
        epST=(1-m2STn**2/m0STn/m4STn)**0.5      
        feST=m0STn/mn1STn   
        Tm01ST = m0STn / m1STn  # Tm01: mean period based on m0 and m1
        Tm02ST = (m0STn / m2STn) ** 0.5  # Tm02: mean period based on m0 and m2
        data1 += (("Torsethaugen-S",str(round(mn1STn,2)),str(round(m0STn, 2)),str(round(m1STn, 2)),str(round(m2STn, 2)),str(round(m4STn, 3)),str(round(vST,2)),str(round(epST,2)),str(round(4.004 * m0STn ** 0.5, 3))),)
        # data1 += (("sT",str(round(mn1STn,2)),str(round(m0STn, 2)),str(round(m1STn, 2)),str(round(m2STn, 2)),str(round(m4STn, 3)),str(round(vST,2)),str(round(epST,2)),str(round(4.004 * m0STn ** 0.5, 3))),)
        # note.append(str9)
        plt.plot(f, SfST, label="Torsethaugen-S", color="green", ls="-.", )   

    # JONSWAP and JONSWAP-G Spectra #20220329
    if c1 == 1 and X != None and U != None and el != None:  # 20220327
        X0J = 9.81 * X / U10 ** 2
        alpha = 0.076 / X0J ** 0.22
        fpJ = 3.5 * 9.81 / (U10 * X0J ** 0.33)

        if gamma != None and fpJ != None:
            SfJ = alpha * 9.81 ** 2 * np.exp(-1.25 * fpJ ** 4 / f ** 4) * gamma ** (
                np.exp(-0.5 * (f - fpJ) ** 2 / 0.07 ** 2 / fpJ ** 2)) / (2 * math.pi) ** 4 / f ** 5 * (f <= fpJ) + \
                    alpha * 9.81 ** 2 * np.exp(-1.25 * fpJ ** 4 / f ** 4) * gamma ** (
                        np.exp(-0.5 * (f - fpJ) ** 2 / 0.09 ** 2 / fpJ ** 2)) / (2 * math.pi) ** 4 / f ** 5 * (
                                f > fpJ)  # SfJ: Spectral energy density of JONSWAP (m^2s)
            SfJmax = alpha * 9.81 ** 2 * np.exp(-1.25 * fpJ ** 4 / fpJ ** 4) * gamma ** (
                np.exp(-0.5 * (fpJ - fpJ) ** 2 / 0.07 ** 2 / fpJ ** 2)) / (2 * math.pi) ** 4 / fpJ ** 5

            mn1Jn=df*sum(SfJ/f)# m-1 (a numerical solution)
            m0Jn = sum(df * SfJ)  # m0 
            m1Jn = sum(df * f * SfJ)  # m1
            m2Jn = sum(df * f ** 2 * SfJ)  # m2 
            m4Jn=sum(df*f**4*SfJ)# m4 (a numerical solution.)
            vJ=(m0Jn*m2Jn/m1Jn**2-1)**0.5
            epJ=(1-m2Jn**2/m0Jn/m4Jn)**0.5    
            feJ=m0Jn/mn1Jn     
            Tm01J = m0Jn / m1Jn  # Tm01: mean period based on m0 and m1
            Tm02J = (m0Jn / m2Jn) ** 0.5  # Tm02: mean period based on m0 and m2

            data1 += (("JONSWAP ",str(round(mn1Jn,2)),str(round(m0Jn, 2)),str(round(m1Jn, 2)),str(round(m2Jn, 2)),str(round(m4Jn, 3)),str(round(vJ,2)),str(round(epJ,2)),str(round(4.004 * m0Jn ** 0.5, 3))),)
            # note.append(str10)
            plt.plot(f, SfJ, label="JONSWAP", color="red", linewidth=1)

    if c1 == 2 and gamma != None and Hs != None:
        if Tz != None:
            fpJG = (1 - 0.532 / (gamma + 2.5) ** 0.569) / Tz
        if Ts != None:
            fpJG = (1 - 0.132 / (gamma + 0.2) ** 0.559) / Ts
        else:
            fpJG = None

        if fpJG != None:
            alphaG1 = 0.0624 / (0.23 + 0.0336 * gamma - 0.185 / (1.9 + gamma))
            alphaG2 = 0.0624 * (1.094 - 0.01915 * math.log(gamma)) / (0.23 + 0.0336 * gamma - 0.185 / (1.9 + gamma))

            SfJG1 = alphaG1 * Hs ** 2 * fpJG ** 4 * np.exp(-1.25 * fpJG ** 4 / f ** 4) * gamma ** (
                np.exp(-0.5 * (f - fpJG) ** 2 / 0.07 ** 2 / fpJG ** 2)) / f ** 5 * (f <= fpJG) + \
                    alphaG1 * Hs ** 2 * fpJG ** 4 * np.exp(-1.25 * fpJG ** 4 / f ** 4) * gamma ** (
                        np.exp(-0.5 * (f - fpJG) ** 2 / 0.09 ** 2 / fpJG ** 2)) / f ** 5 * (
                                f > fpJG)  # SfJG: Spectral energy density of JONSWAP-G (m^2s)
            SfJG1max = alphaG1 * Hs ** 2 * fpJG ** 4 * np.exp(-1.25 * fpJG ** 4 / fpJG ** 4) * gamma ** (
                np.exp(-0.5 * (fpJG - fpJG) ** 2 / 0.07 ** 2 / fpJG ** 2)) / fpJG ** 5
            mn1JG1n=df*sum(SfJG1/f)# m-1 (a numerical solution)
            m0JG1n = sum(df * SfJG1)  # m0 
            m1JG1n = sum(df * f * SfJG1)  # m1
            m2JG1n = sum(df * f ** 2 * SfJG1)  # m2 
            m4JG1n=sum(df*f**4*SfJG1)# m4 (a numerical solution.)
            vJG1=(m0JG1n*m2JG1n/m1JG1n**2-1)**0.5
            epJG1=(1-m2JG1n**2/m0JG1n/m4JG1n)**0.5  
            feJG1=m0JG1n/mn1JG1n    
            Tm01JG1 = m0JG1n / m1JG1n  # Tm01: mean period based on m0 and m1
            Tm02JG1 = (m0JG1n / m2JG1n) ** 0.5  # Tm02: mean period based on m0 and m2
                        
            data1 += (("JONSWAP-G1",str(round(mn1JG1n,2)),str(round(m0JG1n, 2)),str(round(m1JG1n, 2)),str(round(m2JG1n, 2)),str(round(m4JG1n, 3)),str(round(vJG1,2)),str(round(epJG1,2)),str(round(4.004 * m0JG1n ** 0.5, 3))),)
            # data1 += (("J-G1",str(round(mn1JG1n,2)),str(round(m0JG1n, 2)),str(round(m1JG1n, 2)),str(round(m2JG1n, 2)),str(round(m4JG1n, 3)),str(round(vJG1,2)),str(round(epJG1,2)),str(round(4.004 * m0JG1n ** 0.5, 3))),)
            # note.append(str11)
            plt.plot(f, SfJG1, label="JONSWAP-G1", color="red", linewidth=0.5)

            SfJG2 = alphaG2 * Hs ** 2 * fpJG ** 4 * np.exp(-1.25 * fpJG ** 4 / f ** 4) * gamma ** (
                np.exp(-0.5 * (f - fpJG) ** 2 / 0.07 ** 2 / fpJG ** 2)) / f ** 5 * (f <= fpJG) + \
                    alphaG2 * Hs ** 2 * fpJG ** 4 * np.exp(-1.25 * fpJG ** 4 / f ** 4) * gamma ** (
                        np.exp(-0.5 * (f - fpJG) ** 2 / 0.09 ** 2 / fpJG ** 2)) / f ** 5 * (
                                f > fpJG)  # SfJG: Spectral energy density of JONSWAP-G (m^2s)
            SfJG2max = alphaG2 * Hs ** 2 * fpJG ** 4 * np.exp(-1.25 * fpJG ** 4 / fpJG ** 4) * gamma ** (
                np.exp(-0.5 * (fpJG - fpJG) ** 2 / 0.07 ** 2 / fpJG ** 2)) / fpJG ** 5
            mn1JG2n=df*sum(SfJG2/f)
            m0JG2n = sum(df * SfJG2)  # m0 
            m1JG2n = sum(df * f * SfJG2)  # m1
            m2JG2n = sum(df * f ** 2 * SfJG2)  # m2 
            m4JG2n=sum(df*f**4*SfJG2)# m4 (a numerical solution.)
            vJG2=(m0JG2n*m2JG2n/m1JG2n**2-1)**0.5
            epJG2=(1-m2JG2n**2/m0JG2n/m4JG2n)**0.5  
            feJG2=m0JG2n/mn1JG2n   
            Tm01JG2 = m0JG2n / m1JG2n  # Tm01: mean period based on m0 and m1
            Tm02JG2 = (m0JG2n / m2JG2n) ** 0.5  # Tm02: mean period based on m0 and m2 
                
            data1 += (("JONSWAP-G2",str(round(mn1JG2n,2)),str(round(m0JG2n, 2)),str(round(m1JG2n, 2)),str(round(m2JG2n, 2)),str(round(m4JG2n, 3)),str(round(vJG2,2)),str(round(epJG2,2)),str(round((3.812-0.0013*gamma**2+0.021*gamma) * m0JG2n ** 0.5, 3))),)
            # data1 += (("J-G2",str(round(mn1JG2n,2)),str(round(m0JG2n, 2)),str(round(m1JG2n, 2)),str(round(m2JG2n, 2)),str(round(m4JG2n, 3)),str(round(vJG2,2)),str(round(epJG2,2)),str(round((3.812-0.0013*gamma**2+0.021*gamma) * m0JG2n ** 0.5, 3))),)
            # note.append(str12)
            plt.plot(f, SfJG2, label="JONSWAP-G2", color="red", linewidth=1, ls="--")

    # Liu Spectrum and Mitsuyasu Spectrum
    if c1 == 1 and X != None and U != None and el != None:  # 20220327

        # Liu Spectrum
        U0L = U10 * (U10 ** 2 / 9.81 / X) ** (1 / 3)
        X0L = 9.81 * X / U0L ** 2
        fpLiu = 0.8 ** 0.25 * 5500 ** 0.25 * 9.81 / (2 * math.pi) / U0L / X0L ** (1 / 3)
        SfLiu = 2 * math.pi * 0.4 * 9.81 ** 2 * np.exp(
            -5500 * (9.81 / (2 * math.pi * f) / U0L / X0L ** (1 / 3)) ** 4) / X0L ** 0.25 / (2 * math.pi * f) ** 5
        SfLiumax = 2 * math.pi * 0.4 * 9.81 ** 2 * np.exp(
            -5500 * (9.81 / (2 * math.pi * fpLiu) / U0L / X0L ** (1 / 3)) ** 4) / X0L ** 0.25 / (
                                2 * math.pi * fpLiu) ** 5
        ALiu = 0.4 * 9.81 ** 2 / X0L ** 0.25 / (2 * math.pi) ** 4
        BLiu = 5500 * (9.81 / (2 * math.pi) / U0L / X0L ** (1 / 3)) ** 4
        mn1Liu=0.2266*ALiu/BLiu**1.25 # m-1  
        m0Liu = 0.25 * ALiu / BLiu
        m1Liu = 0.306 * ALiu / BLiu ** 0.75
        m2Liu = math.pi ** 0.5 * ALiu / BLiu ** 0.5 / 4
        m4Liu=sum(df*f**4*SfLiu)# m4 (a numerical solution.)
        vLiu=(m0Liu*m2Liu/m1Liu**2-1)**0.5
        epLiu=(1-m2Liu**2/m0Liu/m4Liu)**0.5     
        feLiu=m0Liu/mn1Liu  
        Tm01Liu = m0Liu / m1Liu  # Tm01: mean period based on m0 and m1
        Tm02Liu = (m0Liu / m2Liu) ** 0.5  # Tm02: mean period based on m0 and m2
        
        data1 += (("Liu",str(round(mn1Liu,2)),str(round(m0Liu, 2)),str(round(m1Liu, 2)),str(round(m2Liu, 2)),str(round(m4Liu, 3)),str(round(vLiu,2)),str(round(epLiu,2)),str(round(4.004 * m0Liu ** 0.5, 3))),)
        # note.append(str13)
        plt.plot(f, SfLiu, label="Liu", color='green', ls="-.")

        # Mitsuyasu Spectrum
        U0M = U10 / 25
        X0M = 9.81 * X / U0M ** 2
        fpM = 9.81 * (9.17 - 0.32 * math.log(X0M, 10)) / 10 / X0M ** 0.312 / U0M
        SfM = [0 for j in range(round((fu - fl) / df))]
        for i in range(round((fu - fl) / df)):
            if f[i] <= 0.3 * fpM:
                SfM[i] = 0
            elif f[i] <= fpM:
                SfM[i] = 5.86 * np.exp(22.1 * X0M ** 0.312 * f[i] * U0M / 9.81) * 9.81 ** 2 / f[i] ** 5 / 10 ** 13
            else:
                SfM[i] = 3.79 * 9.81 ** 2 / f[i] ** 5 / X0M ** 0.308 / 10000
        SfMmax = 5.86 * np.exp(22.1 * X0M ** 0.312 * fpM * U0M / 9.81) * 9.81 ** 2 / fpM ** 5 / 10 ** 13
        mn1Mn=df*sum(SfM/f)    
        m0Mn = df * sum(SfM)  # m0 
        m1Mn = df * sum(f * SfM)
        m2Mn = df * sum(f ** 2 * SfM)
        m4Mn=sum(df*f**4*SfM)# m4 (a numerical solution.)
        vM=(m0Mn*m2Mn/m1Mn**2-1)**0.5
        epM=(1-m2Mn**2/m0Mn/m4Mn)**0.5     
        feM=m0Mn/mn1Mn      
        Tm01M = m0Mn / m1Mn  # Tm01: mean period based on m0 and m1
        Tm02M = (m0Mn / m2Mn) ** 0.5  # Tm02: mean period based on m0 and m2
        
        data1 += (("Mitsuyasu",str(round(mn1Mn,2)),str(round(m0Mn, 2)),str(round(m1Mn, 2)),str(round(m2Mn, 2)),str(round(m4Mn, 3)),str(round(vM,2)),str(round(epM,2)),str(round(4.004 * m0Mn ** 0.5, 3))),)
        # note.append(str14)
        plt.plot(f, SfM, label="Mitsuyasu", color="blue", linewidth=2.5)

    # TMA Spectrum #20220329
    if c1 == 1 and X != None and U != None and el != None and d != None:  # 20220327

        La = (9.81 * d) ** 0.5 / fpJ  # assumed wave length (m)
        Lu = 9.81 / 2 / math.pi / fpJ ** 2 * math.tanh(2 * math.pi * d / La)  # updated wave length (m)
        while (abs(La - Lu) > tol):
            La = Lu
            Lu = 9.81 / 2 / math.pi / fpJ ** 2 * math.tanh(2 * math.pi * d / La)
        Lp = Lu  # wave length corresponding to fp at water dpeth d (m)

        alphaTMA = 0.0078 * (2 * math.pi * U10 ** 2 / 9.81 / Lp) ** 0.49
        gammaTMA = 2.47 * (2 * math.pi * U10 ** 2 / 9.81 / Lp) ** 0.39
        SfTMA = (2 * (math.pi * f) ** 2 * d) * alphaTMA * 9.81 * np.exp(-1.25 * fpJ ** 4 / f ** 4) * gammaTMA ** (
            np.exp(-0.5 * (f - fpJ) ** 2 / (0.07 * (f <= fpJ) + 0.09 * (f > fpJ)) ** 2 / fpJ ** 2)) / (
                            2 * math.pi) ** 4 / f ** 5 * (f <= (9.81 / d) ** 0.5 / 2 / math.pi) + \
                (1 - 0.5 * (2 - 2 * math.pi * f * (d / 9.81) ** 0.5) ** 2) * alphaTMA * 9.81 ** 2 * np.exp(
            -1.25 * fpJ ** 4 / f ** 4) * gammaTMA ** (
                    np.exp(-0.5 * (f - fpJ) ** 2 / (0.07 * (f <= fpJ) + 0.09 * (f > fpJ)) ** 2 / fpJ ** 2)) / (
                            2 * math.pi) ** 4 / f ** 5 * (
                            f > (9.81 / d) ** 0.5 / 2 / math.pi)  # SfTMA: Spectral energy density of TMA (m^2s)

        mn1TMAn=df*sum(SfTMA/f)# m-1 (a numerical solution)
        m0TMAn = sum(df * SfTMA)  # m0 
        m1TMAn = sum(df * f * SfTMA)  # m1
        m2TMAn = sum(df * f ** 2 * SfTMA)  # m2 
        m4TMAn=sum(df*f**4*SfTMA)# m4 (a numerical solution.)
        vTMA=(m0TMAn*m2TMAn/m1TMAn**2-1)**0.5
        epTMA=(1-m2TMAn**2/m0TMAn/m4TMAn)**0.5  
        feTMA=m0TMAn/mn1TMAn   
        Tm01TMA = m0TMAn / m1TMAn  # Tm01: mean period based on m0 and m1
        Tm02TMA = (m0TMAn / m2TMAn) ** 0.5  # Tm02: mean period based on m0 and m2
        # fpJ????? peak????

        data1 += (("TMA",str(round(mn1TMAn,2)),str(round(m0TMAn, 2)),str(round(m1TMAn, 2)),str(round(m2TMAn, 2)),str(round(m4TMAn, 3)),str(round(vTMA, 2)),str(round(epTMA, 2)),str(round(4.004 * m0TMAn ** 0.5, 3))),)
        # note.append(str15)
        plt.plot(f, SfTMA, label="TMA", ls="--", color="red", linewidth=1)

    # Wen Spectrum
    if c1==1:
        if Ts == None and Tz != None:#20220327
            Ts = 1.2 * Tz # 20220327  
            
    if c1 == 1 and Hs != None and Ts != None and d != None:  # 20220327
        PWen = 95.3 * Hs ** 1.35 / Ts ** 2.7
        SfWen = [0 for j in range(round((fu - fl) / df))]
        Fsw = 0.626 * Hs / d  # shallow water factor

        if Fsw <= 0.1:
            if PWen >= 1.54 and PWen < 6.77:
                for i in range(round((fu - fl) / df)):
                    if f[i] <= 1.05 / Ts:
                        SfWen[i] = 0.0687 * Hs ** 2 * Ts * PWen / np.exp(
                            95 * ((1.1 * Ts * f[i] - 1) ** 2) ** 1.2 * np.log(
                                PWen / (1.522 - 0.245 * PWen + 0.00292 * PWen ** 2)))
                    else:
                        SfWen[i] = 0.0824 * Hs ** 2 * (1.522 - 0.245 * PWen + 0.00292 * PWen ** 2) / Ts ** 3 / f[
                            i] ** 4

        elif Fsw <= 0.5:
            if PWen >= 1.27 and PWen < 6.77:
                for i in range(round((fu - fl) / df)):
                    if f[i] <= 1.05 / Ts:
                        SfWen[i] = 0.0687 * Hs ** 2 * Ts * PWen / np.exp(
                            95 * ((1.1 * Ts * f[i] - 1) ** 2) ** 1.2 * np.log(
                                PWen * (5.813 - 5.137 * Fsw) / (6.77 - 1.088 * PWen + 0.013 * PWen ** 2) / (
                                            1.307 - 1.426 * Fsw)))
                    else:
                        SfWen[i] = 0.0687 * Hs ** 2 * Ts * (6.77 - 1.088 * PWen + 0.013 * PWen ** 2) * (
                                    1.307 - 1.426 * Fsw) * (1.05 / Ts / f[i]) ** (2 * (2 - Fsw)) / (
                                                5.813 - 5.137 * Fsw)

        if max(SfWen) > 0:
            mn1Wenn=df*sum(SfWen/f)
            m0Wenn=df*sum(SfWen) 
            m1Wenn = df * sum(f * SfWen)
            m2Wenn = df * sum(f ** 2 * SfWen)
            m4Wenn=sum(df*f**4*SfWen)# m4 (a numerical solution.)
            vWen=(m0Wenn*m2Wenn/m1Wenn**2-1)**0.5
            epWen=(1-m2Wenn**2/m0Wenn/m4Wenn)**0.5  
            feWen=m0Wenn/mn1Wenn    
            Tm01Wen = m0Wenn / m1Wenn  # Tm01: mean period based on m0 and m1
            Tm02Wen = (m0Wenn / m2Wenn) ** 0.5  # Tm02: mean period based on m0 and m2
            fpWen = df * SfWen.index(max(SfWen)) + fl  # 1.05/Ts # 邱大洪(2010)？？？

            data1 += (("文圣常",str(round(mn1Wenn,2)),str(round(m0Wenn, 2)),str(round(m1Wenn, 2)),str(round(m2Wenn, 2)),str(round(m4Wenn, 3)),str(round(vWen, 2)),str(round(epWen, 2)),str(round(4.004 * m0Wenn ** 0.5, 3))),)
            # note.append(str16)
            plt.plot(f, SfWen, label="文圣常谱", linewidth=0.5, color="black")

    note.extend([''])
    # data2_heading1 = "Smax","fp","Tp","fe","Te","fa","Ta","frms","Tm\u2080\u2082"
    # data2_heading2 = "(m\u00b2s)","(Hz)","(s)","(Hz)","(s)","(Hz)","(s)","(Hz)","(s)"
    data2_heading = "Smax (m\u00b2s)","fp (Hz)","Tp (s)","fe (Hz)","Te (s)","fa (Hz)","Ta (s)","frms (Hz)","Tm\u2080\u2082 (s)"

    if c1==1:
        if X!=None and U!=None and el!=None and gamma!=None:
            data2 += (("JONSWAP",str(round(SfJmax, 2)),str(round(fpJ, 3)),str(round(1 / fpJ, 1)),str(round(feJ,3)),str(round(1/feJ,1)),str(round(1 / Tm01J, 3)),str(round(Tm01J, 1)),str(round(1 / Tm02J, 3)),str(round(Tm02J, 1))),)
            # note.append(str26) 
        if X!=None and U!=None and el!=None:
            data2 += (("Liu",str(round(SfLiumax, 2)),str(round(fpLiu, 3)),str(round(1 / fpLiu, 1)),str(round(feLiu,3)),str(round(1/feLiu,1)),str(round(1 / Tm01Liu, 3)),str(round(Tm01Liu, 1)),str(round(1 / Tm02Liu, 3)),str(round(Tm02Liu, 1))),) 
            # note.append(str27)                
            data2 += (("Mitsuyasu",str(round(SfMmax, 2)),str(round(fpM, 3)),str(round(1 / fpM, 1)),str(round(feM,3)),str(round(1/feM,1)),str(round(1 / Tm01M, 3)),str(round(Tm01M, 1)),str(round(1 / Tm02M, 3)),str(round(Tm02M, 1))),)  
            # note.append(str28) 
        if X!=None and U!=None and el!=None and d!=None:
            data2 += (("TMA",str(round(max(SfTMA), 2)),str(round(fpJ, 3)),str(round(1 / fpJ, 1)),str(round(feTMA,3)),str(round(1/feTMA,1)),str(round(1 / Tm01TMA, 3)),str(round(Tm01TMA, 1)),str(round(1 / Tm02TMA, 3)),str(round(Tm02TMA, 1))),) 
            # note.append(str29) 
        if Hs!=None and Ts!=None and d!=None and max(SfWen)>0:  
            data2 += (("文圣常",str(round(max(SfWen), 2)),str(round(fpWen, 3)),str(round(1 / fpWen, 1)),str(round(feWen,3)),str(round(1/feWen,1)),str(round(1 / Tm01Wen, 3)),str(round(Tm01Wen, 1)),str(round(1 / Tm02Wen, 3)),str(round(Tm02Wen, 1))),) 
            # note.append(str30) 

    if c1==2:
        if Ts!=None and Hs!=None:
            data2 += (("B-M",str(round(SfBMmax, 2)),str(round(fpBM, 3)),str(round(1 / fpBM, 1)),str(round(feBM,3)),str(round(1/feBM,1)),str(round(1 / Tm01BM, 3)),str(round(Tm01BM, 1)),str(round(1 / Tm02BM, 3)),str(round(Tm02BM, 1))),)
            # note.append(str19) 
            data2 += (('M B-M',str(round(SfMBMmax,2)),str(round(fpMBM,3)),str(round(1/fpMBM,1)),str(round(feMBM,3)),str(round(1/feMBM,1)),str(round(1/Tm01MBM,3)),str(round(Tm01MBM,1)),str(round(1/Tm02MBM,3)),str(round(Tm02MBM,1))),)
            # note.append(str20) 
        if HsPM!=None:   
            data2 += (("P-M",str(round(SfPMmax, 2)),str(round(fpPM, 3)),str(round(1 / fpPM, 1)),str(round(fePM,3)),str(round(1/fePM,1)),str(round(1 / Tm01PM, 3)),str(round(Tm01PM, 1)),str(round(1 / Tm02PM, 3)),str(round(Tm02PM, 1))),) 
            # note.append(str21)
        if Hs!=None:   
            data2 += (("O-H",str(round(SfOHmax1, 2)),str(round(fp1OH, 3)),str(round(1 / fp1OH, 1)),str(round(feOH,3)),str(round(1/feOH,1)),str(round(1 / Tm01OH, 3)),str(round(Tm01OH, 1)),str(round(1 / Tm02OH, 3)),str(round(Tm02OH, 1))),) 
            # note.append(str22)
        if Hs!=None and Tp!=None and X!=None:
            data2 += (("Torsethaugen-S",str(round(max(SfST), 2)),str(round(1 / Tp, 3)),str(round(Tp, 1)),str(round(feST,3)),str(round(1/feST,1)),str(round(1 / Tm01ST, 3)),str(round(Tm01ST, 1)),str(round(1 / Tm02ST, 3)),str(round(Tm02ST, 1))),)
            # data2 += (("sT",str(round(max(SfST), 2)),str(round(1 / Tp, 3)),str(round(Tp, 1)),str(round(feST,3)),str(round(1/feST,1)),str(round(1 / Tm01ST, 3)),str(round(Tm01ST, 1)),str(round(1 / Tm02ST, 3)),str(round(Tm02ST, 1))),)
            # note.append(str23)
        if Hs!=None and fpJG!=None and gamma!=None:      
            data2 += (("JONSWAP-G1",str(round(SfJG1max, 2)),str(round(fpJG, 3)),str(round(1 / fpJG, 1)),str(round(feJG1,3)),str(round(1/feJG1,1)),str(round(1 / Tm01JG1, 3)),str(round(Tm01JG1, 1)),str(round(1 / Tm02JG1, 3)),str(round(Tm02JG1, 1))),) 
            # data2 += (("J-G1",str(round(SfJG1max, 2)),str(round(fpJG, 3)),str(round(1 / fpJG, 1)),str(round(feJG1,3)),str(round(1/feJG1,1)),str(round(1 / Tm01JG1, 3)),str(round(Tm01JG1, 1)),str(round(1 / Tm02JG1, 3)),str(round(Tm02JG1, 1))),) 
            # note.append(str24)
            data2 += (("JONSWAP-G2",str(round(SfJG2max, 2)),str(round(fpJG, 3)),str(round(1 / fpJG, 1)),str(round(feJG2,3)),str(round(1/feJG2,1)),str(round(1 / Tm01JG2, 3)),str(round(Tm01JG2, 1)),str(round(1 / Tm02JG2, 3)),str(round(Tm02JG2, 1))),)
            # data2 += (("J-G2",str(round(SfJG2max, 2)),str(round(fpJG, 3)),str(round(1 / fpJG, 1)),str(round(feJG2,3)),str(round(1/feJG2,1)),str(round(1 / Tm01JG2, 3)),str(round(Tm01JG2, 1)),str(round(1 / Tm02JG2, 3)),str(round(Tm02JG2, 1))),)
            # note.append(str25)

    # Illstrations and Data Export
    
    note.extend([''])
    # content.extend(['说明：'])
    # content.extend(['1. 计算结果中的频率均为循环频率f(Hz)。'])
    content.extend(['计算结果中的频率均为循环频率f(Hz)。'])
    # note.extend(['2. 表中各物理量： Smax为谱密度峰值，fp为Smax的循环频率（除非另有说明），Tp=1/fp，m\u2080为谱零阶原点矩，m\u2081为谱1阶原点矩，m\u2082为谱二阶原点矩，m\u2084为谱四阶原点矩，\u03BD为谱宽[=(m\u2080m\u2082/m\u2081\u00b2-1)\u2070\u22C5\u2075]，\u03B5为谱带宽[=(1-m\u2082\u00b2/m\u2080/m\u2084)\u2070\u22C5\u2075]，fa为平均频率(=m\u2081/m\u2080)，Ta=1/fa，\
    # frms为均方根频率[=(m\u2082/m\u2080)\u2070\u22C5\u2075]，Tm\u2080\u2082=1/frms，Hsm\u2080为通过m\u2080按m\u2080和Hs间近似关系估计得到的Hs。'])
    # content.extend(['2. 表中各物理量： m\u208b\u2081为谱负一阶原点矩，m\u2080为谱零阶原点矩，m\u2081为谱1阶原点矩，m\u2082为谱二阶原点矩，m\u2084为谱四阶原点矩，\u03BD为谱宽[=(m\u2080m\u2082/m\u2081\u00b2-1)\u2070\u22C5\u2075]，\u03B5为谱带宽[=(1-m\u2082\u00b2/m\u2080/m\u2084)\u2070\u22C5\u2075]，Hsm\u2080为通过m\u2080按m\u2080和Hs间近似关系估计得到的Hs，\
    # Smax为谱密度峰值，fp为Smax的循环频率（除非另有说明），Tp=1/fp，fe为能量频率(=m\u2080/m\u208b\u2081)，Te为能量周期(=1/fe)，fa为平均频率(=m\u2081/m\u2080)，Ta=1/fa，frms为均方根频率[=(m\u2082/m\u2080)\u2070\u22C5\u2075]，Tm\u2080\u2082=1/frms。'])
    content.extend(['表中各物理量： m\u208b\u2081为谱负一阶原点矩，m\u2080为谱零阶原点矩，m\u2081为谱1阶原点矩，m\u2082为谱二阶原点矩，m\u2084为谱四阶原点矩，\u03BD为谱宽[=(m\u2080m\u2082/m\u2081\u00b2-1)\u2070\u22C5\u2075]，\u03B5为谱带宽[=(1-m\u2082\u00b2/m\u2080/m\u2084)\u2070\u22C5\u2075]，Hsm\u2080为通过m\u2080按m\u2080和Hs间近似关系估计得到的Hs，\
    Smax为谱密度峰值，fp为Smax的循环频率（除非另有说明），Tp=1/fp，fe为能量频率(=m\u2080/m\u208b\u2081)，Te为能量周期(=1/fe)，fa为平均频率(=m\u2081/m\u2080)，Ta=1/fa，frms为均方根频率[=(m\u2082/m\u2080)\u2070\u22C5\u2075]，Tm\u2080\u2082=1/frms。'])

    # content.extend(['3. 除非另有说明,表中的Smax和fp均为谱计算的结果。由于频率域离散化的精度限制，直接计算得到的fp不一定落在一个频率域离散点上，故直接计算得到的Smax有可能不会在图中显示。'])
    content.extend(['除非另有说明,表中的Smax和fp均为谱计算的结果。由于频率域离散化的精度限制，直接计算得到的fp不一定落在一个频率域离散点上，故直接计算得到的Smax有可能不会在图中显示。'])
    
    if c1 == 1:     
        if X!=None and U!=None and el!=None:   #20220327 
            # content.extend(['4. Liu谱的零至二阶原点矩按基本Bretschneider谱型的理论方法求得，其它原点矩则均为数值近似值。'])
            content.extend(['Liu谱的零至二阶原点矩按基本Bretschneider谱型的理论方法求得，其它原点矩则均为数值近似值。'])
        else:
            # content.extend(['4. 由于输入参数不满足JONSWAP谱、Liu谱、Mitsuyasu谱的要求，这三个谱在此不适用。'])
            content.extend(['由于输入参数不满足JONSWAP谱、Liu谱、Mitsuyasu谱的要求，这三个谱在此不适用。'])
        if X!=None and U!=None and el!=None and d!=None:#20220327
            # content.extend(['5. TMA谱的Smax直接从图中读取，fp为JONSWAP谱的fp。这个fp并不一定对应TMA谱的Smax。'])
            content.extend(['TMA谱的Smax直接从图中读取，fp为JONSWAP谱的fp。这个fp并不一定对应TMA谱的Smax。'])
        else:
            # content.extend(['5. 由于输入参数不满足TMA谱的要求，该谱在此不适用。'])
            content.extend(['由于输入参数不满足TMA谱的要求，该谱在此不适用。'])
        if Hs!=None and Ts!=None and d!=None and max(SfWen)>0: #20220327   
            # content.extend(['6. 文圣常谱的Smax和fp直接从图中读取。'])
            content.extend(['文圣常谱的Smax和fp直接从图中读取。'])
        else:
            # content.extend(['6. 由于输入参数不满足文圣常谱的要求，该谱在此不适用。'])
            content.extend(['由于输入参数不满足文圣常谱的要求，该谱在此不适用。'])
        if gamma==None:
            # content.extend(['7. 由于输入参数不满足JONSWAP谱的要求，该谱在此不适用。'])
            content.extend(['由于输入参数不满足JONSWAP谱的要求，该谱在此不适用。'])
    if c1 == 2:
        if HsPM != None:
            if U != None: 
                # content.extend(['4. P-M谱仅根据输入的风速计算得到，未使用任何已知波浪要素。'])
                content.extend(['P-M谱仅根据输入的风速计算得到，未使用任何已知波浪要素。'])
            else:
                # content.extend(['4. 输入的已知波浪要素适用于P-M谱。'])
                content.extend(['输入的已知波浪要素适用于P-M谱。'])
        else:
            # content.extend(['4. 由于输入参数不满足P-M谱的要求，该谱在此不适用。'])    
            content.extend(['由于输入参数不满足P-M谱的要求，该谱在此不适用。'])    
        if Ts!=None and Hs!=None and HsPM!=None:
            # content.extend(['5. B-M、M B-M、P-M谱的负一至二阶原点矩按理论方法求得，其它原点矩则均为数值近似值。'])
            content.extend(['B-M、M B-M、P-M谱的负一至二阶原点矩按理论方法求得，其它原点矩则均为数值近似值。'])
        else:
            if Ts!=None and Hs!=None:
                # content.extend(['5. B-M、M B-M谱的负一至二阶原点矩按理论方法求得，其它原点矩则均为数值近似值。'])  
                content.extend(['B-M、M B-M谱的负一至二阶原点矩按理论方法求得，其它原点矩则均为数值近似值。'])  
            if HsPM!=None:
                # content.extend(['5. P-M谱的负一至二阶原点矩按理论方法求得，其它原点矩则均为数值近似值。'])      
                content.extend(['P-M谱的负一至二阶原点矩按理论方法求得，其它原点矩则均为数值近似值。'])      
        if Hs!=None:#20220327               
            # str1="6. 计算结果中的O-H谱仅为最可能谱型。表中的fp为其低频成分的峰值频率，Smax位于fp处，高频成分的峰值频率在"+str(round(fp2OH, 2))+"Hz。"    
            str1="计算结果中的O-H谱仅为最可能谱型。表中的fp为其低频成分的峰值频率，Smax位于fp处，高频成分的峰值频率在"+str(round(fp2OH, 2))+"Hz。"    
            content.append(str1)
        else:
            # content.extend(['6. 由于输入参数不满足O-H谱的要求，该谱在此不适用。'])
            content.extend(['由于输入参数不满足O-H谱的要求，该谱在此不适用。'])
        if Hs!=None and Tp!=None and X!=None: #20220327 
            # str2='7. 对于Torsethaugen-S谱，Smax直接从图中读取，Tp为输入的参数，fp为Tp的倒数。fp实为主峰频率，次峰频率在'+str(round(1 / Tps * (Tp <= Tf) + 1 / Tpw * (Tp > Tf), 2))+ 'Hz。'  # 20220328
            str2='对于Torsethaugen-S谱，Smax直接从图中读取，Tp为输入的参数，fp为Tp的倒数。fp实为主峰频率，次峰频率在'+str(round(1 / Tps * (Tp <= Tf) + 1 / Tpw * (Tp > Tf), 2))+ 'Hz。'  # 20220328
            content.append(str2)           
        else:
            # content.extend(['7. 由于输入参数不满足Torsethaugen-S谱的要求，该谱在此不适用。'])
            content.extend(['由于输入参数不满足Torsethaugen-S谱的要求，该谱在此不适用。'])
        if Hs == None or fpJG == None or gamma==None:
            # content.extend(['8. 由于输入参数不满足JONSWAP-G1谱和JONSWAP-G1谱的要求，这两个谱在此不适用。'])
            content.extend(['由于输入参数不满足JONSWAP-G1谱和JONSWAP-G1谱的要求，这两个谱在此不适用。'])
        if Ts == None or Hs==None:        
            # content.extend(['9. 由于输入参数不满足P-M谱的要求，该谱在此不适用。'])
            content.extend(['由于输入参数不满足P-M谱的要求，该谱在此不适用。'])
                                                    
    # note.extend([''])  # 20220310
    ending = '---结果展示结束---'
    plt.xlabel('f (Hz)')
    plt.ylabel('S (m$^2$s)')         
    plt.legend()
    # plt.rcParams['font.sans-serif'] = ['Kaiti']  # ['FangSong']
    # plt.show()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_stream = base64.b64encode(img.getvalue()).decode()
    plt.close("all")
    # print(note)
    # print(img_stream)
    # print(data1_heading)
    # print(data2_heading)
    # print(data1)
    # print(data2)
    # print(content)
    # return  img_stream, heading, data1, data1_heading1, data1_heading2, data2, data2_heading1, data2_heading2, content, ending
    return  img_stream, heading, data1, data1_heading, data2, data2_heading, content, ending
    # return  img_stream, note
