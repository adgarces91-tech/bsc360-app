// @ts-nocheck
import { useState, useEffect } from 'react';

// Demo Data: Objetivos reales de Copec para pre-cargar el paso 2 automáticamente
const DEMO_OBJECTIVES_COPEC = [
    { perspective: "Financiera", objective: "Maximizar ROIC en operaciones retail", kpi: "ROIC", current_value: 14.5, target_value: 18.0, unit: "%" },
    { perspective: "Clientes", objective: "Aumentar la lealtad del cliente", kpi: "NPS", current_value: 42.0, target_value: 60.0, unit: "puntos" },
    { perspective: "Procesos", objective: "Optimizar gestión de inventario", kpi: "Rotación", current_value: 8.5, target_value: 12.0, unit: "x" },
    { perspective: "Aprendizaje", objective: "Desarrollar liderazgo de tienda", kpi: "% Certificados", current_value: 35.0, target_value: 85.0, unit: "%" },
    { perspective: "ESG/ODS", objective: "Transición a energías renovables", kpi: "% Renovables", current_value: 12.0, target_value: 45.0, unit: "%" },
];

interface CompanyContextFormProps {
    data: any;
    onUpdate: (data: any) => void;
    onNext: () => void;
}

const CompanyContextForm = ({ data, onUpdate, onNext }: CompanyContextFormProps) => {
    // Estado local inicializado con los datos que vengan del padre o valores por defecto
    const [localData, setLocalData] = useState({
        company_data: {
            name: data.company_data?.name || '',
            industry: data.company_data?.industry || '',
            employees: data.company_data?.employees || '',
            description: data.company_data?.description || ''
        },
        market_data: {
            inflation: data.market_data?.inflation || 3.8,
            interest_rate: data.market_data?.interest_rate || 6.25,
            sector_growth: data.market_data?.sector_growth || 2.5,
            trends: data.market_data?.trends || ''
        },
        // Guardamos los objetivos aquí también para pasarlos al padre al hacer auto-fill
        bsc_objectives: data.bsc_objectives || []
    });

    // Sincronizar cambios con el componente padre (Dashboard.tsx)
    useEffect(() => {
        onUpdate(localData);
    }, [localData]);

    const handleChange = (section: string, field: string, value: any) => {
        setLocalData(prev => ({
            ...prev,
            [section]: {
                ...prev[section],
                [field]: value
            }
        }));
    };

    // Función "Mágica": Rellena el contexto Y los objetivos del paso 2
    const handleAutoFillCopec = () => {
        const copecData = {
            company_data: {
                name: 'Empresas Copec S.A.',
                industry: 'Energía y Retail',
                employees: '15000',
                description: 'Líder en distribución de combustibles y soluciones energéticas en Chile.'
            },
            market_data: {
                inflation: 3.8,
                interest_rate: 6.25,
                sector_growth: 4.2,
                trends: 'Transición energética, Electromovilidad, Experiencia de cliente digital'
            },
            bsc_objectives: DEMO_OBJECTIVES_COPEC // ¡Aquí ocurre la magia para el Paso 2!
        };
        
        setLocalData(copecData);
        // Forzamos la actualización inmediata hacia arriba
        onUpdate(copecData);
    };

    return (
        <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
            
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-800">🏢 Contexto Empresarial</h2>
                <button
                    onClick={handleAutoFillCopec}
                    className="flex items-center gap-2 bg-indigo-50 text-indigo-700 px-4 py-2 rounded-full hover:bg-indigo-100 font-semibold transition-colors border border-indigo-200 shadow-sm"
                >
                    <span>🚀</span> Auto-rellenar Demo Copec
                </button>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                {/* --- SECCIÓN 1: DATOS DE LA EMPRESA (Tipo B) --- */}
                <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4 border-b border-gray-100 pb-2">
                    1. Información de la Organización
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Nombre Empresa</label>
                        <input
                            type="text"
                            value={localData.company_data.name}
                            onChange={(e) => handleChange('company_data', 'name', e.target.value)}
                            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                            placeholder="Ej: Empresas Copec S.A."
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Industria / Sector</label>
                        <input
                            type="text"
                            value={localData.company_data.industry}
                            onChange={(e) => handleChange('company_data', 'industry', e.target.value)}
                            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                            placeholder="Ej: Energía y Retail"
                        />
                    </div>
                </div>

                {/* --- SECCIÓN 2: CONTEXTO DE MERCADO (Tipo A) --- */}
                <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4 border-b border-gray-100 pb-2 pt-2">
                    2. Variables Macroeconómicas (Inputs para la IA)
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Inflación Anual (%)</label>
                        <div className="relative">
                            <input
                                type="number"
                                value={localData.market_data.inflation}
                                onChange={(e) => handleChange('market_data', 'inflation', parseFloat(e.target.value))}
                                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none pr-8"
                                placeholder="3.8"
                            />
                            <span className="absolute right-3 top-3 text-gray-400 font-bold">%</span>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">Impacta costos y precios.</p>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Tasa de Interés (%)</label>
                        <div className="relative">
                            <input
                                type="number"
                                value={localData.market_data.interest_rate}
                                onChange={(e) => handleChange('market_data', 'interest_rate', parseFloat(e.target.value))}
                                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none pr-8"
                                placeholder="6.25"
                            />
                            <span className="absolute right-3 top-3 text-gray-400 font-bold">%</span>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">Impacta costo capital.</p>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Crecimiento Sector (%)</label>
                        <div className="relative">
                            <input
                                type="number"
                                value={localData.market_data.sector_growth}
                                onChange={(e) => handleChange('market_data', 'sector_growth', parseFloat(e.target.value))}
                                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none pr-8"
                                placeholder="4.2"
                            />
                            <span className="absolute right-3 top-3 text-gray-400 font-bold">%</span>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">Ref.: PIB sectorial.</p>
                    </div>
                </div>

                <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Tendencias Clave del Mercado</label>
                    <textarea
                        value={localData.market_data.trends}
                        onChange={(e) => handleChange('market_data', 'trends', e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none h-24 resize-none"
                        placeholder="Ej: Digitalización, Escasez de talento, Regulaciones ambientales..."
                    />
                    <p className="text-xs text-gray-500 mt-1">💡 La IA usará esto para recomendar acciones de innovación y detectar riesgos.</p>
                </div>
            </div>

            <div className="flex justify-end pt-4">
                <button
                    onClick={onNext}
                    disabled={!localData.company_data.name}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                    Siguiente: Definir Objetivos ➜
                </button>
            </div>
        </div>
    );
};

export default CompanyContextForm;
