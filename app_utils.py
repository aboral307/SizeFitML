# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 21:47:25 2020

@author: anind
"""

def size_pref_correction(pred, size_pref, corr_factors):
    pred_final = pred + corr_factors[size_pref]
    if pred_final>4:
        pred_final = 4
        return pred_final
    elif pred_final<0:
        pred_final = 0
        return pred_final
    else:
        return pred_final