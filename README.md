# 🧠 Includ.IA - Cognitive Engine (Microserviço de IA)

API desenvolvida em **Python (FastAPI)** responsável pela inteligência generativa da plataforma Includ.IA. Utiliza o modelo **Google Gemini 2.5 Flash** para processamento de linguagem natural.

## 🚀 Funcionalidades
1.  **Gatekeeper (Moderação):** Analisa bios e textos para bloquear discurso de ódio antes de salvar no banco.
2.  **Inclusão (Vagas):** Reescreve descrições de vagas removendo viéses inconscientes.
3.  **Anonimização:** Remove dados sensíveis (PII) de currículos para Blind Recruitment.

## 🛠️ Tecnologias
* Python 3.10
* FastAPI & Uvicorn
* Google Generative AI SDK
* Docker

## ⚙️ Como Rodar Localmente
1.  Configure o `.env` com sua `GEMINI_API_KEY`.
2.  Instale dependências: `pip install -r requirements.txt`
3.  Execute: `uvicorn main:app --reload`
4.  Documentação (Swagger): Acesse `http://127.0.0.1:8000`

## 🧪 Testes
Execute `pytest` para validar os endpoints de saúde.