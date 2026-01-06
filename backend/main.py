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
        # Preferimos Flash para velocidad y manejo de JSON
        for c in candidates: 
            if "flash" in c: return c
        return candidates[0] if candidates else "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

# --- FUNCIÓN DE CIRUGÍA JSON (NUEVO) ---
# Esta función extrae el JSON válido aunque la IA escriba texto antes o después
def extract_json_safely(text):
    try:
        # Intento 1: Limpieza básica
        clean = text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except:
        try:
            # Intento 2: Buscar la primera llave { y la última }
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = text[start:end]
                return json.loads(json_str)
        except:
            return None

@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    # 1. PREPARACIÓN Y VALIDACIÓN DE DATOS
    empresa = request.company_data.get('name', 'Empresa') if isinstance(request.company_data, dict) else "Empresa"
    
    # Manejo seguro de datos vacíos
    strategy = json.dumps(request.strategy_data or {}, ensure_ascii=False)
    market = json.dumps(request.market_data or {}, ensure_ascii=False)
    
    inflation = request.market_data.get('inflation', 0) if isinstance(request.market_data, dict) else 0
    interest = request.market_data.get('interest_rate', 0) if isinstance(request.market_data, dict) else 0

    # 2. MOTOR MATEMÁTICO (Python)
    processed_objectives = []
    total_progress = 0
    count = 0

    for obj in request.objectives:
        try:
            current = float(obj.get('current_value', 0))
            target = float(obj.get('target_value', 1))
            progress = (current / target) * 100 if target != 0 else 0
            
            # Formateo de Presupuesto
            budget_val = obj.get('financing', 0)
            # Aseguramos que sea un número antes de formatear
            if isinstance(budget_val, (int, float)) and budget_val > 0:
                budget_str = f"${budget_val:,.0f} USD"
            else:
                budget_str = "No definido"

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

            # Inyectamos las variables pre-calculadas
            obj['calculated_progress'] = round(progress, 2)
            obj['budget_formatted'] = budget_str
            obj['status_emoji'] = emoji
            obj['status_text'] = status_txt

            processed_objectives.append(obj)
            total_progress += progress
            count += 1
        except Exception as e:
            # Si falla un objetivo, no rompemos todo, solo lo marcamos
            obj['calculated_progress'] = 0
            obj['status_emoji'] = "⚪"
            obj['status_text'] = "Error Datos"
            processed_objectives.append(obj)

    global_avg = round(total_progress / count, 2) if count > 0 else 0
    objectives_json = json.dumps(processed_objectives, ensure_ascii=False)

    modelo_elegido = get_best_model(API_KEY)

    # 3. PROMPT BLINDADO
    prompt_text = f"""
    Actúa como Auditor Estratégico Senior (Big Four).
    Genera un INFORME FINAL BSC 360° en formato JSON estricto.

    --- DATOS PRE-PROCESADOS ---
    EMPRESA: {empresa}
    SALUD GLOBAL: {global_avg}%
    OBJETIVOS: {objectives_json}
    INFLACIÓN: {inflation}%
    
    --- INSTRUCCIONES CRÍTICAS ---
    1. Debes COPIAR EXACTAMENTE los valores 'status_emoji' y 'status_text' del JSON de objetivos. ¡No los omitas!
    2. El campo 'budget_formatted' contiene el presupuesto en USD. Úsalo.
    3. NO inventes cálculos matemáticos, usa 'calculated_progress'.

    --- PLANTILLA MARKDOWN PARA 'strategic_analysis' ---
    
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

    # 4. ENVÍO Y MANEJO DE ERRORES
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_elegido}:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = { "contents": [{"parts": [{"text": prompt_text}]}] }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result_json = response.json()
        
        if 'candidates' not in result_json:
            raise ValueError(f"Google API Error: {result_json}")
        
        texto_ia = result_json['candidates'][0]['content']['parts'][0]['text']
        
        # --- EXTRACCIÓN SEGURA ---
        final_data = extract_json_safely(texto_ia)
        
        if not final_data:
            raise ValueError("No se pudo encontrar JSON válido en la respuesta de la IA")
            
        return final_data

    except Exception as e:
        print(f"❌ Error Técnico: {str(e)}")
        # Respuesta de emergencia legible
        return {
            "strategic_analysis": f"### ⚠️ Error Técnico Momentáneo\n\nLa IA no pudo estructurar la respuesta correctamente.\n\n**Causa:** {str(e)}\n\n**Solución:** Intenta reducir la cantidad de texto en 'Línea de Acción' o prueba nuevamente en 10 segundos.",
            "radar_chart": [],
            "stats": {"total_objectives": 0, "avg_progress": 0, "near_target": 0}
        }
