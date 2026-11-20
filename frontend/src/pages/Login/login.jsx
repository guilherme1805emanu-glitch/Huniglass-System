
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import api from '../../services/api'
import './login.css'

function Login() {
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [erro, setErro] = useState('')
  const [carregando, setCarregando] = useState(false)
  const [mostrarSenha, setMostrarSenha] = useState(false)

  const { login } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(event) {
    event.preventDefault()
    setErro('')
    setCarregando(true)

    try {
      const resposta = await api.post('/auth/login', {
        email,
        senha,
      })

      const dadosUsuario = resposta.data.dados

      if (!dadosUsuario?.token || !dadosUsuario?.cargo) {
        setErro('Não foi possível validar os dados de acesso.')
        return
      }

      login(dadosUsuario)

      // Por enquanto, o Dashboard é a única área interna criada.
      // As rotas específicas dos outros perfis serão adicionadas depois.
      const cargo = dadosUsuario.cargo.toLowerCase()

      if (['administrativo', 'socio'].includes(cargo)) {
        navigate('/dashboard', { replace: true })
      } else if (cargo === 'cliente') {
        navigate('/area-cliente', { replace: true })
      } else {
        setErro(
          'A área deste perfil ainda está sendo configurada. Entre em contato com o administrador.'
        )
      }      
    } catch (erroLogin) {
      console.error('Erro no login:', erroLogin)

      setErro(
        erroLogin.response?.status === 401
          ? 'E-mail ou senha incorretos.'
          : 'Não foi possível entrar. Verifique a conexão e tente novamente.'
      )
    } finally {
      setCarregando(false)
    }
  }

  return (
    <main className="login-page">
      <section className="login-brand">
        <Link to="/" className="login-logo">
          <span className="login-logo-mark">H</span>
          <span>
            <strong>HUNIGLASS</strong>
            <small>S Y S T E M</small>
          </span>
        </Link>

        <div className="login-brand-content">
          <span className="login-eyebrow">
            TECNOLOGIA • VIDRO • ALUMÍNIO
          </span>

          <h1>
            Bem-vindo à
            <span> Huniglass.</span>
          </h1>

          <p>
            Acesse sua conta para acompanhar projetos,
            atividades e operações.
          </p>
        </div>

        <div className="login-benefits">
          <div>
            <span className="benefit-icon">◈</span>
            <strong>Gestão integrada</strong>
            <small>Informações organizadas</small>
          </div>

          <div>
            <span className="benefit-icon">▤</span>
            <strong>Acompanhamento</strong>
            <small>Pedidos e atividades</small>
          </div>

          <div>
            <span className="benefit-icon">◇</span>
            <strong>Acesso seguro</strong>
            <small>Conforme suas permissões</small>
          </div>
        </div>

        <span className="login-brand-footer">
          HUNIGLASS SYSTEM · SOLUÇÕES EM VIDRO E ALUMÍNIO
        </span>
      </section>

      <section className="login-form-section">
        <div className="login-form-container">
          <Link to="/" className="login-back">
            ← Voltar para o início
          </Link>

          <div className="login-heading">
            <span className="login-heading-label">SUA CONTA</span>
            <h2>Entrar na sua conta</h2>
            <p>Informe seus dados para continuar.</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="login-field">
              <label htmlFor="email">E-mail</label>
              <input
                id="email"
                type="email"
                placeholder="seu@email.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                autoComplete="username"
                required
              />
            </div>

            <div className="login-field">
              <label htmlFor="senha">Senha</label>

              <div className="password-wrapper">
                <input
                  id="senha"
                  type={mostrarSenha ? 'text' : 'password'}
                  placeholder="Digite sua senha"
                  value={senha}
                  onChange={(event) => setSenha(event.target.value)}
                  autoComplete="current-password"
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setMostrarSenha(!mostrarSenha)}
                  aria-label={mostrarSenha ? 'Ocultar senha' : 'Mostrar senha'}
                >
                  {mostrarSenha ? 'Ocultar' : 'Mostrar'}
                </button>
              </div>
            </div>

            {erro && (
              <div className="login-error" role="alert">
                {erro}
              </div>
            )}

            <button
              type="submit"
              className="login-submit"
              disabled={carregando}
            >
              {carregando ? 'Verificando acesso...' : 'Entrar na plataforma'}
              {!carregando && <span>→</span>}
            </button>
          </form>

          <div className="login-register">
            <span>Você não possui cadastro?</span>
            {' '}
            <Link to="/cadastro-cliente">Cadastre-se</Link>
          </div>

          <p className="login-security">
            <span>◇</span> Acesso protegido · Huniglass System
          </p>
        </div>
      </section>
    </main>
  )
}

export default Login
