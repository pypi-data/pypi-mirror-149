# 著作者：叶凯文
# Author: YE KAIWEN
# 版权归著作者叶凯文所有
# Copyright (c) 2022 YE KAIWEN. All Rights Reserved.

import numpy as np
import pandas as pd
from .Models import common_model
from .StockModels import company_model,AFREQS
from .ModelSets import common_modelset
from .StockModelSets import company_modelset

class ConnectionMethod1:
    def __init__(self,dtpow=2,fmpow=2,dtsopen=1/2,fmsopen=1/2):
        self.dtpow=dtpow
        self.fmpow=fmpow
        self.dtsopen=dtsopen
        self.fmsopen=fmsopen

    def seriesmethod(self,series1,series2):
        distance = pow(pow(series1-series2,self.dtpow).sum(),self.dtsopen)
        formator = pow(pow(series1+series2,self.fmpow).sum(),self.fmsopen)
        return distance / formator

    def elementmethod(self,element1,element2):
        distance = pow(pow(element1-element2,self.dtpow),self.dtsopen)
        formator = pow(pow(element1+element2,self.fmpow),self.fmsopen)
        return distance / formator

class ConnectionMethod2:
    def __init__(self,dtpow=2,fmpow=2,dtsopen=1/2,fmsopen=1/2):
        self.dtpow=dtpow
        self.fmpow=fmpow
        self.dtsopen=dtsopen
        self.fmsopen=fmsopen

    def seriesmethod(self,series1,series2):
        distance = pow(pow(series1-series2,self.dtpow).sum(),self.dtsopen)
        formator = pow((pow(series1,self.fmpow)+pow(series2,self.fmpow)).sum(),self.fmsopen)
        return distance / formator

    def elementmethod(self,element1,element2):
        distance = pow(pow(element1-element2,self.dtpow),self.dtsopen)
        formator = pow((pow(element1,self.fmpow)+pow(element2,self.fmpow)),self.fmsopen)
        return distance / formator

class ConnectionMethod3:
    def __init__(self,coef1,coef2):
        self.coef1=coef1
        self.coef2=coef2

    def seriesmethod(self,series1,series2):
        return self.coef1*np.exp(pow(series1-series2,2).sum()/(2*self.coef2))

    def elementmethod(self,element1,element2):
        return self.coef1 * np.exp(pow(element1 - element2, 2) / (2 * self.coef2))

class ConnectionMethod4:
    def seriesmethod(self,series1,series2):
        simularity=(series1*series2/(series1+series2)).sum()
        if simularity==0:
            return np.inf
        else:
            return 1/simularity

    def elementmethod(self,element1,element2):
        simularity=(element1*element2/(element1+element2))
        if simularity == 0:
            return np.inf
        else:
            return 1 / simularity

class ConnectionMethod5:
    def seriesmethod(self,series1,series2):
        simularity=(series1*series2).sum()/np.sqrt(pow(series1,2).sum()*pow(series2,2).sum())
        if simularity == 0:
            return np.inf
        else:
            return 1 / simularity

    def elementmethod(self,element1,element2):
        simularity=(element1*element2)/np.sqrt(pow(element1,2)*pow(element2,2))
        if simularity == 0:
            return np.inf
        else:
            return 1 / simularity

class CommonResonanceModel:
    def __init__(self,models,connection):
        self._models=models
        self._connection=connection
        self.__getfreqparams()

    def __getfreqparams(self):
        if isinstance(self._models[0], common_model):
            self._freq=self._models[0]._mparams['freq']
            self._AP=len(pd.date_range(start='2022-01-01',end='2022-12-31',freq=self._freq))
        elif isinstance(self._models[0], company_model):
            if (self._models[0]._mparams['ttm']):
                self._freq=AFREQS[self._models[0]._mparams['reportdate'][-4:]]
                self._AP=1
            else:
                self._freq='Q-DEC'
                self._AP = 4
        elif isinstance(self._models[0], StockSetDimensionModel):
            if (self._models[0]._mparams['ttm']):
                self._freq=AFREQS[self._models[0]._mparams['reportdate'][-4:]]
                self._AP=1
            else:
                self._freq='Q-DEC'
                self._AP = 4
        elif isinstance(self._models[0], ModelSetDimensionModel):
            self._freq=self._models[0]._mparams['freq']
            self._AP=len(pd.date_range(start='2022-01-01',end='2022-12-31',freq=self._freq))
        else:
            raise Exception("模型类型错误")
        reportlist=[]
        for model in self._models:
            if isinstance(model,common_model):
                if (model._mparams['freq']==self._freq):
                    reportlist.append(model._data.index[-1])
                else:
                    raise Exception("模型类型错误")
            elif isinstance(model,company_model):
                if (model._mparams['ttm']):
                    if (AFREQS[model._mparams['reportdate'][-4:]]==self._freq):
                        reportlist.append(pd.to_datetime(model._mparams['reportdate']))
                    else:
                        raise Exception("模型类型错误")
                else:
                    reportlist.append(pd.to_datetime(model._mparams['reportdate']))
            elif isinstance(model,StockSetDimensionModel):
                if (model._mparams['ttm']):
                    if (AFREQS[model._mparams['reportdate'][-4:]]==self._freq):
                        reportlist.append(pd.to_datetime(model._mparams['reportdate']))
                    else:
                        raise Exception("模型类型错误")
                else:
                    reportlist.append(pd.to_datetime(model._mparams['reportdate']))
            elif isinstance(model,ModelSetDimensionModel):
                if (model._mparams['freq']==self._freq):
                    reportlist.append(model.data().index[-1])
                else:
                    raise Exception("模型类型错误")
            else:
                raise Exception("模型类型错误")
        reportmax=np.array(reportlist).max()
        periodgaps=[]
        for report in reportlist:
            periodgaps.append(len(pd.date_range(start=report,end=reportmax,freq=self._freq))-1)
        self._periodgaps=periodgaps

    def forecast(self,t,droplow=0):
        fores=[]
        mnum=len(self._models)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        for i in range(mnum):
            foreseries=self._models[i].forecast(t+self._periodgaps[i])
            fores.append(foreseries.iloc[self._periodgaps[i]:])
        if len(fores)==0:
            return None
        elif len(fores)==1:
            return fores[0]
        fores=pd.DataFrame(fores).transpose()
        resonances=[]
        for i in range(mnum):
            cw=0
            for j in range(mnum):
                if i==j:
                    continue
                cw+=self._connection.seriesmethod(fores[i],fores[j])
            if cw==0:
                return fores[0]
            resonances.append(1/cw)
        resonances=pd.Series(resonances)
        for m in range(droplow):
            dinx=resonances.idxmin()
            del resonances[dinx]
            del fores[dinx]
        return (fores*resonances).sum(1)/(resonances.sum())

    def pv(self,r,droplow=0):
        pvs=[]
        mnum = len(self._models)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        sr=pow(1+r,1/self._AP)-1
        for i in range(mnum):
            if self._models[i]._mparams['seasonal']:
                pvs.append(self._models[i].pv(r)*pow(1+r,self._periodgaps[i]/self._AP))
            else:
                pvs.append(self._models[i].pv(sr) * pow(1+r, self._periodgaps[i] / self._AP))
        if len(pvs)==0:
            return None
        elif len(pvs)==1:
            return pvs[0]
        pvs=pd.Series(pvs)
        resonances=[]
        for i in range(mnum):
            cw=0
            for j in range(mnum):
                if i==j:
                    continue
                cw+=self._connection.elementmethod(pvs[i],pvs[j])
            if cw==0:
                return pvs[0]
            resonances.append(1/cw)
        resonances=pd.Series(resonances)
        for m in range(droplow):
            dinx=resonances.idxmin()
            del resonances[dinx]
            del pvs[dinx]
        return (pvs*resonances).sum()/(resonances.sum())

    def irr(self,price,tradedate,droplow=0):
        rates=[]
        mnum = len(self._models)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        for i in range(mnum):
            irr = self._models[i].irr(price, tradedate)
            if type(irr) == float:
                if self._models[i]._mparams['seasonal']:
                    rates.append(1+irr)
                else:
                    rates.append(pow(1 + irr,self._AP))
        if len(rates)==0:
            return None
        elif len(rates)==1:
            return rates[0]-1
        rates=np.log(pd.Series(rates))
        resonances=[]
        for i in range(len(rates)):
            cw=0
            for j in range(len(rates)):
                if i==j:
                    continue
                cw+=self._connection.elementmethod(rates[i],rates[j])
            if cw==0:
                return np.exp(rates[0])-1
            resonances.append(1/cw)
        resonances=pd.Series(resonances)
        for m in range(droplow-(mnum-len(rates))):
            dinx=resonances.idxmin()
            del resonances[dinx]
            del rates[dinx]
        if len(rates)>0:
            return np.exp((rates * resonances).sum() / (resonances.sum()))-1
        else:
            return None

    def batchirr(self,priceseries,droplow=0):
        batchrates=[]
        mnum = len(self._models)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        for i in range(mnum):
            if self._models[i]._mparams['seasonal']:
                batchrates.append(1+self._models[i].batchirr(priceseries)['IRRs'])
            else:
                batchrates.append(pow(1+self._models[i].batchirr(priceseries)['IRRs'],self._AP))
        batchrates=np.log(pd.DataFrame(batchrates).transpose())
        irrs=pd.Series(index=batchrates.index)
        for index,row in batchrates.iterrows():
            rates=row.copy(deep=True).dropna()
            if len(rates) == 0:
                irrs[index]=np.nan
                continue
            elif len(rates) == 1:
                irrs[index]=np.exp(rates.values[0])-1
                continue
            rates=rates.reset_index(drop=True)
            resonances = []
            homo=False
            for i in range(len(rates)):
                cw = 0
                for j in range(len(rates)):
                    if i == j:
                        continue
                    cw += self._connection.elementmethod(rates[i], rates[j])
                if cw == 0:
                    homo = True
                    break
                resonances.append(1 / cw)
            if homo:
                resonances = pd.Series(np.ones(len(rates)))
            else:
                resonances = pd.Series(resonances)
            for m in range(droplow-(mnum-len(rates))):
                dinx = resonances.idxmin()
                del resonances[dinx]
                del rates[dinx]
            if len(rates)>0:
                irrs[index] = np.exp((rates * resonances).sum() / (resonances.sum()))-1
            else:
                irrs[index]=np.nan
        return irrs

    def achieverate(self,price,r,tradedate,droplow=0):
        acrs = []
        mnum = len(self._models)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        sr = pow(1 + r, 1 / self._AP) - 1
        for i in range(mnum):
            if self._models[i]._mparams['seasonal']:
                acrs.append(self._models[i].achieverate(price,r,tradedate))
            else:
                acrs.append(self._models[i].achieverate(price,sr,tradedate))
        if len(acrs) == 0:
            return None
        elif len(acrs) == 1:
            return acrs[0]
        acrs = pd.Series(acrs)
        resonances = []
        for i in range(mnum):
            cw = 0
            for j in range(mnum):
                if i == j:
                    continue
                cw += self._connection.elementmethod(acrs[i], acrs[j])
            if cw == 0:
                return acrs[0]
            resonances.append(1 / cw)
        resonances = pd.Series(resonances)
        for m in range(droplow):
            dinx=resonances.idxmin()
            del resonances[dinx]
            del acrs[dinx]
        return (acrs*resonances).sum()/(resonances.sum())

    def batchachieverate(self,priceseries,r,droplow=0):
        batchacrs=[]
        mnum = len(self._models)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        sr = pow(1 + r, 1 / self._AP) - 1
        for i in range(mnum):
            if self._models[i]._mparams['seasonal']:
                batchacrs.append(self._models[i].batchachieverate(priceseries,r))
            else:
                batchacrs.append(self._models[i].batchachieverate(priceseries,sr))
        batchacrs=pd.DataFrame(batchacrs).transpose()
        acrs=pd.Series(index=batchacrs.index)
        for index,row in batchacrs.iterrows():
            rates=row.copy(deep=True)
            if len(rates) == 0:
                acrs[index]=np.nan
                continue
            elif len(rates) == 1:
                acrs[index]=rates.values[0]
                continue
            resonances = []
            homo = False
            for i in range(mnum):
                cw = 0
                for j in range(mnum):
                    if i == j:
                        continue
                    cw += self._connection.elementmethod(rates[i], rates[j])
                if cw == 0:
                    homo = True
                    break
                resonances.append(1 / cw)
            if homo:
                resonances = pd.Series(np.ones(len(rates)))
            else:
                resonances = pd.Series(resonances)
            for m in range(droplow):
                dinx = resonances.idxmin()
                del resonances[dinx]
                del rates[dinx]
            acrs[index] = (rates*resonances).sum()/(resonances.sum())
        return acrs

class CompanyResonanceModel(CommonResonanceModel):
    def __init__(self,models,connection):
        self._models=models
        self._connection=connection
        self.__getfreqparams()

    def __getfreqparams(self):
        if isinstance(self._models[0], company_model):
            if (self._models[0]._mparams['ttm']):
                self._freq=AFREQS[self._models[0]._mparams['reportdate'][-4:]]
                self._AP=1
            else:
                self._freq='Q-DEC'
                self._AP = 4
        elif isinstance(self._models[0], StockSetDimensionModel):
            if (self._models[0]._mparams['ttm']):
                self._freq=AFREQS[self._models[0]._mparams['reportdate'][-4:]]
                self._AP=1
            else:
                self._freq='Q-DEC'
                self._AP = 4
        else:
            raise Exception("模型类型错误")
        reportlist=[]
        for model in self._models:
            if isinstance(model,company_model):
                if (model._mparams['ttm']):
                    if (AFREQS[model._mparams['reportdate'][-4:]]==self._freq):
                        reportlist.append(pd.to_datetime(model._mparams['reportdate']))
                    else:
                        raise Exception("模型类型错误")
                else:
                    reportlist.append(pd.to_datetime(model._mparams['reportdate']))
            elif isinstance(model,StockSetDimensionModel):
                if (model._mparams['ttm']):
                    if (AFREQS[model._mparams['reportdate'][-4:]]==self._freq):
                        reportlist.append(pd.to_datetime(model._mparams['reportdate']))
                    else:
                        raise Exception("模型类型错误")
                else:
                    reportlist.append(pd.to_datetime(model._mparams['reportdate']))
            else:
                raise Exception("模型类型错误")
        reportmax=np.array(reportlist).max()
        periodgaps=[]
        for report in reportlist:
            periodgaps.append(len(pd.date_range(start=report,end=reportmax,freq=self._freq))-1)
        self._periodgaps=periodgaps

    def irr_trade(self,pricemode,tradedate,droplow=0):
        rates=[]
        mnum = len(self._models)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        for i in range(mnum):
            irr=self._models[i].irr_trade(pricemode,tradedate)
            if type(irr)==float:
                if self._models[i]._mparams['seasonal']:
                    rates.append(1+irr)
                else:
                    rates.append(pow(1 + irr,self._AP))
        if len(rates)==0:
            return None
        elif len(rates)==1:
            return rates[0]-1
        rates=np.log(pd.Series(rates))
        resonances=[]
        for i in range(len(rates)):
            cw=0
            for j in range(len(rates)):
                if i==j:
                    continue
                cw+=self._connection.elementmethod(rates[i],rates[j])
            if cw==0:
                return np.exp(rates[0])-1
            resonances.append(1/cw)
        resonances=pd.Series(resonances)
        for m in range(droplow-(mnum-len(rates))):
            dinx=resonances.idxmin()
            del resonances[dinx]
            del rates[dinx]
        if len(rates)>0:
            return np.exp((rates * resonances).sum() / (resonances.sum()))-1
        else:
            return None

    def batchirr_trade(self,pricemode,startdate,enddate,droplow=0):
        batchrates=[]
        mnum = len(self._models)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        for i in range(mnum):
            if self._models[i]._mparams['seasonal']:
                batchrates.append(1+self._models[i].batchirr_trade(pricemode,startdate,enddate)['IRRs'])
            else:
                batchrates.append(pow(1+self._models[i].batchirr_trade(pricemode,startdate,enddate)['IRRs'],self._AP))
        batchrates=np.log(pd.DataFrame(batchrates).transpose())
        irrs=pd.Series(index=batchrates.index)
        for index,row in batchrates.iterrows():
            rates=row.copy(deep=True).dropna()
            if len(rates) == 0:
                irrs[index] = np.nan
                continue
            elif len(rates) == 1:
                irrs[index] = np.exp(rates.values[0]) - 1
                continue
            rates=rates.reset_index(drop=True)
            resonances = []
            homo = False
            for i in range(len(rates)):
                cw = 0
                for j in range(len(rates)):
                    if i == j:
                        continue
                    cw += self._connection.elementmethod(rates[i], rates[j])
                if cw == 0:
                    homo = True
                    break
                resonances.append(1 / cw)
            if homo:
                resonances = pd.Series(np.ones(len(rates)))
            else:
                resonances = pd.Series(resonances)
            for m in range(droplow-(mnum-len(rates))):
                dinx = resonances.idxmin()
                del resonances[dinx]
                del rates[dinx]
            if len(rates)>0:
                irrs[index] = np.exp((rates * resonances).sum() / (resonances.sum()))-1
            else:
                irrs[index] = np.nan
        return irrs

    def achieverate_trade(self, pricemode, tradedate, r,droplow=0):
        acrs = []
        mnum = len(self._models)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        sr = pow(1 + r, 1 / self._AP) - 1
        for i in range(mnum):
            if self._models[i]._mparams['seasonal']:
                acrs.append(self._models[i].achieverate_trade(pricemode, tradedate, r))
            else:
                acrs.append(self._models[i].achieverate_trade(pricemode, tradedate, sr))
        if len(acrs) == 0:
            return None
        elif len(acrs) == 1:
            return acrs[0]
        acrs = pd.Series(acrs)
        resonances = []
        for i in range(mnum):
            cw = 0
            for j in range(mnum):
                if i == j:
                    continue
                cw += self._connection.elementmethod(acrs[i], acrs[j])
            if cw == 0:
                return acrs[0]
            resonances.append(1 / cw)
        resonances = pd.Series(resonances)
        for m in range(droplow):
            dinx=resonances.idxmin()
            del resonances[dinx]
            del acrs[dinx]
        return (acrs*resonances).sum()/(resonances.sum())

    def batchachieverate_trade(self, pricemode, startdate, enddate, r,droplow=0):
        batchacrs=[]
        mnum = len(self._models)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        sr = pow(1 + r, 1 / self._AP) - 1
        for i in range(mnum):
            if self._models[i]._mparams['seasonal']:
                batchacrs.append(self._models[i].batchachieverate_trade(pricemode, startdate, enddate, r))
            else:
                batchacrs.append(self._models[i].batchachieverate_trade(pricemode, startdate, enddate,sr))
        batchacrs=pd.DataFrame(batchacrs).transpose()
        acrs=pd.Series(index=batchacrs.index)
        for index,row in batchacrs.iterrows():
            rates=row.copy(deep=True)
            if len(rates) == 0:
                acrs[index]=np.nan
                continue
            elif len(rates) == 1:
                acrs[index]=rates.values[0]
                continue
            resonances = []
            homo = False
            for i in range(mnum):
                cw = 0
                for j in range(mnum):
                    if i == j:
                        continue
                    cw += self._connection.elementmethod(rates[i], rates[j])
                if cw == 0:
                    homo = True
                    break
                resonances.append(1 / cw)
            if homo:
                resonances = pd.Series(np.ones(len(rates)))
            else:
                resonances = pd.Series(resonances)
            for m in range(droplow):
                dinx = resonances.idxmin()
                del resonances[dinx]
                del rates[dinx]
            acrs[index] = (rates*resonances).sum()/(resonances.sum())
        return acrs

class ModelSetDimensionModel:
    def __init__(self,modelset,dimension):
        self._modelset=modelset
        self._dimension=dimension
        self._mparams=modelset._mparams

    def model(self):
        return self._modelset.modelset()[self._dimension]

    def fit(self):
        return self._modelset.fit(self._dimension)

    def forecast(self,t):
        return self._modelset.forecast(self._dimension,t)

    def pv(self,r):
        return self._modelset.pv(self._dimension,r)

    def irr(self,price,tradedate):
        return self._modelset.irr(self._dimension,price,tradedate)

    def batchirr(self,priceseries):
        return self._modelset.batchirr(self._dimension,priceseries)

    def achieverate(self,price,r,tradedate):
        return self._modelset.achieverate(self._dimension,price,r,tradedate)

    def batchachieverate(self,priceseries,r):
        return self._modelset.batchachieverate(self._dimension,priceseries,r)

    def data(self):
        return self._modelset._data[self._dimension]

class StockSetDimensionModel(ModelSetDimensionModel):
    def irr_trade(self, pricemode, tradedate):
        return self._modelset.irr_trade(self._dimension, pricemode, tradedate)

    def batchirr_trade(self, pricemode, startdate, enddate):
        return self._modelset.batchirr_trade(self._dimension, pricemode, startdate, enddate)

    def achieverate_trade(self,pricemode, tradedate, r):
        return self._modelset.achieverate_trade(self._dimension,pricemode, tradedate, r)

    def batchachieverate_trade(self, pricemode, startdate, enddate, r):
        return self._modelset.batchachieverate_trade(self._dimension, pricemode, startdate, enddate, r)

    def incdata(self):
        return self._modelset.incdata(self._dimension)

class CommonResonanceModelSet:
    def __init__(self,modelsets,connection):
        self._modelsets=modelsets
        self._connection=connection
        self.__getfreqparams()

    def __getfreqparams(self):
        if isinstance(self._modelsets[0], common_modelset):
            self._freq = self._modelsets[0]._mparams['freq']
            self._AP = len(pd.date_range(start='2022-01-01', end='2022-12-31', freq=self._freq))
        elif isinstance(self._modelsets[0], company_modelset):
            if (self._modelsets[0]._mparams['ttm']):
                self._freq = AFREQS[self._modelsets[0]._mparams['reportdate'][-4:]]
                self._AP = 1
            else:
                self._freq = 'Q-DEC'
                self._AP = 4
        else:
            raise Exception("模型类型错误")
        reportlist = []
        for modelset in self._modelsets:
            if isinstance(modelset, common_modelset):
                if (modelset._mparams['freq'] == self._freq):
                    reportlist.append(modelset._data.index[-1])
                else:
                    raise Exception("模型类型错误")
            elif isinstance(modelset, company_modelset):
                if (modelset._mparams['ttm']) :
                    if (AFREQS[modelset._mparams['reportdate'][-4:]] == self._freq):
                        reportlist.append(pd.to_datetime(modelset._mparams['reportdate']))
                    else:
                        raise Exception("模型类型错误")
                else:
                    reportlist.append(pd.to_datetime(modelset._mparams['reportdate']))
            else:
                raise Exception("模型类型错误")
        reportmax = np.array(reportlist).max()
        periodgaps = []
        for report in reportlist:
            periodgaps.append(len(pd.date_range(start=report, end=reportmax, freq=self._freq)) - 1)
        self._periodgaps = periodgaps

    def forecast(self,dimension,t,droplow=0):
        fores=[]
        mnum=len(self._modelsets)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        for i in range(mnum):
            foreseries=self._modelsets[i].forecast(dimension,t+self._periodgaps[i])
            fores.append(foreseries.iloc[self._periodgaps[i]:])
        if len(fores)==0:
            return None
        elif len(fores)==1:
            return fores[0]
        fores=pd.DataFrame(fores).transpose()
        resonances=[]
        for i in range(mnum):
            cw=0
            for j in range(mnum):
                if i==j:
                    continue
                cw+=self._connection.seriesmethod(fores[i],fores[j])
            if cw==0:
                return fores[0]
            resonances.append(1/cw)
        resonances=pd.Series(resonances)
        for m in range(droplow):
            dinx=resonances.idxmin()
            del resonances[dinx]
            del fores[dinx]
        return (fores*resonances).sum(1)/(resonances.sum())

    def pv(self,dimension,r,droplow=0):
        pvs=[]
        mnum = len(self._modelsets)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        sr=pow(1+r,1/self._AP)-1
        for i in range(mnum):
            if self._modelsets[i]._mparams['seasonal']:
                pvs.append(self._modelsets[i].pv(dimension,r)*pow(1+r,self._periodgaps[i]/self._AP))
            else:
                pvs.append(self._modelsets[i].pv(dimension,sr) * pow(1+r, self._periodgaps[i] / self._AP))
        if len(pvs)==0:
            return None
        elif len(pvs)==1:
            return pvs[0]
        pvs=pd.Series(pvs)
        resonances=[]
        for i in range(mnum):
            cw=0
            for j in range(mnum):
                if i==j:
                    continue
                cw+=self._connection.elementmethod(pvs[i],pvs[j])
            if cw==0:
                return pvs[0]
            resonances.append(1/cw)
        resonances=pd.Series(resonances)
        for m in range(droplow):
            dinx=resonances.idxmin()
            del resonances[dinx]
            del pvs[dinx]
        return (pvs*resonances).sum()/(resonances.sum())

    def irr(self,dimension,price,tradedate,droplow=0):
        rates=[]
        mnum = len(self._modelsets)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        for i in range(mnum):
            irr=self._modelsets[i].irr(dimension,price,tradedate)
            if type(irr)==float:
                if self._modelsets[i]._mparams['seasonal']:
                    rates.append(1+irr)
                else:
                    rates.append(pow(1 + irr,self._AP))
        if len(rates)==0:
            return None
        elif len(rates)==1:
            return rates[0]-1
        rates=np.log(pd.Series(rates))
        resonances=[]
        for i in range(len(rates)):
            cw=0
            for j in range(len(rates)):
                if i==j:
                    continue
                cw+=self._connection.elementmethod(rates[i],rates[j])
            if cw==0:
                return np.exp(rates[0])-1
            resonances.append(1/cw)
        resonances=pd.Series(resonances)
        for m in range(droplow-(mnum-len(rates))):
            dinx=resonances.idxmin()
            del resonances[dinx]
            del rates[dinx]
        if len(rates)>0:
            return np.exp((rates * resonances).sum() / (resonances.sum()))-1
        else:
            return None

    def batchirr(self,dimension,priceseries,droplow=0):
        batchrates=[]
        mnum = len(self._modelsets)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        for i in range(mnum):
            if self._modelsets[i]._mparams['seasonal']:
                batchrates.append(1+self._modelsets[i].batchirr(dimension,priceseries)['IRRs'])
            else:
                batchrates.append(pow(1+self._modelsets[i].batchirr(dimension,priceseries)['IRRs'],self._AP))
        batchrates=np.log(pd.DataFrame(batchrates).transpose())
        irrs=pd.Series(index=batchrates.index)
        for index,row in batchrates.iterrows():
            rates=row.copy(deep=True).dropna()
            if len(rates) == 0:
                irrs[index] = np.nan
                continue
            elif len(rates) == 1:
                irrs[index] = np.exp(rates.values[0]) - 1
                continue
            rates=rates.reset_index(drop=True)
            resonances = []
            homo = False
            for i in range(len(rates)):
                cw = 0
                for j in range(len(rates)):
                    if i == j:
                        continue
                    cw += self._connection.elementmethod(rates[i], rates[j])
                if cw == 0:
                    homo = True
                    break
                resonances.append(1 / cw)
            if homo:
                resonances = pd.Series(np.ones(len(rates)))
            else:
                resonances = pd.Series(resonances)
            for m in range(droplow-(mnum-len(rates))):
                dinx = resonances.idxmin()
                del resonances[dinx]
                del rates[dinx]
            if len(rates)>0:
                irrs[index] = np.exp((rates * resonances).sum() / (resonances.sum()))-1
            else:
                irrs[index] = np.nan
        return irrs

    def achieverate(self,dimension,price,r,tradedate,droplow=0):
        acrs = []
        mnum = len(self._modelsets)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        sr = pow(1 + r, 1 / self._AP) - 1
        for i in range(mnum):
            if self._modelsets[i]._mparams['seasonal']:
                acrs.append(self._modelsets[i].achieverate(dimension,price,r,tradedate))
            else:
                acrs.append(self._modelsets[i].achieverate(dimension,price,sr,tradedate))
        if len(acrs) == 0:
            return None
        elif len(acrs) == 1:
            return acrs[0]
        acrs = pd.Series(acrs)
        resonances = []
        for i in range(mnum):
            cw = 0
            for j in range(mnum):
                if i == j:
                    continue
                cw += self._connection.elementmethod(acrs[i], acrs[j])
            if cw == 0:
                return acrs[0]
            resonances.append(1 / cw)
        resonances = pd.Series(resonances)
        for m in range(droplow):
            dinx=resonances.idxmin()
            del resonances[dinx]
            del acrs[dinx]
        return (acrs*resonances).sum()/(resonances.sum())

    def batchachieverate(self,dimension,priceseries,r,droplow=0):
        batchacrs=[]
        mnum = len(self._modelsets)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        sr = pow(1 + r, 1 / self._AP) - 1
        for i in range(mnum):
            if self._modelsets[i]._mparams['seasonal']:
                batchacrs.append(self._modelsets[i].batchachieverate(dimension,priceseries,r))
            else:
                batchacrs.append(self._modelsets[i].batchachieverate(dimension,priceseries,sr))
        batchacrs=pd.DataFrame(batchacrs).transpose()
        acrs=pd.Series(index=batchacrs.index)
        for index,row in batchacrs.iterrows():
            rates=row.copy(deep=True)
            if len(rates) == 0:
                acrs[index]=np.nan
                continue
            elif len(rates) == 1:
                acrs[index]=rates.values[0]
                continue
            resonances = []
            homo = False
            for i in range(mnum):
                cw = 0
                for j in range(mnum):
                    if i == j:
                        continue
                    cw += self._connection.elementmethod(rates[i], rates[j])
                if cw == 0:
                    homo = True
                    break
                resonances.append(1 / cw)
            if homo:
                resonances = pd.Series(np.ones(len(rates)))
            else:
                resonances = pd.Series(resonances)
            for m in range(droplow):
                dinx = resonances.idxmin()
                del resonances[dinx]
                del rates[dinx]
            acrs[index] = (rates*resonances).sum()/(resonances.sum())
        return acrs

class CompanyResonanceModelSet(CommonResonanceModelSet):
    def __init__(self,modelsets,connection):
        self._modelsets=modelsets
        self._connection=connection
        self.__getfreqparams()

    def __getfreqparams(self):
        if isinstance(self._modelsets[0], company_modelset):
            if (self._modelsets[0]._mparams['ttm']):
                self._freq = AFREQS[self._modelsets[0]._mparams['reportdate'][-4:]]
                self._AP = 1
            else:
                self._freq = 'Q-DEC'
                self._AP = 4
        else:
            raise Exception("模型类型错误")
        reportlist = []
        for modelset in self._modelsets:
            if isinstance(modelset, company_modelset):
                if (modelset._mparams['ttm']):
                    if (AFREQS[modelset._mparams['reportdate'][-4:]] == self._freq):
                        reportlist.append(pd.to_datetime(modelset._mparams['reportdate']))
                    else:
                        raise Exception("模型类型错误")
                else:
                    reportlist.append(pd.to_datetime(modelset._mparams['reportdate']))
            else:
                raise Exception("模型类型错误")
        reportmax = np.array(reportlist).max()
        periodgaps = []
        for report in reportlist:
            periodgaps.append(len(pd.date_range(start=report, end=reportmax, freq=self._freq)) - 1)
        self._periodgaps = periodgaps

    def irr_trade(self,dimension,pricemode,tradedate,droplow=0):
        rates=[]
        mnum = len(self._modelsets)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        for i in range(mnum):
            irr=self._modelsets[i].irr_trade(dimension,pricemode,tradedate)
            if type(irr)==float:
                if self._modelsets[i]._mparams['seasonal']:
                    rates.append(1+irr)
                else:
                    rates.append(pow(1 + irr,self._AP))
        if len(rates)==0:
            return None
        elif len(rates)==1:
            return rates[0]-1
        rates=np.log(pd.Series(rates))
        resonances=[]
        for i in range(len(rates)):
            cw=0
            for j in range(len(rates)):
                if i==j:
                    continue
                cw+=self._connection.elementmethod(rates[i],rates[j])
            if cw==0:
                return np.exp(rates[0])-1
            resonances.append(1/cw)
        resonances=pd.Series(resonances)
        for m in range(droplow-(mnum-len(rates))):
            dinx=resonances.idxmin()
            del resonances[dinx]
            del rates[dinx]
        if len(rates)>0:
            return np.exp((rates * resonances).sum() / (resonances.sum()))-1
        else:
            return None

    def batchirr_trade(self,dimension,pricemode,startdate,enddate,droplow=0):
        batchrates=[]
        mnum = len(self._modelsets)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        for i in range(mnum):
            if self._modelsets[i]._mparams['seasonal']:
                batchrates.append(1+self._modelsets[i].batchirr_trade(dimension,pricemode,startdate,enddate)['IRRs'])
            else:
                batchrates.append(pow(1+self._modelsets[i].batchirr_trade(dimension,pricemode,startdate,enddate)['IRRs'],self._AP))
        batchrates=np.log(pd.DataFrame(batchrates).transpose())
        irrs=pd.Series(index=batchrates.index)
        for index,row in batchrates.iterrows():
            rates=row.copy(deep=True).dropna()
            if len(rates) == 0:
                irrs[index] = np.nan
                continue
            elif len(rates) == 1:
                irrs[index] = np.exp(rates.values[0]) - 1
                continue
            rates=rates.reset_index(drop=True)
            resonances = []
            homo = False
            for i in range(len(rates)):
                cw = 0
                for j in range(len(rates)):
                    if i == j:
                        continue
                    cw += self._connection.elementmethod(rates[i], rates[j])
                if cw == 0:
                    homo = True
                    break
                resonances.append(1 / cw)
            if homo:
                resonances = pd.Series(np.ones(len(rates)))
            else:
                resonances = pd.Series(resonances)
            for m in range(droplow-(mnum-len(rates))):
                dinx = resonances.idxmin()
                del resonances[dinx]
                del rates[dinx]
            if len(rates)>0:
                irrs[index] = np.exp((rates * resonances).sum() / (resonances.sum()))-1
            else:
                irrs[index] = np.nan
        return irrs

    def achieverate_trade(self,dimension, pricemode, tradedate, r,droplow=0):
        acrs = []
        mnum = len(self._modelsets)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        sr = pow(1 + r, 1 / self._AP) - 1
        for i in range(mnum):
            if self._modelsets[i]._mparams['seasonal']:
                acrs.append(self._modelsets[i].achieverate_trade(dimension,pricemode, tradedate, r))
            else:
                acrs.append(self._modelsets[i].achieverate_trade(dimension,pricemode, tradedate, sr))
        if len(acrs) == 0:
            return None
        elif len(acrs) == 1:
            return acrs[0]
        acrs = pd.Series(acrs)
        resonances = []
        for i in range(mnum):
            cw = 0
            for j in range(mnum):
                if i == j:
                    continue
                cw += self._connection.elementmethod(acrs[i], acrs[j])
            if cw == 0:
                return acrs[0]
            resonances.append(1 / cw)
        resonances = pd.Series(resonances)
        for m in range(droplow):
            dinx=resonances.idxmin()
            del resonances[dinx]
            del acrs[dinx]
        return (acrs*resonances).sum()/(resonances.sum())

    def batchachieverate_trade(self,dimension, pricemode, startdate, enddate, r,droplow=0):
        batchacrs=[]
        mnum = len(self._modelsets)
        if droplow>=mnum:
            raise Exception("异常剔除数量应小于分析模型数量")
        sr = pow(1 + r, 1 / self._AP) - 1
        for i in range(mnum):
            if self._modelsets[i]._mparams['seasonal']:
                batchacrs.append(self._modelsets[i].batchachieverate_trade(dimension,pricemode, startdate, enddate, r))
            else:
                batchacrs.append(self._modelsets[i].batchachieverate_trade(dimension,pricemode, startdate, enddate,sr))
        batchacrs=pd.DataFrame(batchacrs).transpose()
        acrs=pd.Series(index=batchacrs.index)
        for index,row in batchacrs.iterrows():
            rates=row.copy(deep=True)
            if len(rates) == 0:
                acrs[index]=np.nan
                continue
            elif len(rates) == 1:
                acrs[index]=rates.values[0]
                continue
            resonances = []
            homo = False
            for i in range(mnum):
                cw = 0
                for j in range(mnum):
                    if i == j:
                        continue
                    cw += self._connection.elementmethod(rates[i], rates[j])
                if cw == 0:
                    homo = True
                    break
                resonances.append(1 / cw)
            if homo:
                resonances = pd.Series(np.ones(len(rates)))
            else:
                resonances = pd.Series(resonances)
            for m in range(droplow):
                dinx = resonances.idxmin()
                del resonances[dinx]
                del rates[dinx]
            acrs[index] = (rates*resonances).sum()/(resonances.sum())
        return acrs


