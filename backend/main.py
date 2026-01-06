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

# --- PLAN B: GENERADOR DE RESPALDO (FORMATO FINAL TESIS) ---
def generate_fallback_report(empresa, global_avg, objectives, inflation):
    """Genera el informe con 3 opciones de contingencia si falla la IA."""
    
    details = ""
    for i, obj in enumerate(objectives, 1):
        gap_abs = round(obj.get('gap_absolute', 0), 2)
        target = obj.get('target_value', 1)
        progress = obj.get('calculated_progress', 0)
        
        # Lógica simple para prioridades en modo respaldo
        risk_level = "ALTO" if progress < 70 else "MEDIO" if progress < 90 else "BAJO"
        
        details += f"""
### 📊 Objetivo #{i}: {obj.get('objective', 'Objetivo Estratégico')}
**📍 Perspectiva:** {obj.get('perspective', 'General')}
**🎯 Línea de Acción:** {obj.get('action_line', 'No definida')}
**📈 KPI Principal:** {obj.get('kpi', 'KPI')}

**📊 Situación Actual:**
* **Valor Actual:** {obj.get('current_value', 0)} {obj.get('unit', '')}
* **Meta Establecida:** {obj.get('target_value', 0)} {obj.get('unit', '')}
* **Brecha Absoluta:** {gap_abs} {obj.get('unit', '')}
* **Avance:** {progress}%
* **Estado:** {obj.get('status_emoji', '⚪')} {obj.get('status_text', 'No definido')}

**🛡️ PLAN DE CONTINGENCIA (3 ESCENARIOS):**
* **Opción A (Conservadora - Eficiencia):** Revisión inmediata de procesos para optimizar recursos actuales sin gasto adicional.
* **Opción B (Moderada - Reasignación):** Reasignar presupuesto de áreas con superávit para cubrir la brecha de {gap_abs}.
* **Opción C (Agresiva - Inversión):** Ejecutar el presupuesto total ({obj.get('budget_formatted', 'N/A')}) para contratar servicios externos o tecnología.

**⚠️ ANÁLISIS DETALLADO DE RIESGOS:**
* **Riesgo Principal:** No alcanzar la meta anual debido a factores internos o inflación ({inflation}%).
* **Impacto Operativo:** {risk_level}. Afecta directamente la perspectiva {obj.get('perspective')}.
* **Probabilidad:** { 'ALTA' if progress < 70 else 'MEDIA' }.

**⏱️ Timeline de Implementación:**
* **Inmediato (15-30 días)** | **Prioridad:** { 'ALTA' if progress < 70 else 'MEDIA' }

**💰 Recursos Necesarios:**
* **Presupuesto Asignado:** {obj.get('budget_formatted', 'N/A')}
* **Responsable:** {obj.get('responsible', 'Gerencia')}

---
"""

    report = f"""
# INFORME EJECUTIVO - BALANCED SCORECARD 360° (MODO CONTINGENCIA)

## RESUMEN EJECUTIVO
El análisis estratégico revela un desempeño general del {global_avg}%. Este reporte ha sido generado automáticamente por el motor de contingencia debido a latencia en el servicio cognitivo.

## RECOMENDACIONES POR OBJETIVO
{details}

## PLAN DE IMPLEMENTACIÓN
* **Corto Plazo:** Activar Opción A (Conservadora) en todos los objetivos CRÍTICOS.
* **Mediano Plazo:** Evaluar Opción B o C según disponibilidad de caja.
"""
    return report

@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    try:
        # 1. PROCESAMIENTO MATEMÁTICO (Nunca falla)
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
            gap_abs = target - current

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

        # 2. INTENTO CON IA (PLAN A - FORMATO LUJO CON 3 OPCIONES)
        try:
            objectives_json = json.dumps(processed_objectives, ensure_ascii=False)
            strategy = json.dumps(request.strategy_data or {}, ensure_ascii=False)
            
            prompt_text = f"""
            Actúa como Auditor Estratégico Senior.
            Genera un informe detallado usando estos datos.
            
            DATOS:
            Empresa: {empresa} | Inflación: {inflation}%
            Objetivos: {objectives_json}

            --- ESTRUCTURA OBLIGATORIA (MARKDOWN) ---
            Genera 'strategic_analysis' siguiendo EXACTAMENTE este formato para CADA OBJETIVO:

            # INFORME EJECUTIVO - BALANCED SCORECARD 360°
            
            ## RESUMEN EJECUTIVO
            (Resumen de 3 líneas sobre la salud de la empresa).
            * **Total Objetivos:** {count}
            * **Cumplimiento Promedio:** {global_avg}%
            * **Objetivo Crítico:** (Menciona el peor)
            * **Mejor Desempeño:** (Menciona el mejor)

            ## RECOMENDACIONES POR OBJETIVO

            ### 📊 Objetivo: [Nombre Objetivo]
            **📍 Perspectiva:** [Perspectiva] | **KPI:** [KPI]
            **🎯 Línea de Acción:** [action_line]

            **📊 Situación Actual:**
            * **Valor Actual:** [current_value] [unit]
            * **Meta:** [target_value] [unit]
            * **Brecha:** [gap_absolute] [unit]
            * **Avance:** [calculated_progress]%
            * **Estado:** [status_emoji] [status_text]

            **🛡️ PLAN DE CONTINGENCIA (3 OPCIONES):**
            * **Opción A (Conservadora):** (Acción de eficiencia interna / bajo costo).
            * **Opción B (Moderada):** (Reasignación de recursos / gestión táctica).
            * **Opción C (Agresiva):** (Inversión fuerte usando el presupuesto de [budget_formatted] / transformación).

            **⚠️ ANÁLISIS DETALLADO DE RIESGOS:**
            * **Riesgo Principal:** (Qué pasa si fallamos).
            * **Impacto:** ALTO/MEDIO/BAJO.
            * **Probabilidad:** ALTA/MEDIA/BAJA.
            * **Mitigación:** (Acción preventiva rápida).

            **⏱️ Timeline & Recursos:**
            * **Plazo:** Inmediato (15-30 días).
            * **Presupuesto:** [budget_formatted].
            * **Equipo:** [responsible].

            **🔗 Interdependencias:**
            (Impacto cruzado con otros objetivos).

            ---
            (Repetir para todos)

            ## PLAN DE IMPLEMENTACIÓN PRIORIZADO
            * **Semana 1-4 (Urgente):** Acciones para objetivos CRÍTICOS.
            * **Mes 2-3 (Estructural):** Acciones para objetivos en ALERTA.

            --- FIN ESTRUCTURA ---

            RESPONDE SOLO JSON.
            """
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            response = requests.post(url, headers={"Content-Type": "application/json"}, json={"contents": [{"parts": [{"text": prompt_text}]}]}, timeout=25)
            
            if response.status_code == 200:
                json_res = extract_json_safely(response.json()['candidates'][0]['content']['parts'][0]['text'])
                if json_res:
                    json_res['radar_chart'] = final_radar
                    json_res['stats'] = {"total_objectives": count, "avg_progress": global_avg, "near_target": 0}
                    return json_res

        except Exception as e:
            print(f"⚠️ Falló IA: {str(e)}")

        # 3. PLAN B (Formato extendido con 3 opciones)
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
