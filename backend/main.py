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
    return "gemini-1.5-flash"

def safe_float(value):
    try:
        if value is None or value == "": return 0.0
        return float(str(value).replace("$", "").replace(",", "").strip())
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
            if start != -1 and end != 0: return json.loads(text[start:end])
        except:
            return None

# --- PLAN B: GENERADOR DE RESPALDO (FORMATO EXTENDIDO) ---
def generate_fallback_report(empresa, global_avg, objectives, inflation):
    """Genera un informe detallado si la IA falla, imitando la estructura solicitada."""
    
    details = ""
    for i, obj in enumerate(objectives, 1):
        gap_abs = round(obj.get('gap_absolute', 0), 2)
        target = obj.get('target_value', 1)
        
        details += f"""
### 📊 Objetivo #{i}: {obj.get('objective', 'Objetivo Estratégico')}
**📍 Perspectiva:** {obj.get('perspective', 'General')}
**🎯 Línea de Acción:** {obj.get('action_line', 'No definida')}
**📈 KPI Principal:** {obj.get('kpi', 'KPI')}

**📊 Situación Actual:**
* **Valor Actual:** {obj.get('current_value', 0)} {obj.get('unit', '')}
* **Meta Establecida:** {obj.get('target_value', 0)} {obj.get('unit', '')}
* **Brecha Absoluta:** {gap_abs} {obj.get('unit', '')}
* **Avance:** {obj.get('calculated_progress', 0)}%
* **Estado:** {obj.get('status_emoji', '⚪')} {obj.get('status_text', 'No definido')}

**💡 RECOMENDACIONES ESTRATÉGICAS:**
* **Plan de Choque:** Implementar equipo de tarea ("Task Force") dedicado a cerrar la brecha de {gap_abs} {obj.get('unit', '')}.
* **Monitoreo Intensivo:** Revisión semanal del KPI {obj.get('kpi')} con la gerencia responsable.
* **Recursos Urgentes:** Asignación prioritaria del presupuesto disponible ({obj.get('budget_formatted', 'N/A')}).
* **Análisis de Causas:** Revisar impacto de factores externos (Inflación {inflation}%) en la ejecución.

**⏱️ Timeline de Implementación:**
* **Inmediato (15-30 días)** | **Prioridad:** { 'ALTA' if obj.get('calculated_progress', 0) < 70 else 'MEDIA' }

**💰 Recursos Necesarios:**
* **Presupuesto:** {obj.get('budget_formatted', 'N/A')}
* **Equipo:** Responsable directo ({obj.get('responsible', 'Gerencia')}) + soporte analítico.

**📋 Métricas de Seguimiento:**
* **KPI Principal:** {obj.get('kpi')}
* **Meta Intermedia:** Alcanzar el {target * 0.9} {obj.get('unit', '')} en el próximo trimestre.

**⚠️ Riesgos:** Riesgo de incumplimiento estratégico si no se toman acciones correctivas inmediatas.
**🔗 Interdependencias:** Este objetivo impacta directamente en la perspectiva {obj.get('perspective')}.

---
"""

    report = f"""
# INFORME EJECUTIVO - BALANCED SCORECARD 360° (MODO CONTINGENCIA)

## RESUMEN EJECUTIVO
El análisis del Balanced Scorecard 360° revela un desempeño general con oportunidades de mejora claras.
* **Total Objetivos Analizados:** {len(objectives)}
* **Promedio Global:** {global_avg}%
* **Contexto:** Datos generados en modo de respaldo por alta latencia en IA.

## RECOMENDACIONES POR OBJETIVO
{details}

## PLAN DE IMPLEMENTACIÓN PRIORIZADO
* **Acción Inmediata (30 días):** Enfocarse en los objetivos marcados como CRÍTICOS.
* **Mediano Plazo (60-90 días):** Consolidar los objetivos en estado ALERTA.
"""
    return report

@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    try:
        # 1. PROCESAMIENTO MATEMÁTICO
        empresa = request.company_data.get('name', 'Empresa') if isinstance(request.company_data, dict) else "Empresa"
        inflation = safe_float(request.market_data.get('inflation', 0)) if isinstance(request.market_data, dict) else 0
        
        processed_objectives = []
        total_progress = 0
        count = 0
        radar_data = {"Financiera": [], "Clientes": [], "Procesos": [], "Aprendizaje": [], "ESG/ODS": []}

        for obj in request.objectives:
            current = safe_float(obj.get('current_value', 0))
            target = safe_float(obj.get('target_value', 1))
            budget_val = safe_float(obj.get('financing', 0))

            progress = (current / target) * 100 if target != 0 else 0
            gap_abs = target - current # Cálculo de la brecha absoluta

            # Semáforos
            if progress < 70: emoji, txt = "🔴", "CRÍTICO"
            elif progress < 90: emoji, txt = "🟡", "ALERTA"
            else: emoji, txt = "🟢", "ÓPTIMO"

            obj.update({
                'calculated_progress': round(progress, 2),
                'gap_absolute': round(gap_abs, 2),
                'budget_formatted': f"${budget_val:,.0f} USD" if budget_val > 0 else "No definido",
                'status_emoji': emoji,
                'status_text': txt
            })
            
            processed_objectives.append(obj)
            total_progress += progress
            count += 1
            
            persp = obj.get('perspective', 'Otros')
            if persp in radar_data: radar_data[persp].append(progress)
            elif "Procesos" in persp: radar_data["Procesos"].append(progress)

        global_avg = round(total_progress / count, 2) if count > 0 else 0
        
        final_radar = []
        for subject, values in radar_data.items():
            avg = sum(values) / len(values) if values else 0
            final_radar.append({"subject": subject, "A": round(avg, 1), "fullMark": 100})

        # 2. INTENTO CON IA (PLAN A - FORMATO LUJO)
        try:
            objectives_json = json.dumps(processed_objectives, ensure_ascii=False)
            strategy = json.dumps(request.strategy_data or {}, ensure_ascii=False)
            
            prompt_text = f"""
            Actúa como Auditor Estratégico Senior.
            Tu tarea es generar un informe IDÉNTICO a la estructura solicitada, usando los datos provistos.
            
            DATOS CLAVE:
            Empresa: {empresa}
            Inflación: {inflation}%
            Objetivos: {objectives_json}

            --- ESTRUCTURA OBLIGATORIA (MARKDOWN) ---
            Genera el contenido de 'strategic_analysis' siguiendo EXACTAMENTE este formato para CADA OBJETIVO:

            # INFORME EJECUTIVO - BALANCED SCORECARD 360°
            
            ## RESUMEN EJECUTIVO
            El análisis del Balanced Scorecard 360° revela... (Resumen de 3 líneas).
            * **Total Objetivos Analizados:** {count}
            * **Cumplimiento Promedio:** {global_avg}%
            * **Objetivo Crítico:** (Menciona el peor)
            * **Mejor Desempeño:** (Menciona el mejor)

            ## RECOMENDACIONES POR OBJETIVO

            ### 📊 Objetivo: [Nombre Objetivo]
            **📍 Perspectiva:** [Perspectiva]
            **🎯 Línea de Acción:** [action_line]
            **📈 KPI Principal:** [KPI]

            **📊 Situación Actual:**
            * **Valor Actual:** [current_value] [unit]
            * **Meta Establecida:** [target_value] [unit]
            * **Brecha Absoluta:** [gap_absolute] (Calculado: Meta - Real)
            * **Avance:** [calculated_progress]%
            * **Estado:** [status_emoji] [status_text]

            **💡 RECOMENDACIONES ESTRATÉGICAS:**
            * **Plan de Choque:** (Acción agresiva inmediata).
            * **Monitoreo Intensivo:** (Qué revisar diariamente).
            * **Recursos Urgentes:** (Usa el presupuesto: [budget_formatted]).
            * **Hitos Semanales:** (Define un micro-objetivo).
            * **Análisis de Causas:** (Por qué existe la brecha, considerando inflación {inflation}%).

            **⏱️ Timeline de Implementación:**
            * **Inmediato (15-30 días)**
            * **Prioridad:** ALTA/MEDIA/BAJA

            **💰 Recursos Necesarios:**
            * **Presupuesto:** [budget_formatted]
            * **Equipo:** [responsible] y soporte externo.

            **📋 Métricas de Seguimiento:**
            * **KPI Principal:** [KPI] (Seguimiento [frequency])
            * **Meta Intermedia:** (Un valor entre el actual y la meta).

            **⚠️ Riesgos y Consideraciones:**
            (Riesgo de no actuar).

            **🔗 Interdependencias:**
            (Cómo afecta a otras áreas).

            ---
            (Repetir para todos los objetivos)

            ## PLAN DE IMPLEMENTACIÓN PRIORIZADO
            * **Acción Inmediata (0-30 días):** Lista de acciones críticas.
            * **Mediano Plazo (30-90 días):** Lista de acciones estructurales.

            --- FIN ESTRUCTURA ---

            RESPONDE SOLO JSON:
            {{
                "strategic_analysis": "MARKDOWN...",
                "radar_chart": [], 
                "stats": {{}}
            }}
            """
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            response = requests.post(url, headers={"Content-Type": "application/json"}, json={"contents": [{"parts": [{"text": prompt_text}]}]}, timeout=25) # Timeout extendido para informes largos
            
            if response.status_code == 200:
                json_res = extract_json_safely(response.json()['candidates'][0]['content']['parts'][0]['text'])
                if json_res:
                    json_res['radar_chart'] = final_radar
                    json_res['stats'] = {"total_objectives": count, "avg_progress": global_avg, "near_target": 0}
                    return json_res
                    
        except Exception as e:
            print(f"⚠️ Falló IA: {str(e)}")

        # 3. PLAN B (Formato extendido)
        return {
            "strategic_analysis": generate_fallback_report(empresa, global_avg, processed_objectives, inflation),
            "radar_chart": final_radar,
            "stats": {"total_objectives": count, "avg_progress": global_avg, "near_target": 0}
        }

    except Exception as e:
        return {
            "strategic_analysis": f"# Error Crítico\n{str(e)}",
            "radar_chart": [],
            "stats": {"total_objectives": 0, "avg_progress": 0, "near_target": 0}
        }
