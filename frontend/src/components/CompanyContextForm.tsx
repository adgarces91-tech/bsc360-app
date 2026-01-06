// @ts-nocheck
import { useState, useEffect } from 'react';

// DATOS REALES DE COPEC (Basado en tus PDFs 02.1 - 02.5)
const DEMO_FULL_COPEC = {
    company_data: {
        name: 'Empresas Copec S.A.',
        industry: 'Energía y Recursos Naturales',
        employees: '37800', // Dato real aproximado
        description: 'Holding industrial líder en energía, forestal y combustibles.'
    },
    strategy_data: {
        mission: 'Entregar soluciones energéticas sostenibles y productos de alta calidad.',
        vision: 'Ser líderes en la transición energética y movilidad del futuro.',
        values: 'Sostenibilidad, Innovación, Excelencia, Compromiso.',
        priorities: 'Descarbonización, Digitalización de clientes, Eficiencia Operacional.'
    },
    market_data: {
        inflation: 3.8,
        interest_rate: 6.25,
        sector_growth: 4.2,
        confidence_index: 68,
        trends: 'Electromovilidad, Hidrógeno Verde, Automatización logística.'
    },
    competition_data: {
        competitors: 'Enex (Shell), Esmax (Petrobras), CMPC.',
        position: 'Líder de Mercado (Market Leader)'
    },
    // Objetivos BSC precargados para el paso 2
    bsc_objectives: [
        { perspective: "Financiera", objective: "Maximizar ROIC en operaciones retail", kpi: "ROIC", current_value: 14.5, target_value: 18.0, unit: "%" },
        { perspective: "Clientes", objective: "Aumentar la lealtad del cliente", kpi: "NPS", current_value: 42.0, target_value: 60.0, unit: "puntos" },
        { perspective: "Procesos", objective: "Optimizar gestión de inventario", kpi: "Rotación", current_value: 8.5, target_value: 12.0, unit: "x" },
        { perspective: "Aprendizaje", objective: "Desarrollar liderazgo de tienda", kpi: "% Certificados", current_value: 35.0, target_value: 85.0, unit: "%" },
        { perspective: "ESG/ODS", objective: "Transición a energías renovables", kpi: "% Renovables", current_value: 12.0, target_value: 45.0, unit: "%" }
    ]
};

interface CompanyContextFormProps {
    data: any;
    onUpdate: (data: any) => void;
    onNext: () => void;
}

const CompanyContextForm = ({ data, onUpdate, onNext }: CompanyContextFormProps) => {
    // Inicialización robusta del estado con todas las secciones
    const [localData, setLocalData] = useState({
        company_data: data.company_data || { name: '', industry: '', employees: '', description: '' },
        strategy_data: data.strategy_data || { mission: '', vision: '', values: '', priorities: '' },
        market_data: data.market_data || { inflation: 0, interest_rate: 0, sector_growth: 0, confidence_index: 0, trends: '' },
        competition_data: data.competition_data || { competitors: '', position: '' },
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
            
            {/* HEADER CON ACCIÓN */}
            <div className="flex justify-between items-center bg-indigo-50 p-4 rounded-xl border border-indigo-100">
                <div>
                    <h2 className="text-2xl font-black text-indigo-900">Contexto Empresarial 360°</h2>
                    <p className="text-sm text-indigo-600">Completa la ficha estratégica para calibrar la IA.</p>
                </div>
                <button onClick={handleAutoFill} className="bg-indigo-600 text-white px-5 py-2 rounded-lg font-bold hover:bg-indigo-700 transition shadow-lg flex items-center gap-2">
                    ⚡ Auto-rellenar Copec
                </button>
            </div>

            {/* --- SECCIÓN 1: IDENTIDAD ORGANIZACIONAL --- */}
            <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <span className="bg-gray-100 text-gray-600 px-2 py-0.5 rounded">01</span> Organización
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="md:col-span-2">
                        <label className="label">Nombre Empresa</label>
                        <input type="text" className="input-field" placeholder="Ej: Empresas Copec S.A."
                            value={localData.company_data.name} onChange={e => handleChange('company_data', 'name', e.target.value)} />
                    </div>
                    <div>
                        <label className="label">Nº Empleados</label>
                        <input type="text" className="input-field" placeholder="Ej: 37.800"
                            value={localData.company_data.employees} onChange={e => handleChange('company_data', 'employees', e.target.value)} />
                    </div>
                    <div className="md:col-span-3">
                        <label className="label">Descripción / Rubro</label>
                        <input type="text" className="input-field" placeholder="Holding industrial, energía..."
                            value={localData.company_data.industry} onChange={e => handleChange('company_data', 'industry', e.target.value)} />
                    </div>
                </div>
            </section>

            {/* --- SECCIÓN 2: ESTRATEGIA CORPORATIVA (NUEVO) --- */}
            <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 border-l-4 border-l-blue-500">
                <h3 className="text-sm font-bold text-blue-500 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <span className="bg-blue-50 text-blue-600 px-2 py-0.5 rounded">02</span> Estrategia Corporativa
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label className="label">Misión</label>
                        <textarea className="input-area" rows={2} placeholder="Propósito fundamental..."
                            value={localData.strategy_data.mission} onChange={e => handleChange('strategy_data', 'mission', e.target.value)} />
                    </div>
                    <div>
                        <label className="label">Visión</label>
                        <textarea className="input-area" rows={2} placeholder="Aspiración futura..."
                            value={localData.strategy_data.vision} onChange={e => handleChange('strategy_data', 'vision', e.target.value)} />
                    </div>
                    <div className="md:col-span-2">
                        <label className="label">Prioridades Estratégicas 2026</label>
                        <input type="text" className="input-field" placeholder="Ej: Transformación Digital, Sostenibilidad..."
                            value={localData.strategy_data.priorities} onChange={e => handleChange('strategy_data', 'priorities', e.target.value)} />
                    </div>
                </div>
            </section>

            {/* --- SECCIÓN 3: MACROECONOMÍA Y MERCADO --- */}
            <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 border-l-4 border-l-green-500">
                <h3 className="text-sm font-bold text-green-600 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <span className="bg-green-50 text-green-700 px-2 py-0.5 rounded">03</span> Entorno de Mercado
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                    <div>
                        <label className="label">Inflación (%)</label>
                        <input type="number" className="input-field" value={localData.market_data.inflation}
                            onChange={e => handleChange('market_data', 'inflation', parseFloat(e.target.value))} />
                    </div>
                    <div>
                        <label className="label">Tasa Interés (%)</label>
                        <input type="number" className="input-field" value={localData.market_data.interest_rate}
                            onChange={e => handleChange('market_data', 'interest_rate', parseFloat(e.target.value))} />
                    </div>
                    <div>
                        <label className="label">Crecimiento (%)</label>
                        <input type="number" className="input-field" value={localData.market_data.sector_growth}
                            onChange={e => handleChange('market_data', 'sector_growth', parseFloat(e.target.value))} />
                    </div>
                    <div>
                        <label className="label">Confianza (0-100)</label>
                        <input type="number" className="input-field" value={localData.market_data.confidence_index}
                            onChange={e => handleChange('market_data', 'confidence_index', parseInt(e.target.value))} />
                    </div>
                </div>
                <div>
                    <label className="label">Tendencias Clave</label>
                    <input type="text" className="input-field" placeholder="Tecnologías, regulaciones..."
                        value={localData.market_data.trends} onChange={e => handleChange('market_data', 'trends', e.target.value)} />
                </div>
            </section>

            {/* --- SECCIÓN 4: COMPETENCIA (NUEVO) --- */}
            <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 border-l-4 border-l-orange-500">
                <h3 className="text-sm font-bold text-orange-500 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <span className="bg-orange-50 text-orange-600 px-2 py-0.5 rounded">04</span> Competencia
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label className="label">Principales Competidores</label>
                        <input type="text" className="input-field" placeholder="Ej: Shell, Petrobras..."
                            value={localData.competition_data.competitors} onChange={e => handleChange('competition_data', 'competitors', e.target.value)} />
                    </div>
                    <div>
                        <label className="label">Posición de Mercado</label>
                        <select className="input-field"
                            value={localData.competition_data.position} onChange={e => handleChange('competition_data', 'position', e.target.value)}>
                            <option value="">Seleccionar...</option>
                            <option value="Líder">Líder de Mercado</option>
                            <option value="Retador">Retador (Challenger)</option>
                            <option value="Seguidor">Seguidor</option>
                            <option value="Nicho">Nicho Especializado</option>
                        </select>
                    </div>
                </div>
            </section>

            <div className="flex justify-end pt-6">
                <button onClick={onNext} disabled={!localData.company_data.name}
                    className="bg-gray-900 hover:bg-black text-white px-10 py-4 rounded-xl font-bold text-lg shadow-xl transition-all flex items-center gap-3">
                    Siguiente: Definir Objetivos ➜
                </button>
            </div>

            {/* Estilos CSS en línea para limpiar el código */}
            <style>{`
                .label { display: block; font-size: 0.75rem; font-weight: 700; color: #4b5563; margin-bottom: 0.25rem; text-transform: uppercase; }
                .input-field { width: 100%; padding: 0.75rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; font-size: 0.95rem; outline: none; transition: all; }
                .input-field:focus { border-color: #6366f1; ring: 2px; ring-color: #e0e7ff; }
                .input-area { width: 100%; padding: 0.75rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; resize: none; outline: none; }
                .input-area:focus { border-color: #6366f1; }
            `}</style>
        </div>
    );
};

export default CompanyContextForm;
