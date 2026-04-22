# 🤖 Paulo GPT

> **Agente de IA Multimodal** — Chat com suporte a texto, PDF e câmera/imagens, alimentado pela [OpenRouter API](https://openrouter.ai).

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![OpenRouter](https://img.shields.io/badge/OpenRouter-API-6c63ff?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## ✨ Funcionalidades

| Recurso | Status |
|---|---|
| 💬 Chat com streaming em tempo real | ✅ Ativo |
| 🧬 14 modelos de IA (gratuitos e pagos) | ✅ Ativo |
| 📄 Análise de documentos PDF | ✅ Ativo |
| 📷 Câmera do celular (via rede local) | ✅ Ativo |
| 🖼️ Upload de imagens (jpg/png/webp) | ✅ Ativo |
| 🎭 Personas configuráveis (sem restrições, programador, etc.) | ✅ Ativo |
| 🌙 Tema Dark / Light | ✅ Ativo |
| 💾 Histórico de conversas persistente | ✅ Ativo |
| 📱 QR Code para acesso pelo celular | ✅ Ativo |
| 📊 Métricas de sessão (tokens / mensagens) | ✅ Ativo |

---

## 📷 Status da Integração com Câmera

> ✅ **A integração com câmera está FUNCIONANDO corretamente.**

### Como funciona

A câmera utiliza o componente nativo `st.camera_input()` do Streamlit, que acessa a câmera do dispositivo diretamente pelo browser sem necessidade de plugins externos.

### Configuração necessária (já aplicada)

O arquivo `.streamlit/config.toml` já está corretamente configurado para habilitar o acesso da câmera via rede local:

```toml
[server]
address = "0.0.0.0"      # Aceita conexões externas (celular na mesma Wi-Fi)
port = 8501
enableCORS = false        # Desabilita CORS — necessário para câmera funcionar
enableXsrfProtection = false

[browser]
serverAddress = "localhost"
gatherUsageStats = false
```

> ⚠️ `enableCORS = false` é **essencial** — sem isso o browser bloqueia o acesso à câmera por política de segurança (CORS).

### Fluxo de uso da câmera

```
Usuário seleciona "📷 Câmera do Celular"
     ↓
st.camera_input() abre o browser da câmera
     ↓
Foto capturada → convertida para Base64 (JPEG)
     ↓
Armazenada em st.session_state.pending_image
     ↓
Na próxima mensagem, enviada ao modelo como multimodal (image_url)
     ↓
Modelo com visão (GPT-4o, Claude, Gemini) analisa a imagem
```

### Modelos com suporte a imagens

| Modelo | Visão |
|---|---|
| openai/gpt-4o | ✅ |
| openai/gpt-4o-mini | ✅ |
| anthropic/claude-3.5-sonnet | ✅ |
| anthropic/claude-3-haiku | ✅ |
| google/gemini-flash-1.5 | ✅ |
| Demais modelos | ❌ (alerta exibido) |

> Se o modelo não suportar visão, o app **exibe aviso e bloqueia o envio** — protegendo contra erros de API.

### Acesso pelo celular

1. O app detecta automaticamente o IP local da máquina
2. Gera um **QR Code** na sidebar apontando para `http://<IP>:8501`
3. Escaneie com o celular (na mesma rede Wi-Fi)
4. A câmera do celular fica disponível diretamente no app

---

## 🚀 Instalação e Execução Local

### Pré-requisitos

- Python 3.10+
- Chave de API do [OpenRouter](https://openrouter.ai/keys)

### 1. Clone o repositório

```bash
git clone https://github.com/Paulo207/Painel-de-controle-de-log-stica-da-cadeia-de-suprimentos.git
cd "Paulo Gpt"
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a chave de API

Crie o arquivo `.env` na raiz do projeto:

```env
OPENROUTER_API_KEY=sk-or-v1-sua-chave-aqui
```

> Obtenha sua chave gratuita em [openrouter.ai/keys](https://openrouter.ai/keys)

### 5. Execute o app

```bash
streamlit run app.py
```

Acesse: **http://localhost:8501**

---

## ☁️ Deploy no Streamlit Cloud (Recomendado)

### Passo a passo

1. **Faça push do código para o GitHub** (sem o `.env` — já está no `.gitignore`)

2. **Acesse** [share.streamlit.io](https://share.streamlit.io) e faça login com GitHub

3. **Clique em "New app"** e selecione o repositório

4. **Configure o Main file path:** `app.py`

5. **Configure o Secret da API Key:**
   - Vá em **Advanced settings → Secrets**
   - Adicione:
     ```toml
     OPENROUTER_API_KEY = "sk-or-v1-sua-chave-aqui"
     ```

6. **Clique em "Deploy"** — o app fica disponível em `https://seu-app.streamlit.app`

> ✅ O app já suporta `st.secrets` nativamente — nenhuma alteração de código necessária.

### ⚠️ Nota sobre câmera no Streamlit Cloud

No deploy em cloud, a câmera funciona via HTTPS (o Streamlit Cloud provê SSL automaticamente). O `enableCORS = false` do `config.toml` **não é necessário** no cloud, mas não causa problemas.

---

## 🗂️ Estrutura do Projeto

```
Paulo Gpt/
├── app.py                    # Aplicação principal (Streamlit)
├── memory.py                 # Módulo de persistência de conversas (JSON)
├── requirements.txt          # Dependências Python
├── .env                      # Chave de API (NÃO sobe para o GitHub)
├── .gitignore                # Arquivos ignorados pelo Git
├── .streamlit/
│   └── config.toml           # Configuração do Streamlit (CORS, porta, etc.)
└── memory/
    └── conversations.json    # Histórico salvo (gerado automaticamente)
```

---

## ⚙️ Variáveis de Ambiente

| Variável | Descrição | Onde configurar |
|---|---|---|
| `OPENROUTER_API_KEY` | Chave de API do OpenRouter | `.env` (local) ou Streamlit Secrets (cloud) |

---

## 📦 Dependências

```
streamlit>=1.35.0      # Framework web
requests>=2.31.0       # Chamadas HTTP para a API
python-dotenv>=1.0.0   # Leitura do .env
pdfplumber>=0.10.0     # Extração de texto de PDFs
Pillow>=10.0.0         # Processamento de imagens
```

---

## 🧬 Modelos Disponíveis

| Ícone | Nome | ID OpenRouter | Custo |
|---|---|---|---|
| 🦙 | Llama 3.3 70B | `meta-llama/llama-3.3-70b-instruct:free` | Grátis |
| 🔥 | DeepSeek R1 | `deepseek/deepseek-r1:free` | Grátis |
| 🆓 | GLM-4.5 Air | `z-ai/glm-4.5-air:free` | Grátis |
| 🆓 | Gemma 3 27B | `google/gemma-3-27b-it:free` | Grátis |
| 🆓 | Llama 3.1 8B | `meta-llama/llama-3.1-8b-instruct:free` | Grátis |
| 🆓 | Mistral 7B | `mistralai/mistral-7b-instruct:free` | Grátis |
| 🧠 | GPT-4o | `openai/gpt-4o` | Pago |
| ⚡ | GPT-4o Mini | `openai/gpt-4o-mini` | Pago |
| 🔮 | Claude 3.5 Sonnet | `anthropic/claude-3.5-sonnet` | Pago |
| 🌟 | Claude 3 Haiku | `anthropic/claude-3-haiku` | Pago |
| 🌙 | Gemini Flash 1.5 | `google/gemini-flash-1.5` | Pago |

---

## 🔐 Segurança

- A chave de API **nunca é exposta** ao frontend
- O `.env` está no `.gitignore` — não sobe para o GitHub
- No Streamlit Cloud, use **Secrets** para proteger a chave
- A chave pode ser sobrescrita pelo usuário via sidebar sem afetar o `.env`

---

## 📝 Licença

MIT License — use, modifique e distribua livremente.

---

*Desenvolvido com ❤️ usando Streamlit + OpenRouter*
