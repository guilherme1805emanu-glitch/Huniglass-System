import './header.css'
import { useAuth } from '../../contexts/AuthContext.jsx'


function Header() {

    const { logout } = useAuth()
    
  return (
    <header className="header">
      <div className="header-title">
        Huniglass System
      </div>

      <div className="header-user">
        <span>Administrador</span>

        <button onClick={logout}>
            Sair
        </button>

      </div>
    </header>
  )
}

export default Header