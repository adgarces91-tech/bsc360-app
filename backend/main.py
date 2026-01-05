import time
import json
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Any, Optional
import os

# --- CONFIGURACIÓN ---
# Asegúrate de que tu variable de entorno en Render se llame API_KEY
API_KEY = os.getenv("API_KEY") 

app = FastAPI()

# Configuración de CORS para permitir peticiones desde el Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definición del modelo de datos que viene del Frontend
class AnalysisRequest(BaseModel):
    company_name: Optional[str] = None
    companyName: Optional[str] = None
    industry: Optional[str] = None
    market_data: Any = None
    objectives: List[Any] = []
    class Config:
        extra = "allow"

# Función auxiliar para elegir el mejor modelo de Gemini disponible
def get_best_model(api_key):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = requests.get(url)
        data = response.json()
        candidates = []
        if "models" in data:
            for m in data["models"]:
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    candidates.append(m["name"].replace("models/", ""))
        
        # Priorizamos modelos 'flash' por velocidad y capacidad de análisis
        for c in candidates:
            if "flash" in c: return c
        return candidates[0] if candidates else "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

# --- ENDPOINT PRINCIPAL DE ANÁLISIS ---
@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    # Extraer datos básicos
    empresa = request.company_name or request.companyName or "Empresa"
    
    # 1. Selección del Modelo
    modelo_elegido = get_best_model(API_KEY)

    # 2. SUPER-PROMPT ESTRATÉGICO (Basado en Estructura de Entradas/Salidas)
    # Este prompt obliga a la IA a generar cálculos matemáticos y estimaciones financieras
    prompt_text = """
    Actúa como Auditor Estratégico Senior (Nivel Big Four).
    Tu misión es cruzar los antecedentes internos de la empresa con el contexto de mercado proporcionado para generar un INFORME DE AUDITORÍA ESTRATÉGICA 360° riguroso.

    FUENTES DE INFORMACIÓN (Inputs):
    1. DATOS INTERNOS: KPIs, Metas y Valores Actuales (Provistos en el JSON adjunto).
    2. CONTEXTO DE MERCADO: Inflación, Tasas, Tendencias (Provistos en el JSON adjunto).

    TU TAREA (Outputs a Generar por cada Objetivo):
    1. 🧮 CÁLCULOS MATEMÁTICOS OBLIGATORIOS:
       - Brecha Absoluta = (Meta - Valor Actual)
       - Brecha Porcentual = ((Valor Actual - Meta) / Meta) * 100
       - Avance % = (Valor Actual / Meta) * 100
       - Semáforo: (🔴 Crítico < 70% | 🟡 En Observación 70-90% | 🟢 Bajo Riesgo > 90%)

    2. 🧠 INTELIGENCIA DE NEGOCIOS (Valor Agregado):
       - DIAGNÓSTICO CONTEXTUAL: Explica la brecha cruzando datos (Ej: "¿Cómo afecta la inflación alta a este costo?").
       - PLAN DE CHOQUE: Acciones inmediatas para corregir el rumbo.
       - RECURSOS ESTIMADOS: Estima presupuesto en USD y Tiempo para cerrar la brecha.
       - PROYECCIÓN DE RIESGO: "Sin acción, la brecha aumentará a X% en 3 meses".

    ESTRUCTURA OBLIGATORIA DEL INFORME (Markdown dentro del campo 'strategic_analysis'):
    
    # 📊 INFORME EJECUTIVO - BALANCED SCORECARD 360°
    **Resumen de Salud:**
    * Total Objetivos: [N]
    * Promedio Global: [X]%
    * 📉 Objetivo Más Crítico: [Nombre] (Brecha: [X]%)

    ---
    # 🎯 ANÁLISIS DETALLADO POR OBJETIVO
    (Repite esta estructura exacta para CADA objetivo):

    ## 📌 Objetivo: [Nombre]
    * **Perspectiva:** [Financiera/Clientes/Procesos/Aprendizaje/ESG]
    * **KPI:** [Nombre KPI]

    ### 📉 Diagnóstico de Brechas:
    * **Real vs Meta:** [Valor Actual] vs [Meta]
    * **Brecha:** [Valor Absoluto] ([Porcentaje]%)
    * **Avance:** [Porcentaje]%
    * **Estado:** [EMOJI SEMÁFORO]

    ### 🧠 Inteligencia Estratégica:
    * **Análisis Causa-Raíz:** [Análisis cruzado con datos de mercado]
    * **Plan de Choque:** [Acción Inmediata]
    * **Recursos Estimados:** Presupuesto estimado: $[Monto USD]. Tiempo: [Semanas/Meses].
    * **Riesgo de Inacción:** [Proyección a 3 meses]

    ---
    # 🗓️ PLAN DE IMPLEMENTACIÓN PRIORIZADO
    * **Acción Inmediata (30 días):** [Lista]
    * **Mediano Plazo (60-90 días):** [Lista]

    FORMATO DE RESPUESTA JSON (Estricto):
    {
        "strategic_analysis": "Todo el markdown generado arriba...",
        "radar_chart": [
            {"subject": "Financiera", "A": [PROMEDIO_REAL_CALCULADO], "fullMark": 100},
            {"subject": "Clientes", "A": [PROMEDIO_REAL_CALCULADO], "fullMark": 100},
            {"subject": "Procesos", "A": [PROMEDIO_REAL_CALCULADO], "fullMark": 100},
            {"subject": "Aprendizaje", "A": [PROMEDIO_REAL_CALCULADO], "fullMark": 100},
            {"subject": "ESG/ODS", "A": [PROMEDIO_REAL_CALCULADO], "fullMark": 100}
        ],
        "stats": {
            "total_objectives": [CONTEO_TOTAL],
            "avg_progress": [PROMEDIO_GLOBAL],
            "near_target": [CONTEO_OBJETIVOS_VERDES]
        }
    }
    """

    # 3. ENVÍO A GOOGLE GEMINI
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_elegido}:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    # Preparamos el mensaje combinando tus instrucciones y los datos reales
    # IMPORTANTE: Aquí se inyectan los datos reales del usuario
    payload = {
        "contents": [{
            "parts": [{
                "text": f"{prompt_text}\n\nDATOS REALES A ANALIZAR:\nEmpresa: {empresa}\nObjetivos: {json.dumps(request.objectives)}\nMercado: {json.dumps(request.market_data)}"
            }]
        }]
    }

    try:
        # Ejecutar la petición a Google
        response = requests.post(url, headers=headers, json=payload)
        result_json = response.json()
        
        # Extraemos el texto que generó la IA
        # Si la estructura de respuesta cambia, el try/except capturará el error
        if 'candidates' in result_json and result_json['candidates']:
            texto_ia = result_json['candidates'][0]['content']['parts'][0]['text']
        else:
            raise ValueError(f"Respuesta inesperada de Google: {result_json}")
        
        # Limpiamos el texto para que sea un JSON válido (quitamos ```json)
        clean_text = texto_ia.replace("```json", "").replace("```", "").strip()
        
        return json.loads(clean_text)
        
    except Exception as e:
        print(f"❌ Error técnico: {str(e)}")
        # Respuesta de emergencia en caso de fallo para que el Frontend no se rompa
        return {
            "strategic_analysis": f"### ⚠️ Error de Análisis\nOcurrió un error al procesar los datos con la IA.\n\n**Detalle técnico:** {str(e)}",
            "radar_chart": [],
            "stats": {"total_objectives": 0, "avg_progress": 0, "near_target": 0}
        }
