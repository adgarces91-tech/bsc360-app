import time
import json
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Any, Optional

# --- CONFIGURACIÓN ---
API_KEY = "AIzaSyBeDM0o2U3Qg5yX-bdInb-VvM5tdN9b8UA" 

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

@app.post("/api/analyze")
async def analyze_data(request: AnalysisRequest):
    empresa = request.company_name or request.companyName or "Empresa"
    
    # 1. DEBUG DE DATOS (¡Esto es vital!)
    print(f"📥 DATOS RECIBIDOS DEL FRONTEND:")
    print(f" - Empresa: {empresa}")
    print(f" - Cantidad de Objetivos: {len(request.objectives)}")
    # Imprimimos el primer objetivo para ver si tiene datos reales
    if request.objectives:
        print(f" - Ejemplo Objetivo 1: {request.objectives[0]}")
    else:
        print(f" ⚠️ ALERTA: La lista de objetivos está VACÍA. La IA inventará datos.")

    # 2. SELECCIÓN DE MODELO
    modelo_elegido = get_best_model(API_KEY)
    print(f"🧠 Analizando con: {modelo_elegido}...")

    # 3. PROMPT "ANALISTA FINANCIERO" (Estructura Rígida con Cálculos)
    objetivos_text = json.dumps(request.objectives, indent=2)
    
    prompt_text = f"""
    Actúa como un Auditor de Estrategia Corporativa.
    Analiza los siguientes datos reales de la empresa '{empresa}'.
    
    DATOS DE ENTRADA (OBJETIVOS Y KPIs):
    {objetivos_text}

    TU TAREA:
    Generar un informe técnico detallado. Para cada objetivo crítico, DEBES CALCULAR las brechas.
    No inventes que "faltan datos" si los datos están ahí. Úsalos.

    ESTRUCTURA EXACTA DEL INFORME (Markdown):
    
    ### 📊 Estado de Situación 2026
    * **Diagnóstico Global:** [Resumen técnico de 3 líneas]
    * **Indicador de Salud:** [Calcula un % promedio de cumplimiento general]

    ---
    ### 🎯 Análisis de Desviaciones (Top 3 Críticos)
    
    #### 1. [Nombre del Objetivo]
    * **Situación Actual:** (Ej: Valor Real 18% vs Meta 25%)
    * **📉 Análisis de Brecha:**
      - **Brecha Absoluta:** [Diferencia numérica]
      - **Cumplimiento:** [Calcula el % logrado]
    * **🔥 Acción Correctiva:** [Solución técnica inmediata]
    * **💰 Presupuesto Estimado:** $XX,XXX USD.

    #### 2. [Nombre del Objetivo]
    ... (Repetir estructura con cálculos) ...

    #### 3. [Nombre del Objetivo]
    ... (Repetir estructura con cálculos) ...

    ---
    ### 🚀 Plan de Implementación
    * **Corto Plazo (Semana 1-4):** Acciones de choque.
    * **Mediano Plazo (Mes 2-3):** Estabilización.

    ---------------------------------------------------
    Responde SOLO con este JSON:
    {{
        "strategic_analysis": "Tu markdown aquí...",
        "radar_chart": [
            {{"subject": "Financiera", "A": 100, "fullMark": 150}},
            {{"subject": "Clientes", "A": 100, "fullMark": 150}},
            {{"subject": "Procesos", "A": 100, "fullMark": 150}},
            {{"subject": "Aprendizaje", "A": 100, "fullMark": 150}},
            {{"subject": "Sostenibilidad", "A": 100, "fullMark": 150}}
        ]
    }}
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_elegido}:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            print(f"❌ Error API: {response.text}")
            return {"strategic_analysis": f"Error Google: {response.text}", "radar_chart": []}

        result_json = response.json()
        
        if "candidates" not in result_json:
            return {"strategic_analysis": "La IA no pudo procesar los datos numéricos.", "radar_chart": []}

        texto_ia = result_json['candidates'][0]['content']['parts'][0]['text']
        clean_text = texto_ia.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)

    except Exception as e:
        print(f"Error grave: {e}")
        return {"strategic_analysis": f"Error técnico: {str(e)}", "radar_chart": []}