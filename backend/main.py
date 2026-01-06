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

class AnalysisRequest(BaseModel):
    company_data: Any = {}      
    strategy_data: Any = {}     
    market_data: Any = {}       
    competition_data: Any = {}  
    objectives: List[Any] = []
    company_name: Optional[str] = None
    class Config: extra = "allow"

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
    # PREPARACIÓN DE DATOS (Variables Limpias)
    empresa = request.company_data.get('name', 'Empresa') if isinstance(request.company_data, dict) else "Empresa"
    strategy = json.dumps(request.strategy_data, ensure_ascii=False)
    market = json.dumps(request.market_data, ensure_ascii=False)
    objectives = json.dumps(request.objectives, ensure_ascii=False)
    
    # Extraemos inflación y tasa para análisis financiero
    inflation = request.market_data.get('inflation', 0) if isinstance(request.market_data, dict) else 0
    interest = request.market_data.get('interest_rate', 0) if isinstance(request.market_data, dict) else 0

    modelo_elegido = get_best_model(API_KEY)

    # --- PROMPT "EDICIÓN DE LUJO" ---
    prompt_text = f"""
    Actúa como Auditor Estratégico Senior (Big Four).
    Genera un INFORME FINAL DE AUDITORÍA BSC 360° con formato visual rico, usando emojis y alertas.

    --- CONTEXTO ---
    EMPRESA: {empresa}
    ESTRATEGIA: {strategy}
    MERCADO: {market}
    OBJETIVOS: {objectives}

    --- INSTRUCCIONES DE FORMATO VISUAL (OBLIGATORIO) ---
    1. Usa EMOJIS en todos los títulos y secciones clave.
    2. SISTEMA DE SEMÁFORO:
       - Si el avance es < 70%: 🔴 CRÍTICO
       - Si el avance es 70-90%: 🟡 ALERTA
       - Si el avance es > 90%: 🟢 ÓPTIMO
    3. Separa claramente cada objetivo con una línea divisoria (---).
    4. El estilo debe ser "Ejecutivo Directo": frases cortas, datos duros, sin relleno.

    --- PLANTILLA DE CONTENIDO (Usar Markdown) ---
    Genera el campo 'strategic_analysis' siguiendo EXACTAMENTE este esquema:

    # 📊 INFORME EJECUTIVO - BSC 360°
    
    ## 🏦 Resumen de Salud Estratégica
    * **Empresa:** {empresa}
    * **Contexto Financiero:** Inflación {inflation}% | Tasas {interest}%
    * **Total Objetivos:** [N]
    * **Promedio Global:** [X]%
    * **🚨 Alerta Principal:** [Objetivo con peor desempeño]

    ---
    # 🎯 ANÁLISIS DETALLADO POR OBJETIVO
    (Repite esto para cada objetivo):

    ### 📌 [Nombre del Objetivo]
    **Perspectiva:** [Perspectiva] | **KPI:** [Nombre KPI]

    > **ESTADO ACTUAL:** [SEMÁFORO 🔴🟡🟢] [Estado Texto]
    
    **📉 LAS CIFRAS:**
    * **Meta:** [Valor Meta]
    * **Real:** [Valor Actual]
    * **Brecha:** [Valor] ([Porcentaje]%)
    * **Cumplimiento:** [Porcentaje]%

    **🧠 ANÁLISIS & ACCIÓN:**
    * **🔍 Diagnóstico:** (¿Por qué ocurre la brecha? Relacionar con mercado).
    * **⚡ Plan de Choque:** [Acción Inmediata 1]
    * **💰 Presupuesto:** $[Monto] USD (Detallar items).
    * **⚠️ Riesgo:** [Riesgo de inacción].
    * **🔗 Interdependencias:** [Impacto en otros objetivos].

    ---
    (Fin del loop de objetivos)

    # 🚀 PLAN DE IMPLEMENTACIÓN
    * **Inmediato (0-30 días):** [Lista]
    * **Mediano Plazo (30-90 días):** [Lista]

    --- FIN PLANTILLA ---

    RESPONDE SOLO CON ESTE JSON:
    {{
        "strategic_analysis": "El markdown generado...",
        "radar_chart": [
            {{"subject": "Financiera", "A": [CALCULO_REAL], "fullMark": 100}},
            {{"subject": "Clientes", "A": [CALCULO_REAL], "fullMark": 100}},
            {{"subject": "Procesos", "A": [CALCULO_REAL], "fullMark": 100}},
            {{"subject": "Aprendizaje", "A": [CALCULO_REAL], "fullMark": 100}},
            {{"subject": "ESG/ODS", "A": [CALCULO_REAL], "fullMark": 100}}
        ],
        "stats": {{
            "total_objectives": [CONTEO],
            "avg_progress": [PROMEDIO_GLOBAL],
            "near_target": [CONTEO_VERDES]
        }}
    }}
    """

    # 3. ENVÍO A GOOGLE
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_elegido}:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = { "contents": [{"parts": [{"text": prompt_text}]}] }

    try:
        print("📡 Enviando a Gemini...")
        response = requests.post(url, headers=headers, json=payload)
        result_json = response.json()
        
        if 'candidates' not in result_json: 
            print("Error API:", result_json)
            raise ValueError("Respuesta inválida de Google")
        
        texto_ia = result_json['candidates'][0]['content']['parts'][0]['text']
        clean_text = texto_ia.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)

    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "strategic_analysis": f"### ⚠️ Error Técnico\n{str(e)}",
            "radar_chart": [],
            "stats": {"total_objectives": 0, "avg_progress": 0, "near_target": 0}
        }
