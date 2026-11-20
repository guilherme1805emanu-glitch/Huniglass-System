import "./home.css";

function Home() {
  const services = [
    {
      title: "Portas de Vidro",
      description:
        "Elegância, luminosidade e integração para ambientes residenciais e comerciais.",
      image: "/servicos/porta-de-vidro.jpg",
    },
    {
      title: "Portas de Alumínio",
      description:
        "Design moderno, resistência e acabamento para valorizar sua entrada.",
      image: "/servicos/porta-de-aluminio.jpg",
    },
    {
      title: "Portões",
      description:
        "Segurança e sofisticação em soluções de alumínio sob medida.",
      image: "/servicos/portao.jpg",
    },
    {
      title: "Janelas e Esquadrias",
      description:
        "Esquadrias planejadas para unir conforto, estética e funcionalidade.",
      image: "/servicos/esquadrias.jpg",
    },
  ];

  return (
    <div className="home">
      <div className="glass-shard glass-shard-one"></div>
      <div className="glass-shard glass-shard-two"></div>
      <div className="glass-shard glass-shard-three"></div>

      {/* HEADER */}
      <header className="home-header">
        <div className="home-logo">
          <div className="logo-mark">H</div>

          <div className="logo-text">
            <strong>HUNIGLASS</strong>
            <span>VIDROS E ALUMÍNIO</span>
          </div>
        </div>

        <nav className="home-nav">
          <a href="#inicio">Início</a>
          <a href="#sobre">Sobre nós</a>
          <a href="#servicos">Serviços</a>
          <a href="#projetos">Projetos</a>
          <a href="#contato">Contato</a>
        </nav>

        <div className="home-header-actions">
          <a href="/login" className="btn-login">
            Entrar
          </a>

          <a href="#contato" className="btn-primary">
            Solicitar orçamento
            <span>↗</span>
          </a>
        </div>
      </header>

      <main>
        {/* HERO */}
        <section className="hero" id="inicio">
          <div className="hero-glow"></div>

          <div className="hero-content">
            <span className="eyebrow">HUNIGLASS</span>

            <h1>
              Soluções em vidro
              <br />
              e alumínio para
              <strong> transformar seus projetos.</strong>
            </h1>

            <p>
              Unimos qualidade, precisão e experiência para criar
              soluções em vidro e alumínio que valorizam cada espaço.
            </p>

            <div className="hero-actions">
              <a href="#contato" className="btn-primary btn-large">
                Solicitar orçamento
                <span>→</span>
              </a>

              <a href="#sobre" className="hero-link">
                Conheça a Huniglass
                <span className="play-circle">▶</span>
              </a>
            </div>

            <div className="hero-features">
              <div>
                <span className="feature-icon">◇</span>

                <div>
                  <strong>Qualidade</strong>
                  <small>em cada detalhe</small>
                </div>
              </div>

              <div>
                <span className="feature-icon">✦</span>

                <div>
                  <strong>Precisão</strong>
                  <small>em cada projeto</small>
                </div>
              </div>

              <div>
                <span className="feature-icon">◈</span>

                <div>
                  <strong>Experiência</strong>
                  <small>que faz diferença</small>
                </div>
              </div>
            </div>
          </div>
        </section>
        {/* SERVIÇOS */}
        <section className="services-section" id="servicos">
          <div className="section-heading">
            <div>
              <span className="eyebrow">NOSSOS SERVIÇOS</span>

              <h2>
                Soluções completas
                <br />
                para o seu projeto.
              </h2>
            </div>

            <p>
              Do planejamento à instalação, entregamos soluções
              pensadas para unir estética, funcionalidade e qualidade.
            </p>
          </div>

          <div className="services-window">
            <div className="services-track">
              {[...services, ...services].map((service, index) => (
                <article className="service-card" key={index}>
                  <img
                    src={service.image}
                    alt={service.title}
                    className="service-image"
                  />

                  <div className="service-overlay"></div>

                  <div className="service-card-content">
                    <span className="service-number">
                      {String((index % services.length) + 1).padStart(2, "0")}
                    </span>

                    <div>
                      <h3>{service.title}</h3>

                      <p>{service.description}</p>
                    </div>

                    <span className="service-arrow">↗</span>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* SOBRE */}
        <section className="about-section" id="sobre">
          <div className="about-visual">
            <img
              src="/servicos/sobre.jpg"
              alt="Projeto Huniglass em vidro e alumínio"
              className="about-image"
            />

            <div className="about-glass"></div>
            <div className="about-line line-one"></div>
            <div className="about-line line-two"></div>

            <div className="about-floating-card">
              <span>HUNIGLASS</span>
              <strong>Precisão em cada detalhe.</strong>
            </div>
          </div>

          <div className="about-content">
            <span className="eyebrow">SOBRE A HUNIGLASS</span>

            <h2>
              Tradição e inovação
              <strong> em cada projeto.</strong>
            </h2>

            <p>
              A Huniglass trabalha com soluções em vidro e alumínio
              desenvolvidas para diferentes tipos de ambientes e
              necessidades.
            </p>

            <p>
              Nosso propósito é transformar projetos em soluções
              funcionais, seguras e visualmente marcantes, sempre
              valorizando a qualidade de cada etapa.
            </p>

            <div className="about-points">
              <div>
                <span>01</span>

                <div>
                  <strong>Compromisso</strong>
                  <small>com cada cliente</small>
                </div>
              </div>

              <div>
                <span>02</span>

                <div>
                  <strong>Qualidade</strong>
                  <small>em materiais e execução</small>
                </div>
              </div>

              <div>
                <span>03</span>

                <div>
                  <strong>Personalização</strong>
                  <small>para cada projeto</small>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* PROJETOS */}
        <section className="projects-section" id="projetos">
          <div className="projects-heading">
            <span className="eyebrow">NOSSOS PROJETOS</span>

            <h2>
              Projetos que
              <strong> impressionam.</strong>
            </h2>

            <p>
              Soluções em vidro e alumínio pensadas para valorizar
              cada detalhe do ambiente.
            </p>
          </div>

          <div className="project-feature">
            <img
              src="/servicos/projeto-01.jpg"
              alt="Projeto residencial moderno com vidro e alumínio"
              className="project-image"
            />

            <div className="project-overlay"></div>

            <div className="project-content">
              <span className="project-number">PROJETO 01</span>

              <h3>
                Arquitetura
                <br />
                moderna
                <br />
                em vidro e
                <br />
                alumínio.
              </h3>

              <p>
                Fachada de alto padrão com grandes painéis de vidro,
                esquadrias escuras e integração entre os ambientes.
              </p>

              <span className="project-arrow">↗</span>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="cta-section" id="contato">
          <div className="cta-glass"></div>

          <span className="eyebrow">SEU PROJETO COMEÇA AQUI</span>

          <h2>
            Vamos transformar
            <br />
            sua ideia em realidade?
          </h2>

          <p>
            Conte-nos o que você precisa e descubra as possibilidades
            para o seu projeto.
          </p>

          <a href="#" className="btn-primary btn-large">
            Solicitar orçamento
            <span>→</span>
          </a>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="home-footer">
        <div className="footer-brand">
          <div className="logo-mark">H</div>

          <div className="logo-text">
            <strong>HUNIGLASS</strong>
            <span>VIDROS E ALUMÍNIO</span>
          </div>
        </div>

        <div className="footer-middle">
          QUALIDADE <span>•</span> SEGURANÇA <span>•</span> CONFIANÇA
        </div>

        <div className="footer-contact">
          <span>Av. Osório de Paiva, 6016</span>
          <span>85 98582-1042</span>
          <span>© Huniglass</span>
        </div>
      </footer>
    </div>
  );
}

export default Home;