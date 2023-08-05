# 著作者：叶凯文
# Author: YE KAIWEN
# 版权归著作者叶凯文所有
# Copyright (c) 2022 YE KAIWEN. All Rights Reserved.

from .VQconnect import VQC
from .commonform import modelcate
from .companyform import formatbatchirrparams,formatunitirrparams,formatbatchachieverateparams,formatunitachieverateparams

def formatframesetparams(mfunc,mparams):
    stockcode=mparams.pop('stockcode')
    reportdate=mparams.pop('reportdate')
    adjdate=mparams.pop('adjdate')
    mfunc=mfunc[:-8]+'model'
    return {'stockcode':stockcode,'reportdate':reportdate,'adjdate':adjdate,'mcate':modelcate[mfunc],'mfunc':mfunc,'mparams':mparams}

def getcompanymodel(mfunc,mparams):
    fparams=formatframesetparams(mfunc,mparams)
    if type(fparams)==dict:
        try:
            params = {'datatype': 'CompanyUS', 'modeltype': 'FrameSet', 'restype': 'Model', 'params':fparams}
            return VQC.service(params)
        except:
            print("网络请求出错")
            return None
    else:
        return None

def formatmodelsetxparams(modelset,mparams,vparams,mfunc):
    if type(modelset)!=dict:
        return None
    stockcode=mparams.pop('stockcode')
    reportdate=mparams.pop('reportdate')
    adjdate = mparams.pop('adjdate')
    dimension=vparams.pop('dimension')
    return {'modelset':modelset,'stockcode':stockcode,'reportdate':reportdate,'dimension':dimension,'adjdate':adjdate,'mcate':modelcate[(mfunc[:-8]+'model')]}

def getcompanyservice(restype,model,mfunc,mparams,vparams):
    fparams = formatmodelsetxparams(modelset=model, mparams=mparams, vparams=vparams, mfunc=mfunc)
    fparams=globals()['format'+restype.lower()+'params'](fparams=fparams,vparams=vparams)
    if type(fparams)==dict:
        try:
            params = {'datatype': 'CompanyUS', 'modeltype': 'ModelSet', 'restype': restype, 'params':fparams}
            return VQC.service(params)
        except:
            print("网络请求出错")
            return None
    else:
        return None

