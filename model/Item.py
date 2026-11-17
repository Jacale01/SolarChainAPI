from dao.index import db


class Item(db.Model):
    __tablename__ = "itens"

    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    troca_id = db.Column(db.Integer, db.ForeignKey("trocas.id"), nullable=False)

    produto = db.relationship("Produto", back_populates="itens")
    troca = db.relationship("Troca", back_populates="itens")

    def to_dict(self):
        return {
            "id": self.id,
            "quantidade": self.quantidade,
            "produto": self.produto.to_dict() if self.produto else None,
        }

    def getSubValor(self):
        if self.produto is None:
            return 0
        return self.produto.preco * self.quantidade
