from flask_jwt_extended import create_access_token

from repository.UsuarioRepository import UsuarioRepository


class AuthService:
    @staticmethod
    def register(nome, email, password):
        if not nome or not email or not password:
            raise ValueError("nome, email e password são obrigatórios")
        if UsuarioRepository.find_by_email(email):
            raise ValueError("email já cadastrado")
        return UsuarioRepository.create(nome, email, password)

    @staticmethod
    def login(email, password):
        usuario = UsuarioRepository.find_by_email(email)
        if usuario is None or not UsuarioRepository.verify_password(usuario, password):
            raise ValueError("credenciais inválidas")
        token = create_access_token(identity=usuario.email)
        return {"access_token": token, "token_type": "Bearer", "user": usuario.to_dict()}
