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
    prompt_text = f"""
    Actúa como Auditor Estratégico Senior. Genera un Balanced Scorecard 360° para '{empresa}'.
    
    CONTEXTO EMPRESARIAL Y MERCADO:
    {json.dumps(request.market_data, indent=2)}
    
    OBJETIVOS ESTRATÉGICOS (MATRIZ):
    {json.dumps(request.objectives, indent=2)}

    TAREAS DE ANÁLISIS:
    1. Calcula el % de Avance para cada objetivo: (Valor Actual / Meta).
    2. Determina el ESTADO usando esta escala:
       - 🔴 CRÍTICO: Avance inferior al 70%.
       - 🟡 EN OBSERVACIÓN: Avance entre 70% y 90%.
       - 🟢 BAJO RIESGO: Avance superior al 90%.
    3. Cruza los datos con la Inflación y Tasa de Interés del mercado.

    ESTRUCTURA DEL INFORME (Markdown):
    ### 📊 Dashboard Estratégico 2026
    * Diagnóstico basado en el contexto de la empresa.
    * Indicador de Salud Global (%).

    ### 🎯 Recomendaciones por Objetivo (Semáforo Inteligente)
    (Para cada objetivo analizado):
    #### [Nombre del Objetivo] [EMOJI SEGÚN ESTADO]
    - **Estado:** [CRÍTICO / EN OBSERVACIÓN / BAJO RIESGO]
    - **KPI:** [Nombre del KPI]
    - **Análisis:** Valor [Valor Actual] vs Meta [Meta]. Avance del [%].
    - **Acción Correctiva:** Basada en la 'Línea de Acción' y datos de mercado.

    Responde estrictamente con este formato JSON:
    {{
        "strategic_analysis": "### 📊 Informe Ejecutivo... (Incluye aquí el análisis detallado con semáforos 🔴🟡🟢 y el Plan de Implementación completo)",
        "radar_chart": [
            {{"subject": "Financiera", "A": [CALCULA_PROMEDIO_REAL], "fullMark": 100}},
            {{"subject": "Clientes", "A": [CALCULA_PROMEDIO_REAL], "fullMark": 100}},
            {{"subject": "Procesos", "A": [CALCULA_PROMEDIO_REAL], "fullMark": 100}},
            {{"subject": "Aprendizaje", "A": [CALCULA_PROMEDIO_REAL], "fullMark": 100}},
            {{"subject": "ESG/ODS", "A": [CALCULA_PROMEDIO_REAL], "fullMark": 100}}
        ],
        "stats": {{
            "total_objectives": [CONTEO_TOTAL],
            "avg_progress": [PROMEDIO_TOTAL_GENERAL],
            "near_target": [CONTEO_OBJETIVOS_EN_VERDE]
        }}
    }}
