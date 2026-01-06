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
    
    const handleObjChange = (index: number, field: string, value: any) => {
        const updatedObjectives = [...objectives];
        updatedObjectives[index] = { ...updatedObjectives[index], [field]: value };
        onUpdate(updatedObjectives);
    };

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
            
            <div className="flex justify-between items-center bg-white p-4 rounded-xl border border-gray-100 shadow-sm sticky top-20 z-10">
                <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                    <span className="bg-indigo-600 text-white w-8 h-8 flex items-center justify-center rounded-full text-sm">2</span>
                    Definición de Objetivos (Detalle Técnico)
                </h2>
                <span className="bg-indigo-50 text-indigo-700 text-sm font-bold px-3 py-1 rounded-full border border-indigo-100">
                    {objectives.length} KPIs Activos
                </span>
            </div>

            <div className="grid gap-6 pb-20">
                {objectives.map((obj, idx) => (
                    <div key={idx} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:border-indigo-300 transition-all">
                        
                        {/* Cabecera del Objetivo */}
                        <div className="flex justify-between items-start mb-6 border-b border-gray-100 pb-4">
                            <div>
                                <span className={`text-xs font-bold px-2 py-1 rounded uppercase tracking-wider ${
                                    obj.perspective === 'Financiera' ? 'bg-green-100 text-green-700' :
                                    obj.perspective === 'Clientes' ? 'bg-blue-100 text-blue-700' :
                                    obj.perspective === 'Procesos' ? 'bg-yellow-100 text-yellow-700' :
                                    'bg-purple-100 text-purple-700'
                                }`}>
                                    {obj.perspective}
                                </span>
                                <h3 className="text-lg font-bold mt-2 text-gray-800">{obj.objective}</h3>
                            </div>
                            {/* Input de Unidad Editable */}
                            <div className="w-24">
                                <label className="block text-[10px] font-bold text-gray-400 uppercase text-right mb-1">Unidad</label>
                                <input 
                                    className="w-full text-right text-xs font-bold text-gray-500 bg-gray-50 border-none rounded focus:ring-0" 
                                    value={obj.unit || ''} 
                                    onChange={(e) => handleObjChange(idx, 'unit', e.target.value)}
                                    placeholder="%"
                                />
                            </div>
                        </div>

                        {/* GRID DE DATOS TÉCNICOS */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
                            
                            {/* Columna 1: Definición */}
                            <div className="space-y-3 border-r border-gray-100 pr-4">
                                <h4 className="text-xs font-black text-gray-400 uppercase tracking-widest mb-2">Definición</h4>
                                <div>
                                    <label className="block text-xs font-semibold text-gray-600 mb-1">KPI (Indicador)</label>
                                    <input className="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none" value={obj.kpi} onChange={(e) => handleObjChange(idx, 'kpi', e.target.value)} />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-gray-600 mb-1">Fórmula Cálculo</label>
                                    <input className="w-full border border-gray-300 rounded-md p-2 text-sm bg-gray-50 text-gray-500 font-mono text-xs" value={obj.formula || ''} placeholder="Ej: (A/B)*100" onChange={(e) => handleObjChange(idx, 'formula', e.target.value)} />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-gray-600 mb-1">Frecuencia</label>
                                    <input className="w-full border border-gray-300 rounded-md p-2 text-sm" value={obj.frequency || ''} placeholder="Mensual" onChange={(e) => handleObjChange(idx, 'frequency', e.target.value)} />
                                </div>
                            </div>

                            {/* Columna 2: Metas (CON UNIDADES VISUALES) */}
                            <div className="space-y-3 border-r border-gray-100 pr-4 bg-gray-50/50 p-3 rounded-lg">
                                <h4 className="text-xs font-black text-indigo-400 uppercase tracking-widest mb-2">Métricas ({obj.unit})</h4>
                                
                                <div className="grid grid-cols-2 gap-3">
                                    {/* LÍNEA BASE + UNIDAD */}
                                    <div className="relative">
                                        <label className="block text-xs font-semibold text-gray-600 mb-1">Línea Base</label>
                                        <div className="relative">
                                            <input 
                                                type="number" 
                                                className="w-full border border-gray-300 rounded-md p-2 pr-8 text-sm" 
                                                value={obj.baseline || 0} 
                                                onChange={(e) => handleObjChange(idx, 'baseline', parseFloat(e.target.value))} 
                                            />
                                            <span className="absolute right-2 top-2 text-xs text-gray-400 font-bold pointer-events-none">{obj.unit}</span>
                                        </div>
                                    </div>

                                    {/* META + UNIDAD */}
                                    <div className="relative">
                                        <label className="block text-xs font-bold text-indigo-600 mb-1">Meta Objetivo</label>
                                        <div className="relative">
                                            <input 
                                                type="number" 
                                                className="w-full border-2 border-indigo-100 rounded-md p-2 pr-8 text-sm font-bold text-indigo-700 focus:border-indigo-500 outline-none" 
                                                value={obj.target_value} 
                                                onChange={(e) => handleObjChange(idx, 'target_value', parseFloat(e.target.value))} 
                                            />
                                            <span className="absolute right-2 top-2 text-xs text-indigo-300 font-bold pointer-events-none">{obj.unit}</span>
                                        </div>
                                    </div>
                                </div>

                                {/* VALOR ACTUAL + UNIDAD */}
                                <div className="relative mt-2">
                                    <label className="block text-xs font-semibold text-gray-600 mb-1">Valor Actual (Real)</label>
                                    <div className="relative">
                                        <input 
                                            type="number" 
                                            className="w-full border border-gray-300 rounded-md p-2 pr-8 text-sm font-bold text-gray-800" 
                                            value={obj.current_value} 
                                            onChange={(e) => handleObjChange(idx, 'current_value', parseFloat(e.target.value))} 
                                        />
                                        <span className="absolute right-2 top-2 text-xs text-gray-400 font-bold pointer-events-none">{obj.unit}</span>
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-xs font-semibold text-gray-600 mb-1">Fuente Datos</label>
                                    <input className="w-full border border-gray-300 rounded-md p-2 text-xs text-gray-500" value={obj.data_source || ''} onChange={(e) => handleObjChange(idx, 'data_source', e.target.value)} />
                                </div>
                            </div>

                            {/* Columna 3: Gestión */}
                            <div className="space-y-3 pl-2">
                                <h4 className="text-xs font-black text-gray-400 uppercase tracking-widest mb-2">Gestión</h4>
                                <div>
                                    <label className="block text-xs font-semibold text-gray-600 mb-1">Línea de Acción</label>
                                    <textarea rows={3} className="w-full border border-gray-300 rounded-md p-2 text-xs resize-none focus:ring-2 focus:ring-indigo-500 outline-none" value={obj.action_line || ''} onChange={(e) => handleObjChange(idx, 'action_line', e.target.value)} />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-gray-600 mb-1">Responsable</label>
                                    <input className="w-full border border-gray-300 rounded-md p-2 text-sm" value={obj.responsible || ''} onChange={(e) => handleObjChange(idx, 'responsible', e.target.value)} />
                                </div>
                                
                                {/* Presupuesto USD */}
                                <div>
                                    <label className="block text-xs font-bold text-green-700 mb-1">Presupuesto (USD)</label>
                                    <div className="relative">
                                        <span className="absolute left-3 top-2 text-green-600 font-bold">$</span>
                                        <input 
                                            type="number" 
                                            className="w-full border border-green-200 bg-green-50 rounded-md p-2 pl-6 font-mono text-green-800 font-bold focus:ring-2 focus:ring-green-500 outline-none" 
                                            placeholder="0"
                                            value={obj.financing || ''} 
                                            onChange={(e) => handleObjChange(idx, 'financing', parseFloat(e.target.value))} 
                                        />
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                ))}
            </div>

            <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 shadow-lg z-20">
                <div className="max-w-6xl mx-auto flex justify-between items-center">
                    <button onClick={onBack} className="text-gray-500 font-bold hover:text-gray-900 px-6 py-2 transition-colors">
                        ← Volver a Contexto
                    </button>
                    <div className="text-xs text-gray-400 hidden md:block">
                        Asegúrate de que las unidades (%) coincidan con los valores ingresados.
                    </div>
                    <button
                        onClick={onSubmit}
                        disabled={isLoading}
                        className="bg-gray-900 hover:bg-black text-white px-8 py-3 rounded-lg font-bold shadow-lg transition-all disabled:opacity-50 flex items-center gap-2 transform hover:-translate-y-1"
                    >
                        {isLoading ? (
                            <>
                                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                                Analizando Datos...
                            </>
                        ) : (
                            <>✨ Generar Informe Final</>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ObjectivesForm;
