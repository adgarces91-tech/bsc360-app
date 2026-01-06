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

# --- FUNCIÓN DE LIMPIEZA EXTREMA ---
def clean_number(value):
    """Intenta convertir lo que sea en un número. Si falla, devuelve 0."""
    try:
        if not value: return 0.0
        # Convertir a string, quitar $ y comas, dejar puntos si hay decimales
        s = str(value).replace("$", "").replace(",", "")
        return float(s)
    except:
        return 0.0

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
    try: # TRY GIGANTE PARA ATRAPAR TODO
        
        # 1. DATOS BÁSICOS
        empresa = "Empresa"
        if isinstance(request.company_data, dict):
            empresa = request.company_data.get('name', 'Empresa')
        elif request.company_name:
            empresa = request.company_name

        # Manejo de diccionarios vacíos
        market_data = request.market_data if isinstance(request.market_data, dict) else {}
        
        inflation = clean_number(market_data.get('inflation', 0))
        interest = clean_number(market_data.get('interest_rate', 0))

        # 2. PROCESAMIENTO DE OBJETIVOS (Indestructible)
        processed_objectives = []
        total_progress = 0
        count = 0

        for obj in request.objectives:
            # Valores por defecto seguros
            kpi_name = obj.get('kpi', 'KPI')
            
            # Limpieza numérica agresiva
            current = clean_number(obj.get('current_value', 0))
            target = clean_number(obj.get('target_value', 1))
            budget_raw = clean_number(obj.get('financing', 0))

            # Cálculo Seguro
            progress = 0.0
            if target != 0:
                progress = (current / target) * 100
            
            # Formateo
            budget_str = f"${budget_raw:,.0f} USD" if budget_raw > 0 else "No definido"

            # Semáforos
            if progress < 70:
                emoji, txt = "🔴", "CRÍTICO"
            elif progress < 90:
                emoji, txt = "🟡", "ALERTA"
            else:
                emoji, txt = "🟢", "ÓPTIMO"

            # Guardamos datos limpios
            obj['calculated_progress'] = round(progress, 2)
            obj['budget_formatted'] = budget_str
            obj['status_emoji'] = emoji
            obj['status_text'] = txt
            
            processed_objectives.append(obj)
            total_progress += progress
            count += 1

        global_avg = round(total_progress / count, 2) if count > 0 else 0
        
        # Preparamos textos JSON
        obj_json = json.dumps(processed_objectives, ensure_ascii=False)
        strategy_json = json.dumps(request.strategy_data or {}, ensure_ascii=False)
        market_json = json.dumps(market_data, ensure_ascii=False)

        modelo_elegido = get_best_model(API_KEY)

        # 3. PROMPT
        prompt_text = f"""
        Actúa como Auditor Estratégico Senior.
        Genera un JSON con el análisis BSC.
        
        EMPRESA: {empresa}
        SALUD: {global_avg}%
        OBJETIVOS: {obj_json}
        
        INSTRUCCIONES:
        1. Copia los valores 'calculated_progress', 'status_emoji', 'budget_formatted'.
        2. Genera 'Plan de Contingencia' con 3 opciones.
        
        RESPONDE SOLO CON ESTE JSON:
        {{
            "strategic_analysis": "MARKDOWN DEL INFORME AQUÍ...",
            "radar_chart": [
                {{"subject": "Financiera", "A": {global_avg}, "fullMark": 100}},
                {{"subject": "Clientes", "A": {global_avg}, "fullMark": 100}},
                {{"subject": "Procesos", "A": {global_avg}, "fullMark": 100}},
                {{"subject": "Aprendizaje", "A": {global_avg}, "fullMark": 100}},
                {{"subject": "ESG/ODS", "A": {global_avg}, "fullMark": 100}}
            ],
            "stats": {{
                "total_objectives": {count},
                "avg_progress": {global_avg},
                "near_target": 2
            }}
        }}
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_elegido}:generateContent?key={API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = { "contents": [{"parts": [{"text": prompt_text}]}] }

        print("📡 Enviando a Google...")
        response = requests.post(url, headers=headers, json=payload)
        result_json = response.json()
        
        if 'candidates' not in result_json:
            # ERROR DE GOOGLE DETECTADO
            error_msg = result_json.get('error', {}).get('message', 'Error desconocido de Google')
            raise ValueError(f"Google API Error: {error_msg}")

        texto_ia = result_json['candidates'][0]['content']['parts'][0]['text']
        final_data = extract_json_safely(texto_ia)
        
        if not final_data:
            raise ValueError("La IA no devolvió un JSON válido.")

        return final_data

    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {str(e)}")
        # AQUÍ ESTÁ LA CLAVE: Devolvemos el error en el informe para leerlo
        return {
            "strategic_analysis": f"""
# ⚠️ REPORTE DE DIAGNÓSTICO
Ocurrió un error técnico. Muestra esto al desarrollador:

**ERROR:** `{str(e)}`

**SOLUCIÓN RÁPIDA:**
1. Recarga la página (Ctrl + F5).
2. Usa el botón 'Cargar Datos Copec'.
3. No dejes campos vacíos.
            """,
            "radar_chart": [],
            "stats": {"total_objectives": 0, "avg_progress": 0, "near_target": 0}
        }
