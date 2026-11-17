from dao.index import db
from model.Traducao import Traducao


def create(energia_gerada, cliente_id=None):
    traducao = Traducao(energiaGerada=float(energia_gerada), cliente_id=cliente_id)
    db.session.add(traducao)
    db.session.commit()
    return traducao.to_dict()


def list_all(page=1, per_page=10):
    query = db.session.query(Traducao).order_by(Traducao.id.asc())
    page = max(1, page)
    per_page = max(1, per_page)
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return {
        "items": [item.to_dict() for item in items],
        "pagina_atual": page,
        "por_pagina": per_page,
        "total_registros": total,
        "total_paginas": max(1, (total + per_page - 1) // per_page) if total else 1,
    }


def find_by_id(traducao_id):
    return db.session.get(Traducao, traducao_id)


def update(traducao_id, energia_gerada):
    traducao = db.session.get(Traducao, traducao_id)
    if traducao is None:
        return None
    traducao.energiaGerada = float(energia_gerada)
    db.session.commit()
    return traducao.to_dict()


def delete(traducao_id):
    traducao = db.session.get(Traducao, traducao_id)
    if traducao is None:
        return False
    db.session.delete(traducao)
    db.session.commit()
    return True
