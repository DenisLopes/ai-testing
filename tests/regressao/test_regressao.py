import json
import pytest
from pathlib import Path
from utils.cliente_ia import ClienteIA
from utils.avaliador import Avaliador


cliente = ClienteIA()
avaliador = Avaliador()

_casos_path = Path(__file__).parent.parent.parent / "casos_de_teste" / "regressao.json"
casos = json.loads(_casos_path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("caso", casos, ids=[c["id"] for c in casos])
def test_regressao_ia(caso, request):
    """Garante que respostas conhecidas e estáveis não mudem entre versões do modelo."""
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
        f"[{caso['id']}] REGRESSAO DETECTADA — Esperado: '{caso['esperado']}' | "
        f"Recebido: '{resposta['texto'][:200]}'"
    )
