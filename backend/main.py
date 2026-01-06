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

# --- MODELO DE DATOS ROBUSTO ---
class AnalysisRequest(BaseModel):
    # Aceptamos cualquier estructura para evitar errores de validación
    company_data: Any = {}      
    strategy_data: Any = {}     
    market_data: Any = {}       
    competition_data: Any = {}  
    objectives: List[Any] = []
    
    # Compatibilidad con versiones anteriores
    company_name: Optional[str] = None

    class Config:
        extra = "allow"

def get_best_model(api_key):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = requests.get(url)
        candidates = [m["name"].replace("models/", "") for m in response.json().get("models", []) if "generateContent" in m.get("supportedGenerationMethods", [])]
        # Priorizamos Flash por velocidad y manejo de contexto largo
        for c in candidates: 
            if "flash" in c: return c
        return candidates[0] if candidates else "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    # 1. Preparación de Datos (Convertimos todo a texto seguro)
    empresa_nombre = request.company_data.get('name', 'Empresa') if isinstance(request.company_data, dict) else "Empresa"
    
    # Serializamos los objetos a JSON string para que la IA los lea como texto
    strategy_txt = json.dumps(request.strategy_data, ensure_ascii=False)
    market_txt = json.dumps(request.market_data, ensure_ascii=False)
    competition_txt = json.dumps(request.competition_data, ensure_ascii=False)
    objectives_txt = json.dumps(request.objectives, ensure_ascii=False)

    modelo_elegido = get_best_model(API_KEY)

    # 2. PROMPT CON F-STRING (A prueba de errores de sintaxis)
    # Nota: Usamos {{ }} dobles para las llaves que queremos que la IA vea en el JSON de ejemplo.
    # Las llaves simples { } son las variables de Python que inyectamos.
    prompt_text = f"""
    Actúa como Auditor Estratégico Senior (Big Four).
    Genera un INFORME DE AUDITORÍA ESTRATÉGICA 360° riguroso.

    --- CONTEXTO DE LA EMPRESA (INPUTS) ---
    1. EMPRESA: {empresa_nombre}
    2. ESTRATEGIA: {strategy_txt} (Misión, Visión, Prioridades)
    3. MERCADO: {market_txt} (Inflación, Tasas, Tendencias)
    4. COMPETENCIA: {competition_txt}
    5. OBJETIVOS KPI: {objectives_txt}

    --- INSTRUCCIONES DE SALIDA (OUTPUTS) ---
    
    TAREA 1: CÁLCULOS MATEMÁTICOS (Para los Gráficos)
    Analiza cada objetivo en 'objectives_txt'.
    Calcula el % de cumplimiento: (Valor Actual / Meta) * 100.
    Agrupa por perspectiva y calcula el PROMEDIO simple (0-100) para cada una.
    *IMPORTANTE: Debes devolver un número real en el JSON, no una fórmula.*

    TAREA 2: ANÁLISIS ESTRATÉGICO
    Cruza la 'Misión' con los 'Resultados'. Si la inflación ({request.market_data.get('inflation', 0)}%) es alta, menciónalo en el análisis financiero.

    --- FORMATO DE RESPUESTA JSON ESTRICTO ---
    Responde ÚNICAMENTE con este JSON (sin markdown extra):
    {{
        "strategic_analysis": "Aquí escribe el informe completo en formato Markdown (usa ### para títulos, ** para negritas). Incluye secciones de 'Diagnóstico', 'Plan de Acción' y 'Presupuesto Estimado'.",
        "radar_chart": [
            {{"subject": "Financiera", "A": 85, "fullMark": 100}},
            {{"subject": "Clientes", "A": 70, "fullMark": 100}},
            {{"subject": "Procesos", "A": 90, "fullMark": 100}},
            {{"subject": "Aprendizaje", "A": 60, "fullMark": 100}},
            {{"subject": "ESG/ODS", "A": 40, "fullMark": 100}}
        ],
        "stats": {{
            "total_objectives": 10,
            "avg_progress": 75.5,
            "near_target": 3
        }}
    }}
    """

    # 3. Envío a Google
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_elegido}:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }

    try:
        print("📡 Enviando petición a Gemini...")
        response = requests.post(url, headers=headers, json=payload)
        result_json = response.json()
        
        # Validación básica de respuesta
        if 'candidates' not in result_json:
            print(f"⚠️ Error API Google: {result_json}")
            raise ValueError("La IA rechazó la solicitud o hubo un error de cuota.")

        texto_ia = result_json['candidates'][0]['content']['parts'][0]['text']
        
        # Limpieza quirúrgica del JSON
        clean_text = texto_ia.replace("```json", "").replace("```", "").strip()
        
        return json.loads(clean_text)

    except Exception as e:
        print(f"❌ Error Crítico: {str(e)}")
        # Respuesta de emergencia para que el Frontend no se quede en blanco
        return {
            "strategic_analysis": f"### ⚠️ Error de Análisis\n\nNo pudimos procesar los datos complejos.\n**Error técnico:** {str(e)}\n\n*Intenta reducir la cantidad de texto en los objetivos.*",
            "radar_chart": [
                {"subject": "Error", "A": 0, "fullMark": 100},
                {"subject": "Reintentar", "A": 0, "fullMark": 100},
                {"subject": "Revisar Logs", "A": 0, "fullMark": 100},
                {"subject": "Conexión", "A": 0, "fullMark": 100},
                {"subject": "Soporte", "A": 0, "fullMark": 100}
            ],
            "stats": {"total_objectives": 0, "avg_progress": 0, "near_target": 0}
        }
