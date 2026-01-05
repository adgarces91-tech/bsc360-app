// @ts-nocheck
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

function App() {
    return (
        <Routes>
            {/* 1. La ruta raíz ("/") ahora muestra el Login */}
            <Route path="/" element={<Login />} />

            {/* 2. La ruta "/login" también muestra el Login */}
            <Route path="/login" element={<Login />} />

            {/* 3. La ruta "/dashboard" muestra tu súper Dashboard */}
            <Route path="/dashboard" element={<Dashboard />} />

            {/* 4. Cualquier otra ruta desconocida te manda al Login */}
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
}

export default App;