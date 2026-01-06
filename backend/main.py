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
    # Intentamos usar Flash que es más rápido y estable
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

# --- PLAN B: GENERADOR DE RESPALDO (Python puro) ---
def generate_fallback_report(empresa, global_avg, objectives, inflation):
    """Genera un informe válido si la IA falla."""
    
    details = ""
    for obj in objectives:
        details += f"""
### 📌 {obj.get('objective', 'Objetivo Estratégico')}
**KPI:** {obj.get('kpi', 'KPI')} | **Perspectiva:** {obj.get('perspective', 'General')}

> **ESTADO:** {obj.get('status_emoji', '⚪')} {obj.get('status_text', 'No definido')}
> **CUMPLIMIENTO:** {obj.get('calculated_progress', 0)}%

**📉 LAS CIFRAS:**
* **Meta:** {obj.get('target_value', 0)} {obj.get('unit', '')}
* **Real:** {obj.get('current_value', 0)} {obj.get('unit', '')}
* **Presupuesto:** {obj.get('budget_formatted', 'N/A')}

**🧠 ANÁLISIS TÉCNICO:**
* **Diagnóstico:** El desempeño actual muestra una brecha del {round(100 - obj.get('calculated_progress', 0), 1)}% respecto a la meta.
* **Recomendación:** Se sugiere revisar la ejecución presupuestaria y reforzar las acciones correctivas inmediatas.

**🛡️ PLAN DE CONTINGENCIA SUGERIDO:**
* **Opción A (Eficiencia):** Revisión de procesos para optimizar recursos actuales.
* **Opción B (Inversión):** Evaluar inyección de capital adicional si el ROI lo justifica.
* **Opción C (Redefinición):** Ajustar la meta si las condiciones de mercado (Inflación {inflation}%) persisten.

---
"""

    report = f"""
# 📊 INFORME DE AUDITORÍA (MODO CONTINGENCIA)

## 🏦 Resumen Ejecutivo
* **Empresa:** {empresa}
* **Salud Global:** {global_avg}% de cumplimiento.
* **Contexto:** Inflación {inflation}%.
* **Diagnóstico:** La organización presenta un desempeño global del {global_avg}%. Se han detectado desviaciones que requieren gestión priorizada en los objetivos marcados como CRÍTICOS o ALERTA.

---
# 🎯 DETALLE DE DESEMPEÑO
{details}

# 🚀 PRÓXIMOS PASOS
* Priorizar los objetivos con cumplimiento inferior al 70%.
* Revisar la asignación de presupuestos en la próxima reunión de comité.
"""
    return report

@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    # 1. PROCESAMIENTO MATEMÁTICO (Nunca falla)
    try:
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
            
            # Semáforos
            if progress < 70: emoji, txt = "🔴", "CRÍTICO (Atención Inmediata)"
            elif progress < 90: emoji, txt = "🟡", "ALERTA (Desviación Moderada)"
            else: emoji, txt = "🟢", "ÓPTIMO (En Meta)"

            obj.update({
                'calculated_progress': round(progress, 2),
                'budget_formatted': f"${budget_val:,.0f} USD" if budget_val > 0 else "No definido",
                'status_emoji': emoji,
                'status_text': txt
            })
            
            processed_objectives.append(obj)
            total_progress += progress
            count += 1
            
            # Datos para Radar (agrupación simple)
            persp = obj.get('perspective', 'Otros')
            if persp in radar_data: radar_data[persp].append(progress)
            elif "Procesos" in persp: radar_data["Procesos"].append(progress) # Catch 'Procesos Internos'

        global_avg = round(total_progress / count, 2) if count > 0 else 0
        
        # Preparamos datos del Radar
        final_radar = []
        for subject, values in radar_data.items():
            avg = sum(values) / len(values) if values else 0
            final_radar.append({"subject": subject, "A": round(avg, 1), "fullMark": 100})

        # 2. INTENTO CON IA (PLAN A)
        try:
            objectives_json = json.dumps(processed_objectives, ensure_ascii=False)
            strategy_json = json.dumps(request.strategy_data or {}, ensure_ascii=False)
            
            prompt_text = f"""
            Actúa como Auditor Estratégico. Genera un JSON válido.
            DATOS: Empresa {empresa}, Salud {global_avg}%, Objetivos {objectives_json}.
            INSTRUCCIONES:
            1. Usa 'calculated_progress', 'status_emoji', 'budget_formatted' TAL CUAL.
            2. Genera 'Plan de Contingencia' con 3 opciones para cada objetivo.
            RESPONDE SOLO JSON:
            {{
                "strategic_analysis": "MARKDOWN COMPLETO...",
                "radar_chart": [], 
                "stats": {{}}
            }}
            """
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            response = requests.post(url, headers={"Content-Type": "application/json"}, json={"contents": [{"parts": [{"text": prompt_text}]}]}, timeout=15)
            
            if response.status_code == 200:
                json_res = extract_json_safely(response.json()['candidates'][0]['content']['parts'][0]['text'])
                if json_res:
                    # Inyectamos nuestros datos matemáticos seguros al JSON de la IA por si acaso
                    json_res['radar_chart'] = final_radar
                    json_res['stats'] = {"total_objectives": count, "avg_progress": global_avg, "near_target": 0}
                    return json_res
                    
        except Exception as e:
            print(f"⚠️ Falló la IA ({str(e)}), activando PLAN B...")

        # 3. PLAN B: GENERACIÓN MANUAL (Si la IA falla, esto se ejecuta)
        # Esto garantiza que SIEMPRE tengas un informe, pase lo que pase.
        fallback_report = generate_fallback_report(empresa, global_avg, processed_objectives, inflation)
        
        return {
            "strategic_analysis": fallback_report,
            "radar_chart": final_radar,
            "stats": {
                "total_objectives": count,
                "avg_progress": global_avg,
                "near_target": len([o for o in processed_objectives if o['calculated_progress'] >= 70])
            }
        }

    except Exception as e:
        # PLAN C: Si falla hasta Python (imposible), devolvemos error plano
        return {
            "strategic_analysis": f"# Error Crítico\n{str(e)}",
            "radar_chart": [],
            "stats": {"total_objectives": 0, "avg_progress": 0, "near_target": 0}
        }
