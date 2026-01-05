// @ts-nocheck
import { 
    Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
    ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip 
} from 'recharts';

interface AnalysisResultsProps {
    analysis: string;
    radarData: any[];
    stats?: {
        total_objectives: number;
        avg_progress: number;
        near_target: number;
    };
}

const AnalysisResults = ({ analysis, radarData, stats }: AnalysisResultsProps) => {
    const formatCorporateText = (text: string) => {
        return text
            .replace(/### (.*)/g, '<h3 class="text-xl font-bold text-gray-900 mt-8 mb-4 pb-2 border-b border-gray-200">$1</h3>')
            .replace(/#### (.*)/g, '<h4 class="text-lg font-bold text-gray-800 mt-6 mb-2">$1</h4>')
            .replace(/\*\*(.*?)\*\*/g, '<span class="font-bold text-gray-900">$1</span>')
            .replace(/\n\* /g, '<br/><span class="text-indigo-600 font-bold mr-2">•</span>')
            .replace(/\n/g, '<br />');
    };

    return (
        <div className="space-y-8 animate-in fade-in duration-700">
            
            {/* --- 1. TARJETAS DE ESTADÍSTICAS (IGUAL A LA FOTO) --- */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-indigo-600 p-6 rounded-xl shadow-lg text-white">
                    <p className="text-indigo-100 text-sm font-bold uppercase">Total Objetivos</p>
                    <h2 className="text-4xl font-black mt-2">{stats?.total_objectives || 10}</h2>
                </div>
                <div className="bg-indigo-500 p-6 rounded-xl shadow-lg text-white">
                    <p className="text-indigo-100 text-sm font-bold uppercase">Progreso Promedio</p>
                    <h2 className="text-4xl font-black mt-2">{stats?.avg_progress || 92.1}%</h2>
                </div>
                <div className="bg-indigo-400 p-6 rounded-xl shadow-lg text-white">
                    <p className="text-indigo-100 text-sm font-bold uppercase">Cerca de Meta</p>
                    <h2 className="text-4xl font-black mt-2">{stats?.near_target || 2}</h2>
                </div>
                <div className="bg-indigo-300 p-6 rounded-xl shadow-lg text-white">
                    <p className="text-indigo-100 text-sm font-bold uppercase">Perspectivas</p>
                    <h2 className="text-4xl font-black mt-2">5</h2>
                </div>
            </div>

            {/* --- 2. GRÁFICOS LADO A LADO --- */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                
                {/* GRÁFICO DE BARRAS: PROGRESO POR PERSPECTIVA */}
                <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                    <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wide mb-6 flex items-center gap-2">
                        <span>📊</span> Progreso por Perspectiva
                    </h3>
                    <div className="h-80 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={radarData}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                                <XAxis dataKey="subject" tick={{fontSize: 10}} />
                                <YAxis domain={[0, 100]} tick={{fontSize: 10}} />
                                <Tooltip />
                                <Bar dataKey="A" fill="#4f46e5" radius={[4, 4, 0, 0]} barSize={40} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* GRÁFICO DE RADAR: VISTA 360° */}
                <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                    <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wide mb-6 flex items-center gap-2">
                        <span>🕸️</span> Vista 360°
                    </h3>
                    <div className="h-80 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
                                <PolarGrid stroke="#e5e7eb" />
                                <PolarAngleAxis dataKey="subject" tick={{ fill: '#374151', fontSize: 11, fontWeight: 600 }} />
                                <PolarRadiusAxis domain={[0, 100]} tick={false} axisLine={false} />
                                <Radar name="Avance" dataKey="A" stroke="#4f46e5" strokeWidth={2} fill="#6366f1" fillOpacity={0.4} />
                            </RadarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* --- 3. INFORME DETALLADO --- */}
            <div className="bg-white p-10 rounded-xl shadow-md border border-gray-200">
                <div className="flex justify-between items-end mb-8 border-b border-gray-200 pb-4">
                    <h1 className="text-3xl font-bold text-gray-900">Análisis Estratégico Completo</h1>
                    <button onClick={() => window.print()} className="bg-gray-900 text-white px-5 py-2 rounded-lg text-sm font-medium transition-colors">
                        🖨️ Guardar PDF
                    </button>
                </div>
                <div className="prose prose-lg max-w-none text-gray-600" dangerouslySetInnerHTML={{ __html: formatCorporateText(analysis) }} />
            </div>
        </div>
    );
};

export default AnalysisResults;
