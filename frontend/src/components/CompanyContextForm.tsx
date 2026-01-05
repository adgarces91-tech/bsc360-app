import { useState, useEffect } from 'react';

// Demo Data constant (Can be moved to a shared constant file)
const DEMO_DATA = {
    company_data: {
        name: "Empresas Copec S.A.",
        industry: "Retail/Energía"
    },
    market_data: {
        sector_growth: 4.2,
        inflation: 3.8,
        interest_rate: 6.25,
        confidence_index: 68
    },
    bsc_objectives: [
        { perspective: "Financiera", objective: "Maximizar ROIC en operaciones retail", kpi: "ROIC", current_value: 14.5, target_value: 18.0, unit: "%" },
        { perspective: "Clientes", objective: "Aumentar la lealtad del cliente", kpi: "NPS", current_value: 42.0, target_value: 60.0, unit: "puntos" },
        { perspective: "Procesos", objective: "Optimizar gestión de inventario", kpi: "Rotación", current_value: 8.5, target_value: 12.0, unit: "x" },
        { perspective: "Aprendizaje", objective: "Desarrollar liderazgo de tienda", kpi: "% Certificados", current_value: 35.0, target_value: 85.0, unit: "%" },
        { perspective: "ESG/ODS", objective: "Transición a energías renovables", kpi: "% Renovables", current_value: 12.0, target_value: 45.0, unit: "%" },
    ]
};

interface CompanyContextFormProps {
    data: any;
    onUpdate: (data: any) => void;
    onNext: () => void;
}

const CompanyContextForm = ({ data, onUpdate, onNext }: CompanyContextFormProps) => {
    const [localData, setLocalData] = useState(data);

    useEffect(() => {
        setLocalData(data);
    }, [data]);

    const handleChange = (section: string, field: string, value: any) => {
        const newData = {
            ...localData,
            [section]: {
                ...localData[section],
                [field]: value
            }
        };
        setLocalData(newData);
        onUpdate(newData);
    };

    const loadDemo = () => {
        // Load everything including objectives, but only show company/market here
        onUpdate(DEMO_DATA);
    };

    return (
        <div className="bg-white p-8 rounded-lg shadow-lg border border-gray-200 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex justify-between items-center mb-8">
                <h2 className="text-2xl font-bold text-gray-800">Paso 1: Contexto Empresarial</h2>
                <button
                    onClick={loadDemo}
                    className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold hover:bg-blue-200 transition-colors"
                >
                    🚀 Cargar Demo Copec
                </button>
            </div>

            <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Nombre de la Empresa</label>
                        <input
                            type="text"
                            value={localData.company_data.name}
                            onChange={(e) => handleChange('company_data', 'name', e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            placeholder="Ej. Mi Empresa S.A."
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Industria</label>
                        <input
                            type="text"
                            value={localData.company_data.industry}
                            onChange={(e) => handleChange('company_data', 'industry', e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            placeholder="Ej. Tecnología, Retail..."
                        />
                    </div>
                </div>

                <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-800 mb-4">Datos de Mercado</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div>
                            <label className="block text-xs font-semibold text-gray-600 mb-1">Crecimiento Sector (%)</label>
                            <input
                                type="number"
                                step="0.1"
                                value={localData.market_data.sector_growth}
                                onChange={(e) => handleChange('market_data', 'sector_growth', parseFloat(e.target.value))}
                                className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-indigo-500"
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-semibold text-gray-600 mb-1">Inflación (%)</label>
                            <input
                                type="number"
                                step="0.1"
                                value={localData.market_data.inflation}
                                onChange={(e) => handleChange('market_data', 'inflation', parseFloat(e.target.value))}
                                className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-indigo-500"
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-semibold text-gray-600 mb-1">Tasa Interés (%)</label>
                            <input
                                type="number"
                                step="0.01"
                                value={localData.market_data.interest_rate}
                                onChange={(e) => handleChange('market_data', 'interest_rate', parseFloat(e.target.value))}
                                className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-indigo-500"
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-semibold text-gray-600 mb-1">Índice Confianza</label>
                            <input
                                type="number"
                                value={localData.market_data.confidence_index}
                                onChange={(e) => handleChange('market_data', 'confidence_index', parseInt(e.target.value))}
                                className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-indigo-500"
                            />
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-8 flex justify-end">
                <button
                    onClick={onNext}
                    disabled={!localData.company_data.name}
                    className="px-8 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-semibold shadow-md disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center gap-2"
                >
                    Siguiente: Definir Objetivos
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
                </button>
            </div>
        </div>
    );
};

export default CompanyContextForm;
