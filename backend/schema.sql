-- Esquema de Base de Datos para la Plataforma BSC 360° Analytics
-- Nota: La tabla 'users' es manejada automáticamente por Supabase Auth. 
-- Nos referiremos a ella a través de su UUID en nuestras tablas.

-- Tabla para almacenar la información general de cada análisis/empresa de un usuario.
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    name TEXT NOT NULL,
    industry TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
-- Habilitar Row Level Security (RLS) es mandatorio para la tabla 'companies'.
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;


-- Tabla para almacenar cada informe o análisis generado por la IA.
-- Se vincula a una empresa y a un usuario.
-- La cláusula ON DELETE CASCADE es crítica para el data integrity; garantiza que todos los datos de un usuario se eliminen si este es borrado de auth.users.
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    gemini_response TEXT, -- Almacena el texto completo del análisis de IA.
    generated_at TIMESTAMPTZ DEFAULT NOW()
);
-- Habilitar RLS es mandatorio para la tabla 'reports'.
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;


-- Tabla para almacenar los datos de mercado en el momento de la generación de un informe.
CREATE TABLE market_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_id UUID REFERENCES reports(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    sector_growth NUMERIC(5, 2),
    inflation NUMERIC(5, 2),
    interest_rate NUMERIC(5, 2),
    confidence_index INT
);
-- Habilitar RLS es mandatorio para la tabla 'market_data'.
ALTER TABLE market_data ENABLE ROW LEVEL SECURITY;


-- Tabla para los objetivos estratégicos de un informe, agrupados por perspectiva.
CREATE TABLE objectives (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_id UUID REFERENCES reports(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    perspective TEXT NOT NULL, -- ej. 'Financiera', 'Clientes', 'Procesos', 'Aprendizaje', 'ESG/ODS'
    name TEXT NOT NULL
);
-- Habilitar RLS es mandatorio para la tabla 'objectives'.
ALTER TABLE objectives ENABLE ROW LEVEL SECURITY;


-- Tabla para los KPIs asociados a cada objetivo estratégico.
CREATE TABLE kpis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    objective_id UUID REFERENCES objectives(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    name TEXT NOT NULL,
    current_value NUMERIC(10, 2) NOT NULL,
    target_value NUMERIC(10, 2) NOT NULL,
    unit TEXT
);
-- Habilitar RLS es mandatorio para la tabla 'kpis'.
ALTER TABLE kpis ENABLE ROW LEVEL SECURITY;


-- Políticas RLS: Permiten a los usuarios realizar todas las operaciones (SELECT, INSERT, UPDATE, DELETE) únicamente sobre sus propios registros.
CREATE POLICY "Los usuarios pueden gestionar sus propias compañías"
ON companies FOR ALL
USING (auth.uid() = user_id);

CREATE POLICY "Los usuarios pueden gestionar sus propios informes"
ON reports FOR ALL
USING (auth.uid() = user_id);

CREATE POLICY "Los usuarios pueden gestionar sus propios datos de mercado"
ON market_data FOR ALL
USING (auth.uid() = user_id);

CREATE POLICY "Los usuarios pueden gestionar sus propios objetivos"
ON objectives FOR ALL
USING (auth.uid() = user_id);

CREATE POLICY "Los usuarios pueden gestionar sus propios KPIs"
ON kpis FOR ALL
USING (auth.uid() = user_id);
