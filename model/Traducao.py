from dao.index import db


class Traducao(db.Model):
    __tablename__ = "traducao"

    id = db.Column(db.Integer, primary_key=True)
    energiaGerada = db.Column("energiaGerada", db.Float, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=True)

    cliente = db.relationship("Cliente", back_populates="traducoes")

    @property
    def tokensGerados(self):
        return int((self.energiaGerada ** 2) / 10000)

    def to_dict(self):
        return {
            "id": self.id,
            "energiaGerada": self.energiaGerada,
            "tokensGerados": self.tokensGerados,
            "cliente_id": self.cliente_id,
        }
