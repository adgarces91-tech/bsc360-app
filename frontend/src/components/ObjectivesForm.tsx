// @ts-nocheck
import { useState } from 'react';

interface ObjectivesFormProps {
    objectives: any[];
    onUpdate: (objs: any[]) => void;
    onBack: () => void;
    onSubmit: () => void;
    isLoading: boolean;
}

const ObjectivesForm = ({ objectives, onUpdate, onBack, onSubmit, isLoading }: ObjectivesFormProps) => {
    
    // Función para actualizar un campo específico de un objetivo
    const handleObjChange = (index: number, field: string, value: any) => {
        const updatedObjectives = [...objectives];
        updatedObjectives[index] = { ...updatedObjectives[index], [field]: value };
        onUpdate(updatedObjectives);
    };

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
            
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-800">2. Definición de Objetivos (Detalle Técnico)</h2>
                <span className="bg-indigo-100 text-indigo-800 text-xs font-bold px-3 py-1 rounded-full">
                    {objectives.length} Objetivos Cargados
                </span>
            </div>

            <div className="grid gap-6">
                {objectives.map((obj, idx) => (
                    <div key={idx} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                        
                        {/* Cabecera del Objetivo */}
                        <div className="flex justify-between items-start mb-4 border-b pb-4">
                            <div>
                                <span className={`text-xs font-bold px-2 py-1 rounded uppercase ${
                                    obj.perspective === 'Financiera' ? 'bg-green-100 text-green-700' :
                                    obj.perspective === 'Clientes' ? 'bg-blue-100 text-blue-700' :
                                    obj.perspective === 'Procesos' ? 'bg-yellow-100 text-yellow-700' :
                                    'bg-purple-100 text-purple-700'
                                }`}>
                                    {obj.perspective}
                                </span>
                                <h3 className="text-lg font-bold mt-2 text-gray-800">{obj.objective}</h3>
                            </div>
                        </div>

                        {/* GRID DE DATOS TÉCNICOS (CASILLAS PDF) */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                            
                            {/* Columna 1: Definición */}
                            <div className="space-y-2">
                                <div>
                                    <label className="block text-xs font-bold text-gray-400 uppercase">KPI</label>
                                    <input className="w-full border rounded p-1" value={obj.kpi} onChange={(e) => handleObjChange(idx, 'kpi', e.target.value)} />
                                </div>
                                <div>
                                    <label className="block text-xs font-bold text-gray-400 uppercase">Fórmula Cálculo</label>
                                    <input className="w-full border rounded p-1 bg-gray-50" value={obj.formula || ''} placeholder="Ej: (A/B)*100" onChange={(e) => handleObjChange(idx, 'formula', e.target.value)} />
                                </div>
                                <div>
                                    <label className="block text-xs font-bold text-gray-400 uppercase">Frecuencia</label>
                                    <input className="w-full border rounded p-1" value={obj.frequency || ''} placeholder="Mensual" onChange={(e) => handleObjChange(idx, 'frequency', e.target.value)} />
                                </div>
                            </div>

                            {/* Columna 2: Metas */}
                            <div className="space-y-2">
                                <div className="grid grid-cols-2 gap-2">
                                    <div>
                                        <label className="block text-xs font-bold text-gray-400 uppercase">Línea Base</label>
                                        <input type="number" className="w-full border rounded p-1" value={obj.baseline || 0} onChange={(e) => handleObjChange(idx, 'baseline', parseFloat(e.target.value))} />
                                    </div>
                                    <div>
                                        <label className="block text-xs font-bold text-gray-400 uppercase">Meta</label>
                                        <input type="number" className="w-full border rounded p-1 font-bold text-indigo-600" value={obj.target_value} onChange={(e) => handleObjChange(idx, 'target_value', parseFloat(e.target.value))} />
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-xs font-bold text-gray-400 uppercase">Valor Actual</label>
                                    <input type="number" className="w-full border rounded p-1 font-bold" value={obj.current_value} onChange={(e) => handleObjChange(idx, 'current_value', parseFloat(e.target.value))} />
                                </div>
                                <div>
                                    <label className="block text-xs font-bold text-gray-400 uppercase">Fuente Datos</label>
                                    <input className="w-full border rounded p-1 text-xs" value={obj.data_source || ''} onChange={(e) => handleObjChange(idx, 'data_source', e.target.value)} />
                                </div>
                            </div>

                            {/* Columna 3: Gestión */}
                            <div className="space-y-2">
                                <div>
                                    <label className="block text-xs font-bold text-gray-400 uppercase">Línea de Acción</label>
                                    <textarea rows={2} className="w-full border rounded p-1 text-xs resize-none" value={obj.action_line || ''} onChange={(e) => handleObjChange(idx, 'action_line', e.target.value)} />
                                </div>
                                <div>
                                    <label className="block text-xs font-bold text-gray-400 uppercase">Responsable</label>
                                    <input className="w-full border rounded p-1" value={obj.responsible || ''} onChange={(e) => handleObjChange(idx, 'responsible', e.target.value)} />
                                </div>
                                <div>
                                    <label className="block text-xs font-bold text-gray-400 uppercase">Financiamiento</label>
                                    <input className="w-full border rounded p-1" value={obj.financing || ''} onChange={(e) => handleObjChange(idx, 'financing', e.target.value)} />
                                </div>
                            </div>

                        </div>
                    </div>
                ))}
            </div>

            <div className="flex justify-between pt-6 border-t border-gray-200">
                <button onClick={onBack} className="text-gray-600 font-medium hover:text-gray-900 px-6 py-3">
                    ← Volver a Contexto
                </button>
                <button
                    onClick={onSubmit}
                    disabled={isLoading}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-10 py-3 rounded-xl font-bold shadow-xl transition-all disabled:opacity-50 flex items-center gap-2"
                >
                    {isLoading ? 'Analizando con IA...' : '✨ Generar Informe Final'}
                </button>
            </div>
        </div>
    );
};

export default ObjectivesForm;
