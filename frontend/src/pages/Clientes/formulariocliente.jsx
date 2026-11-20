
import { useEffect, useState } from 'react'
import api from '../../services/api'
import './formulariocliente.css'

const dadosIniciais = {
  nome: '',
  telefone: '',
  email: '',
  cpf_cnpj: '',
  endereco: '',
  cidade: '',
  estado: '',
  observacoes: '',
}

function FormularioCliente({ aoFechar, aoSalvar, cliente = null }) {
  const [formulario, setFormulario] = useState(dadosIniciais)
  const [salvando, setSalvando] = useState(false)
  const [erro, setErro] = useState('')

  const editando = Boolean(cliente?.id)

  useEffect(() => {
    if (cliente) {
      setFormulario({
        nome: cliente.nome || '',
        telefone: cliente.telefone || '',
        email: cliente.email || '',
        cpf_cnpj: cliente.cpf_cnpj || '',
        endereco: cliente.endereco || '',
        cidade: cliente.cidade || '',
        estado: cliente.estado || '',
        observacoes: cliente.observacoes || '',
      })
    } else {
      setFormulario(dadosIniciais)
    }
  }, [cliente])

  function atualizarCampo(evento) {
    const { name, value } = evento.target

    setFormulario((anterior) => ({
      ...anterior,
      [name]: value,
    }))
  }

  async function enviarFormulario(evento) {
    evento.preventDefault()
    setErro('')

    if (!formulario.nome.trim()) {
      setErro('Informe o nome do cliente.')
      return
    }

    if (!formulario.telefone.trim()) {
      setErro('Informe o telefone do cliente.')
      return
    }

    const dados = {
      ...formulario,
      nome: formulario.nome.trim(),
      telefone: formulario.telefone.trim(),
      email: formulario.email.trim(),
      cpf_cnpj: formulario.cpf_cnpj.trim(),
      endereco: formulario.endereco.trim(),
      cidade: formulario.cidade.trim(),
      estado: formulario.estado.trim(),
      observacoes: formulario.observacoes.trim(),
    }

    try {
      setSalvando(true)

      if (editando) {
        await api.put(`/clientes/${cliente.id}`, dados)
      } else {
        await api.post('/clientes/', dados)
      }

      await aoSalvar(editando)
    } catch (error) {
      console.error(
        editando ? 'Erro ao editar cliente:' : 'Erro ao cadastrar cliente:',
        error
      )

      const resposta = error.response?.data
      const detalhes = resposta?.detalhes

      let mensagem =
        resposta?.mensagem ||
        `Não foi possível ${editando ? 'atualizar' : 'cadastrar'} o cliente. Verifique os dados e tente novamente.`

      if (detalhes && typeof detalhes === 'object') {
        const primeiroErro = Object.values(detalhes).flat()[0]

        if (typeof primeiroErro === 'string') {
          mensagem = primeiroErro
        }
      }

      setErro(mensagem)
    } finally {
      setSalvando(false)
    }
  }

  return (
    <div
      className="form-cliente-overlay"
      onMouseDown={(evento) => {
        if (evento.target === evento.currentTarget && !salvando) {
          aoFechar()
        }
      }}
    >
      <section
        className="form-cliente-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="titulo-form-cliente"
      >
        <header className="form-cliente-header">
          <div>
            <span className="form-cliente-etiqueta">
              GESTÃO COMERCIAL
            </span>

            <h2 id="titulo-form-cliente">
              {editando ? 'Editar cliente' : 'Novo cliente'}
            </h2>

            <p>
              {editando
                ? 'Atualize as informações do cliente cadastrado.'
                : 'Preencha as informações para cadastrar um cliente.'}
            </p>
          </div>

          <button
            type="button"
            className="form-cliente-fechar"
            onClick={aoFechar}
            disabled={salvando}
            aria-label="Fechar formulário"
          >
            ×
          </button>
        </header>

        <form onSubmit={enviarFormulario}>
          <div className="form-cliente-conteudo">
            <div className="form-cliente-secao">
              <h3>Informações principais</h3>
              <p>Os campos com * são obrigatórios.</p>
            </div>

            <div className="form-cliente-grid">
              <label className="campo-cliente campo-largo">
                Nome completo ou razão social *
                <input
                  name="nome"
                  value={formulario.nome}
                  onChange={atualizarCampo}
                  placeholder="Digite o nome do cliente"
                  maxLength={150}
                  required
                  autoFocus
                />
              </label>

              <label className="campo-cliente">
                Telefone *
                <input
                  name="telefone"
                  type="tel"
                  value={formulario.telefone}
                  onChange={atualizarCampo}
                  placeholder="(85) 99999-9999"
                  maxLength={30}
                  required
                />
              </label>

              <label className="campo-cliente">
                E-mail
                <input
                  name="email"
                  type="email"
                  value={formulario.email}
                  onChange={atualizarCampo}
                  placeholder="cliente@email.com"
                  maxLength={150}
                />
              </label>

              <label className="campo-cliente campo-largo">
                CPF ou CNPJ
                <input
                  name="cpf_cnpj"
                  value={formulario.cpf_cnpj}
                  onChange={atualizarCampo}
                  placeholder="Digite o CPF ou CNPJ"
                  maxLength={20}
                />
              </label>
            </div>

            <div className="form-cliente-secao">
              <h3>Endereço</h3>
              <p>Informações para contato e atendimento.</p>
            </div>

            <div className="form-cliente-grid">
              <label className="campo-cliente campo-largo">
                Rua, número e complemento
                <input
                  name="endereco"
                  value={formulario.endereco}
                  onChange={atualizarCampo}
                  placeholder="Rua, número, bairro e complemento"
                  maxLength={250}
                />
              </label>

              <label className="campo-cliente">
                Cidade
                <input
                  name="cidade"
                  value={formulario.cidade}
                  onChange={atualizarCampo}
                  placeholder="Ex.: Fortaleza"
                  maxLength={100}
                />
              </label>

              <label className="campo-cliente">
                Estado
                <select
                  name="estado"
                  value={formulario.estado}
                  onChange={atualizarCampo}
                >
                  <option value="">Selecione</option>
                  <option value="AC">Acre</option>
                  <option value="AL">Alagoas</option>
                  <option value="AP">Amapá</option>
                  <option value="AM">Amazonas</option>
                  <option value="BA">Bahia</option>
                  <option value="CE">Ceará</option>
                  <option value="DF">Distrito Federal</option>
                  <option value="ES">Espírito Santo</option>
                  <option value="GO">Goiás</option>
                  <option value="MA">Maranhão</option>
                  <option value="MT">Mato Grosso</option>
                  <option value="MS">Mato Grosso do Sul</option>
                  <option value="MG">Minas Gerais</option>
                  <option value="PA">Pará</option>
                  <option value="PB">Paraíba</option>
                  <option value="PR">Paraná</option>
                  <option value="PE">Pernambuco</option>
                  <option value="PI">Piauí</option>
                  <option value="RJ">Rio de Janeiro</option>
                  <option value="RN">Rio Grande do Norte</option>
                  <option value="RS">Rio Grande do Sul</option>
                  <option value="RO">Rondônia</option>
                  <option value="RR">Roraima</option>
                  <option value="SC">Santa Catarina</option>
                  <option value="SP">São Paulo</option>
                  <option value="SE">Sergipe</option>
                  <option value="TO">Tocantins</option>
                </select>
              </label>

              <label className="campo-cliente campo-largo">
                Observações
                <textarea
                  name="observacoes"
                  value={formulario.observacoes}
                  onChange={atualizarCampo}
                  placeholder="Informações adicionais sobre o cliente..."
                  rows={3}
                  maxLength={1000}
                />
              </label>
            </div>

            {erro && (
              <div className="form-cliente-erro" role="alert">
                <strong>Não foi possível salvar.</strong>
                <p>{erro}</p>
              </div>
            )}
          </div>

          <footer className="form-cliente-acoes">
            <button
              type="button"
              className="form-cliente-cancelar"
              onClick={aoFechar}
              disabled={salvando}
            >
              Cancelar
            </button>

            <button
              type="submit"
              className="form-cliente-salvar"
              disabled={salvando}
            >
              {salvando
                ? 'Salvando...'
                : editando
                  ? 'Salvar alterações'
                  : 'Salvar cliente'}
            </button>
          </footer>
        </form>
      </section>
    </div>
  )
}

export default FormularioCliente
