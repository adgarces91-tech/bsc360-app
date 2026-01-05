import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [error, setError] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        // --- AQUÍ ESTÁ EL TRUCO (LOGIN FALSO) ---
        if (formData.username.toLowerCase() === 'michelle' && formData.password === '1234') {
            // Si coincide, mandamos al usuario al Dashboard
            navigate('/dashboard');
        } else {
            // Si no, mostramos error
            setError('Credenciales incorrectas. Intenta con michelle / 1234');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100">

                {/* LOGO O TÍTULO */}
                <div className="text-center mb-8">
                    <div className="bg-indigo-600 text-white w-12 h-12 rounded-lg flex items-center justify-center text-xl font-bold mx-auto mb-4">
                        360
                    </div>
                    <h2 className="text-2xl font-bold text-gray-800">Bienvenido de nuevo</h2>
                    <p className="text-gray-500 text-sm">Ingresa a la Plataforma BSC Analytics</p>
                </div>

                {/* FORMULARIO */}
                <form onSubmit={handleSubmit} className="space-y-6">

                    {/* Usuario */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Usuario</label>
                        <input
                            type="text"
                            placeholder="Ej. michelle"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                            value={formData.username}
                            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                        />
                    </div>

                    {/* Contraseña */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
                        <input
                            type="password"
                            placeholder="••••"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                        />
                    </div>

                    {/* Mensaje de Error */}
                    {error && (
                        <div className="text-red-500 text-sm text-center bg-red-50 p-2 rounded">
                            {error}
                        </div>
                    )}

                    {/* Botón */}
                    <button
                        type="submit"
                        className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-lg shadow-md transition-all transform hover:-translate-y-0.5"
                    >
                        Iniciar Sesión
                    </button>
                </form>

                <div className="mt-6 text-center text-xs text-gray-400">
                    Versión Demo Tesis 1.0
                </div>
            </div>
        </div>
    );
};

export default Login;