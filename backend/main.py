import time
import json
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Any, Optional
import os
# --- CONFIGURACIÓN ---
API_KEY = os.getenv("API_KEY") 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    company_name: Optional[str] = None
    companyName: Optional[str] = None
    industry: Optional[str] = None
    market_data: Any = None
    objectives: List[Any] = []
    class Config:
        extra = "allow"

def get_best_model(api_key):
    """Detecta modelos disponibles, priorizando los estables"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = requests.get(url)
        data = response.json()
        candidates = []
        if "models" in data:
            for m in data["models"]:
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    candidates.append(m["name"].replace("models/", ""))
        
        # Lógica: Si hay Flash (rápido y bueno para datos), úsalo.
        for c in candidates:
            if "flash" in c: return c
        return candidates[0] if candidates else "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    # Extraer datos para el reporte
    empresa = request.company_name or request.companyName or "Empresa"
    
    # 1. SELECCIÓN DE MODELO
    modelo_elegido = get_best_model(API_KEY)

    # 2. PROMPT CON LÓGICA DE SEMÁFORO (Matriz Operativa)
    # Rojo: < 70% | Amarillo: 70-90% | Verde: > 90%
    prompt_text = """
    Actúa como Auditor Estratégico Senior. Genera un Balanced Scorecard 360°.
    
    ESTRUCTURA DEL INFORME (Markdown):
    ### 📊 Dashboard Estratégico 2026
    ### 🎯 Recomendaciones por Objetivo (Semáforo Inteligente 🔴🟡🟢)

    Responde estrictamente con este formato JSON:
    {
        "strategic_analysis": "Informe completo aquí...",
        "radar_chart": [
            {"subject": "Financiera", "A": 85, "fullMark": 100},
            {"subject": "Clientes", "A": 75, "fullMark": 100},
            {"subject": "Procesos", "A": 90, "fullMark": 100},
            {"subject": "Aprendizaje", "A": 65, "fullMark": 100},
            {"subject": "ESG/ODS", "A": 80, "fullMark": 100}
        ],
        "stats": {
            "total_objectives": 10,
            "avg_progress": 92.1,
            "near_target": 2
        }
    }
    """
# 3. ENVÍO A GOOGLE GEMINI
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_elegido}:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    # Preparamos el mensaje combinando tus instrucciones y los datos reales
    payload = {
        "contents": [{
            "parts": [{
                "text": f"{prompt_text}\n\nDATOS REALES A ANALIZAR:\nEmpresa: {empresa}\nObjetivos: {json.dumps(request.objectives)}\nMercado: {json.dumps(request.market_data)}"
            }]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result_json = response.json()
        
        # Extraemos el texto que generó la IA
        texto_ia = result_json['candidates'][0]['content']['parts'][0]['text']
        
        # Limpiamos el texto para que sea un JSON válido
        clean_text = texto_ia.replace("```json", "").replace("```", "").strip()
        
        return json.loads(clean_text)
        
    except Exception as e:
        print(f"❌ Error técnico: {str(e)}")
        return {
            "strategic_analysis": f"Error al conectar con la IA: {str(e)}",
            "radar_chart": [],
            "stats": {"total_objectives": 0, "avg_progress": 0, "near_target": 0}
        }
