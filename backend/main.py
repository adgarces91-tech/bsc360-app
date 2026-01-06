import time
import json
import requests
import re
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

# --- 1. FUNCIÓN BLINDADA PARA NÚMEROS (NUEVO) ---
# Convierte cualquier cosa (texto, null, vacío) en un número flotante seguro.
def safe_float(value):
    try:
        if value is None or value == "":
            return 0.0
        # Convertimos a string, quitamos símbolos de moneda y comas
        clean_val = str(value).replace("$", "").replace(",", "").strip()
        return float(clean_val)
    except:
        return 0.0

# --- 2. FUNCIÓN DE CIRUGÍA JSON ---
def extract_json_safely(text):
    try:
        clean = text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except:
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != 0:
                return json.loads(text[start:end])
        except:
            return None

@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    # PREPARACIÓN DE DATOS
    empresa = request.company_data.get('name', 'Empresa') if isinstance(request.company_data, dict) else "Empresa"
    
    # Manejo seguro de datos vacíos
    strategy = json.dumps(request.strategy_data or {}, ensure_ascii=False)
    market = json.dumps(request.market_data or {}, ensure_ascii=False)
    
    inflation = safe_float(request.market_data.get('inflation', 0)) if isinstance(request.market_data, dict) else 0
    interest = safe_float(request.market_data.get('interest_rate', 0)) if isinstance(request.market_data, dict) else 0

    # MOTOR MATEMÁTICO (Ahora usa safe_float)
    processed_objectives = []
    total_progress = 0
    count = 0

    for obj in request.objectives:
        try:
            # Usamos la función blindada para evitar errores de tipo
            current = safe_float(obj.get('current_value', 0))
            target = safe_float(obj.get('target_value', 1))
            
            # Cálculo de Avance (Evitamos división por cero)
            if target == 0:
                progress = 0.0
            else:
                progress = (current / target) * 100
            
            # Formateo de Presupuesto
            budget_val = safe_float(obj.get('financing', 0))
            budget_str = f"${budget_val:,.0f} USD" if budget_val > 0 else "No definido"

            # Lógica de Semáforo
            if progress < 70:
                emoji = "🔴"
                status_txt = "CRÍTICO (Atención Inmediata)"
            elif progress < 90:
                emoji = "🟡"
                status_txt = "ALERTA (Desviación Moderada)"
            else:
                emoji = "🟢"
                status_txt = "ÓPTIMO (En Meta)"

            # Inyectamos variables
            obj['calculated_progress'] = round(progress, 2)
            obj['budget_formatted'] = budget_str
            obj['status_emoji'] = emoji
            obj['status_text'] = status_txt

            processed_objectives.append(obj)
            total_progress += progress
            count += 1
        except Exception:
            # Si algo falla aquí, recuperamos el objetivo con valores por defecto
            obj['calculated_progress'] = 0
            obj['status_emoji'] = "⚪"
            obj['status_text'] = "Error Datos"
            processed_objectives.append(obj)

    global_avg = round(total_progress / count, 2) if count > 0 else 0
    objectives_json = json.dumps(processed_objectives, ensure_ascii=False)

    modelo_elegido = get_best_model(API_KEY)

    # PROMPT
    prompt_text = f"""
    Actúa como Auditor Estratégico Senior (Big Four).
    Genera un INFORME FINAL BSC 360° en formato JSON estricto.

    --- DATOS PRE-PROCESADOS ---
    EMPRESA: {empresa}
    SALUD GLOBAL: {global_avg}%
    OBJETIVOS: {objectives_json}
    INFLACIÓN: {inflation}%
    
    --- INSTRUCCIONES CRÍTICAS ---
    1. COPIA EXACTAMENTE los valores 'status_emoji', 'status_text', 'calculated_progress' y 'budget_formatted'.
    2. NO inventes números. Usa los provistos.

    --- PLANTILLA MARKDOWN ---
    
    # 📊 INFORME DE GESTIÓN - BSC 360°
    
    ## 🏦 Resumen Ejecutivo
    * **Empresa:** {empresa}
    * **Entorno:** Inflación {inflation}% | Tasa {interest}%
    * **Salud General:** {global_avg}% cumplimiento.
    * **Diagnóstico:** (Resumen ejecutivo de 3 líneas).

    ---
    # 🎯 DETALLE DE DESEMPEÑO
    (Iterar por cada objetivo):

    ### 📌 [objective]
    **KPI:** [kpi] | **Perspectiva:** [perspective]

    > **ESTADO:** [status_emoji] [status_text]
    > **CUMPLIMIENTO:** [calculated_progress]%

    **📉 LAS CIFRAS:**
    * **Meta:** [target_value] [unit]
    * **Real:** [current_value] [unit]
    * **Brecha:** (Diferencia simple)
    * **Presupuesto:** [budget_formatted]

    **🧠 ANÁLISIS & ESTRATEGIA:**
    * **🔍 Causa Raíz:** (Análisis cruzado con mercado).
    
    **🛡️ PLAN DE CONTINGENCIA (3 Escenarios):**
    1. **Conservador:** (Bajo costo).
    2. **Moderado:** (Equilibrado).
    3. **Agresivo:** (Alto impacto).

    **⚠️ Riesgo:** [Consecuencia].

    ---
    # 🚀 PLAN DE IMPLEMENTACIÓN
    * **Corto Plazo:** [Acciones]
    * **Mediano Plazo:** [Acciones]

    --- FIN PLANTILLA ---

    RESPONDE SOLO CON ESTE JSON:
    {{
        "strategic_analysis": "Markdown string...",
        "radar_chart": [
            {{"subject": "Financiera", "A": [PROMEDIO_REAL], "fullMark": 100}},
            {{"subject": "Clientes", "A": [PROMEDIO_REAL], "fullMark": 100}},
            {{"subject": "Procesos", "A": [PROMEDIO_REAL], "fullMark": 100}},
            {{"subject": "Aprendizaje", "A": [PROMEDIO_REAL], "fullMark": 100}},
            {{"subject": "ESG/ODS", "A": [PROMEDIO_REAL], "fullMark": 100}}
        ],
        "stats": {{
            "total_objectives": {count},
            "avg_progress": {global_avg},
            "near_target": [CALCULAR_VERDES]
        }}
    }}
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_elegido}:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = { "contents": [{"parts": [{"text": prompt_text}]}] }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result_json = response.json()
        
        if 'candidates' not in result_json: raise ValueError(f"Google API Error: {result_json}")
        
        texto_ia = result_json['candidates'][0]['content']['parts'][0]['text']
        final_data = extract_json_safely(texto_ia)
        
        if not final_data: raise ValueError("JSON no encontrado")
            
        return final_data

    except Exception as e:
        print(f"❌ Error Técnico: {str(e)}")
        # Mensaje amigable para el usuario en la presentación
        return {
            "strategic_analysis": f"### ⚠️ Aviso de Sistema\n\nNo pudimos procesar uno de los datos ingresados manualmente (posiblemente un texto en un campo numérico).\n\n**Sugerencia:** Revisa que los campos de 'Meta' y 'Valor Actual' sean números válidos e intenta nuevamente.",
            "radar_chart": [],
            "stats": {"total_objectives": 0, "avg_progress": 0, "near_target": 0}
        }
