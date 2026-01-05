import {
    Radar,
    RadarChart,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
    ResponsiveContainer
} from 'recharts';

interface AnalysisResultsProps {
    analysis: string;
    radarData: any[];
}

const AnalysisResults = ({ analysis, radarData }: AnalysisResultsProps) => {

    // Función para limpiar el texto y darle formato corporativo
    const formatCorporateText = (text: string) => {
        return text
            // 1. Limpieza de Títulos Grandes (###) -> Texto Grande Negro con línea divisoria
            .replace(/### (.*)/g, '<h3 class="text-xl font-bold text-gray-900 mt-8 mb-4 pb-2 border-b border-gray-200">$1</h3>')

            // 2. Limpieza de Subtítulos (####) -> Texto Mediano Negro
            .replace(/#### (.*)/g, '<h4 class="text-lg font-bold text-gray-800 mt-6 mb-2">$1</h4>')

            // 3. Negritas (**texto**) -> Solo un poco más oscuro, sin colores raros
            .replace(/\*\*(.*?)\*\*/g, '<span class="font-bold text-gray-900">$1</span>')

            // 4. Listas (* item) -> Convertir asteriscos en "bullets" visuales limpios
            .replace(/\n\* /g, '<br/><span class="text-indigo-600 font-bold mr-2">•</span>')

            // 5. Limpieza final de basura Markdown que pudiera quedar
            .replace(/###/g, '') // Por si queda algún ### suelto
            .replace(/\n/g, '<br />');
    };

    // Extraemos el diagnóstico breve para la tarjeta superior
    const diagnosisMatch = analysis.match(/\*\*Diagnóstico Global:\*\*(.*?)(?=\.)/s);
    const shortDiagnosis = diagnosisMatch
        ? diagnosisMatch[1].replace(/\*/g, '').trim() + "."
        : "Análisis estratégico completado. Revisa el detalle abajo.";

    return (
        <div className="space-y-8 animate-in fade-in duration-700">

            {/* --- SECCIÓN SUPERIOR: VISUALIZACIÓN --- */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                {/* GRÁFICO DE RADAR */}
                <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200 flex flex-col">
                    <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wide mb-4 text-center">
                        Cobertura Estratégica 360°
                    </h3>
                    <div className="h-80 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
                                <PolarGrid stroke="#e5e7eb" />
                                <PolarAngleAxis
                                    dataKey="subject"
                                    tick={{ fill: '#374151', fontSize: 11, fontWeight: 600 }}
                                />
                                <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                                <Radar
                                    name="Cumplimiento"
                                    dataKey="A"
                                    stroke="#4f46e5"
                                    strokeWidth={2}
                                    fill="#6366f1"
                                    fillOpacity={0.3}
                                />
                            </RadarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* RESUMEN EJECUTIVO (Tarjeta destacada) */}
                <div className="bg-gray-900 p-8 rounded-xl shadow-lg text-white flex flex-col justify-center relative">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                        <svg width="100" height="100" viewBox="0 0 24 24" fill="white"><path d="M12 2L2 7l10 5 10-5-10-5zm0 9l2.5-1.25L12 8.5l-2.5 1.25L12 11zm0 2.5l-5-2.5-5 2.5L12 22l10-8.5-5-2.5-5 2.5z" /></svg>
                    </div>

                    <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-indigo-400">
                        Estado Estratégico
                    </h3>

                    <p className="text-gray-300 text-lg leading-relaxed font-light">
                        "{shortDiagnosis}"
                    </p>

                    <div className="mt-8 pt-6 border-t border-gray-700 flex gap-4 text-sm text-gray-400">
                        <div className="flex flex-col">
                            <span className="font-bold text-white">Empresas Copec S.A.</span>
                            <span>Reporte Corporativo 2026</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* --- SECCIÓN INFERIOR: INFORME DETALLADO (FORMATO DOCUMENTO) --- */}
            <div className="bg-white p-10 rounded-xl shadow-md border border-gray-200">
                <div className="flex justify-between items-end mb-8 border-b border-gray-200 pb-4">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Informe Detallado</h1>
                        <p className="text-gray-500 mt-1">Generado por BSC 360° AI Engine</p>
                    </div>
                    <button
                        onClick={() => window.print()}
                        className="bg-gray-900 hover:bg-black text-white px-5 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
                    >
                        <span>🖨️</span> Imprimir / Guardar PDF
                    </button>
                </div>

                {/* CONTENIDO DEL INFORME CON ESTILO LIMPIO */}
                <div
                    className="prose prose-lg max-w-none text-gray-600 leading-relaxed"
                    dangerouslySetInnerHTML={{ __html: formatCorporateText(analysis) }}
                />
            </div>
        </div>
    );
};

export default AnalysisResults;