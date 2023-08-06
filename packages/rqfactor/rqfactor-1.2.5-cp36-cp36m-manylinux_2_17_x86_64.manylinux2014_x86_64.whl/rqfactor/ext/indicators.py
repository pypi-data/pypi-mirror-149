# -*- coding:utf-8 -*-
from rqfactor import Pricing, Factor
from rqfactor.indicators import *
from rqfactor.rolling import *

__all__ = ['INDICATORS']

CLOSE = Pricing.close
HIGH = Pricing.high
LOW = Pricing.low
OPEN = Pricing.open
VOLUME = Pricing.volume
AMOUNT = Pricing.total_turnover
VV = (HIGH + LOW + OPEN + CLOSE) / 4
AMOV = VOLUME * (OPEN + CLOSE) / 2
HSL = Factor('volume_unadjusted') / Factor('capital')


def indicators():
    # 均线指标
    macd_diff, macd_dea, macd_hist = MACD()
    trix, matrix = TRIX()
    boll_up, boll, boll_down = BOLL()
    bbi, bbiboll_up, bbiboll_down = BBIBOLL()
    asi, asit = ASI()

    dpo, madpo = DPO()
    mcst = MCST()

    # 超买超卖指标
    obos = OBOS()
    KDJ_K, KDJ_D, KDJ_J = KDJ()
    RSI6, RSI10 = RSI(6), RSI(10)
    wr = WR(10)
    lwr1, lwr2 = LWR()
    BIAS5, BIAS10, BIAS20 = BIAS()
    BIAS36 = MA(CLOSE, 3) - MA(CLOSE, 6)
    BIAS612 = MA(CLOSE, 6) - MA(CLOSE, 12)
    MABIAS = MA(BIAS36, 6)
    accer = ACCER()
    cyf = CYF()
    SWL, SWS = FSL()
    adtm, maadtm = ADTM()
    tr, atr = ATR()
    dkx, madkx = DKX()
    tapi, matapi = TAPI()
    osc = OSC()
    cci = CCI()
    roc = ROC()
    mfi = MFI()
    mtm, mamtm = MTM()
    marsi6, marsi10 = MARSI(6), MARSI(10)
    skd_k, skd_d = SKD()
    udl, maudl = UDL()
    DI1, DI2, ADX, ADXR = DMI()

    # 能量指标
    ar, br = ARBR()
    vr, mavr = VR()
    cr, macr1, macr2, macr3, macr4 = CR()
    mass, mamass = MASS()
    sy, _ = PSY()
    pcnt = PCNT()
    cyr, macyr = CYR()

    ret = dict(locals())
    for N in [3, 5, 10, 20, 30, 55, 60, 120, 250]:
        ret['MA{}'.format(N)] = MA(CLOSE, N)
        ret['EMA{}'.format(N)] = EMA(CLOSE, N)
        ret['HMA{}'.format(N)] = MA(HIGH, N)
        ret['LMA{}'.format(N)] = MA(LOW, N)
        ret['VMA{}'.format(N)] = MA(VV, N)
        ret['AMV{}'.format(N)] = SUM(AMOV, N) / SUM(VOLUME, N)
        ret['VOL{}'.format(N)] = MA(HSL, N) * 100

    for N in [5, 10, 20]:
        ret['davol{}'.format(N)] = ret['VOL{}'.format(N)] / ret['VOL120']
    return {k.upper(): v for k, v in ret.items() if k != 'N' and k != '_'}


INDICATORS = indicators()
