import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
})

api.interceptors.request.use((config) => {

  const usuarioSalvo = localStorage.getItem('usuario')

  if (usuarioSalvo) {

    const usuario = JSON.parse(usuarioSalvo)

    if (usuario.token) {
      config.headers.Authorization = `Bearer ${usuario.token}`
    }

  }

  return config
})

export default api