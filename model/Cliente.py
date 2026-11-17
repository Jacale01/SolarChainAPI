from dao.index import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)
    cpf = db.Column(db.String(20), nullable=False, unique=True)
    endereco = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)

    usuario = db.relationship("Usuario", back_populates="clientes")
    trocas = db.relationship("Troca", back_populates="cliente", cascade="all, delete-orphan")
    traducoes = db.relationship("Traducao", back_populates="cliente", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email,
            "cpf": self.cpf,
            "endereco": self.endereco,
            "usuario_id": self.usuario_id,
        }
