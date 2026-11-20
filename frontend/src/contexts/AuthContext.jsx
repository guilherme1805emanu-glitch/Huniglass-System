import { createContext, useContext, useState } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
const [usuario, setUsuario] = useState(() => {
  const usuarioSalvo = localStorage.getItem('usuario')

  return usuarioSalvo ? JSON.parse(usuarioSalvo) : null
})
  function login(dadosUsuario) {
    setUsuario(dadosUsuario)
    localStorage.setItem('usuario', JSON.stringify(dadosUsuario))
  }
  function logout() {
    setUsuario(null)
    localStorage.removeItem('usuario')
  }
  return (
    <AuthContext.Provider value={{ usuario, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}