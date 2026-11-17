from datetime import datetime

from dao.index import db


class Troca(db.Model):
    __tablename__ = "trocas"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20), nullable=False, default=lambda: datetime.utcnow().strftime("%Y-%m-%d"))
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    cliente = db.relationship("Cliente", back_populates="trocas")
    itens = db.relationship("Item", back_populates="troca", cascade="all, delete-orphan")

    def getValorTotal(self):
        return sum(item.getSubValor() for item in self.itens)

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "cliente": self.cliente.to_dict() if self.cliente else None,
            "itens": [item.to_dict() for item in self.itens],
        }
