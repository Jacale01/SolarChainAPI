from werkzeug.security import check_password_hash, generate_password_hash

from dao.index import db
from model.Usuario import Usuario


class UsuarioRepository:
    @staticmethod
    def create(nome, email, password):
        usuario = Usuario(
            nome=nome,
            email=email.lower().strip(),
            password_hash=generate_password_hash(password),
            is_admin=False,
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def find_by_email(email):
        if email is None:
            return None
        return db.session.query(Usuario).filter(Usuario.email == email.lower().strip()).first()

    @staticmethod
    def verify_password(usuario, password):
        if usuario is None:
            return False
        return check_password_hash(usuario.password_hash, password)
