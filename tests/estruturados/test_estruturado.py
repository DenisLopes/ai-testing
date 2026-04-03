import json
import allure
import pytest
from pathlib import Path
from utils.cliente_ia import ClienteIA
from utils.avaliador import Avaliador


cliente = ClienteIA()
avaliador = Avaliador()

_casos_path = Path(__file__).parent.parent.parent / "casos_de_teste" / "estruturados.json"
casos = json.loads(_casos_path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("caso", casos, ids=[c["id"] for c in casos])
@allure.suite("Estruturados")
def test_resposta_estruturada(caso, request):
    allure.dynamic.title(caso["id"])
    allure.dynamic.label("feature", caso["categoria"])
    allure.dynamic.description(f"Pergunta: {caso['pergunta']}\nEsperado: {caso['esperado']}")

    with allure.step(f"Enviar pergunta: {caso['pergunta']}"):
        resposta = cliente.perguntar(caso["pergunta"])
        allure.attach(resposta["texto"], name="Resposta da IA", attachment_type=allure.attachment_type.TEXT)

    with allure.step(f"Avaliar resposta ({caso['tipo']})"):
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
        f"[{caso['id']}] Esperado: '{caso['esperado']}' | "
        f"Recebido: '{resposta['texto'][:200]}'"
    )
