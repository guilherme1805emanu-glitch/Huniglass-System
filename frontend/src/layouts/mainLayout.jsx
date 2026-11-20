import Sidebar from '../components/Sidebar/sidebar.jsx'
import Header from '../components/Header/header.jsx'
import './mainlayout.css'

function MainLayout({ children }) {
  return (
    <div className="main-layout">

      <Sidebar />

      <div className="main-content">
        <Header />

        <main className="main-page">
          {children}
        </main>
      </div>

    </div>
  )
}

export default MainLayout