# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st 
import pandas as pd
import numpy as np
import os
import joblib  # Biblioteca para carregar modelos salvos
from pycaret.regression import load_model, predict_model
from pycaret.datasets import get_data

 #Caminho para o arquivo
path = r"https://github.com/mdslima/deploy_app_equipe/Airframe.csv"

# Ler csv
dados = pd.read_csv(path)

# Define o caminho do arquivo
#caminho_arquivo = "C:/Users/mdsli/OneDrive/Área de Trabalho/STREAMLIT/recursos/modelo-previsao-delay-airframe.pkl"

# Carregar o modelo
modelo = joblib.load("https://github.com/mdslima/deploy_app_equipe/blob/main/recursos/modelo-previsao-delay-airframe.pkl")


# URL da imagem de exemplo
url_imagem = 'https://www.aereo.jor.br/wp-content/uploads/2023/11/E195-E2-PORTER-e1701298622963.jpg'

# Exibindo a imagem a partir de uma URL
st.image(url_imagem, caption='ERJ 195C', use_column_width=True)

st.header('Previsão de status de horário de vôo.')
st.write('Entre com as caracteristicas do vôo')

#Widgets para fazer os inputs do modelo

col0, col1, col2, col3 = st.columns([3,2,2,0.2])

with col0:
    Airline = st.selectbox(label = 'Companhia aerea', 
        options = dados['Airline'].unique())
    
    DayOfWeek = st.slider(label = 'Dia da semana', 
        min_value=1, 
        max_value=7, 
        value= 1, 
        step=1)
    
    Time = st.slider(label = 'Tempo de vôo', 
        min_value=10, 
        max_value=1325, 
        value= 15, 
        step=1)
    
    Length = st.slider(label = 'Distância', 
        min_value=30, 
        max_value=460, 
        value= 30, 
        step=10)
    
with col1:
    Flight = st.selectbox(label = 'Vôo', 
        options = dados['Flight'].unique())
    
with col2:
    AirportFrom = st.selectbox(label = 'Origem', 
        options = dados['AirportFrom'].unique())
    
    AirportTo = st.selectbox(label = 'Destino', 
        options = dados['AirportTo'].unique())


#Criar um DataFrame com os inputs exatamente iguais aos do dataframe em que foi treinado o modelo
aux =  {'Airline': [Airline],
		'DayOfWeek': [DayOfWeek,],
		'Time': [Time], 
		'Length': [Length],
		'Flight': [ Flight],
		'AirportFrom': [AirportFrom],
		'AirportTo': [AirportTo]}

prever = pd.DataFrame(aux)

st.write(prever)

#Usar o modelo salvo para fazer previsao nesse Dataframe

_, c1, _ = st.columns([2,3,1])

with c1:
	botao = st.button('Calcular Previsão de atraso',
		type = 'primary',
		use_container_width = True)
        
if botao:
	previsao = predict_model(modelo, data = prever)
	valor = round(previsao.loc[0,'prediction_label'])
    
if valor == 0:
    st.write('### A previsão para o vôo é Atraso')
elif valor == 1:
    st.write('### A previsão para o vôo é No Horário')


        
      

    
    
        
    
    
    
    
