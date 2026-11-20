
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../../../services/api'
import './cadastroCliente.css'

function CadastroCliente() {
  const navigate = useNavigate()

  const [formulario, setFormulario] = useState({
    nome: '',
    email: '',
    telefone: '',
    cpf_cnpj: '',
    senha: '',
    confirmarSenha: '',
  })

  const [erro, setErro] = useState('')
  const [sucesso, setSucesso] = useState('')
  const [carregando, setCarregando] = useState(false)

  function handleChange(event) {
    const { name, value } = event.target

    setFormulario((anterior) => ({
      ...anterior,
      [name]: value,
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setErro('')
    setSucesso('')

    if (formulario.senha.length < 8) {
      setErro('A senha precisa ter pelo menos 8 caracteres.')
      return
    }

    if (formulario.senha !== formulario.confirmarSenha) {
      setErro('As senhas não coincidem.')
      return
    }

    setCarregando(true)

    try {
      const { confirmarSenha, ...dadosCliente } = formulario

      await api.post('/auth/cadastro-cliente', dadosCliente)

      setSucesso('Cadastro realizado! Você será direcionado para o login.')

      setTimeout(() => {
        navigate('/login', { replace: true })
      }, 1200)
    } catch (erroCadastro) {
      const mensagem = erroCadastro.response?.data?.mensagem

      setErro(
        mensagem ||
        'Não foi possível realizar o cadastro. Verifique os dados e tente novamente.'
      )
    } finally {
      setCarregando(false)
    }
  }

  return (
    <main className="cadastro-cliente-page">
      <section className="cadastro-cliente-brand">
        <Link to="/" className="cadastro-cliente-logo">
          <span className="cadastro-cliente-logo-mark">H</span>
          <span>
            <strong>HUNIGLASS</strong>
            <small>VIDRO E ALUMÍNIO</small>
          </span>
        </Link>

        <div className="cadastro-cliente-brand-content">
          <span className="cadastro-cliente-eyebrow">
            SUA EXPERIÊNCIA COMEÇA AQUI
          </span>

          <h1>
            Seu projeto merece
            <span> uma solução sob medida.</span>
          </h1>

          <p>
            Crie sua conta para facilitar o contato com a nossa equipe
            e dar o primeiro passo para transformar sua ideia em realidade.
          </p>
        </div>

        <p className="cadastro-cliente-footer">
          HUNIGLASS · SOLUÇÕES EM VIDRO E ALUMÍNIO
        </p>
      </section>

      <section className="cadastro-cliente-form-section">
        <div className="cadastro-cliente-container">
          <Link to="/" className="cadastro-cliente-back">
            ← Voltar ao site
          </Link>

          <header className="cadastro-cliente-heading">
            <span>CADASTRO DE CLIENTE</span>
            <h2>Crie sua conta</h2>
            <p>Preencha os dados para começar.</p>
          </header>

          <form
            className="cadastro-cliente-form"
            onSubmit={handleSubmit}
          >
            <div className="cadastro-cliente-field">
              <label htmlFor="nome">Nome completo *</label>
              <input
                id="nome"
                name="nome"
                value={formulario.nome}
                onChange={handleChange}
                placeholder="Digite seu nome completo"
                autoComplete="name"
                maxLength={150}
                required
              />
            </div>

            <div className="cadastro-cliente-field">
              <label htmlFor="email">E-mail *</label>
              <input
                id="email"
                name="email"
                type="email"
                value={formulario.email}
                onChange={handleChange}
                placeholder="voce@exemplo.com"
                autoComplete="email"
                maxLength={150}
                required
              />
            </div>

            <div className="cadastro-cliente-field">
              <label htmlFor="telefone">Telefone *</label>
              <input
                id="telefone"
                name="telefone"
                type="tel"
                value={formulario.telefone}
                onChange={handleChange}
                placeholder="(85) 99999-9999"
                autoComplete="tel"
                maxLength={20}
                required
              />
            </div>

            <div className="cadastro-cliente-field">
              <label htmlFor="cpf_cnpj">CPF ou CNPJ (opcional)</label>
              <input
                id="cpf_cnpj"
                name="cpf_cnpj"
                value={formulario.cpf_cnpj}
                onChange={handleChange}
                placeholder="Digite seu CPF ou CNPJ"
                maxLength={20}
              />
            </div>

            <div className="cadastro-cliente-field">
              <label htmlFor="senha">Senha *</label>
              <input
                id="senha"
                name="senha"
                type="password"
                value={formulario.senha}
                onChange={handleChange}
                placeholder="Mínimo de 8 caracteres"
                autoComplete="new-password"
                minLength={8}
                required
              />
            </div>

            <div className="cadastro-cliente-field">
              <label htmlFor="confirmarSenha">Confirmar senha *</label>
              <input
                id="confirmarSenha"
                name="confirmarSenha"
                type="password"
                value={formulario.confirmarSenha}
                onChange={handleChange}
                placeholder="Digite a senha novamente"
                autoComplete="new-password"
                minLength={8}
                required
              />
            </div>

            {erro && (
              <div className="cadastro-cliente-message error" role="alert">
                {erro}
              </div>
            )}

            {sucesso && (
              <div className="cadastro-cliente-message success" role="status">
                {sucesso}
              </div>
            )}

            <button
              type="submit"
              className="cadastro-cliente-submit"
              disabled={carregando}
            >
              {carregando ? 'CRIANDO CONTA...' : 'CRIAR MINHA CONTA'}
              {!carregando && <span>→</span>}
            </button>
          </form>

          <p className="cadastro-cliente-login">
            Já possui cadastro? <Link to="/login">Faça login</Link>
          </p>

          <p className="cadastro-cliente-security">
            Seus dados devem ser tratados com segurança.
          </p>
        </div>
      </section>
    </main>
  )
}

export default CadastroCliente
