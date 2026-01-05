// @ts-nocheck
import { useState } from 'react';
import { supabase } from '@/lib/supabaseClient';
import CompanyContextForm from '@/components/CompanyContextForm';
import ObjectivesForm from '@/components/ObjectivesForm';
import AnalysisResults from '@/components/AnalysisResults';
import { analyzeData } from '@/lib/api';

const Dashboard = () => {
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [analysisData, setAnalysisData] = useState(null);

    // ESTRUCTURA MAESTRA DE DATOS
    const [formData, setFormData] = useState({
        company_data: { name: '', industry: '' },
        market_data: { sector_growth: 0, inflation: 0, interest_rate: 0, confidence_index: 0 },
        bsc_objectives: []
    });

    // --- MANEJADORES DEL PASO 1 (CONTEXTO) ---
    const handleContextUpdate = (newData) => {
        // Actualizamos estado sin perder lo que ya teníamos
        setFormData(prev => ({
            ...prev,
            company_data: newData.company_data,
            market_data: newData.market_data,
            // Si la demo trae objetivos, los guardamos también
            bsc_objectives: newData.bsc_objectives || prev.bsc_objectives
        }));
    };

    // --- MANEJADORES DEL PASO 2 (OBJETIVOS) ---
    const handleObjectivesUpdate = (newObjectives) => {
        setFormData(prev => ({
            ...prev,
            bsc_objectives: newObjectives
        }));
    };

    // --- ENVÍO FINAL A LA IA ---
    const handleFinalSubmit = async () => {
        const objectives = formData.bsc_objectives;
        console.log("🚀 Iniciando análisis con objetivos:", objectives);

        setLoading(true);
        setError(null);

        try {
            // Empaquetamos para Python
            const payload = {
                company_name: formData.company_data.name || "Empresa",
                industry: formData.company_data.industry || "General",
                objectives: objectives, // <--- Aquí van los datos reales
                market_data: formData.market_data
            };

            console.log("📤 Payload enviado:", payload);

            const result = await analyzeData(payload);
            console.log("📥 Respuesta recibida:", result);

            if (!result) throw new Error("La IA no respondió.");

            setAnalysisData({
                analysis: result.strategic_analysis,
                radar: result.radar_chart
            });
            setStep(3);

        } catch (err) {
            console.error("❌ Error:", err);
            setError("Error: " + (err.message || "Fallo de conexión"));
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setStep(1);
        setAnalysisData(null);
        setFormData({
            company_data: { name: '', industry: '' },
            market_data: { sector_growth: 0, inflation: 0, interest_rate: 0, confidence_index: 0 },
            bsc_objectives: []
        });
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            <header className="bg-white shadow-sm p-4">
                <div className="max-w-7xl mx-auto flex justify-between items-center">
                    <h1 className="text-xl font-bold text-indigo-600">BSC Analytics 360°</h1>
                    <button onClick={() => supabase.auth.signOut()} className="text-sm text-red-500 hover:underline">
                        Cerrar Sesión
                    </button>
                </div>
            </header>

            <main className="flex-grow p-6">
                <div className="max-w-5xl mx-auto">

                    {error && !loading && (
                        <div className="bg-red-100 text-red-700 p-4 mb-6 rounded border border-red-300">
                            <p className="font-bold">Error:</p>
                            <p>{error}</p>
                            <button onClick={() => setLoading(false)} className="underline mt-2">Reintentar</button>
                        </div>
                    )}

                    {/* Lógica de Pasos */}

                    {step === 1 && (
                        // PASO 1: CONTEXTO
                        // Usa 'data' porque así lo pide tu componente
                        <CompanyContextForm
                            data={formData}
                            onUpdate={handleContextUpdate}
                            onNext={() => setStep(2)}
                        />
                    )}

                    {step === 2 && (
                        // PASO 2: OBJETIVOS
                        // Usa 'objectives' porque así lo pide tu componente (¡ESTO ARREGLA EL CRASH!)
                        <ObjectivesForm
                            objectives={formData.bsc_objectives}
                            onUpdate={handleObjectivesUpdate}
                            onBack={() => setStep(1)}
                            onSubmit={handleFinalSubmit}
                            isLoading={loading}
                        />
                    )}

                    {step === 3 && analysisData && (
                        // PASO 3: RESULTADOS
                        <div>
                            <button onClick={handleReset} className="mb-4 text-indigo-600 font-medium hover:underline">
                                ← Nuevo Análisis
                            </button>
                            <AnalysisResults
                                analysis={analysisData.analysis}
                                radarData={analysisData.radar}
                            />
                        </div>
                    )}

                </div>
            </main>
        </div>
    );
};

export default Dashboard;