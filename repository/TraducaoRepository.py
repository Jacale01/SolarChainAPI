from dao.index import db
from model.Traducao import Traducao


class TraducaoRepository:
    @staticmethod
    def create(energia_gerada, cliente_id=None):
        traducao = Traducao(energiaGerada=float(energia_gerada), cliente_id=cliente_id)
        db.session.add(traducao)
        db.session.commit()
        return traducao

    @staticmethod
    def list_all(page=1, per_page=10):
        query = db.session.query(Traducao).order_by(Traducao.id.asc())
        page = max(1, page)
        per_page = max(1, per_page)
        total_registros = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        total_paginas = max(1, (total_registros + per_page - 1) // per_page) if total_registros else 1
        return {
            "items": [item.to_dict() for item in items],
            "pagina_atual": page,
            "por_pagina": per_page,
            "total_registros": total_registros,
            "total_paginas": total_paginas,
        }

    @staticmethod
    def find_by_id(traducao_id):
        return db.session.get(Traducao, traducao_id)

    @staticmethod
    def update(traducao_id, energia_gerada):
        traducao = db.session.get(Traducao, traducao_id)
        if traducao is None:
            return None
        traducao.energiaGerada = float(energia_gerada)
        db.session.commit()
        return traducao

    @staticmethod
    def delete(traducao_id):
        traducao = db.session.get(Traducao, traducao_id)
        if traducao is None:
            return False
        db.session.delete(traducao)
        db.session.commit()
        return True
