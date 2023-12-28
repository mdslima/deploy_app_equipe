import streamlit as st
from openai import OpenAI
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from reportlab.pdfgen import canvas


st.title("stock market app")
st.write('Bem-vindo ao assistente pessoal para dúvidas sobre o mercado de ações.')

st.markdown("""
 Faça uma pergunta na caixa de texto.

 Clique no botão para obter a resposta.
""")

# Chave da API OpenAI
chave = st.sidebar.text_input('Chave da API OpenAI', type='password')
client = OpenAI(api_key=chave)


###################################################################

# Iniciar Histórico de Chat
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
    
# Iniciar Histórico de Conversas
if "conversas" not in st.session_state:
    st.session_state.conversas = pd.DataFrame(columns=["Data/Hora", "Tokens", "Custo Estimado", "Histórico"])
    
# Opções do Usuário
opcoes_criatividade = st.slider("Nível de Criatividade", 0, 10, 5)
opcoes_tamanho_resposta = st.slider("Tamanho da Resposta (Palavras)", 1, 300, 20)
opcoes_estilo_escrita = st.selectbox("Estilo de Escrita", ["Normal", "Técnica"])    

# Função de moderação
def moderação(pergunta):
    palavras_proibidas = ["violento", "inapropriado", "conteúdo adulto"]
    regras_gerais = ["palavrões", "linguagem ofensiva", "perguntas inadequadas"]
    
    for palavra in palavras_proibidas:
        if palavra in pergunta.lower():
            return True
    
    for regra in regras_gerais:
        if regra in pergunta.lower():
            return True
    
    return False
    
# Adicionar botão para finalizar a conversa
finalizar_conversa = st.button("Finalizar Conversa")

# React to user input
prompt = st.text_input("Faça sua pergunta")

if prompt and not finalizar_conversa:
    # Verificar se o input do usuário viola as regras de moderação
    if moderação(prompt):
        resposta_moderação = "Desculpe, sua pergunta viola as regras de moderação. Por favor, faça uma pergunta apropriada."
        with st.chat_message("system"):
            st.markdown(resposta_moderação)
        st.session_state.mensagens.append({"role": "system", "content": resposta_moderação})
    else:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.mensagens.append({"role": "user", "content": prompt})

        # Ajustar parâmetros com base nas opções do usuário
        parametros_modelo = {
            'criatividade': opcoes_criatividade / 10,
            'tamanho_resposta': opcoes_tamanho_resposta,
            'estilo_resposta': opcoes_estilo_escrita
        }

        chamada = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=st.session_state.mensagens,
            temperature=parametros_modelo['criatividade']
        )

        resposta_original = chamada.choices[0].message.content

        # Limitar o tamanho da resposta com base nas opções do usuário
        resposta_limitada = " ".join(resposta_original.split()[:opcoes_tamanho_resposta])

        # Display assistant response in chat message container
        with st.chat_message("system"):
            st.markdown(resposta_limitada)
        # Add assistant response to chat history
        st.session_state.mensagens.append({"role": "system", "content": resposta_limitada})
        
#################################################################################        
        
# Verificar se o botão "Finalizar Conversa" foi clicado
if finalizar_conversa:
    # Finalizar a conversa e alimentar o conjunto de dados
    st.session_state.mensagens.append({"role": "system", "content": "Conversa finalizada"})
    
 # Cálculos fictícios para fins de exemplo, substitua pelos valores reais
    custo_estimado = 42
    tokens_utilizados = 123

# Converter mensagens do chat para uma representação mais simples (string)
    historico_simples = []
    for mensagem in st.session_state.mensagens:
        historico_simples.append(f"{mensagem['role']}: {mensagem['content']}")
    
    # Criar DataFrame com informações da conversa
    conversa_atual = {
        "Data/Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Tokens": tokens_utilizados,
        "Custo Estimado": custo_estimado,
        "Histórico": [", ".join(historico_simples)]
    }
    
    # Limpar mensagens após finalizar a conversa
    st.session_state.mensagens = []  # Adicione esta linha para limpar as mensagens
    
    st.session_state.conversas = st.session_state.conversas.append(conversa_atual, ignore_index=True)
    # Limpar mensagens após finalizar a conversa
    st.session_state.mensagens = []

    # Exibir DataFrame na tela
    st.write("### DataFrame de Todas as Conversas")
    st.write(st.session_state.conversas)
########################################################################################
# Gera um PDF com o histórico da conversa
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Adiciona os dados do DataFrame ao PDF
    for index, row in st.session_state.conversas.iterrows():
        pdf.cell(200, 10, txt="Data/Hora: " + str(row["Data/Hora"]), ln=True, align="L")
        pdf.cell(200, 10, txt="Tokens: " + str(row["Tokens"]), ln=True, align="L")
        pdf.cell(200, 10, txt="Custo Estimado: " + str(row["Custo Estimado"]), ln=True, align="L")
        pdf.cell(200, 10, txt="Histórico:", ln=True, align="L")
        dialogos = row["Histórico"]
        for dialogo in dialogos:
            pdf.multi_cell(0, 10, txt=dialogo, align="L")
            
    
    pdf.output("historico_conversa.pdf")
    
    # Permite ao usuário baixar o PDF
    with open("historico_conversa.pdf", "rb") as file:
        btn = st.download_button(
            label="Baixar Histórico da Conversa em PDF",
            data=file,
            file_name="historico_conversa.pdf",
            mime="application/octet-stream"
        )
        
        
#########################################################################

# Adicionar o componente de upload de arquivo
arquivo_upload = st.file_uploader("Faça upload do arquivo de texto", type=['txt'])

# Verificar se um arquivo foi enviado
if arquivo_upload is not None:
    conteudo_arquivo = arquivo_upload.getvalue().decode("utf-8")  # Lê o conteúdo do arquivo

    # Mostrar o conteúdo do arquivo
    st.write("### Conteúdo do Arquivo Enviado:")
    st.write(conteudo_arquivo)

    # Usar o conteúdo do arquivo na conversa com o chatbot
    # Aqui você pode processar o conteúdo do arquivo antes de enviá-lo para o modelo de linguagem
    # Por exemplo, você pode adicioná-lo como uma mensagem ou usá-lo como contexto para a pergunta ao chatbot
    # Dependendo da lógica do seu aplicativo

    # Exemplo de uso do conteúdo do arquivo como contexto
    if not finalizar_conversa and prompt:
        # Combine a pergunta do usuário com o conteúdo do arquivo
        pergunta_com_contexto = f"{prompt} {conteudo_arquivo}"

        # ... resto do seu código para interagir com o chatbot usando pergunta_com_contexto
