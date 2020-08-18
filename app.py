# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 13:56:34 2020

@author: anind
"""

import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle
from app_utils import size_pref_correction

app = Flask(__name__)
SizeFitModel = pickle.load(open('KNNModel.pkl', 'rb'))
FeatureScaler = pickle.load(open('KNNScaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    cols = ['user_weight', 'user_height', 'tummy_codes']
    tummy_map = {'Flatter':0, 'Average':1, 'Curvier':2}
    
    pred_map = {0: 'X-Small', 1: 'Small', 2: 'Medium', 3: 'Large', 4: 'X-Large'}
    corr_factors = {'Very Tight':-3, 'Tight':-2, 'Slightly Tight':-1, 'Average':0, 'Slightly Loose':1, 'Loose':2, 'Looser':3}
    
    #user_age = float(request.form.get('user_age'))
    user_weight = float(request.form.get('user_weight'))
    user_height = float(request.form.get('user_height'))
    tummy_shape = request.form.get('tummy_shape')
    #hip_shape = request.form.get('hip_shape')
    size_preference = request.form.get('size_preference')
    
    #user_weight=55
    #user_height=150
    #tummy_shape='Curvier'
    #size_preference='Very Tight'
    
    input_params = np.zeros(3)
    input_params[0] = user_weight
    input_params[1] = user_height
    input_params[2] = tummy_map[tummy_shape]
    input_features = pd.DataFrame([input_params],columns=cols)
    input_scaled = FeatureScaler.transform(input_features)
    pred_value = SizeFitModel.predict(input_scaled)
    
    input_params[2] = tummy_map['Average']
    input_features = pd.DataFrame([input_params],columns=cols)
    input_scaled = FeatureScaler.transform(input_features)
    pred_value_base = SizeFitModel.predict(input_scaled)
        
    if tummy_map[tummy_shape]==2 and pred_value[0]<pred_value_base[0]:
        pred_value[0]=pred_value_base[0]
    elif tummy_map[tummy_shape]==0 and pred_value[0]>pred_value_base[0]:
        pred_value[0]=pred_value_base[0]
    
    pred_pref = size_pref_correction(pred_value[0],size_preference,corr_factors)
    
    return render_template('index.html', prediction_text1='Recommended size is: {}'.format(pred_map[pred_value[0]]),
                           prediction_text2='Recommended size based on size preference is: {}'.format(pred_map[pred_pref]))

if __name__ == "__main__":
    app.run(debug=True)