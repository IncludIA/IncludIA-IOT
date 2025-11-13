import os
import logging
import json
import asyncio
import google.generativeai as genai
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import List, Optional, Any

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("includia-brain")

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    logger.critical("CRÍTICO: GEMINI_API_KEY não encontrada no .env")
    raise RuntimeError("API Key é obrigatória.")

genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"

app = FastAPI(
    title="Includ.IA - Cognitive Engine",
    description="Microsserviço de IA Generativa para validação, moderação e inclusão.",
    version="5.0.0 - Global Solution Edition",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VagaRequest(BaseModel):
    cargo: str
    descricao_original: str


class ModeracaoRequest(BaseModel):
    texto_usuario: str = Field(
        ..., description="Texto a ser analisado (Bio, Comentário, Vaga)."
    )
    contexto: str = Field("perfil_usuario", description="Onde o texto será usado.")


class ModeracaoResponse(BaseModel):
    aprovado: bool
    motivo: Optional[str] = None
    score_seguranca: int = Field(..., description="De 0 a 100, quão seguro é o texto.")


class CurriculoRequest(BaseModel):
    texto_curriculo: str


class RateLimitException(Exception):
    """Erro personalizado para quando estourar a cota do Google"""

    pass


@retry(
    retry=retry_if_exception_type(RateLimitException),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=15),
    reraise=True,
)
def chamar_gemini_blindado(prompt: str) -> Any:
    """
    Executa chamadas à IA com proteção contra falhas de rede e limites de cota.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)

        response = model.generate_content(
            prompt, generation_config={"response_mime_type": "application/json"}
        )

        return json.loads(response.text)

    except Exception as e:
        erro_str = str(e)
        if "429" in erro_str or "quota" in erro_str.lower():
            logger.warning(
                f"⚠️ Cota excedida ({MODEL_NAME}). Aguardando para tentar novamente..."
            )
            raise RateLimitException("Limite de requisições atingido temporariamente.")
        elif "404" in erro_str:
            logger.error(f"❌ Modelo '{MODEL_NAME}' não encontrado na sua conta.")
            raise HTTPException(
                status_code=500, detail=f"Modelo inválido: {MODEL_NAME}"
            )
        else:
            logger.error(f"❌ Erro desconhecido na IA: {e}")
            raise HTTPException(
                status_code=502, detail="Falha no processamento cognitivo."
            )


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    return {"status": "online", "model": MODEL_NAME, "version": "5.0.0"}


@app.post(
    "/api/v1/seguranca/moderar", response_model=ModeracaoResponse, tags=["Segurança"]
)
async def moderar_conteudo(request: ModeracaoRequest):
    """
    Analisa se o texto é seguro para ser salvo no banco de dados.
    Retorna 'aprovado': true/false.
    """
    logger.info(f"Moderando conteúdo para: {request.contexto}")

    prompt = f"""
    Atue como um Auditor de Conteúdo (Trust & Safety).
    Analise o texto abaixo para o contexto: {request.contexto}.
    
    Critérios de Reprovação:
    1. Discurso de ódio, racismo, sexismo, homofobia.
    2. Assédio ou bullying.
    3. Conteúdo sexualmente explícito.
    4. Linguagem excessivamente violenta.
    
    Texto: "{request.texto_usuario}"
    
    Retorne JSON:
    {{
        "aprovado": boolean,
        "motivo": "Explicação curta se reprovado, ou null se aprovado",
        "score_seguranca": inteiro de 0 (perigoso) a 100 (seguro)
    }}
    """
    return chamar_gemini_blindado(prompt)


@app.post("/api/v1/vagas/inclusiva", tags=["Recrutamento"])
async def tornar_vaga_inclusiva(request: VagaRequest):
    """Reescreve descrições de vagas para remover viéses inconscientes."""
    prompt = f"""
    Atue como Especialista em D&I. Reescreva a vaga: "{request.cargo}".
    Remova termos excludentes (idade, gênero, 'workaholic', 'ninja').
    Texto original: "{request.descricao_original}"
    
    Retorne JSON: {{ "texto_inclusivo": "...", "alteracoes": ["termo X removido", ...] }}
    """
    return chamar_gemini_blindado(prompt)


@app.post("/api/v1/candidatos/anonimizar", tags=["Candidatos"])
async def anonimizar_perfil(request: CurriculoRequest):
    """Remove PII (Dados Pessoais) de currículos para triagem imparcial."""
    prompt = f"""
    Analise este currículo e extraia APENAS competências.
    REMOVA: Nome, Idade, Gênero, Endereço, Locais específicos.
    Currículo: "{request.texto_curriculo}"
    
    Retorne JSON: 
    {{ 
        "resumo_profissional": "Resumo em 3ª pessoa...", 
        "hard_skills": ["Java", "SQL"...], 
        "soft_skills": ["Liderança"...]
    }}
    """
    return chamar_gemini_blindado(prompt)
