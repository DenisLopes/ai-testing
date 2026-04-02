"""
conftest.py — Hooks globais do pytest.

Ao final de cada sessão pytest que coletou resultados de IA,
gera automaticamente:
  - relatoriosjson/relatorio_<timestamp>.json
  - relatorioshtml/relatorio_<timestamp>.html
  - evidencias/evidencia_<timestamp>.txt
"""

import sys
import json
import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

_resultados: list[dict] = []


@pytest.fixture(autouse=True)
def _capturar_resultado_ia(request):
    yield
    dado = getattr(request.node, "_resultado_ia", None)
    if dado is not None:
        _resultados.append(dado)


def pytest_sessionfinish(session, exitstatus):
    if not _resultados:
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    _salvar_json(_resultados, timestamp)
    _salvar_html(_resultados, timestamp)
    _salvar_evidencia_txt(_resultados, timestamp)

    total = len(_resultados)
    aprovados = sum(1 for r in _resultados if r["passou"])
    taxa = round((aprovados / total) * 100, 1)

    print(f"\n{'='*60}")
    print(f"  Relatório gerado — {aprovados}/{total} aprovados ({taxa}%)")
    print(f"  relatoriosjson/relatorio_{timestamp}.json")
    print(f"  relatorioshtml/relatorio_{timestamp}.html")
    print(f"  evidencias/evidencia_{timestamp}.txt")
    print(f"{'='*60}")


# ---------------------------------------------------------------------------
# Funções de geração de arquivos
# ---------------------------------------------------------------------------

def _salvar_json(resultados: list[dict], timestamp: str) -> None:
    total = len(resultados)
    aprovados = sum(1 for r in resultados if r["passou"])
    taxa = round((aprovados / total) * 100, 1) if total else 0

    payload = {
        "timestamp": timestamp,
        "modelo": resultados[0]["modelo"] if resultados else "",
        "total": total,
        "aprovados": aprovados,
        "reprovados": total - aprovados,
        "taxa_aprovacao": taxa,
        "casos": resultados,
    }

    pasta = Path(__file__).parent / "relatoriosjson"
    pasta.mkdir(exist_ok=True)
    (pasta / f"relatorio_{timestamp}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _salvar_html(resultados: list[dict], timestamp: str) -> None:
    total = len(resultados)
    aprovados = sum(1 for r in resultados if r["passou"])
    reprovados = total - aprovados
    taxa = round((aprovados / total) * 100, 1) if total else 0
    modelo = resultados[0]["modelo"] if resultados else ""
    cor_taxa = "#22c55e" if taxa >= 80 else "#f59e0b" if taxa >= 60 else "#ef4444"

    linhas = ""
    for r in resultados:
        sc = "passou" if r["passou"] else "falhou"
        lb = "PASSOU" if r["passou"] else "FALHOU"
        resp = r["resposta"][:200].replace("<", "&lt;").replace(">", "&gt;")
        linhas += f"""
        <tr class="{sc}">
            <td><strong>{r['id']}</strong></td>
            <td>{r['categoria']}</td>
            <td>{r['pergunta']}</td>
            <td><code>{r['esperado']}</code></td>
            <td class="resposta">{resp}</td>
            <td>{r['tempo_ms']} ms</td>
            <td><span class="badge {sc}">{lb}</span></td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relatório de Evidência — AI Testing Portfolio</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #f8fafc; color: #1e293b; padding: 2rem; }}
  h1 {{ font-size: 1.8rem; margin-bottom: 0.25rem; }}
  .meta {{ color: #64748b; font-size: 0.9rem; margin-bottom: 2rem; }}
  .cards {{ display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 2rem; }}
  .card {{ background: #fff; border-radius: 12px; padding: 1.2rem 1.8rem; box-shadow: 0 1px 4px rgba(0,0,0,.08); min-width: 150px; }}
  .card .label {{ font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: .05em; }}
  .card .valor {{ font-size: 2rem; font-weight: 700; margin-top: .2rem; }}
  .card .valor.taxa {{ color: {cor_taxa}; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,.08); }}
  th {{ background: #1e293b; color: #fff; padding: .75rem 1rem; text-align: left; font-size: .85rem; text-transform: uppercase; letter-spacing: .05em; }}
  td {{ padding: .75rem 1rem; border-bottom: 1px solid #f1f5f9; font-size: .9rem; vertical-align: top; }}
  tr:last-child td {{ border-bottom: none; }}
  tr.passou {{ background: #f0fdf4; }}
  tr.falhou {{ background: #fff7f7; }}
  .badge {{ display: inline-block; padding: .2rem .6rem; border-radius: 999px; font-size: .8rem; font-weight: 600; }}
  .badge.passou {{ background: #dcfce7; color: #166534; }}
  .badge.falhou {{ background: #fee2e2; color: #991b1b; }}
  .resposta {{ max-width: 350px; word-break: break-word; color: #475569; }}
  code {{ background: #f1f5f9; padding: .1rem .4rem; border-radius: 4px; font-size: .85rem; }}
  footer {{ margin-top: 2rem; text-align: center; color: #94a3b8; font-size: .8rem; }}
</style>
</head>
<body>
<h1>Relatório de Evidência</h1>
<p class="meta">Gerado em {timestamp.replace('_', ' ')} &nbsp;|&nbsp; Modelo: <strong>{modelo}</strong></p>
<div class="cards">
  <div class="card"><div class="label">Total</div><div class="valor">{total}</div></div>
  <div class="card"><div class="label">Aprovados</div><div class="valor" style="color:#22c55e">{aprovados}</div></div>
  <div class="card"><div class="label">Reprovados</div><div class="valor" style="color:#ef4444">{reprovados}</div></div>
  <div class="card"><div class="label">Taxa de Aprovação</div><div class="valor taxa">{taxa}%</div></div>
</div>
<table>
  <thead>
    <tr><th>ID</th><th>Categoria</th><th>Pergunta</th><th>Esperado</th><th>Resposta</th><th>Tempo</th><th>Status</th></tr>
  </thead>
  <tbody>{linhas}
  </tbody>
</table>
<footer>AI Testing Portfolio &mdash; {timestamp}</footer>
</body>
</html>"""

    pasta = Path(__file__).parent / "relatorioshtml"
    pasta.mkdir(exist_ok=True)
    (pasta / f"relatorio_{timestamp}.html").write_text(html, encoding="utf-8")


def _salvar_evidencia_txt(resultados: list[dict], timestamp: str) -> None:
    total = len(resultados)
    aprovados = sum(1 for r in resultados if r["passou"])
    taxa = round((aprovados / total) * 100, 1) if total else 0

    linhas = [
        "=" * 60,
        "  EVIDÊNCIA DE EXECUÇÃO — AI Testing Portfolio",
        f"  Data/Hora : {timestamp.replace('_', ' ')}",
        f"  Modelo    : {resultados[0]['modelo'] if resultados else ''}",
        "=" * 60,
        "",
        f"  Total     : {total}",
        f"  Aprovados : {aprovados}",
        f"  Reprovados: {total - aprovados}",
        f"  Taxa      : {taxa}%",
        "",
        "-" * 60,
    ]
    for r in resultados:
        status = "PASSOU" if r["passou"] else "FALHOU"
        linhas += [
            "",
            f"[{r['id']}] {r['categoria']} — {status}",
            f"  Pergunta : {r['pergunta']}",
            f"  Esperado : {r['esperado']}",
            f"  Resposta : {r['resposta'][:200]}",
            f"  Tempo    : {r['tempo_ms']} ms",
            f"  Tipo     : {r['tipo']}",
        ]
    linhas += ["", "=" * 60]

    pasta = Path(__file__).parent / "evidencias"
    pasta.mkdir(exist_ok=True)
    (pasta / f"evidencia_{timestamp}.txt").write_text("\n".join(linhas), encoding="utf-8")
