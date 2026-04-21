"""Notificaciones del pipeline vía Telegram con fallback a GitHub issue.

Filosofía: el pipeline nunca debe perder editorial por un fallo de
notificación. Si Telegram cae, intentamos abrir un issue en el repo con
`gh` CLI. Si ambos fallan, el error se loguea y el pipeline continúa.

Uso típico:
    from src.notify import notify
    notify("Resumen semanal publicado OK", level="ok")

Niveles soportados: "ok" | "info" | "warning" | "critical".
"""
from __future__ import annotations

import logging
import os
import subprocess
from typing import Final

import httpx

log = logging.getLogger("notify")

_LEVEL_ICON: Final[dict[str, str]] = {
    "ok": "✅",
    "info": "ℹ️",
    "warning": "⚠️",
    "critical": "🚨",
}

_TELEGRAM_TIMEOUT_S: Final[float] = 10.0


def send_telegram(message: str, level: str = "info") -> bool:
    """Envía un mensaje al chat configurado. Devuelve True si Telegram acusa 200.

    Si faltan los secrets o la API devuelve error, devuelve False sin lanzar.
    Deliberadamente silencioso ante fallos para no romper el pipeline.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat:
        log.warning("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID no configurados; skip.")
        return False

    icon = _LEVEL_ICON.get(level, "")
    text = f"{icon} {message}".strip()

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": "true",
    }
    try:
        resp = httpx.post(url, data=payload, timeout=_TELEGRAM_TIMEOUT_S)
        if resp.status_code == 200 and resp.json().get("ok"):
            return True
        log.error("Telegram respondió %d: %s", resp.status_code, resp.text[:300])
        return False
    except Exception as exc:  # noqa: BLE001
        log.error("Telegram excepción: %s", exc)
        return False


def _fallback_github_issue(message: str, level: str) -> bool:
    """Abre un issue en el repo como red de seguridad si Telegram falla.

    Requiere `gh` CLI autenticado (disponible en Actions vía GH_TOKEN o en el
    entorno local del usuario). Devuelve True si el issue se crea.
    """
    title = f"[{level.upper()}] Alerta pipeline ({message[:60].splitlines()[0]})"
    body = (
        f"Telegram no pudo entregar esta alerta. Cuerpo original:\n\n"
        f"```\n{message}\n```"
    )
    try:
        result = subprocess.run(
            [
                "gh",
                "issue",
                "create",
                "--title",
                title,
                "--body",
                body,
                "--label",
                "alerta",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        if result.returncode == 0:
            log.warning("Alerta caída a issue GitHub: %s", result.stdout.strip())
            return True
        # Si la etiqueta "alerta" no existe, reintenta sin label
        if "label" in (result.stderr or ""):
            result = subprocess.run(
                ["gh", "issue", "create", "--title", title, "--body", body],
                check=False,
                capture_output=True,
                text=True,
                timeout=20,
            )
            if result.returncode == 0:
                log.warning("Alerta caída a issue (sin label): %s", result.stdout.strip())
                return True
        log.error("gh issue create falló: %s", result.stderr[:300])
        return False
    except Exception as exc:  # noqa: BLE001
        log.error("Fallback gh issue excepción: %s", exc)
        return False


def notify(message: str, level: str = "info") -> bool:
    """Intenta Telegram; si falla, intenta abrir issue en GitHub (solo en Actions).

    Devuelve True si alguno de los dos canales entregó. False si ambos fallaron.
    Nunca lanza: las notificaciones son best-effort y no deben romper el pipeline.

    Política de fallback:
    - En GitHub Actions (GITHUB_ACTIONS=true): si Telegram falla, abre issue.
      El editor no está delante; necesitamos dejar traza en el repo.
    - En local (sin GITHUB_ACTIONS): si Telegram falla, log y silencio. El
      editor ya ve el output en terminal; no tiene sentido ensuciar issues.
    - Excepción: si level=="critical" siempre se intenta fallback (es una
      alerta crítica que no queremos perder bajo ninguna circunstancia).
    """
    if send_telegram(message, level):
        return True

    in_actions = os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
    if not in_actions and level != "critical":
        log.info("Telegram no disponible en local; alerta visible en stdout. Skip fallback a issue.")
        return False

    log.warning("Telegram falló; intentando fallback a issue GitHub.")
    return _fallback_github_issue(message, level)


def main() -> int:
    """Smoke test manual: `python -m src.notify`."""
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s] %(message)s")
    ok = notify("Smoke test desde `src.notify` (ignorar).", level="info")
    print("ok" if ok else "fail")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
