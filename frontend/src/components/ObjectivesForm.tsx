import { useState } from 'react';

interface ObjectivesFormProps {
    objectives: any[];
    onUpdate: (objectives: any[]) => void;
    onBack: () => void;
    onSubmit: () => void;
    isLoading: boolean;
}

const ObjectivesForm = ({ objectives, onUpdate, onBack, onSubmit, isLoading }: ObjectivesFormProps) => {

    const [newObj, setNewObj] = useState({
        perspective: 'Financiera',
        objective: '',
        kpi: '',
        current_value: 0,
        target_value: 0,
        unit: '%'
    });

    const categories = ['Financiera', 'Clientes', 'Procesos', 'Aprendizaje', 'ESG/ODS'];

    const handleAdd = () => {
        if (!newObj.objective || !newObj.kpi) return;
        onUpdate([...objectives, newObj]);
        // Reiniciamos el formulario, volviendo los valores a 0
        setNewObj({ ...newObj, objective: '', kpi: '', current_value: 0, target_value: 0 });
    };

    const handleDelete = (index: number) => {
        onUpdate(objectives.filter((_, i) => i !== index));
    };

    return (
        <div className="bg-white p-8 rounded-lg shadow-lg border border-gray-200 animate-in fade-in slide-in-from-right-8 duration-500">
            <div className="flex justify-between items-center mb-8">
                <h2 className="text-2xl font-bold text-gray-800">Paso 2: Objetivos Estratégicos BSC</h2>
                <div className="text-sm text-gray-500">
                    Total Objetivos: <span className="font-bold text-indigo-600">{objectives.length}</span>
                </div>
            </div>

            {/* Lista de Objetivos Agregados */}
            <div className="mb-8 space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                {objectives.length === 0 && (
                    <div className="text-center py-10 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                        <p className="text-gray-500">No hay objetivos definidos aún.</p>
                        <p className="text-sm text-gray-400">Agrega uno abajo o carga el Demo en el paso anterior.</p>
                    </div>
                )}
                {objectives.map((obj, idx) => (
                    <div key={idx} className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4 hover:border-indigo-300 transition-colors group">
                        <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                                <span className={`text-xs font-bold px-2 py-1 rounded uppercase tracking-wider ${obj.perspective === 'Financiera' ? 'bg-green-100 text-green-700' :
                                        obj.perspective === 'Clientes' ? 'bg-blue-100 text-blue-700' :
                                            obj.perspective === 'Procesos' ? 'bg-yellow-100 text-yellow-700' :
                                                obj.perspective === 'Aprendizaje' ? 'bg-purple-100 text-purple-700' :
                                                    'bg-teal-100 text-teal-700'
                                    }`}>
                                    {obj.perspective}
                                </span>
                                <h3 className="font-semibold text-gray-800">{obj.objective}</h3>
                            </div>
                            <div className="text-sm text-gray-600 flex items-center gap-4">
                                <span>KPI: <strong>{obj.kpi}</strong></span>
                                <span className="bg-gray-100 px-2 rounded text-xs">Actual: {obj.current_value}</span>
                                <span className="bg-indigo-50 text-indigo-700 px-2 rounded text-xs font-bold">Meta: {obj.target_value}</span>
                            </div>
                        </div>
                        <button
                            onClick={() => handleDelete(idx)}
                            className="text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity p-2"
                        >
                            🗑️
                        </button>
                    </div>
                ))}
            </div>

            {/* Formulario para Agregar Nuevo */}
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 mb-8">
                <h4 className="text-sm font-bold text-gray-700 uppercase mb-4 tracking-wider flex items-center gap-2">
                    <span>➕</span> Agregar Nuevo Objetivo
                </h4>

                <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-start">

                    {/* Perspectiva */}
                    <div className="md:col-span-3">
                        <label className="block text-xs font-semibold text-gray-500 mb-1">Perspectiva</label>
                        <select
                            className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-indigo-500 outline-none"
                            value={newObj.perspective}
                            onChange={(e) => setNewObj({ ...newObj, perspective: e.target.value })}
                        >
                            {categories.map(c => <option key={c} value={c}>{c}</option>)}
                        </select>
                    </div>

                    {/* Descripción y KPI */}
                    <div className="md:col-span-5 space-y-4 md:space-y-0 md:grid md:grid-cols-1 gap-4">
                        <div>
                            <label className="block text-xs font-semibold text-gray-500 mb-1">Objetivo Estratégico</label>
                            <input
                                type="text"
                                placeholder="Ej: Aumentar Ventas"
                                className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-indigo-500 outline-none"
                                value={newObj.objective}
                                onChange={(e) => setNewObj({ ...newObj, objective: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-semibold text-gray-500 mb-1">Nombre del KPI</label>
                            <input
                                type="text"
                                placeholder="Ej: Ingresos Mensuales"
                                className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-indigo-500 outline-none"
                                value={newObj.kpi}
                                onChange={(e) => setNewObj({ ...newObj, kpi: e.target.value })}
                            />
                        </div>
                    </div>

                    {/* Números (Con las etiquetas que pediste) */}
                    <div className="md:col-span-2">
                        <label className="block text-xs font-bold text-gray-600 mb-1">Valor Actual</label>
                        <input
                            type="number"
                            className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-indigo-500 outline-none font-mono"
                            value={newObj.current_value}
                            onChange={(e) => setNewObj({ ...newObj, current_value: parseFloat(e.target.value) })}
                        />
                        <p className="text-[10px] text-gray-400 mt-1 text-center">Hoy</p>
                    </div>

                    <div className="md:col-span-2">
                        <label className="block text-xs font-bold text-indigo-600 mb-1">Meta</label>
                        <input
                            type="number"
                            className="w-full p-2 border border-indigo-300 rounded focus:ring-2 focus:ring-indigo-500 outline-none font-mono bg-indigo-50"
                            value={newObj.target_value}
                            onChange={(e) => setNewObj({ ...newObj, target_value: parseFloat(e.target.value) })}
                        />
                        <p className="text-[10px] text-indigo-400 mt-1 text-center">Objetivo</p>
                    </div>
                </div>

                <div className="mt-4 flex justify-end">
                    <button
                        onClick={handleAdd}
                        disabled={!newObj.objective || !newObj.kpi}
                        className="px-6 py-2 bg-gray-900 text-white rounded hover:bg-black font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        + Agregar a la Lista
                    </button>
                </div>
            </div>

            {/* Botones de Navegación */}
            <div className="flex justify-between pt-4 border-t border-gray-200">
                <button
                    onClick={onBack}
                    className="px-6 py-2 text-gray-600 font-medium hover:text-gray-900 flex items-center gap-2"
                >
                    ← Volver
                </button>
                <button
                    onClick={onSubmit}
                    disabled={objectives.length === 0 || isLoading}
                    className={`px-8 py-3 rounded-full font-bold text-white shadow-lg flex items-center gap-2 ${isLoading
                            ? 'bg-indigo-400 cursor-wait'
                            : 'bg-indigo-600 hover:bg-indigo-700 transform hover:-translate-y-1 transition-all'
                        }`}
                >
                    {isLoading ? 'Analizando...' : 'Generar Análisis Estratégico ✨'}
                </button>
            </div>
        </div>
    );
};

export default ObjectivesForm;