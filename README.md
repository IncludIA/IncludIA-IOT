# Includ.IA - Cognitive Engine (Microserviço de IA)

> 🚀 **Global Solution 2025 - O Futuro do Trabalho** > *Disruptive Architectures: IOT, IOB & Generative AI*

Esta API, desenvolvida em **Python (FastAPI)**, atua como o "cérebro" da plataforma **Includ.IA**. Ela utiliza o modelo de última geração **Google Gemini 2.5 Flash** para processar linguagem natural, garantindo interações seguras, inclusivas e imparciais no ambiente de recrutamento.

---

## 🎥 Demonstração e Links

[![Deploy da API](https://img.shields.io/badge/☁️%20Deploy-Acessar%20API-blue?style=for-the-badge&logo=google-cloud)](https://app-includia-iot-2771.azurewebsites.net/health)
[![Swagger Docs](https://img.shields.io/badge/📖%20Docs-Swagger%20UI-green?style=for-the-badge&logo=swagger)](https://app-includia-iot-2771.azurewebsites.net/docs)
[![Vídeo Pitch](https://img.shields.io/badge/📺%20YouTube-Assistir%20Pitch-red?style=for-the-badge&logo=youtube)](https://youtu.be/wAlEm5KTDSE)

> **Nota:** Clique nos botões acima para acessar os recursos.

---

## 🧠 Estratégia de IA & Prompt Engineering

Para atender aos requisitos de precisão e responsabilidade ética, implementamos técnicas avançadas de **Prompt Engineering** no design das interações com o LLM:

### 1. Seleção do Modelo
Utilizamos o **Gemini 2.5 Flash**.
* **Motivo:** Otimizado para alta velocidade e baixo custo, essencial para validações em tempo real (ex: feedback instantâneo enquanto o usuário digita) sem prejudicar a experiência no app mobile.

### 2. Técnicas Aplicadas
* **Persona Adoption (Role Playing):** Configuramos a IA para atuar com "personas" específicas em cada endpoint (ex: *"Atue como um Auditor de Conteúdo"* ou *"Atue como Especialista em D&I"*).
* **Zero-Shot Reasoning:** Instruções diretas para tarefas complexas sem necessidade de exemplos prévios.
* **Strict Output Formatting:** Forçamos a saída da IA estritamente em formato **JSON**, garantindo que o front-end possa consumir os dados sem erros.

---

## 🔌 Endpoints da API

Abaixo estão os detalhes de consumo da API.

### 🟢 GET (Verificação de Status)

Utilizado para verificar se a API e o modelo de IA estão operacionais.

**Endpoint:** `GET /health`

**Exemplo de Resposta (200 OK):**
```json
{
  "status": "online",
  "model": "gemini-2.5-flash",
  "version": "5.0.0"
}
```


-----

### 🛡️ POST (Moderação de Conteúdo)

Analisa bios e comentários em tempo real para bloquear discurso de ódio.

**Endpoint:** `POST /api/v1/seguranca/moderar`

**Body da Requisição:**

```json
{
  "texto_usuario": "O candidato é muito velho para essa vaga.",
  "contexto": "comentario_vaga"
}
```

**Exemplo de Resposta:**

```json
{
  "aprovado": false,
  "motivo": "Viés de etarismo (discriminação por idade).",
  "score_seguranca": 15
}
```

-----

### 🤝 POST (Vagas Inclusivas)

Reescreve descrições de vagas removendo viéses inconscientes e termos excludentes.

**Endpoint:** `POST /api/v1/vagas/inclusiva`

**Body da Requisição:**

```json
{
  "cargo": "Desenvolvedor Ninja",
  "descricao_original": "Procuramos um cara jovem e workaholic para codar muito."
}
```

**Exemplo de Resposta:**

```json
{
  "texto_inclusivo": "Procuramos pessoa desenvolvedora comprometida para atuar no desenvolvimento de software...",
  "alteracoes": [
    "Removido termo 'Ninja' (pouco profissional)",
    "Substituído 'cara' por 'pessoa' (gênero neutro)",
    "Removido 'jovem' (etarismo)"
  ]
}
```

-----

### 🕵️ POST (Anonimização de Currículos)

Remove dados sensíveis (PII) para Blind Recruitment.

**Endpoint:** `POST /api/v1/candidatos/anonimizar`

**Body da Requisição:**

```json
{
  "texto_curriculo": "João Silva, 25 anos, moro em São Paulo. Especialista em Java."
}
```

**Exemplo de Resposta:**

```json
{
  "resumo_profissional": "Profissional especialista em Java com experiência na região sudeste...",
  "hard_skills": ["Java"],
  "soft_skills": []
}
```

-----

## 🚀 Como Rodar Localmente

### Pré-requisitos

  * Python 3.10+
  * Uma API Key do Google Gemini

### Instalação

1.  **Clone o repositório e entre na pasta:**

    ```bash
    git clone https://github.com/IncludIA/IncludIA-IOT
    cd IncludIA-IOT
    ```

2.  **Crie o arquivo `.env`:**

    ```env
    GEMINI_API_KEY=cole_sua_chave_aqui
    ```

3.  **Instale as dependências e execute:**

    ```bash
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```

4.  **Acesse:** `http://127.0.0.1:8000/docs`

-----

## 👤 Integrantes

  * **Luiz Eduardo da Silva Pinto** - RM555213
