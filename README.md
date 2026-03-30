# 🤖 AI Bug Report Agent (Multi-LLM)

Este é um agente inteligente de triagem de bugs desenvolvido para transformar logs técnicos confusos ou descrições informais em relatórios profissionais de QA (Quality Assurance). O projeto foi construído com foco em **resiliência** e **escalabilidade**, suportando múltiplos provedores de IA.

---

## 🌟 Diferenciais do Projeto

- **Multi-LLM Support**: Integração com **Google Gemini** (v2.0 Flash) e **Groq (Llama-3.3)**.
- **Resiliência de Modelo**: Sistema de fallback que alterna entre modelos caso um provedor esteja instável.
- **Interface Dupla**:
    - 🖥️ **CLI (Terminal)**: Para desenvolvedores que buscam rapidez no fluxo de trabalho.
    - 🌐 **Web UI (Streamlit)**: Interface amigável para usuários não técnicos ou demonstrações.
- **Persistência de Dados**: Geração automática de arquivos `.md` organizados para documentação de bugs.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **IA/LLM:** Google GenAI SDK & Groq Cloud SDK
* **Interface Web:** [Streamlit](https://streamlit.io/)
* **Ambiente:** `python-dotenv` para gestão de chaves de API e `venv` para isolamento.

---

## 🚀 Como Executar o Projeto

### 1. Clonar o repositório
```bash
git clone [https://github.com/SEU_USUARIO/qa_agent.git](https://github.com/SEU_USUARIO/qa_agent.git)
cd qa_agent
```

### 2. Configurar o Ambiente Virtual (venv)
```bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Chaves de API
Crie um arquivo .env na raiz do projeto com suas chaves:
```dotenv
GEMINI_API_KEY=sua_chave_aqui
GROQ_API_KEY=sua_chave_aqui
```

---

## 🖥️ Modos de Uso

### Opção A: Interface Web (Recomendado para Testes)
```bash
streamlit run app_ui.py
```

### Opção B: Terminal (Via Groq/Llama-3)
```bash
python qa_agent_groq.py
```

### Opção C: Terminal (Via Gemini)
```bash
python qa_agent_gemini.py
```

---

## 📁 Estrutura de Arquivos

* `app_ui.py`: Interface Web unificada (Gemini + Groq).

* `qa_agent_groq.py`: Script CLI focado no modelo Llama-3 via Groq.

* `qa_agent_gemini.py`: Script CLI focado nos modelos Google Gemini.

* `bug_reports/`: Pasta onde os relatórios gerados são salvos automaticamente.

---

## 👩‍💻 Desenvolvido por
Laura Xaraba - Estudante de Engenharia de Software focada em Engenharia de Qualidade e IA Generativa.
