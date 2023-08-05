# 著作者：叶凯文
# Author: YE KAIWEN
# 版权归著作者叶凯文所有
# Copyright (c) 2022 YE KAIWEN. All Rights Reserved.

__author__ = 'YE KAIWEN'
__version__ = '1.1.5'

from valuequant.VQconnect import VQC
import valuequant.Models as Models
import valuequant.ModelSets as ModelSets
import valuequant.StockModels as StockModels
import valuequant.StockModelSets as StockModelSets
import valuequant.StockFrameSets as StockFrameSets
import valuequant.StockNet as StockNet
import valuequant.ResonanceModel as ResonanceModel
import valuequant.StockFrameSetsUS as StockFrameSetsUS
import valuequant.StockStrategyLocal as StockStrategyLocal

def login(name,pswd):
    VQC.login(name,pswd)

def logout():
    VQC.logout()


