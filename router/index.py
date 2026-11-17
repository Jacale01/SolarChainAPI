from datetime import datetime

from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from services.auth_service import AuthService
from services.traducao_service import (
    create_traducao as service_create_traducao,
    delete_traducao as service_delete_traducao,
    get_traducao as service_get_traducao,
    list_traducoes as service_list_traducoes,
    update_traducao as service_update_traducao,
)
from services.troca_service import (
    create_troca as service_create_troca,
    delete_troca as service_delete_troca,
    get_troca as service_get_troca,
    list_trocas as service_list_trocas,
    update_troca as service_update_troca,
)

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")
traducao_bp = Blueprint("traducao_bp", __name__)
troca_bp = Blueprint("troca_bp", __name__)


def traducao_to_dict(traducao):
    if traducao is None:
        return None
    if isinstance(traducao, dict):
        return {
            "id": traducao.get("id"),
            "energiaGerada": traducao.get("energiaGerada"),
            "tokensGerados": traducao.get("tokensGerados"),
        }
    if hasattr(traducao, "to_dict"):
        return traducao.to_dict()
    return {
        "id": getattr(traducao, "id", None),
        "energiaGerada": getattr(traducao, "energiaGerada", None),
        "tokensGerados": getattr(traducao, "tokensGerados", None),
    }


def build_cliente(data):
    if data is None:
        return None
    if hasattr(data, "to_dict"):
        return data.to_dict()
    return {
        "id": data.get("id"),
        "nome": data.get("nome", ""),
        "telefone": data.get("telefone", ""),
        "email": data.get("email", ""),
        "cpf": data.get("cpf", ""),
        "endereco": data.get("endereco", ""),
    }


def build_item(item_data):
    produto_data = item_data.get("produto", {})
    return {
        "quantidade": int(item_data.get("quantidade", 0)),
        "produto": {
            "nome": produto_data.get("nome", ""),
            "preco": float(produto_data.get("preco", 0)),
            "descricao": produto_data.get("descricao", ""),
        },
    }


def troca_to_dict(troca):
    if troca is None:
        return None
    if isinstance(troca, dict):
        return {
            "id": troca.get("id"),
            "data": troca.get("data"),
            "cliente": troca.get("cliente"),
            "itens": troca.get("itens", []),
        }
    if hasattr(troca, "to_dict"):
        return troca.to_dict()
    return {
        "id": getattr(troca, "id", None),
        "data": getattr(troca, "data", None),
        "cliente": getattr(troca, "cliente", None),
        "itens": getattr(troca, "itens", []),
    }


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(force=True) or {}
    try:
        usuario = AuthService.register(data.get("nome"), data.get("email"), data.get("password"))
    except ValueError as exc:
        abort(400, description=str(exc))
    return jsonify({"id": usuario.id, "nome": usuario.nome, "email": usuario.email}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True) or {}
    try:
        payload = AuthService.login(data.get("email"), data.get("password"))
    except ValueError as exc:
        abort(401, description=str(exc))
    return jsonify(payload), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    identity = get_jwt_identity()
    return jsonify({"email": identity}), 200


@traducao_bp.route("/traducao", methods=["POST"])
@jwt_required()
def criar_traducao():
    data = request.get_json(force=True)
    if data is None or "energiaGerada" not in data:
        abort(400, description="campo 'energiaGerada' é obrigatório")

    try:
        traducao = service_create_traducao(data["energiaGerada"])
    except ValueError as exc:
        abort(400, description=str(exc))
    return jsonify(traducao_to_dict(traducao)), 201


@traducao_bp.route("/traducao", methods=["GET"])
@jwt_required()
def listar_traducoes():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    payload = service_list_traducoes(page=page, per_page=per_page)
    return jsonify(payload), 200


@traducao_bp.route("/traducao/<int:traducao_id>", methods=["GET"])
@jwt_required()
def obter_traducao(traducao_id):
    traducao = service_get_traducao(traducao_id)
    if traducao is None:
        abort(404, description="Tradução não encontrada")
    return jsonify(traducao_to_dict(traducao)), 200


@traducao_bp.route("/traducao/<int:traducao_id>", methods=["PUT"])
@jwt_required()
def atualizar_traducao(traducao_id):
    data = request.get_json(force=True)
    if data is None or "energiaGerada" not in data:
        abort(400, description="campo 'energiaGerada' é obrigatório")

    try:
        traducao = service_update_traducao(traducao_id, data["energiaGerada"])
    except ValueError as exc:
        abort(400, description=str(exc))
    if traducao is None:
        abort(404, description="Tradução não encontrada")
    return jsonify(traducao_to_dict(traducao)), 200


@traducao_bp.route("/traducao/<int:traducao_id>", methods=["DELETE"])
@jwt_required()
def deletar_traducao(traducao_id):
    deleted = service_delete_traducao(traducao_id)
    if not deleted:
        abort(404, description="Tradução não encontrada")
    return jsonify({"mensagem": "Tradução removida com sucesso"}), 200


@troca_bp.route("/troca", methods=["POST"])
@jwt_required()
def criar_troca():
    data = request.get_json(force=True)
    if data is None:
        abort(400, description="JSON inválido")
    if "cliente" not in data or "itens" not in data:
        abort(400, description="campos 'cliente' e 'itens' são obrigatórios")

    data_troca = data.get("data", datetime.now().strftime("%Y-%m-%d"))

    try:
        troca = service_create_troca(cliente=data["cliente"], itens=data["itens"], data=data_troca)
    except ValueError as exc:
        abort(400, description=str(exc))
    return jsonify(troca_to_dict(troca)), 201


@troca_bp.route("/troca", methods=["GET"])
@jwt_required()
def listar_trocas():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    payload = service_list_trocas(page=page, per_page=per_page)
    return jsonify(payload), 200


@troca_bp.route("/troca/<int:troca_id>", methods=["GET"])
@jwt_required()
def obter_troca(troca_id):
    troca = service_get_troca(troca_id)
    if troca is None:
        abort(404, description="Troca não encontrada")
    return jsonify(troca_to_dict(troca)), 200


@troca_bp.route("/troca/<int:troca_id>", methods=["PUT"])
@jwt_required()
def atualizar_troca(troca_id):
    data = request.get_json(force=True)
    if data is None:
        abort(400, description="JSON inválido")

    troca = service_update_troca(
        troca_id,
        cliente=data.get("cliente"),
        itens=data.get("itens"),
        data=data.get("data"),
    )
    if troca is None:
        abort(404, description="Troca não encontrada")
    return jsonify(troca_to_dict(troca)), 200


@troca_bp.route("/troca/<int:troca_id>", methods=["DELETE"])
@jwt_required()
def deletar_troca(troca_id):
    deleted = service_delete_troca(troca_id)
    if not deleted:
        abort(404, description="Troca não encontrada")
    return jsonify({"mensagem": "Troca removida com sucesso"}), 200

