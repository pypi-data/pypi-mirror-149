# -*- coding: utf-8 -*-
from collections import namedtuple

from .leaf import Factor
from .rolling import *
from .func import *
from .rolling import AVEDEV


__all__ = [
    'KDJ', 'DMI', 'MACD', 'RSI',
    'BOLL', 'WR', 'BIAS', 'ASI',
    'VR', 'ARBR', 'DPO', 'TRIX',
    'BBIBOLL', 'MCST', 'OBOS',
    'LWR', 'ACCER', 'CYF', 'FSL',
    'ADTM', 'ATR', 'DKX', 'TAPI',
    'OSC',  'CCI',  'ROC', 'MFI',
    'MARSI', 'MTM', 'SKD', 'UDL',
    'CR', 'MASS', 'PSY', 'PCNT',
    'CYR',
]


CLOSE = Factor('close')
OPEN = Factor('open')
HIGH = Factor('high')
LOW = Factor('low')
VOL = Factor('volume')
TURNOVER = Factor('total_turnover')
CAPITAL = Factor('capital')


KDJResult = namedtuple('KDJResult', ['K', 'D', 'J'])


def KDJ(N=9, M1=3, M2=3):
    """随机波动指标"""
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA_CN(RSV, (M1 * 2 - 1))
    D = EMA_CN(K, (M2 * 2 - 1))
    J = K * 3 - D * 2
    return KDJResult(K, D, J)


DMIResult = namedtuple('DMIResult', ['DI1', 'DI2', 'ADX', 'ADXR'])


def DMI(M1=14, M2=6):
    """
    DMI 趋向指标
    """
    TR = SUM(MAX(MAX(HIGH - LOW, ABS(HIGH - REF(CLOSE, 1))), ABS(LOW - REF(CLOSE, 1))), M1)
    HD = HIGH - REF(HIGH, 1)
    LD = REF(LOW, 1) - LOW

    DMP = SUM(IF((HD > 0) & (HD > LD), HD, 0), M1)
    DMM = SUM(IF((LD > 0) & (LD > HD), LD, 0), M1)
    DI1 = DMP * 100 / TR
    DI2 = DMM * 100 / TR
    ADX = MA(ABS(DI2 - DI1) / (DI1 + DI2) * 100, M2)
    ADXR = (ADX + REF(ADX, M2)) / 2

    return DMIResult(DI1, DI2, ADX, ADXR)


MACDResult = namedtuple('MACDResult', ['DIFF', 'DEA', 'HIST'])


def MACD(SHORT=12, LONG=26, M=9):
    """
    MACD 指数平滑移动平均线
    """
    DIFF = EMA_CN(CLOSE, SHORT) - EMA_CN(CLOSE, LONG)
    DEA = EMA_CN(DIFF, M)
    HIST = (DIFF - DEA) * 2
    return MACDResult(DIFF, DEA, HIST)


def RSI(N=6):
    """
    RSI 相对强弱指标
    """
    LC = REF(CLOSE, 1)
    RSI = MA(MAX(CLOSE - LC, 0), N) / MA(ABS(CLOSE - LC), N) * 100
    return RSI


BOLLResult = namedtuple('BOLLResult', ['UPPER', 'MID', 'LOWER'])


def BOLL(N=20, P=2):
    """
    BOLL 布林带
    """
    MID = MA(CLOSE, N)
    UPPER = MID + STD(CLOSE, N) * P
    LOWER = MID - STD(CLOSE, N) * P

    return BOLLResult(UPPER, MID, LOWER)


def WR(N=10):
    """
    W&R 威廉指标
    """
    WR = (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    return WR


BIASResult = namedtuple('BIASResult', ['BIAS1', 'BIAS2', 'BIAS3'])


def BIAS(L1=5, L4=3, L5=10):
    """
    BIAS 乖离率
    """
    BIAS1 = (CLOSE - MA(CLOSE, L1)) / MA(CLOSE, L1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, L4)) / MA(CLOSE, L4) * 100
    BIAS3 = (CLOSE - MA(CLOSE, L5)) / MA(CLOSE, L5) * 100

    return BIASResult(BIAS1, BIAS2, BIAS3)


ASIResult = namedtuple('ASIResult', ['ASI', 'ASIT'])


def ASI(M1=26, M2=10):
    """
    ASI 震动升降指标
    """
    LC = REF(CLOSE, 1)
    AA = ABS(HIGH - LC)
    BB = ABS(LOW - LC)
    CC = ABS(HIGH - REF(LOW, 1))
    DD = ABS(LC - REF(OPEN, 1))
    R = IF((AA > BB) & (AA > CC), AA + BB / 2 + DD / 4, IF((BB > CC) & (BB > AA), BB + AA / 2 + DD / 4, CC + DD / 4))
    X = (CLOSE - LC + (CLOSE - OPEN) / 2 + LC - REF(OPEN, 1))
    SI = X * 16 / R * MAX(AA, BB)
    ASI = SUM(SI, M1)
    ASIT = MA(ASI, M2)

    return ASIResult(ASI, ASIT)


VRResult = namedtuple('VRResult', ['VR', 'MAVR'])


def VR(M1=26, M=6):
    """
    VR容量比率
    """
    LC = REF(CLOSE, 1)
    VR = SUM(IF(CLOSE > LC, VOL, 0), M1) / SUM(IF(CLOSE <= LC, VOL, 0), M1) * 100
    MAVR = MA(VR, M)
    return VRResult(VR, MAVR)


ARBRResult = namedtuple('ARBRResult', ['AR', 'BR'])


def ARBR(M1=26):
    """
    ARBR人气意愿指标
    """
    AR = SUM(HIGH - OPEN, M1) / SUM(OPEN - LOW, M1) * 100
    BR = SUM(MAX(0, HIGH - REF(CLOSE, 1)), M1) / SUM(MAX(0, REF(CLOSE, 1) - LOW), M1) * 100

    return ARBRResult(AR, BR)


DPOResult = namedtuple('DPOResult', ['DPO', 'MADPO'])


def DPO(M1=20, M2=10, M3=6):
    """区间震荡线"""
    DPO = CLOSE - REF(MA(CLOSE, M1), M2)
    MADPO = MA(DPO, M3)

    return DPOResult(DPO, MADPO)


TRIXResult = namedtuple('TRIXResult', ['TRIX', 'MATRIX'])


def TRIX(M1=12, M2=20):
    """三重指数平均移动平均"""
    TR = EMA_CN(EMA_CN(EMA_CN(CLOSE, M1), M1), M1)
    TRIX = (TR - REF(TR, 1)) / REF(TR, 1) * 100
    MATRIX = MA(TRIX, M2)

    return TRIXResult(TRIX, MATRIX)


BBIBOLLResult = namedtuple('BBIBOLLResult', ['BBIBOLL', 'BBIBOLL_UP', 'BBIBOLL_DOWN'])


def BBIBOLL(M1=3, M2=6, M3=12, M4=24, M=6, N=11):
    """多空指标"""
    BBIBOLL = (MA(CLOSE, M1) + MA(CLOSE, M2) + MA(CLOSE, M3) + MA(CLOSE, M4)) / 4
    BBIBOLL_UP = BBIBOLL + M * STD(BBIBOLL, N)
    BBIBOLL_DOWN = BBIBOLL - M * STD(BBIBOLL, N)
    return BBIBOLLResult(BBIBOLL, BBIBOLL_UP, BBIBOLL_DOWN)


def MCST():
    """市场成本"""
    return DMA(TURNOVER / VOL, 100 * VOL / CAPITAL)


def OBOS(N=10):
    """超买超卖指标"""
    r = IF(CLOSE > REF(CLOSE, 1), 1, -1)
    return SUM(r, N)


LWRResult = namedtuple('LWRResult', ['LWR1', 'LWR2'])


def LWR(N=9, M1=3, M2=3):
    """LWR威廉指标"""
    RSV = (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    LWR1 = SMA_CN(RSV, M1, 1)
    LWR2 = SMA_CN(LWR1, M2, 1)
    return LWRResult(LWR1, LWR2)


def ACCER(N=8):
    """幅度涨速"""
    return SLOPE(CLOSE, N) / CLOSE


def CYF(N=21):
    """市场能量 CYF"""
    return 100 - 100 / (1 + EMA_CN(VOL / CAPITAL, N))


FSLResult = namedtuple('FSLResult', ['SWL', 'SWS'])


def FSL():
    """分水岭"""
    SWL = (EMA_CN(CLOSE, 5) * 7 + EMA_CN(CLOSE, 10) * 3) / 10
    SWS = DMA(EMA_CN(CLOSE, 12), MAX(1, 100 * (SUM(VOL, 5) / (3 * CAPITAL))))
    return FSLResult(SWL, SWS)


ADTMResult = namedtuple('ADTMResult', ['ADTM', 'MAADTM'])


def ADTM(N=23, M=8):
    """动态买卖气指标 ADTM"""
    DTM = IF(OPEN <= REF(OPEN, 1), 0, MAX((HIGH - OPEN), (OPEN - REF(OPEN, 1))))
    DBM = IF(OPEN >= REF(OPEN, 1), 0, MAX((OPEN - LOW), (OPEN - REF(OPEN, 1))))
    STM = SUM(DTM, N)
    SBM = SUM(DBM, N)
    ADTM = IF(STM > SBM, (STM - SBM) / STM, IF(STM==SBM, 0, (STM - SBM) / SBM))
    MAADTM = MA(ADTM, M)
    return ADTMResult(ADTM, MAADTM)


ATRResult = namedtuple('ATRResult', ['TR', 'ATR'])


def ATR(N=23, M=9):
    """真实波幅 ATR"""
    TR = SUM(MAX(MAX(HIGH - LOW, ABS(HIGH - REF(CLOSE, 1))), ABS(LOW - REF(CLOSE, 1))), M)
    ATR = MA(TR, N)
    return ATRResult(TR, ATR)


DKXResult = namedtuple('DKXResult', ['DKX', 'MADKX'])


def DKX(M=10):
    """多空线"""
    MID = (3 * CLOSE + LOW + OPEN + HIGH) / 6
    DKX = (20 * MID + 19 * REF(MID, 1) + 18 * REF(MID, 2) + 17 * REF(MID, 3) + 16 * REF(MID, 4) + 15 * REF(MID, 5) +
           14 * REF(MID, 6) + 13 * REF(MID, 7) + 12 * REF(MID, 8) + 11 * REF(MID, 9) + 10 * REF(MID, 10) +
           9 * REF(MID, 11) + 8 * REF(MID, 12) + 7 * REF(MID, 13) + 6 * REF(MID, 14) + 5 * REF(MID, 15) +
           4 * REF(MID, 16) + 3 * REF(MID, 17) + 2 * REF( MID, 18) + REF(MID, 20)) / 210
    MADKX = MA(DKX, M)
    return DKXResult(DKX, MADKX)


TAPIResult = namedtuple('TAPIResult', ['TAPI', 'MATAPI'])


def TAPI(M=6):
    """加权指数成交值"""
    TAPI = TURNOVER / CLOSE
    MATAPI = MA(TAPI, M)
    return TAPIResult(TAPI, MATAPI)


def OSC(N=10):
    """变动速率线"""
    OSC = 100 * (CLOSE - MA(CLOSE, N))
    return OSC


def CCI(N=14):
    """商品路径指标"""
    TYP = (HIGH + LOW + CLOSE) / 3
    CCI = (TYP - MA(TYP, N)) / (0.015 * AVEDEV(TYP, N))
    return CCI


def ROC(N=12):
    """变形率指标"""
    ROC = 100 * (CLOSE - REF(CLOSE, N)) / REF(CLOSE, N)
    return ROC


def MFI(N=14):
    """资金流量指标"""
    TYP = (HIGH + LOW + CLOSE) / 3
    V1 = SUM(IF(TYP > REF(TYP, 1), TYP * VOL, 0), N) / SUM(IF(TYP < REF(TYP, 1), TYP * VOL, 0), N)
    MFI = 100 - (100 / (1 + V1))
    return MFI


MTMResult = namedtuple('MTAResult', ['MTM', 'MAMTM'])


def MTM(N=14, M=6):
    """动量线"""
    MTM = CLOSE - REF(CLOSE, N)
    MAMTM = MA(MTM, M)
    return MTMResult(MTM, MAMTM)


def MARSI(N=6):
    """相对强弱平均线"""
    LC = REF(CLOSE, 1)
    RSI = SMA_CN(MAX(CLOSE - LC, 0), N, 1) / SMA_CN(ABS(CLOSE - LC), N, 1) * 100
    MARSI = MA(RSI, N)
    return MARSI


SKDResult = namedtuple('SKDResult', ['SDK_K', 'SKD_D'])


def SKD(N=9, M=3):
    """慢速随机指标"""
    LOWV = LLV(LOW, N)
    HIGHV = HHV(HIGH, N)
    RSV = EMA_CN((CLOSE - LOWV) / (HIGHV - LOWV) * 100, M)
    SKD_K = EMA_CN(RSV, M)
    SKD_D = MA(SKD_K, M)
    return SKDResult(SKD_K, SKD_D)


UDLResult = namedtuple('UDLResult', ['UDL', 'MAUDL'])


def UDL(N1=3, N2=5, N3=10, N4=20, M=6):
    """引力线"""
    UDL = (MA(CLOSE, N1) + MA(CLOSE, N2) + MA(CLOSE, N3) + MA(CLOSE, N4)) / 4
    MAUDL = MA(UDL, M)
    return UDLResult(UDL, MAUDL)


CRResult = namedtuple('CRResult', ['CR', 'MACR1', 'MACR2', 'MACR3', 'MACR4'])


def CR(N=26, M1=10, M2=20, M3=40, M4=62):
    """CR指标"""
    MID = REF(HIGH + LOW, 1) / 2
    CR = SUM(MAX(0, HIGH - MID), N) / SUM(MAX(0, MID - LOW), N) * 100
    MACR1 = REF(MA(CR, M1), 1 + int(M1 / 2.5))
    MACR2 = REF(MA(CR, M2), 1 + int(M2 / 2.5))
    MACR3 = REF(MA(CR, M3), 1 + int(M3 / 2.5))
    MACR4 = REF(MA(CR, M4), 1 + int(M4 / 2.5))
    return CRResult(CR, MACR1, MACR2, MACR3, MACR4)


MASSResult = namedtuple('MASSResult', ['MASS', 'MAMASS'])


def MASS(N1=9, N2=25, M=6):
    """梅斯线"""
    MASS = SUM(MA(HIGH - LOW, N1) / MA(MA(HIGH - LOW, N1), N1), N2)
    MAMASS = MA(MASS, M)
    return MASSResult(MASS, MAMASS)


PSYResult = namedtuple('PSYResult', ['PSY', 'MAPSY'])


def PSY(M=12, N=9):
    """心理线"""
    PSY = COUNT(CLOSE > REF(CLOSE, 1), N) / N * 100
    MAPSY = MA(PSY, M)
    return PSYResult(PSY, MAPSY)


def PCNT():
    """幅度比"""
    PCNT = (CLOSE - REF(CLOSE, 1)) / CLOSE * 100
    return PCNT


CYRResult = namedtuple('CYRResult', ['CYR', 'MACYR'])


def CYR(N=13, M=5):
    """市场强弱"""
    DIVE = 0.01 * EMA_CN(TURNOVER, N) / EMA_CN(VOL, N)
    CYR = (DIVE / REF(DIVE, 1) - 1) * 100
    MACYR = MA(CYR, M)
    return CYRResult(CYR, MACYR)
