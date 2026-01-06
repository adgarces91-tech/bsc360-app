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
    # 1. PREPARACIÓN DE DATOS
    empresa = request.company_data.get('name', 'Empresa') if isinstance(request.company_data, dict) else "Empresa"
    strategy = json.dumps(request.strategy_data, ensure_ascii=False)
    market = json.dumps(request.market_data, ensure_ascii=False)
    
    inflation = request.market_data.get('inflation', 0) if isinstance(request.market_data, dict) else 0
    interest = request.market_data.get('interest_rate', 0) if isinstance(request.market_data, dict) else 0

    # --- 2. MOTOR MATEMÁTICO (Python calcula, no la IA) ---
    # Esto soluciona el error del "0%" en Clientes y ROI incorrectos
    processed_objectives = []
    total_progress = 0
    count = 0

    for obj in request.objectives:
        try:
            # Forzamos conversión a números para evitar errores
            current = float(obj.get('current_value', 0))
            target = float(obj.get('target_value', 1)) # Evitar división por cero
            
            # Cálculo de Avance
            if target == 0: 
                progress = 0
            else:
                progress = (current / target) * 100
            
            # Tope lógico (opcional, para que no de 500% si se pasa mucho)
            # progress = min(progress, 150) 

            # Agregamos el cálculo al objeto que enviaremos a la IA
            obj['calculated_progress'] = round(progress, 2)
            
            # Determinamos el semáforo nosotros mismos para asegurar precisión
            if progress < 70:
                obj['status_emoji'] = "🔴 CRÍTICO"
                obj['status_text'] = "Requiere Atención Inmediata"
            elif progress < 90:
                obj['status_emoji'] = "🟡 ALERTA"
                obj['status_text'] = "Desviación Moderada"
            else:
                obj['status_emoji'] = "🟢 ÓPTIMO"
                obj['status_text'] = "En Meta"

            processed_objectives.append(obj)
            total_progress += progress
            count += 1
        except Exception as e:
            obj['calculated_progress'] = 0
            obj['status_emoji'] = "⚪ ERROR DATOS"
            processed_objectives.append(obj)

    # Calculamos el promedio global real
    global_avg = round(total_progress / count, 2) if count > 0 else 0
    objectives_json = json.dumps(processed_objectives, ensure_ascii=False)

    modelo_elegido = get_best_model(API_KEY)

    # 3. PROMPT MAESTRO (Ahora recibe los cálculos listos)
    prompt_text = f"""
    Actúa como Auditor Estratégico Senior (Big Four).
    Genera un INFORME FINAL BSC 360° utilizando los CÁLCULOS MATEMÁTICOS YA REALIZADOS.

    --- DATOS PRE-CALCULADOS (USAR ESTOS VALORES, NO RE-CALCULAR) ---
    PROMEDIO GLOBAL: {global_avg}%
    OBJETIVOS DETALLADOS: {objectives_json}
    
    CONTEXTO EXTRA:
    EMPRESA: {empresa}
    ESTRATEGIA: {strategy}
    MERCADO: {market}

    --- INSTRUCCIONES DE FORMATO ---
    1. Usa los valores 'calculated_progress' y 'status_emoji' que vienen en el JSON. ¡No inventes números!
    2. Estructura visual: Usa bloques de cita (>) para destacar el estado.
    3. Separa objetivos con línea horizontal (---).

    --- PLANTILLA DE CONTENIDO (Markdown) ---
    Genera el campo 'strategic_analysis' así:

    # 📊 INFORME DE GESTIÓN - BSC 360°
    
    ## 🏦 Resumen Ejecutivo
    * **Empresa:** {empresa}
    * **Entorno:** Inflación {inflation}% | Tasa {interest}%
    * **Salud General:** {global_avg}% de cumplimiento global.
    * **Diagnóstico:** (Escribe un breve párrafo de 3 líneas resumiendo la situación).

    ---
    # 🎯 DETALLE DE DESEMPEÑO
    (Repite para cada objetivo):

    ### 📌 [Nombre del Objetivo]
    **Perspectiva:** [Perspectiva] | **KPI:** [Nombre KPI]

    > **ESTADO:** [status_emoji] ([status_text])
    > **CUMPLIMIENTO:** [calculated_progress]%

    **📉 LAS CIFRAS:**
    * **Meta:** [target_value] [unit]
    * **Real:** [current_value] [unit]
    * **Brecha:** (Calcula la diferencia simple)

    **🧠 ANÁLISIS & ACCIÓN:**
    * **🔍 Causa Raíz:** (Explica por qué, cruzando con datos de mercado/estrategia).
    * **⚡ Plan de Choque:** [Línea de Acción mejorada].
    * **💰 Inversión Requerida:** $[Estimación USD] (Sé específico).
    * **⚠️ Riesgo:** [Consecuencia de no actuar].

    ---
    # 🚀 PLAN DE IMPLEMENTACIÓN PRIORIZADO
    * **Corto Plazo (Semana 1-4):** [Lista acciones urgentes de objetivos rojos]
    * **Mediano Plazo (Mes 2-3):** [Lista acciones de objetivos amarillos]

    --- FIN PLANTILLA ---

    RESPONDE SOLO CON ESTE JSON:
    {{
        "strategic_analysis": "El markdown generado...",
        "radar_chart": [
            {{"subject": "Financiera", "A": [PROMEDIO_REAL_DE_ESTA_PERSPECTIVA], "fullMark": 100}},
            {{"subject": "Clientes", "A": [PROMEDIO_REAL_DE_ESTA_PERSPECTIVA], "fullMark": 100}},
            {{"subject": "Procesos", "A": [PROMEDIO_REAL_DE_ESTA_PERSPECTIVA], "fullMark": 100}},
            {{"subject": "Aprendizaje", "A": [PROMEDIO_REAL_DE_ESTA_PERSPECTIVA], "fullMark": 100}},
            {{"subject": "ESG/ODS", "A": [PROMEDIO_REAL_DE_ESTA_PERSPECTIVA], "fullMark": 100}}
        ],
        "stats": {{
            "total_objectives": {count},
            "avg_progress": {global_avg},
            "near_target": [CALCULAR_OBJETIVOS_VERDES]
        }}
    }}
    """

    # 4. ENVÍO A GOOGLE
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_elegido}:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = { "contents": [{"parts": [{"text": prompt_text}]}] }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result_json = response.json()
        
        if 'candidates' not in result_json: raise ValueError("Error API Google")
        
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
