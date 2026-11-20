from app import create_app
from database import db
from app.auth.models import Usuario


app = create_app()

with app.app_context():

    usuario = Usuario(
        nome="Administrador",
        email="admin@huniglass.com",
        cargo="socio"
    )

    usuario.definir_senha("123456")

    db.session.add(usuario)
    db.session.commit()

    print("Usuário inicial criado com sucesso!")
    print(f"ID: {usuario.id}")
    print(f"Email: {usuario.email}")
    print(f"Cargo: {usuario.cargo}")