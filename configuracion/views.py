import re
from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.management import call_command
from django.conf import settings
from usuario.decorators import admin_required


ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def _leer_env(clave: str, default: str = "") -> str:
    """Lee el valor actual de una clave en el .env."""
    if not ENV_PATH.exists():
        return default
    contenido = ENV_PATH.read_text(encoding="utf-8")
    patron = re.compile(rf"^{re.escape(clave)}\s*=\s*(.+)$", re.MULTILINE)
    match = patron.search(contenido)
    return match.group(1).strip() if match else default


def _actualizar_env(clave: str, valor: str):
    """Reemplaza o agrega una clave en el archivo .env."""
    if not ENV_PATH.exists():
        ENV_PATH.write_text(f"{clave}={valor}\n", encoding="utf-8")
        return

    contenido = ENV_PATH.read_text(encoding="utf-8")
    patron = re.compile(rf"^{re.escape(clave)}\s*=.*$", re.MULTILINE)

    if patron.search(contenido):
        nuevo = patron.sub(f"{clave}={valor}", contenido)
    else:
        nuevo = contenido.rstrip("\n") + f"\n{clave}={valor}\n"

    ENV_PATH.write_text(nuevo, encoding="utf-8")


def _forzar_recarga():
    """Toca settings.py y views.py para forzar recarga del runserver."""
    base = Path(__file__).resolve().parent.parent
    for path in [
        base / "core" / "settings.py",
        Path(__file__).resolve(),
    ]:
        if path.exists():
            path.touch()


@admin_required
def configuracion_view(request):

    almacenamiento_actual = _leer_env("DB_ENGINE", default="nube")

    if request.method == "POST":
        almacenamiento = request.POST.get("almacenamiento", "nube")

        # Si el usuario quiere cambiar a local y actualmente está en la nube, sincronizamos
        if almacenamiento == "local" and almacenamiento_actual == "nube":
            db_path = settings.BASE_DIR / "db.sqlite3"
            if db_path.exists():
                db_path.unlink()

            call_command("migrate", database="local_db")

            dump_path = settings.BASE_DIR / "neon_dump.json"
            with open(dump_path, "w", encoding="utf-8") as f:
                call_command(
                    "dumpdata",
                    database="neon_db",
                    exclude=[
                        "contenttypes",
                        "auth.Permission",
                        "sessions.session",
                    ],
                    indent=2,
                    stdout=f,
                )

            call_command("loaddata", dump_path, database="local_db")

            if dump_path.exists():
                dump_path.unlink()

        _actualizar_env("DB_ENGINE", almacenamiento)
        _forzar_recarga()

        # Cierra sesión para que el admin entre con la nueva BD activa
        request.session.flush()

        nombre_bd = (
            "Local (SQLite)" if almacenamiento == "local" else "Nube (Neon PostgreSQL)"
        )
        messages.success(
            request,
            f" Base de datos cambiada a {nombre_bd}. "
            "Espera 3 segundos e inicia sesión nuevamente.",
        )
        return redirect("login")

    class Config:
        pass

    config = Config()
    config.almacenamiento = almacenamiento_actual

    context = {"config": config}

    return render(request, "configuracion.html", context)


@admin_required
@require_GET
def probar_conexion_neon(request):
    try:
        import psycopg2
        import environ
        from django.conf import settings
        env = environ.Env()
        environ.Env.read_env(settings.BASE_DIR / ".env")

        conn = psycopg2.connect(
            dbname=env("DB_NAME", default=""),
            user=env("DB_USER", default=""),
            password=env("DB_PASSWORD", default=""),
            host=env("DB_HOST", default=""),
            port=env("DB_PORT", default="5432"),
            connect_timeout=5,
            sslmode="require",
        )
        conn.close()
        return JsonResponse({"ok": True})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)})
