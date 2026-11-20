import { NavLink } from 'react-router-dom'
import './sidebar.css'

function Sidebar() {
  const links = [
    { nome: 'Dashboard', caminho: '/dashboard' },
    { nome: 'Clientes', caminho: '/clientes' },
    { nome: 'Orçamentos', caminho: '#' },
    { nome: 'Pedidos', caminho: '#' },
    { nome: 'Produção', caminho: '#' },
    { nome: 'Instalações', caminho: '#' },
    { nome: 'Estoque', caminho: '#' },
    { nome: 'Financeiro', caminho: '#' },
    { nome: 'Agenda', caminho: '#' },
    { nome: 'Relatórios', caminho: '#' },
  ]

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        Huniglass
      </div>

      <nav>
        {links.map((link) => (
          link.caminho === '#' ? (
            <a
              key={link.nome}
              href="#"
              onClick={(e) => e.preventDefault()}
            >
              {link.nome}
            </a>
          ) : (
            <NavLink
              key={link.nome}
              to={link.caminho}
              className={({ isActive }) =>
                isActive ? 'sidebar-link ativo' : 'sidebar-link'
              }
            >
              {link.nome}
            </NavLink>
          )
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar