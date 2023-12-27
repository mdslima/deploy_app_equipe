import streamlit as st

# Função para mostrar a descrição de cada módulo
def mostrar_descricoes():
    st.header("Descrição dos Módulos do Aplicativo")

    # Módulo 1: Stock market app
    st.subheader("1) Módulo Meu chatbot Stock Market App")
    st.write("""
    Este módulo permite ao usuário obter informações a respeito do mercado de ações em geral desde os conceitos até as cotações de ativos. Permite tambem que 
    seja gerado um arquivo PDF com todo o histórico da conversa. Alem disso é possivel fazer o upload de um texto especifico para que o app dê respostas com base
    nele.
    """)

    # Módulo 2: Previsão de horário de vôo
    st.subheader("2) Modulo Airlines")
    st.write("""
    Este módulo permite através da escolha de certos parametros, definir a probabilidade de um determinado vôo atrasar ou não.
    """)
    
        # Chamada da função para mostrar as descrições
mostrar_descricoes()





