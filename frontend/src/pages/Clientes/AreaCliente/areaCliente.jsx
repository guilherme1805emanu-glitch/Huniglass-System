
import { Link } from 'react-router-dom'
import { useAuth } from '../../../contexts/AuthContext'

function AreaCliente() {
  const { usuario, logout } = useAuth()

  return (
    <main style={{
      minHeight: '100vh',
      padding: '40px 24px',
      boxSizing: 'border-box',
      background: '#f4f8fc',
      color: '#122b49',
      fontFamily: 'Inter, Segoe UI, Arial, sans-serif'
    }}>
      <header style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '16px',
        maxWidth: '1000px',
        margin: '0 auto'
      }}>
        <Link to="/" style={{
          color: '#0b477f',
          fontSize: '20px',
          fontWeight: 800,
          letterSpacing: '2px',
          textDecoration: 'none'
        }}>
          HUNIGLASS
        </Link>

        <button
          onClick={() => {
            logout()
            window.location.href = '/login'
          }}
          style={{
            padding: '11px 18px',
            border: '1px solid #d5e0ed',
            borderRadius: '8px',
            background: '#fff',
            color: '#173554',
            cursor: 'pointer'
          }}
        >
          Sair da conta
        </button>
      </header>

      <section style={{
        maxWidth: '1000px',
        margin: '60px auto 0'
      }}>
        <p style={{
          color: '#0876cf',
          fontSize: '12px',
          fontWeight: 800,
          letterSpacing: '2px'
        }}>
          ÁREA DO CLIENTE
        </p>

        <h1 style={{ fontSize: 'clamp(28px, 5vw, 42px)' }}>
          Olá, {usuario?.nome || 'cliente'}!
        </h1>

        <p style={{ color: '#647991', lineHeight: 1.7 }}>
          Bem-vindo à Huniglass. Aqui ficará o espaço para solicitar
          orçamentos e acompanhar seus projetos.
        </p>

        <article style={{
          marginTop: '32px',
          padding: '28px',
          border: '1px solid #e0e9f3',
          borderRadius: '16px',
          background: '#fff'
        }}>
          <h2 style={{ marginTop: 0 }}>Seus projetos</h2>
          <p style={{ color: '#647991', lineHeight: 1.7 }}>
            Estamos preparando esta área para você acompanhar suas
            solicitações e os próximos passos do seu projeto.
          </p>

          <Link to="/" style={{
            display: 'inline-block',
            marginTop: '12px',
            padding: '13px 18px',
            borderRadius: '8px',
            background: '#0b477f',
            color: '#fff',
            fontWeight: 700,
            textDecoration: 'none'
          }}>
            Conhecer nossos serviços
          </Link>
        </article>
      </section>
    </main>
  )
}

export default AreaCliente
