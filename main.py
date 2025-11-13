import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("A API Key do Gemini não foi encontrada no arquivo .env")

genai.configure(api_key=API_KEY)

app = FastAPI(
    title="Includ.IA AI Service",
    description="Microserviço de Inteligência Artificial para recrutamento inclusivo.",
    version="1.0.0",
)


class VagaRequest(BaseModel):
    descricao_original: str
    cargo: str


@app.post("/api/v1/tornar-inclusiva")
async def tornar_vaga_inclusiva(request: VagaRequest):
    """
    Recebe uma descrição de vaga e utiliza IA Generativa para remover
    termos enviesados e tornar a linguagem mais inclusiva.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
        Você é um especialista sênior em Diversidade, Equidade e Inclusão (DEI).
        Sua tarefa é reescrever a descrição da vaga abaixo para o cargo de "{request.cargo}".
        
        Diretrizes:
        1. Remova qualquer linguagem que denote viés de gênero, idade, raça ou capacidade física.
        2. Substitua termos agressivos (ex: "ninja", "matador", "workaholic") por termos baseados em competência.
        3. Mantenha os requisitos técnicos (Hard Skills), mas suavize a lista de requisitos obrigatórios se for excessiva.
        4. Use uma linguagem neutra e convidativa.
        
        Descrição Original:
        "{request.descricao_original}"
        
        Retorne APENAS o texto reescrito, sem introduções ou explicações.
        """

        response = model.generate_content(prompt)

        return {"cargo": request.cargo, "texto_inclusivo": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na IA: {str(e)}")


@app.get("/health")
def health_check():
    return {"status": "running", "service": "Includ.IA AI"}
