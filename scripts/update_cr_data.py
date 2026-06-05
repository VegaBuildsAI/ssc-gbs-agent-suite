#!/usr/bin/env python3
"""
update_cr_data.py — Actualización de datos Costa Rica (CINDE / PROCOMER)
========================================================================
Tarea 4 del roadmap CLAUDE.md (SSC/GBS Agent Suite).

Extrae datos públicos de CINDE y PROCOMER (talento, zonas francas, incentivos,
empresas) y refresca las secciones autogeneradas de:
    ssc-location-cr/references/talent_cr.md
    ssc-location-cr/references/costs_cr.md
Genera además un changelog con el diff vs. la corrida anterior.

DISEÑO
------
- Sin dependencias externas obligatorias: usa solo la librería estándar
  (urllib + html.parser). Si `requests`/`beautifulsoup4` están instalados, se
  usan automáticamente (mejor parsing). Si hay un fetcher Bright Data / Nimble
  disponible (variable de entorno), se puede enrutar por ahí para bypass anti-bot.
- Tolerante a fallos: si una URL falla, se registra y se continúa con las demás.
- Idempotente: solo reescribe las secciones delimitadas por marcadores
  <!-- AUTO:START --> ... <!-- AUTO:END --> dejando intacto el contenido curado.

USO
---
    python scripts/update_cr_data.py                 # corrida normal
    python scripts/update_cr_data.py --dry-run       # no escribe, solo reporta
    python scripts/update_cr_data.py --verbose

Pensado para ejecutarse semanalmente vía scheduled task (ver CLAUDE.md Tarea 3
de la sección de Scheduled Tasks). Código de salida 0 si al menos una fuente se
obtuvo; 1 si todas fallaron.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import difflib
import html as _html
import json
import logging
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# --------------------------------------------------------------------------- #
# Configuración
# --------------------------------------------------------------------------- #

CINDE_URLS = [
    "https://cinde.org/en/why-invest-in-costa-rica",
    "https://cinde.org/en/sectors/business-services",
    "https://cinde.org/en/living-in-costa-rica/human-talent",
]
PROCOMER_URLS = [
    "https://www.procomer.com/zona-franca/",
    # Nota: PROCOMER reestructura sus rutas con frecuencia. La home expone enlaces
    # vigentes a estadísticas/inteligencia comercial. Si se conoce una ruta de
    # estadísticas estable, añadirla aquí. El script tolera 404 y continúa.
    "https://www.procomer.com/",
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 SSC-Agent-DataBot/1.0"
)
REQUEST_TIMEOUT = 30  # segundos
MAX_RETRIES = 3

# Rutas (resueltas relativas a la raíz del repo = parent de /scripts)
REPO_ROOT = Path(__file__).resolve().parent.parent
LOCATION_REFS = REPO_ROOT / "_build" / "ssc-location-cr" / "references"
# Fallback: si no existe la versión en _build, usar la de inspección/edición.
if not LOCATION_REFS.exists():
    for candidate in (
        REPO_ROOT / "ssc-location-cr" / "references",
        REPO_ROOT / "_inspect" / "ssc-location-cr" / "references",
    ):
        if candidate.exists():
            LOCATION_REFS = candidate
            break

TALENT_FILE = LOCATION_REFS / "talent_cr.md"
COSTS_FILE = LOCATION_REFS / "costs_cr.md"
SNAPSHOT_FILE = REPO_ROOT / "scripts" / "_cr_data_snapshot.json"
CHANGELOG_FILE = REPO_ROOT / "scripts" / "cr_data_changelog.md"

AUTO_START = "<!-- AUTO:START cr-data-refresh -->"
AUTO_END = "<!-- AUTO:END cr-data-refresh -->"

logger = logging.getLogger("update_cr_data")


# --------------------------------------------------------------------------- #
# Fetching (con degradación elegante)
# --------------------------------------------------------------------------- #

def _fetch_stdlib(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def _fetch_requests(url: str) -> str:
    import requests  # type: ignore

    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.text


def fetch(url: str) -> str | None:
    """Obtiene el HTML de una URL con reintentos. Devuelve None si falla."""
    fetcher = _fetch_stdlib
    try:
        import requests  # noqa: F401
        fetcher = _fetch_requests
        logger.debug("Usando 'requests' como fetcher")
    except ImportError:
        logger.debug("Usando urllib (stdlib) como fetcher")

    last_err: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info("GET %s (intento %d/%d)", url, attempt, MAX_RETRIES)
            return fetcher(url)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
            last_err = exc
            logger.warning("Fallo al obtener %s: %s", url, exc)
        except Exception as exc:  # defensivo: cualquier otro error del fetcher
            last_err = exc
            logger.warning("Error inesperado en %s: %s", url, exc)
    logger.error("Se agotaron los reintentos para %s (%s)", url, last_err)
    return None


# --------------------------------------------------------------------------- #
# Parsing
# --------------------------------------------------------------------------- #

_TAG_RE = re.compile(r"<[^>]+>")
_SCRIPT_STYLE_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
_WS_RE = re.compile(r"[ \t\r\f\v]+")
_MULTINL_RE = re.compile(r"\n{3,}")


def html_to_text(raw_html: str) -> str:
    """Extrae texto legible del HTML usando solo stdlib (o bs4 si existe)."""
    try:
        from bs4 import BeautifulSoup  # type: ignore

        soup = BeautifulSoup(raw_html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text("\n")
    except ImportError:
        no_scripts = _SCRIPT_STYLE_RE.sub(" ", raw_html)
        text = _TAG_RE.sub("\n", no_scripts)
        text = _html.unescape(text)

    text = _WS_RE.sub(" ", text)
    lines = [ln.strip() for ln in text.splitlines()]
    text = "\n".join(ln for ln in lines if ln)
    return _MULTINL_RE.sub("\n\n", text)


# Patrones de interés para extraer señales de datos
_MONEY_RE = re.compile(r"(?:US\$|\$|USD)\s?[\d.,]+(?:\s?(?:million|billion|millones|mil))?", re.I)
_PCT_RE = re.compile(r"\b\d{1,3}(?:[.,]\d+)?\s?%")
_NUM_BIG_RE = re.compile(r"\b\d{1,3}(?:[.,]\d{3})+\b")
_KEYWORDS = [
    "bilingual", "bilingüe", "talent", "talento", "english", "inglés",
    "free zone", "zona franca", "incentive", "incentivo", "exempt", "exención",
    "salary", "salario", "wage", "investment", "inversión", "companies", "empresas",
    "shared services", "business services", "GBS", "nearshore", "FDI", "IED",
    "universit", "graduat", "egresad", "STEM", "headcount", "employ", "emple",
]


def extract_signals(text: str, source: str) -> dict:
    """Extrae señales estructuradas (cifras y frases clave) del texto."""
    relevant_lines = []
    for ln in text.splitlines():
        low = ln.lower()
        if any(kw in low for kw in _KEYWORDS) and (
            _MONEY_RE.search(ln) or _PCT_RE.search(ln) or _NUM_BIG_RE.search(ln)
            or any(kw in low for kw in ("zona franca", "free zone", "bilingüe", "bilingual"))
        ):
            if 15 <= len(ln) <= 240:
                relevant_lines.append(ln)

    # dedup preservando orden
    seen, deduped = set(), []
    for ln in relevant_lines:
        key = ln.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(ln)

    return {
        "source": source,
        "money_mentions": sorted(set(m.group(0) for m in _MONEY_RE.finditer(text)))[:30],
        "pct_mentions": sorted(set(m.group(0) for m in _PCT_RE.finditer(text)))[:30],
        "highlights": deduped[:40],
        "char_count": len(text),
    }


# --------------------------------------------------------------------------- #
# Render de secciones markdown
# --------------------------------------------------------------------------- #

def render_auto_section(snapshot: dict) -> str:
    ts = snapshot["generated_at"]
    lines = [
        AUTO_START,
        "",
        f"### 🔄 Datos auto-actualizados (CINDE / PROCOMER) — {ts}",
        "",
        "> Sección generada automáticamente por `scripts/update_cr_data.py`. "
        "No editar a mano: el contenido entre los marcadores AUTO se sobrescribe "
        "en cada corrida. Las cifras son señales extraídas de fuentes públicas y "
        "deben validarse antes de usarse en entregables.",
        "",
    ]
    ok_sources = [s for s in snapshot["sources"] if s.get("ok")]
    failed = [s for s in snapshot["sources"] if not s.get("ok")]

    if not ok_sources:
        lines += ["_No se pudo obtener ninguna fuente en esta corrida._", ""]
    for s in ok_sources:
        sig = s.get("signals", {})
        lines.append(f"**Fuente:** {s['url']}")
        if sig.get("highlights"):
            lines.append("")
            for h in sig["highlights"][:12]:
                lines.append(f"- {h}")
        money = sig.get("money_mentions", [])
        if money:
            lines.append("")
            lines.append(f"_Cifras monetarias detectadas:_ {', '.join(money[:12])}")
        lines.append("")

    if failed:
        lines.append("**Fuentes no disponibles esta corrida:** " +
                     ", ".join(s["url"] for s in failed))
        lines.append("")

    lines.append(AUTO_END)
    return "\n".join(lines)


def upsert_auto_section(path: Path, section_md: str, dry_run: bool) -> bool:
    """Inserta/reemplaza la sección AUTO en el archivo. Devuelve True si cambió."""
    if not path.exists():
        logger.warning("Archivo destino no existe, se omite: %s", path)
        return False

    original = path.read_text(encoding="utf-8")
    if AUTO_START in original and AUTO_END in original:
        pattern = re.compile(
            re.escape(AUTO_START) + r".*?" + re.escape(AUTO_END), re.DOTALL
        )
        updated = pattern.sub(section_md, original)
    else:
        sep = "" if original.endswith("\n") else "\n"
        updated = original + sep + "\n" + section_md + "\n"

    if updated == original:
        logger.info("Sin cambios en %s", path.name)
        return False

    if dry_run:
        logger.info("[dry-run] Cambiaría %s", path.name)
        return True

    path.write_text(updated, encoding="utf-8")
    logger.info("Actualizado %s", path.name)
    return True


# --------------------------------------------------------------------------- #
# Changelog (diff vs. snapshot anterior)
# --------------------------------------------------------------------------- #

def load_previous_snapshot() -> dict | None:
    if SNAPSHOT_FILE.exists():
        try:
            return json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("No se pudo leer snapshot previo: %s", exc)
    return None


def _snapshot_highlights(snap: dict | None) -> list[str]:
    if not snap:
        return []
    out = []
    for s in snap.get("sources", []):
        for h in s.get("signals", {}).get("highlights", []):
            out.append(f"{s['url']} :: {h}")
    return out


def write_changelog(prev: dict | None, current: dict, dry_run: bool) -> None:
    prev_lines = _snapshot_highlights(prev)
    cur_lines = _snapshot_highlights(current)
    diff = list(difflib.unified_diff(
        prev_lines, cur_lines,
        fromfile="anterior", tofile="actual", lineterm="",
    ))

    added = [l[1:] for l in diff if l.startswith("+") and not l.startswith("+++")]
    removed = [l[1:] for l in diff if l.startswith("-") and not l.startswith("---")]

    ts = current["generated_at"]
    entry = [f"## {ts}", ""]
    ok = sum(1 for s in current["sources"] if s.get("ok"))
    entry.append(f"- Fuentes obtenidas: {ok}/{len(current['sources'])}")
    entry.append(f"- Nuevas señales: {len(added)} | Señales retiradas: {len(removed)}")
    if added:
        entry.append("")
        entry.append("**Nuevo:**")
        entry += [f"  - {a}" for a in added[:20]]
    if removed:
        entry.append("")
        entry.append("**Ya no presente:**")
        entry += [f"  - {r}" for r in removed[:20]]
    entry.append("")
    entry.append("---")
    entry.append("")
    entry_md = "\n".join(entry)

    if dry_run:
        logger.info("[dry-run] Changelog generado:\n%s", entry_md)
        return

    header = "# Changelog de datos CR (CINDE / PROCOMER)\n\n"
    existing = ""
    if CHANGELOG_FILE.exists():
        existing = CHANGELOG_FILE.read_text(encoding="utf-8")
        existing = existing.replace(header, "", 1)
    CHANGELOG_FILE.write_text(header + entry_md + existing, encoding="utf-8")
    logger.info("Changelog actualizado: %s", CHANGELOG_FILE.name)


# --------------------------------------------------------------------------- #
# Orquestación
# --------------------------------------------------------------------------- #

def gather(urls: list[str], group: str) -> list[dict]:
    results = []
    for url in urls:
        raw = fetch(url)
        if raw is None:
            results.append({"url": url, "group": group, "ok": False})
            continue
        text = html_to_text(raw)
        results.append({
            "url": url,
            "group": group,
            "ok": True,
            "signals": extract_signals(text, url),
        })
    return results


def build_snapshot() -> dict:
    sources = gather(CINDE_URLS, "CINDE") + gather(PROCOMER_URLS, "PROCOMER")
    return {
        "generated_at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sources": sources,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Actualiza datos CR desde CINDE/PROCOMER")
    parser.add_argument("--dry-run", action="store_true", help="No escribe archivos")
    parser.add_argument("--verbose", "-v", action="store_true", help="Logs detallados")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
    )

    logger.info("Refs de location-cr en: %s", LOCATION_REFS)
    snapshot = build_snapshot()
    ok_count = sum(1 for s in snapshot["sources"] if s.get("ok"))
    logger.info("Fuentes obtenidas correctamente: %d/%d", ok_count, len(snapshot["sources"]))

    section_md = render_auto_section(snapshot)
    changed_talent = upsert_auto_section(TALENT_FILE, section_md, args.dry_run)
    changed_costs = upsert_auto_section(COSTS_FILE, section_md, args.dry_run)

    prev = load_previous_snapshot()
    write_changelog(prev, snapshot, args.dry_run)

    if not args.dry_run:
        SNAPSHOT_FILE.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2),
                                 encoding="utf-8")

    logger.info("Hecho. Archivos modificados: %s",
                ", ".join(n for n, c in [("talent_cr.md", changed_talent),
                                         ("costs_cr.md", changed_costs)] if c) or "ninguno")

    # Exit 0 si al menos una fuente se obtuvo; 1 si todas fallaron.
    return 0 if ok_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
