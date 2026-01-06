// @ts-nocheck
import { useState, useEffect } from 'react';

// DATOS REALES DE COPEC (Corregido: ROIC -> ROI)
const DEMO_FULL_COPEC = {
    company_data: {
        name: 'Empresas Copec S.A.',
        industry: 'Energía y Recursos Naturales',
        employees: '37800',
        description: 'Holding industrial líder en energía, forestal y combustibles.'
    },
    strategy_data: {
        mission: 'Entregar soluciones energéticas sostenibles y productos de alta calidad.',
        vision: 'Ser líderes en la transición energética y movilidad del futuro.',
        values: 'Sostenibilidad, Innovación, Excelencia, Compromiso.',
        priorities: 'Descarbonización, Digitalización de clientes, Eficiencia Operacional.',
        markets: 'Chile (70%), Colombia (10%), Perú (20%)',
        products: 'Combustibles, Tiendas de Conveniencia, Lubricantes, Energía Renovable',
        advantage: 'Red de distribución nacional y marca líder',
        challenges: 'Volatilidad precios petróleo, competencia digital'
    },
    market_data: {
        inflation: 3.8,
        interest_rate: 6.25,
        sector_growth: 4.2,
        confidence_index: 68,
        trends: 'Electromovilidad, Hidrógeno Verde, Automatización logística.',
        energy_price: 5.5,
        labor_cost: 5.2
    },
    competition_data: {
        competitors: 'Enex (Shell), Esmax (Petrobras), CMPC.',
        position: 'Líder de Mercado (Market Leader)'
    },
    // OBJETIVOS: CAMBIO DE ROIC A ROI
    bsc_objectives: [
        { 
            perspective: "Financiera", 
            objective: "Maximizar ROI en operaciones retail", // <--- CAMBIO AQUÍ
            kpi: "ROI", // <--- CAMBIO AQUÍ
            current_value: 14.5, target_value: 18.0, unit: "%",
            action_line: "Optimización de mix de productos y eficiencia operacional",
            data_source: "ERP SAP Consolidado Financiero",
            formula: "(Beneficio Neto / Inversión) x 100", // <--- FÓRMULA AJUSTADA A ROI
            frequency: "Trimestral",
            baseline: 12.8,
            responsible: "Gerente General Retail",
            financing: "Presupuesto CAPEX"
        },
        { 
            perspective: "Clientes", 
            objective: "Aumentar frecuencia de visita", 
            kpi: "Frecuencia Visita", 
            current_value: 2.3, target_value: 2.8, unit: "visitas/mes",
            action_line: "App móvil con beneficios y gamificación",
            data_source: "App Copec Puntos + Analytics",
            formula: "Total visitas / Clientes únicos",
            frequency: "Mensual",
            baseline: 2.3,
            responsible: "Gerente Marketing Digital",
            financing: "Presupuesto Digital"
        },
        { 
            perspective: "Procesos", 
            objective: "Optimizar gestión de inventario", 
            kpi: "Inventory Turnover", 
            current_value: 8.5, target_value: 12.0, unit: "veces/año",
            action_line: "Sistema predictivo de demanda con IA",
            data_source: "WMS + Sistema Inventarios",
            formula: "Costo Ventas / Inventario Promedio",
            frequency: "Mensual",
            baseline: 7.2,
            responsible: "Gerente Supply Chain",
            financing: "Inversión Tecnología"
        },
        { 
            perspective: "Aprendizaje", 
            objective: "Desarrollar liderazgo de tienda", 
            kpi: "% Gerentes Certificados", 
            current_value: 35.0, target_value: 85.0, unit: "%",
            action_line: "Academia de gerentes y mentoring",
            data_source: "LMS Sistema Capacitación",
            formula: "(Certificados / Total) x 100",
            frequency: "Trimestral",
            baseline: 28.0,
            responsible: "Gerente Desarrollo Org.",
            financing: "Presupuesto Capacitación"
        },
        { 
            perspective: "ESG/ODS", 
            objective: "Transición a energías renovables", 
            kpi: "% Energía Renovable", 
            current_value: 12.0, target_value: 45.0, unit: "%",
            action_line: "Paneles solares en estaciones",
            data_source: "Sistema Monitoreo Energético",
            formula: "(kWh renovable / Total) x 100",
            frequency: "Mensual",
            baseline: 8.0,
            responsible: "Gerente Sustentabilidad",
            financing: "Inversión CAPEX Verde"
        }
    ]
};

interface CompanyContextFormProps {
    data: any;
    onUpdate: (data: any) => void;
    onNext: () => void;
}

const CompanyContextForm = ({ data, onUpdate, onNext }: CompanyContextFormProps) => {
    const [localData, setLocalData] = useState({
        company_data: data.company_data || {},
        strategy_data: data.strategy_data || {},
        market_data: data.market_data || {},
        competition_data: data.competition_data || {},
        bsc_objectives: data.bsc_objectives || []
    });

    useEffect(() => { onUpdate(localData); }, [localData]);

    const handleChange = (section: string, field: string, value: any) => {
        setLocalData(prev => ({
            ...prev,
            [section]: { ...prev[section], [field]: value }
        }));
    };

    const handleAutoFill = () => {
        setLocalData(DEMO_FULL_COPEC);
        onUpdate(DEMO_FULL_COPEC);
    };

    return (
        <div className="space-y-8 animate-in fade-in duration-700 pb-10">
            {/* HEADER */}
            <div className="flex justify-between items-center bg-indigo-50 p-4 rounded-xl border border-indigo-100">
                <div>
                    <h2 className="text-2xl font-black text-indigo-900">1. Contexto Empresarial (Full Data)</h2>
                    <p className="text-sm text-indigo-600">Datos extraídos de Reportes Corporativos y de Mercado.</p>
                </div>
                {/* BOTÓN CON TEXTO CORREGIDO */}
                <button onClick={handleAutoFill} className="bg-indigo-600 text-white px-5 py-2 rounded-lg font-bold hover:bg-indigo-700 transition shadow-lg flex items-center gap-2">
                    ⚡ Cargar Datos Copec
                </button>
            </div>

            {/* SECCIÓN 1: ORGANIZACIÓN */}
            <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4 border-b pb-2">01. Organización</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="md:col-span-2">
                        <label className="label">Nombre</label>
                        <input className="input-field" value={localData.company_data.name} onChange={e => handleChange('company_data', 'name', e.target.value)} />
                    </div>
                    <div>
                        <label className="label">Empleados</label>
                        <input className="input-field" value={localData.company_data.employees} onChange={e => handleChange('company_data', 'employees', e.target.value)} />
                    </div>
                    <div className="md:col-span-3">
                        <label className="label">Industria / Rubro</label>
                        <input className="input-field" value={localData.company_data.industry} onChange={e => handleChange('company_data', 'industry', e.target.value)} />
                    </div>
                </div>
            </section>

            {/* SECCIÓN 2: ESTRATEGIA */}
            <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 border-l-4 border-l-blue-500">
                <h3 className="text-sm font-bold text-blue-500 uppercase tracking-wider mb-4 border-b pb-2">02. Estrategia & Posicionamiento</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label className="label">Misión</label>
                        <textarea className="input-area" rows={2} value={localData.strategy_data.mission} onChange={e => handleChange('strategy_data', 'mission', e.target.value)} />
                    </div>
                    <div>
                        <label className="label">Visión</label>
                        <textarea className="input-area" rows={2} value={localData.strategy_data.vision} onChange={e => handleChange('strategy_data', 'vision', e.target.value)} />
                    </div>
                    <div>
                        <label className="label">Mercados Principales</label>
                        <input className="input-field" value={localData.strategy_data.markets} onChange={e => handleChange('strategy_data', 'markets', e.target.value)} />
                    </div>
                    <div>
                        <label className="label">Ventaja Competitiva</label>
                        <input className="input-field" value={localData.strategy_data.advantage} onChange={e => handleChange('strategy_data', 'advantage', e.target.value)} />
                    </div>
                    <div className="md:col-span-2">
                        <label className="label">Desafíos Estratégicos</label>
                        <input className="input-field" value={localData.strategy_data.challenges} onChange={e => handleChange('strategy_data', 'challenges', e.target.value)} />
                    </div>
                </div>
            </section>

            {/* SECCIÓN 3: MERCADO */}
            <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 border-l-4 border-l-green-500">
                <h3 className="text-sm font-bold text-green-600 uppercase tracking-wider mb-4 border-b pb-2">03. Entorno de Mercado (Inputs Financieros)</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div>
                        <label className="label">Inflación (%)</label>
                        <input type="number" className="input-field" value={localData.market_data.inflation} onChange={e => handleChange('market_data', 'inflation', parseFloat(e.target.value))} />
                    </div>
                    <div>
                        <label className="label">Tasa Interés (%)</label>
                        <input type="number" className="input-field" value={localData.market_data.interest_rate} onChange={e => handleChange('market_data', 'interest_rate', parseFloat(e.target.value))} />
                    </div>
                    <div>
                        <label className="label">Crecimiento Sector (%)</label>
                        <input type="number" className="input-field" value={localData.market_data.sector_growth} onChange={e => handleChange('market_data', 'sector_growth', parseFloat(e.target.value))} />
                    </div>
                    <div className="bg-green-50 p-2 rounded border border-green-100">
                        <label className="label text-green-800">Precio Energía (USD/kWh)</label>
                        <input type="number" className="input-field bg-white" value={localData.market_data.energy_price} onChange={e => handleChange('market_data', 'energy_price', parseFloat(e.target.value))} />
                    </div>
                    <div className="bg-green-50 p-2 rounded border border-green-100">
                        <label className="label text-green-800">Costo Laboral (kUSD/año)</label>
                        <input type="number" className="input-field bg-white" value={localData.market_data.labor_cost} onChange={e => handleChange('market_data', 'labor_cost', parseFloat(e.target.value))} />
                    </div>
                     <div>
                        <label className="label">Indice Confianza</label>
                        <input type="number" className="input-field" value={localData.market_data.confidence_index} onChange={e => handleChange('market_data', 'confidence_index', parseFloat(e.target.value))} />
                    </div>
                </div>
            </section>

            {/* SECCIÓN 4: COMPETENCIA */}
            <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 border-l-4 border-l-orange-500">
                <h3 className="text-sm font-bold text-orange-500 uppercase tracking-wider mb-4 border-b pb-2">04. Competencia</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label className="label">Competidores Clave</label>
                        <input className="input-field" value={localData.competition_data.competitors} onChange={e => handleChange('competition_data', 'competitors', e.target.value)} />
                    </div>
                    <div>
                        <label className="label">Posición Mercado</label>
                        <input className="input-field" value={localData.competition_data.position} onChange={e => handleChange('competition_data', 'position', e.target.value)} />
                    </div>
                </div>
            </section>

            <div className="flex justify-end pt-6">
                <button onClick={onNext} disabled={!localData.company_data.name}
                    className="bg-gray-900 hover:bg-black text-white px-10 py-4 rounded-xl font-bold text-lg shadow-xl transition-all flex items-center gap-3">
                    Siguiente: Revisar Objetivos Detallados ➜
                </button>
            </div>

            <style>{`
                .label { display: block; font-size: 0.75rem; font-weight: 700; color: #4b5563; margin-bottom: 0.25rem; text-transform: uppercase; }
                .input-field { width: 100%; padding: 0.5rem; border: 1px solid #e5e7eb; border-radius: 0.375rem; font-size: 0.9rem; }
                .input-area { width: 100%; padding: 0.5rem; border: 1px solid #e5e7eb; border-radius: 0.375rem; resize: none; font-size: 0.9rem; }
            `}</style>
        </div>
    );
};

export default CompanyContextForm;
