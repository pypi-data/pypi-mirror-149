# 著作者：叶凯文
# Author: YE KAIWEN
# 版权归著作者叶凯文所有
# Copyright (c) 2022 YE KAIWEN. All Rights Reserved.

import pandas as pd

from .VQconnect import VQC

class StockNet:
    def __init__(self,freq,periodend,analysiscate,dimension):
        self._netparams={'freq':freq,'periodend':periodend,'analysiscate':analysiscate,'dimension':dimension}
        self.__getNetworkInfo()

    def __getNetworkInfo(self):
        params={'querytype':'NetworkInfo','params':self._netparams}
        try:
            res=VQC.stocknet(params)
            if type(res)==list:
                self._NetID=res[0]
                self._NetworkInfo={'vertexnum':res[1],'edgenum':res[2],'simulimited':res[3]}
        except:
            print("网络请求出错")
            pass

    def NetworkInfo(self):
        if hasattr(self,'_NetworkInfo'):
            return self._NetworkInfo

    def __getNetworkGraphs(self,radius):
        params={'querytype':'NetworkGraphs','params':{'nid':self._NetID,'radius':radius}}
        try:
            res=VQC.stocknet(params)
            if type(res)==list:
                Graphs=pd.DataFrame(res,columns=['sid','vertexnum','edgenum']).set_index('sid',drop=True)
                if hasattr(self,'_Graphs'):
                    self._Graphs[radius]=Graphs
                else:
                    self._Graphs={radius:Graphs}
        except:
            print("网络请求出错")
            pass

    def NetworkGraphs(self,radius):
        if hasattr(self,'_Graphs'):
            if radius in self._Graphs.keys():
                return self._Graphs[radius]
        self.__getNetworkGraphs(radius)
        if hasattr(self,'_Graphs'):
            if radius in self._Graphs.keys():
                return self._Graphs[radius]

    def __getGraphVertexes(self,radius,sid):
        params={'querytype':'GraphVertexes','params':{'nid':self._NetID,'radius':radius,'sid':sid}}
        try:
            res = VQC.stocknet(params)
            if type(res) == list:
                Vertexes=res
                if hasattr(self,'_Vertexes'):
                    self._Vertexes['%s_%s'%(radius,sid)]=Vertexes
                else:
                    self._Vertexes={'%s_%s'%(radius,sid):Vertexes}
        except:
            print("网络请求出错")
            pass

    def GraphVertexes(self,radius,sid):
        if hasattr(self,'_Vertexes'):
            if '%s_%s'%(radius,sid) in self._Vertexes.keys():
                return self._Vertexes['%s_%s'%(radius,sid)]
        self.__getGraphVertexes(radius,sid)
        if hasattr(self,'_Vertexes'):
            if '%s_%s'%(radius,sid) in self._Vertexes.keys():
                return self._Vertexes['%s_%s'%(radius,sid)]

    def VertexNeighbors(self,vertex,edgemode='out'):
        params={'querytype':'VertexNeighbors','params':{'nid':self._NetID,'vertex':vertex,'edgemode':edgemode}}
        try:
            res=VQC.stocknet(params)
            if type(res) == list:
                if edgemode=='out':
                    return pd.DataFrame(res,columns=['endvertex','simularity'])
                elif edgemode=='in':
                    return pd.DataFrame(res,columns=['startvertex','simularity'])
                else:
                    print("edgemode应选择'in'或'out'其中一项")
        except:
            print("网络请求出错")
            pass

    def EdgeFrequency(self,startvertex,endvertex,simulimited):
        params={'querytype':'EdgeFrequency','params':{'startvertex':startvertex,'endvertex':endvertex,'simulimited':simulimited,'freq':self._netparams['freq'],'analysiscate':self._netparams['analysiscate'],'dimension':self._netparams['dimension']}}
        try:
            res=VQC.stocknet(params)
            if type(res)==list:
                return res
        except:
            pass
        print("网络请求出错")

class ParticleCompetitionTraining:
    def __init__(self,network,sid):
        self._trainparams={'nid':network._NetID,'sid':sid}
        self.__getTrainingInfo()

    def __getTrainingInfo(self):
        params={'querytype':'ParticleCompetitionTrainingInfo','params':{'nid':self._trainparams['nid'],'sid':self._trainparams['sid']}}
        try:
            res = VQC.stocknet(params)
            if type(res)==list:
                self._TrainingInfo=pd.DataFrame(res,columns=['tid','psize','avemaxctl']).set_index('tid',drop=True)
                self._TrainingInfo.index=self._TrainingInfo.index.astype(int)
                self._TrainingInfo['psize']=self._TrainingInfo['psize'].astype(int)
        except:
            print("网络请求出错")
            pass

    def TrainingInfo(self):
        if hasattr(self,'_TrainingInfo'):
            return self._TrainingInfo
        self.__getTrainingInfo()
        if hasattr(self,'_TrainingInfo'):
            return self._TrainingInfo

    def __getTrainingParticles(self,tid):
        params={'querytype':'TrainingParticles','params':{'tid':tid}}
        try:
            res=VQC.stocknet(params)
            if type(res)==list:
                Particles=pd.DataFrame(res,columns=['pid','monopolize','overlap','competeL1','competeL2']).set_index('pid',drop=True)
                if hasattr(self,'_Particles'):
                    self._Particles[tid]=Particles
                else:
                    self._Particles={tid:Particles}
        except:
            print("网络请求出错")
            pass

    def Particles(self,tid):
        if hasattr(self, '_Particles'):
            if tid in self._Particles.keys():
                return self._Particles[tid]
        self.__getTrainingParticles(tid)
        if hasattr(self, '_Particles'):
            if tid in self._Particles.keys():
                return self._Particles[tid]

    def __getTrainingVertexes(self,tid):
        params={'querytype':'TrainingVertexes','params':{'tid':tid}}
        try:
            res=VQC.stocknet(params)
            if type(res)==list:
                Vertexes=pd.DataFrame(res,columns=['vertex','uv','pv','top1','top1freq','top2','top2freq','top3','top3freq','top4','top4freq','top5','top5freq','overlap','maxctlnum'])
                if hasattr(self,'_Vertexes'):
                    self._Vertexes[tid]=Vertexes
                else:
                    self._Vertexes={tid:Vertexes}
        except:
            print("网络请求出错")
            pass

    def Vertexes(self,tid):
        if hasattr(self,'_Vertexes'):
            if tid in self._Vertexes.keys():
                return self._Vertexes[tid]
        self.__getTrainingVertexes(tid)
        if hasattr(self,'_Vertexes'):
            if tid in self._Vertexes.keys():
                return self._Vertexes[tid]
