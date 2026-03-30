import streamlit as st
from google import genai
from groq import Groq
import os
from dotenv import load_dotenv
from datetime import datetime # Importante para o nome do arquivo

# Importamos a instrução de um dos arquivos para manter a consistência
from qa_agent_gemini import SYSTEM_INSTRUCTION

load_dotenv()

# --- INTERFACE ---
st.set_page_config(page_title="Multi-LLM QA Agent", page_icon="🕵️‍♀️", layout="centered")

with st.sidebar:
    st.title("⚙️ Configurações")
    provider = st.selectbox("Escolha o Provedor", ["Google Gemini", "Groq (Llama-3)"])
    
    if provider == "Google Gemini":
        model_name = st.selectbox("Modelo", ["gemini-2.0-flash-lite", "gemini-1.5-flash"])
    else:
        model_name = st.selectbox("Modelo", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    
    st.divider()
    st.info("Este agente permite alternar entre provedores de IA para garantir disponibilidade contínua.")

st.title("🤖 Agente de Triagem de Bugs")
st.markdown("Transforme logs ou descrições informais em relatórios profissionais de QA.")

# --- CORE LOGIC ---
def call_ai(prompt, provider, model):
    if provider == "Google Gemini":
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model=model,
            config={'system_instruction': SYSTEM_INSTRUCTION},
            contents=prompt
        )
        return response.text
    else:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content

# --- INPUT AREA ---
user_input = st.text_area("Descreva o problema ou cole o log de erro:", height=200, 
                          placeholder="Traceback (most recent call last)...")

if st.button("🚀 Gerar Relatório Profissional"):
    if len(user_input.strip()) < 10:
        st.warning("⚠️ O conteúdo é muito curto. Por favor, detalhe melhor o erro.")
    else:
        with st.spinner(f"Processando com {provider}..."):
            try:
                # unified call to AI
                report = call_ai(user_input, provider, model_name)
                
                st.subheader("✅ Relatório Estruturado")
                st.markdown(report)
                
                # Preparação para download
                timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                st.download_button(
                    label="📥 Baixar Relatório (.md)",
                    data=report,
                    file_name=f"bug_report_{provider.lower().split()[0]}_{timestamp}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"❌ Falha na comunicação com {provider}: {e}")

# --- FOOTER ---
st.divider()
st.caption("Desenvolvido por Laura Xaraba - Engenheira de Software")