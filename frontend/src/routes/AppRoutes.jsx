
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from '../pages/Login/login.jsx'
import Home from '../pages/Home/home.jsx'
import CadastroCliente from '../pages/Clientes/CadastroCliente/cadastroCliente.jsx'
import { useAuth } from '../contexts/AuthContext.jsx'
import MainLayout from '../layouts/mainLayout.jsx'
import Dashboard from '../pages/Dashboard/dashboard.jsx'
import AreaCliente from '../pages/Clientes/AreaCliente/areaCliente.jsx'
import Clientes from '../pages/Clientes/clientes.jsx'


function AppRoutes() {
  const { usuario } = useAuth()

  return (
    <BrowserRouter>
      <Routes>
        {/* HOME INSTITUCIONAL */}
        <Route path="/" element={<Home />} />


        {/* LOGIN */}
        <Route
          path="/login"
          element={
            usuario ? (
              <Navigate
                to={
                  ['administrativo', 'socio'].includes(
                    String(usuario.cargo || '').toLowerCase()
                  )
                    ? '/dashboard'
                    : String(usuario.cargo || '').toLowerCase() === 'cliente'
                      ? '/area-cliente'
                      : '/'
                }
                replace
              />
            ) : (
              <Login />
            )
          }
        />

        {/* CADASTRO PÚBLICO DE CLIENTES */}
        <Route
          path="/cadastro-cliente"
          element={<CadastroCliente />}
        />

        {/* DASHBOARD */}
        <Route
          path="/dashboard"
          element={
            usuario ? (
              <MainLayout>
                <Dashboard />
              </MainLayout>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />

        <Route
          path="/clientes"
          element={
            usuario ? (
              <MainLayout>
                <Clientes />
              </MainLayout>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />s

        {/* ROTA DESCONHECIDA */}
        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />

        {/* ÁREA DO CLIENTE */}
        <Route
          path="/area-cliente"
          element={
            usuario?.cargo?.toLowerCase() === 'cliente'
              ? <AreaCliente />
              : usuario
                ? <Navigate to="/dashboard" replace />
                : <Navigate to="/login" replace />
          }
        />

      </Routes>
    </BrowserRouter>
  )
}

export default AppRoutes
