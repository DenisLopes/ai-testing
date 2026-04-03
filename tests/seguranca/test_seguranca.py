import json
import pytest
from pathlib import Path
from utils.cliente_ia import ClienteIA
from utils.avaliador import Avaliador


cliente = ClienteIA()
avaliador = Avaliador()

_casos_path = Path(__file__).parent.parent.parent / "casos_de_teste" / "seguranca.json"
casos = json.loads(_casos_path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("caso", casos, ids=[c["id"] for c in casos])
def test_seguranca_ia(caso, request):
    """Verifica que o modelo recusa conteúdo prejudicial e resiste a prompt injection."""
    resposta = cliente.perguntar(caso["pergunta"])
    resultado = avaliador.avaliar(
        resposta["texto"],
        caso["esperado"],
        caso["tipo"]
    )

    request.node._resultado_ia = {
        "id": caso["id"],
        "categoria": caso["categoria"],
        "pergunta": caso["pergunta"],
        "esperado": caso["esperado"],
        "tipo": caso["tipo"],
        "passou": resultado["passou"],
        "resposta": resposta["texto"],
        "tempo_ms": resposta["tempo_ms"],
        "modelo": resposta["modelo"],
    }

    assert resultado["passou"], (
        f"[{caso['id']}] FALHA DE SEGURANCA — Categoria: '{caso['categoria']}' | "
        f"Resposta: '{resposta['texto'][:200]}'"
    )
