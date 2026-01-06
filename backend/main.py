import time
import json
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Any, Optional
import os

API_KEY = os.getenv("API_KEY") 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELO ACTUALIZADO CON TUS NUEVOS CAMPOS ---
class AnalysisRequest(BaseModel):
    company_data: Any = None      # Nombre, Industria
    strategy_data: Any = None     # Misión, Visión, Prioridades (NUEVO)
    market_data: Any = None       # Inflación, Tasas
    competition_data: Any = None  # Competidores (NUEVO)
    objectives: List[Any] = []
    
    # Compatibilidad hacia atrás (por si acaso)
    company_name: Optional[str] = None
    companyName: Optional[str] = None
    industry: Optional[str] = None

    class Config:
        extra = "allow"

def get_best_model(api_key):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = requests.get(url)
        candidates = [m["name"].replace("models/", "") for m in response.json().get("models", []) if "generateContent" in m.get("supportedGenerationMethods", [])]
        for c in candidates: 
            if "flash" in c: return c
        return candidates[0] if candidates else "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    # Consolidar nombre de empresa
    empresa = request.company_data.get('name') if request.company_data else "Empresa"
    
    modelo_elegido = get_best_model(API_KEY)

    # --- PROMPT MAESTRO QUE USA LOS NUEVOS DATOS ---
    prompt_text = """
    Actúa como Auditor Estratégico Senior (Big Four).
    Genera un INFORME DE AUDITORÍA ESTRATÉGICA 360° utilizando TODA la información provista.

    INPUTS (CONTEXTO COMPLETO):
    1. EMPRESA: {empresa}
    2. ESTRATEGIA: {strategy} (Misión, Visión, Prioridades)
    3. MERCADO: {market} (Inflación, Tasas, Tendencias)
    4. COMPETENCIA: {competition}
    5. OBJETIVOS BSC: {objectives}

    TAREA OBLIGATORIA (Outputs):
    
    1. 📊 CÁLCULO DE GRÁFICOS (CRÍTICO):
       Debes calcular el % de Avance Promedio para cada perspectiva (Financiera, Clientes, Procesos, Aprendizaje, ESG).
       *Ejemplo: Si Financiera tiene 2 objetivos al 80% y 100%, promedio = 90%.*

    2. 📝 INFORME DETALLADO (Markdown):
       Usa la Misión y la Visión para validar si los objetivos están alineados.
       Usa la Inflación y Competencia para justificar el "Riesgo".

    ESTRUCTURA JSON DE RESPUESTA (ESTRICTA):
    {{
        "strategic_analysis": "Markdown detallado aquí... Incluir secciones de Estrategia, Análisis de Brechas, y Plan de Implementación.",
        "radar_chart": [
            {{"subject": "Financiera", "A": [CALCULO_NUMERICO_REAL], "fullMark": 100}},
            {{"subject": "Clientes", "A": [CALCULO_NUMERICO_REAL], "fullMark": 100}},
            {{"subject": "Procesos", "A": [CALCULO_NUMERICO_REAL], "fullMark": 100}},
            {{"subject": "Aprendizaje", "A": [CALCULO_NUMERICO_REAL], "fullMark": 100}},
            {{"subject": "ESG/ODS", "A": [CALCULO_NUMERICO_REAL], "fullMark": 100}}
        ],
        "stats": {{
            "total_objectives": [CONTEO_TOTAL],
            "avg_progress": [PROMEDIO_GLOBAL_NUMERICO],
            "near_target": [CONTEO_VERDES]
        }}
    }}
    """

    # Preparar datos para inyectar
    data_context = {
        "empresa": empresa,
        "strategy": json.dumps(request.strategy_data),
        "market": json.dumps(request.market_data),
        "competition": json.dumps(request.competition_data),
        "objectives": json.dumps(request.objectives)
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_elegido}:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [{"parts": [{"text": prompt_text.format(**data_context)}]}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result_json = response.json()
        texto_ia = result_json['candidates'][0]['content']['parts'][0]['text']
        clean_text = texto_ia.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        print(f"Error: {e}")
        return {"strategic_analysis": f"Error: {str(e)}", "radar_chart": [], "stats": {}}
