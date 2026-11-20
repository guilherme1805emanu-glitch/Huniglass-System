
import { useCallback, useEffect, useState } from 'react'
import api from '../../services/api'
import './dashboard.css'

const SECOES = [
  { chave: 'resumo', titulo: 'Visão financeira' },
  { chave: 'operacao', titulo: 'Operação' },
  { chave: 'instalacoes', titulo: 'Instalações' },
  { chave: 'estoque', titulo: 'Estoque' },
]

function formatarMoeda(valor) {
  return Number(valor ?? 0).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
}

function formatarNumero(valor) {
  return Number(valor ?? 0).toLocaleString('pt-BR')
}

function Cartao({ titulo, valor, tipo = 'numero', destaque = false, descricao }) {
  return (
    <article className={`dashboard-card ${destaque ? 'dashboard-card-destaque' : ''}`}>
      <span className="dashboard-card-titulo">{titulo}</span>
      <strong className="dashboard-card-valor">
        {tipo === 'moeda' ? formatarMoeda(valor) : formatarNumero(valor)}
      </strong>
      {descricao && <small className="dashboard-card-descricao">{descricao}</small>}
    </article>
  )
}

function Dashboard() {
  const [dados, setDados] = useState({
    resumo: null,
    pedidos: null,
    producao: null,
    instalacoes: null,
    estoque: null,
  })

  const [carregando, setCarregando] = useState(true)
  const [atualizando, setAtualizando] = useState(false)
  const [erros, setErros] = useState([])
  const [ultimaAtualizacao, setUltimaAtualizacao] = useState(null)

  const carregarDados = useCallback(async (silencioso = false) => {
    if (silencioso) {
      setAtualizando(true)
    } else {
      setCarregando(true)
    }

    setErros([])

    const requisicoes = [
      ['resumo', '/dashboard/resumo'],
      ['pedidos', '/dashboard/pedidos'],
      ['producao', '/dashboard/producao'],
      ['instalacoes', '/dashboard/instalacoes'],
      ['estoque', '/dashboard/estoque'],
    ]

    const resultados = await Promise.allSettled(
      requisicoes.map(([, endpoint]) => api.get(endpoint))
    )

    const novosDados = { ...dados }
    const novasFalhas = []

    resultados.forEach((resultado, indice) => {
      const [chave, endpoint] = requisicoes[indice]

      if (resultado.status === 'fulfilled') {
        novosDados[chave] = resultado.value.data?.dados ?? null
      } else {
        console.error(`Erro ao carregar ${endpoint}:`, resultado.reason)
        novasFalhas.push(endpoint)
      }
    })

    setDados(novosDados)
    setErros(novasFalhas)
    setUltimaAtualizacao(new Date())
    setCarregando(false)
    setAtualizando(false)
  }, [dados])

  useEffect(() => {
    carregarDados()

    // A atualização é manual pelo botão da dashboard.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const { resumo, pedidos, producao, instalacoes, estoque } = dados

  const temDados = Object.values(dados).some((item) => item !== null)

  if (carregando) {
    return (
      <main className="dashboard">
        <header className="dashboard-header">
          <div>
            <span className="dashboard-eyebrow">HUNIGLASS SYSTEM</span>
            <h1>Dashboard</h1>
            <p>Preparando os indicadores da sua empresa...</p>
          </div>
        </header>

        <div className="dashboard-loading" role="status">
          <span className="dashboard-spinner" />
          <span>Carregando informações...</span>
        </div>
      </main>
    )
  }

  if (!temDados && erros.length > 0) {
    return (
      <main className="dashboard">
        <header className="dashboard-header">
          <div>
            <span className="dashboard-eyebrow">HUNIGLASS SYSTEM</span>
            <h1>Dashboard</h1>
            <p>Não foi possível carregar os indicadores.</p>
          </div>
        </header>

        <div className="dashboard-alert dashboard-alert-erro" role="alert">
          <strong>Falha ao carregar os dados</strong>
          <p>Verifique sua conexão com o servidor e tente novamente.</p>
          <button
            className="dashboard-btn"
            onClick={() => carregarDados()}
          >
            Tentar novamente
          </button>
        </div>
      </main>
    )
  }

  return (
    <main className="dashboard">
      <header className="dashboard-header">
        <div>
          <span className="dashboard-eyebrow">HUNIGLASS SYSTEM</span>
          <h1>Dashboard</h1>
          <p>Acompanhe os indicadores e a operação da sua empresa.</p>
        </div>

        <button
          className="dashboard-btn"
          onClick={() => carregarDados(true)}
          disabled={atualizando}
        >
          <span className={atualizando ? 'dashboard-spinner dashboard-spinner-btn' : ''}>
            {!atualizando && '↻'}
          </span>
          {atualizando ? 'Atualizando...' : 'Atualizar dados'}
        </button>
      </header>

      {erros.length > 0 && (
        <div className="dashboard-alert" role="status">
          <strong>Alguns dados não puderam ser atualizados.</strong>
          <p>
            As demais informações continuam disponíveis. Tente atualizar
            novamente em instantes.
          </p>
        </div>
      )}

      {resumo && (
        <section className="dashboard-section">
          <div className="dashboard-section-header">
            <div>
              <span className="dashboard-section-indice">01 / FINANCEIRO</span>
              <h2>Visão financeira</h2>
            </div>
            <span className="dashboard-section-legenda">Resumo financeiro</span>
          </div>

          <div className="dashboard-cards">
            <Cartao
              titulo="Receitas"
              valor={resumo.total_receitas}
              tipo="moeda"
              descricao="Total registrado"
            />
            <Cartao
              titulo="Despesas"
              valor={resumo.total_despesas}
              tipo="moeda"
              descricao="Total registrado"
            />
            <Cartao
              titulo="Saldo"
              valor={resumo.saldo}
              tipo="moeda"
              destaque
              descricao="Resultado financeiro informado pela API"
            />
            <Cartao
              titulo="Valores pendentes"
              valor={resumo.total_pendente}
              tipo="moeda"
              descricao="Aguardando recebimento ou regularização"
            />
            <Cartao
              titulo="Lançamentos"
              valor={resumo.quantidade_lancamentos}
              descricao="Registros financeiros"
            />
          </div>
        </section>
      )}

      {(pedidos || producao) && (
        <section className="dashboard-section">
          <div className="dashboard-section-header">
            <div>
              <span className="dashboard-section-indice">02 / OPERAÇÃO</span>
              <h2>Pedidos e produção</h2>
            </div>
          </div>

          <div className="dashboard-cards">
            {pedidos && (
              <>
                <Cartao titulo="Total de pedidos" valor={pedidos.total_pedidos} />
                <Cartao
                  titulo="Aguardando produção"
                  valor={pedidos.aguardando_producao}
                  descricao="Pedidos nessa etapa"
                />
              </>
            )}

            {producao && (
              <>
                <Cartao titulo="Total de produções" valor={producao.total_producoes} />
                <Cartao
                  titulo="Produções aguardando"
                  valor={producao.aguardando}
                  descricao="Itens pendentes nessa etapa"
                />
              </>
            )}
          </div>
        </section>
      )}

      {instalacoes && (
        <section className="dashboard-section">
          <div className="dashboard-section-header">
            <div>
              <span className="dashboard-section-indice">03 / SERVIÇOS</span>
              <h2>Instalações</h2>
            </div>
          </div>

          <div className="dashboard-cards">
            <Cartao titulo="Total de instalações" valor={instalacoes.total_instalacoes} />
            <Cartao titulo="Agendadas" valor={instalacoes.agendadas} />
            <Cartao titulo="Em andamento" valor={instalacoes.em_andamento} />
            <Cartao titulo="Concluídas" valor={instalacoes.concluidas} />
            <Cartao titulo="Canceladas" valor={instalacoes.canceladas} />
          </div>
        </section>
      )}

      {estoque && (
        <section className="dashboard-section">
          <div className="dashboard-section-header">
            <div>
              <span className="dashboard-section-indice">04 / MATERIAIS</span>
              <h2>Estoque</h2>
            </div>
            {Number(estoque.estoque_baixo ?? 0) +
              Number(estoque.estoque_zerado ?? 0) > 0 && (
              <span className="dashboard-status-atencao">
                Atenção ao estoque
              </span>
            )}
          </div>

          <div className="dashboard-cards">
            <Cartao titulo="Total de materiais" valor={estoque.total_materiais} />
            <Cartao
              titulo="Estoque baixo"
              valor={estoque.estoque_baixo}
              descricao="Materiais que exigem atenção"
            />
            <Cartao
              titulo="Estoque zerado"
              valor={estoque.estoque_zerado}
              descricao="Materiais sem quantidade disponível"
            />
          </div>
        </section>
      )}

      <footer className="dashboard-footer">
        <span>Huniglass System</span>
        <span>
          {ultimaAtualizacao
            ? `Última consulta: ${ultimaAtualizacao.toLocaleTimeString('pt-BR', {
                hour: '2-digit',
                minute: '2-digit',
              })}`
            : 'Aguardando atualização'}
        </span>
      </footer>
    </main>
  )
}

export default Dashboard
