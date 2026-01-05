import { useState } from 'react';

// Copec Demo Data from Specification
const DEMO_DATA = {
    // ... (I will keep the data but I need to be careful with replace_file_content logic.
    // Actually I better use multi_replace or just target the top and the component definition)
    // To be safe I will just replace the import and the component signature.

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
        {
            perspective: "Financiera",
            objective: "Maximizar ROIC en operaciones retail",
            kpi: "ROIC (Return on Invested Capital)",
            current_value: 14.5,
            target_value: 18.0,
            unit: "%"
        },
        {
            perspective: "Financiera",
            objective: "Incrementar ventas same-store",
            kpi: "Same Store Sales Growth",
            current_value: 3.2,
            target_value: 7.5,
            unit: "%"
        },
        {
            perspective: "Clientes",
            objective: "Aumentar la lealtad del cliente",
            kpi: "NPS (Net Promoter Score)",
            current_value: 42.0,
            target_value: 60.0,
            unit: "puntos"
        },
        {
            perspective: "Procesos",
            objective: "Optimizar gestión de inventario",
            kpi: "Inventory Turnover",
            current_value: 8.5,
            target_value: 12.0,
            unit: "veces/año"
        },
        {
            perspective: "Procesos",
            objective: "Reducir pérdidas operacionales",
            kpi: "Shrinkage Rate",
            current_value: 1.8,
            target_value: 0.8,
            unit: "%"
        },
        {
            perspective: "Aprendizaje",
            objective: "Desarrollar liderazgo de tienda",
            kpi: "% Gerentes certificados en liderazgo",
            current_value: 35.0,
            target_value: 85.0,
            unit: "%"
        },
        {
            perspective: "Aprendizaje",
            objective: "Reducir rotación de personal",
            kpi: "Tasa de rotación anual",
            current_value: 28.0,
            target_value: 15.0,
            unit: "%"
        },
        {
            perspective: "ESG/ODS",
            objective: "Transición a energías renovables",
            kpi: "% Energía de fuentes renovables",
            current_value: 12.0,
            target_value: 45.0,
            unit: "%"
        },
        {
            perspective: "ESG/ODS",
            objective: "Reducir residuos plásticos",
            kpi: "Reducción de plástico de un solo uso",
            current_value: 15.0,
            target_value: 60.0,
            unit: "%"
        }
    ]
};

interface AnalysisFormProps {
    onSubmit: (data: any) => void;
    isLoading: boolean;
}

const AnalysisForm = ({ onSubmit, isLoading }: AnalysisFormProps) => {
    const [formData, setFormData] = useState<any>({
        company_data: { name: '', industry: '' },
        market_data: { sector_growth: 0, inflation: 0, interest_rate: 0, confidence_index: 0 },
        bsc_objectives: []
    });

    const loadDemoData = () => {
        setFormData(DEMO_DATA);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formData);
    };

    // Simplified form rendering for brevity, can be expanded to fully editable fields
    return (
        <div className="p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-xl font-bold mb-4">Datos de la Empresa y Estrategia</h2>

            <div className="mb-6 flex justify-end">
                <button
                    type="button"
                    onClick={loadDemoData}
                    className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 font-semibold transition-colors"
                >
                    Cargar Datos de Prueba (Copec)
                </button>
            </div>

            <form onSubmit={handleSubmit}>
                <div className="grid grid-cols-1 gap-6 md:grid-cols-2 mb-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Empresa</label>
                        <input
                            type="text"
                            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                            value={formData.company_data.name}
                            onChange={(e) => setFormData({ ...formData, company_data: { ...formData.company_data, name: e.target.value } })}
                            placeholder="Nombre de la empresa"
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Industria</label>
                        <input
                            type="text"
                            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                            value={formData.company_data.industry}
                            onChange={(e) => setFormData({ ...formData, company_data: { ...formData.company_data, industry: e.target.value } })}
                            placeholder="Industria"
                            required
                        />
                    </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Crecimiento Sector (%)</label>
                        <input type="number" step="0.1" className="w-full border p-2 rounded"
                            value={formData.market_data.sector_growth}
                            onChange={(e) => setFormData({ ...formData, market_data: { ...formData.market_data, sector_growth: parseFloat(e.target.value) } })}
                        />
                    </div>
                    <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Inflación (%)</label>
                        <input type="number" step="0.1" className="w-full border p-2 rounded"
                            value={formData.market_data.inflation}
                            onChange={(e) => setFormData({ ...formData, market_data: { ...formData.market_data, inflation: parseFloat(e.target.value) } })}
                        />
                    </div>
                    <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Tasa Interés (%)</label>
                        <input type="number" step="0.01" className="w-full border p-2 rounded"
                            value={formData.market_data.interest_rate}
                            onChange={(e) => setFormData({ ...formData, market_data: { ...formData.market_data, interest_rate: parseFloat(e.target.value) } })}
                        />
                    </div>
                    <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Índice Confianza</label>
                        <input type="number" className="w-full border p-2 rounded"
                            value={formData.market_data.confidence_index}
                            onChange={(e) => setFormData({ ...formData, market_data: { ...formData.market_data, confidence_index: parseInt(e.target.value) } })}
                        />
                    </div>
                </div>

                {/* BSC Objectives Preview (Read-only for Demo simplicity, or fully editable if needed) */}
                <div className="mb-6">
                    <h3 className="text-lg font-semibold mb-2">Objetivos BSC ({formData.bsc_objectives.length})</h3>
                    {formData.bsc_objectives.length === 0 ? (
                        <p className="text-gray-500 italic text-sm">No hay objetivos cargados. Carga los datos de prueba.</p>
                    ) : (
                        <div className="bg-gray-50 p-4 rounded border border-gray-200 h-64 overflow-y-auto">
                            <ul className="space-y-3">
                                {formData.bsc_objectives.map((obj: any, idx: number) => (
                                    <li key={idx} className="bg-white p-3 rounded shadow-sm text-sm border-l-4 border-blue-500">
                                        <div className="flex justify-between font-bold text-gray-700">
                                            <span>{obj.perspective}</span>
                                            <span className="text-blue-600">{obj.kpi}</span>
                                        </div>
                                        <div className="mt-1">{obj.objective}</div>
                                        <div className="mt-1 text-xs text-gray-500">
                                            Actual: {obj.current_value}{obj.unit} | Meta: {obj.target_value}{obj.unit}
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>

                <div className="flex justify-center">
                    <button
                        type="submit"
                        disabled={isLoading || formData.bsc_objectives.length === 0}
                        className={`px-8 py-3 text-lg font-bold text-white rounded-full shadow-lg transition-all transform hover:scale-105 ${isLoading || formData.bsc_objectives.length === 0
                            ? 'bg-gray-400 cursor-not-allowed'
                            : 'bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800'
                            }`}
                    >
                        {isLoading ? 'Analizando con Gemini AI...' : 'Generar Análisis Estratégico'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default AnalysisForm;
