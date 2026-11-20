
import { useEffect, useState } from 'react'
import api from '../../services/api'
import './clientes.css'
import FormularioCliente from './formulariocliente.jsx'

function Clientes() {
  const [clientes, setClientes] = useState([])
  const [busca, setBusca] = useState('')
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [clienteEditando, setClienteEditando] = useState(null)
  const [mensagemSucesso, setMensagemSucesso] = useState('')

  async function carregarClientes() {
    try {
      setErro('')
      setCarregando(true)

      const resposta = await api.get('/clientes/')

      const dados = Array.isArray(resposta.data)
        ? resposta.data
        : resposta.data?.dados

      setClientes(Array.isArray(dados) ? dados : [])
    } catch (error) {
      console.error('Erro ao carregar clientes:', error)
      setErro(
        error.response?.data?.mensagem ||
        'Não foi possível carregar os clientes. Verifique sua conexão com o servidor.'
      )
    } finally {
      setCarregando(false)
    }
  }

  useEffect(() => {
    carregarClientes()
  }, [])

  const clientesFiltrados = clientes.filter((cliente) => {
    const termo = busca.toLowerCase().trim()

    return (
      String(cliente.nome || '').toLowerCase().includes(termo) ||
      String(cliente.telefone || '').toLowerCase().includes(termo) ||
      String(cliente.email || '').toLowerCase().includes(termo)
    )
  })

  function abrirNovoCliente() {
    setMensagemSucesso('')
    setClienteEditando(null)
    setMostrarFormulario(true)
  }

  async function abrirEdicao(cliente) {
    setMensagemSucesso('')
    setErro('')

    try {
      // Busca os dados completos para preencher todos os campos.
      const resposta = await api.get(`/clientes/${cliente.id}`)

      const dados = resposta.data?.dados ?? resposta.data

      setClienteEditando(dados)
      setMostrarFormulario(true)
    } catch (error) {
      console.error('Erro ao buscar dados do cliente:', error)
      setErro(
        error.response?.data?.mensagem ||
        'Não foi possível carregar os dados deste cliente para edição.'
      )
    }
  }

  async function salvarCliente(editando) {
    setMostrarFormulario(false)
    setClienteEditando(null)

    setMensagemSucesso(
      editando
        ? 'Cliente atualizado com sucesso!'
        : 'Cliente cadastrado com sucesso!'
    )

    await carregarClientes()
  }

  
  async function excluirCliente(cliente) {
    const confirmado = window.confirm(
      `Tem certeza de que deseja excluir o cliente "${cliente.nome}"?\n\nEssa ação não poderá ser desfeita.`
    )

    if (!confirmado) return

    setErro('')
    setMensagemSucesso('')

    try {
      await api.delete(`/clientes/${cliente.id}`)

      setMensagemSucesso(
        `Cliente "${cliente.nome}" excluído com sucesso!`
      )

      await carregarClientes()
    } catch (error) {
      console.error('Erro ao excluir cliente:', error)

      setErro(
        error.response?.data?.mensagem ||
        'Não foi possível excluir o cliente. Verifique se existem orçamentos ou pedidos vinculados.'
      )
    }
  }


  function fecharFormulario() {
    setMostrarFormulario(false)
    setClienteEditando(null)
  }

  return (
    <main className="clientes-page">
      {mensagemSucesso && (
        <div className="clientes-sucesso" role="status">
          {mensagemSucesso}

          <button
            type="button"
            onClick={() => setMensagemSucesso('')}
            aria-label="Fechar mensagem"
          >
            ×
          </button>
        </div>
      )}

      <header className="clientes-header">
        <div>
          <span className="clientes-subtitulo">GESTÃO COMERCIAL</span>
          <h1>Clientes</h1>
          <p>Consulte e organize os clientes cadastrados na Huniglass.</p>
        </div>

        <button
          type="button"
          className="clientes-botao-principal"
          onClick={abrirNovoCliente}
        >
          <span>+</span> Novo cliente
        </button>
      </header>

      <section className="clientes-resumo">
        <div className="clientes-resumo-icone">
          <span>♙</span>
        </div>

        <div>
          <p>Total de clientes</p>
          <strong>{carregando ? '—' : clientes.length}</strong>
        </div>
      </section>

      <section className="clientes-lista">
        <div className="clientes-lista-header">
          <div>
            <h2>Todos os clientes</h2>
            <p>Pesquise os registros cadastrados no sistema.</p>
          </div>

          <button
            type="button"
            className="clientes-botao-atualizar"
            onClick={carregarClientes}
            disabled={carregando}
          >
            ↻ Atualizar
          </button>
        </div>

        <div className="clientes-pesquisa">
          <span>⌕</span>

          <input
            type="text"
            placeholder="Buscar por nome, telefone ou e-mail..."
            value={busca}
            onChange={(evento) => setBusca(evento.target.value)}
          />
        </div>

        {erro && (
          <div className="clientes-erro" role="alert">
            <p>{erro}</p>

            <button type="button" onClick={carregarClientes}>
              Tentar novamente
            </button>
          </div>
        )}

        {carregando ? (
          <div className="clientes-estado">
            Carregando clientes...
          </div>
        ) : !erro && clientesFiltrados.length === 0 ? (
          <div className="clientes-estado">
            <span className="clientes-estado-icone">♙</span>

            <h3>
              {busca
                ? 'Nenhum resultado encontrado'
                : 'Nenhum cliente cadastrado'}
            </h3>

            <p>
              {busca
                ? 'Tente pesquisar usando outro nome, telefone ou e-mail.'
                : 'Quando houver clientes cadastrados, eles aparecerão nesta lista.'}
            </p>
          </div>
        ) : !erro ? (
          <div className="clientes-tabela-wrapper">
            <table className="clientes-tabela">
              <thead>
                <tr>
                  <th>Cliente</th>
                  <th>Telefone</th>
                  <th>E-mail</th>
                  <th>ID</th>
                  <th>Ações</th>
                </tr>
              </thead>

              <tbody>
                {clientesFiltrados.map((cliente) => (
                  <tr key={cliente.id}>
                    <td>
                      <div className="cliente-identificacao">
                        <span className="cliente-avatar">
                          {String(cliente.nome || '?')
                            .charAt(0)
                            .toUpperCase()}
                        </span>

                        <strong>{cliente.nome}</strong>
                      </div>
                    </td>

                    <td>{cliente.telefone || 'Não informado'}</td>
                    <td>{cliente.email || 'Não informado'}</td>

                    <td>
                      <span className="cliente-id">#{cliente.id}</span>
                    </td>

                    
                    <td>
                      <div className="clientes-acoes">
                        <button
                          type="button"
                          className="clientes-botao-editar"
                          onClick={() => abrirEdicao(cliente)}
                        >
                          Editar
                        </button>

                        <button
                          type="button"
                          className="clientes-botao-excluir"
                          onClick={() => excluirCliente(cliente)}
                        >
                          Excluir
                        </button>
                      </div>
                    </td>

                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}

        {!carregando && !erro && clientesFiltrados.length > 0 && (
          <footer className="clientes-lista-footer">
            Exibindo {clientesFiltrados.length} de {clientes.length} clientes
          </footer>
        )}
      </section>

      {mostrarFormulario && (
        <FormularioCliente
          cliente={clienteEditando}
          aoFechar={fecharFormulario}
          aoSalvar={salvarCliente}
          

        />
      )}

      

    </main>
  )
}

export default Clientes
