from dao.index import db
from model.Cliente import Cliente
from model.Item import Item
from model.Produto import Produto
from model.Troca import Troca


class TrocaRepository:
    @staticmethod
    def _serialize_troca(troca):
        return {
            "id": troca.id,
            "data": troca.data,
            "cliente": troca.cliente.to_dict() if troca.cliente else None,
            "itens": [item.to_dict() for item in troca.itens],
        }

    @staticmethod
    def create(cliente, itens, data):
        cliente_payload = cliente if isinstance(cliente, dict) else getattr(cliente, "__dict__", {})
        cliente_obj = None
        if cliente_payload.get("id") is not None:
            cliente_obj = db.session.get(Cliente, cliente_payload["id"])
        if cliente_obj is None:
            cliente_obj = Cliente(
                nome=cliente_payload.get("nome", ""),
                telefone=cliente_payload.get("telefone", ""),
                email=cliente_payload.get("email", ""),
                cpf=cliente_payload.get("cpf", ""),
                endereco=cliente_payload.get("endereco", ""),
            )
            db.session.add(cliente_obj)
            db.session.flush()

        troca = Troca(data=data, cliente_id=cliente_obj.id)
        db.session.add(troca)
        db.session.flush()

        for item_data in itens or []:
            item_payload = item_data if isinstance(item_data, dict) else item_data.__dict__
            produto_payload = item_payload.get("produto", {}) if isinstance(item_payload, dict) else getattr(item_data, "produto", {})
            produto_obj = db.session.query(Produto).filter_by(nome=produto_payload.get("nome")).first()
            if produto_obj is None:
                produto_obj = Produto(
                    nome=produto_payload.get("nome", ""),
                    preco=float(produto_payload.get("preco", 0)),
                    descricao=produto_payload.get("descricao", ""),
                )
                db.session.add(produto_obj)
                db.session.flush()
            item = Item(
                quantidade=int(item_payload.get("quantidade", 0)),
                produto_id=produto_obj.id,
                troca_id=troca.id,
            )
            db.session.add(item)
        db.session.commit()
        return db.session.get(Troca, troca.id)

    @staticmethod
    def list_all(page=1, per_page=10):
        query = db.session.query(Troca).order_by(Troca.id.asc())
        page = max(1, page)
        per_page = max(1, per_page)
        total_registros = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        total_paginas = max(1, (total_registros + per_page - 1) // per_page) if total_registros else 1
        return {
            "items": [TrocaRepository._serialize_troca(item) for item in items],
            "pagina_atual": page,
            "por_pagina": per_page,
            "total_registros": total_registros,
            "total_paginas": total_paginas,
        }

    @staticmethod
    def find_by_id(troca_id):
        return db.session.get(Troca, troca_id)

    @staticmethod
    def update(troca_id, cliente=None, itens=None, data=None):
        troca = db.session.get(Troca, troca_id)
        if troca is None:
            return None
        if data is not None:
            troca.data = data
        if cliente is not None:
            cliente_payload = cliente if isinstance(cliente, dict) else getattr(cliente, "__dict__", {})
            cliente_obj = db.session.get(Cliente, cliente_payload.get("id"))
            if cliente_obj is None:
                cliente_obj = Cliente(
                    nome=cliente_payload.get("nome", ""),
                    telefone=cliente_payload.get("telefone", ""),
                    email=cliente_payload.get("email", ""),
                    cpf=cliente_payload.get("cpf", ""),
                    endereco=cliente_payload.get("endereco", ""),
                )
                db.session.add(cliente_obj)
                db.session.flush()
            troca.cliente_id = cliente_obj.id
        if itens is not None:
            for item in list(troca.itens):
                db.session.delete(item)
            for item_data in itens:
                item_payload = item_data if isinstance(item_data, dict) else item_data.__dict__
                produto_payload = item_payload.get("produto", {}) if isinstance(item_payload, dict) else getattr(item_data, "produto", {})
                produto_obj = db.session.query(Produto).filter_by(nome=produto_payload.get("nome")).first()
                if produto_obj is None:
                    produto_obj = Produto(
                        nome=produto_payload.get("nome", ""),
                        preco=float(produto_payload.get("preco", 0)),
                        descricao=produto_payload.get("descricao", ""),
                    )
                    db.session.add(produto_obj)
                    db.session.flush()
                item = Item(
                    quantidade=int(item_payload.get("quantidade", 0)),
                    produto_id=produto_obj.id,
                    troca_id=troca.id,
                )
                db.session.add(item)
        db.session.commit()
        return db.session.get(Troca, troca.id)

    @staticmethod
    def delete(troca_id):
        troca = db.session.get(Troca, troca_id)
        if troca is None:
            return False
        db.session.delete(troca)
        db.session.commit()
        return True
