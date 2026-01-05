import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom' // <-- Importamos el paraguas
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <BrowserRouter> {/* <-- Envolvemos TODA la aplicación aquí */}
            <App />
        </BrowserRouter>
    </React.StrictMode>,
)