"""UI mínima: python3 app.py y abrir http://localhost:8000"""
import importlib
import inspect
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from main import par_ambiguo, pasos_ataque, dijkstra, crear_estacion, verificar_todas

PAGINA = Path(__file__).with_name("index.html")
ESTILOS = Path(__file__).with_name("styles.css")
N_MAX = 1000


def leer_peticion(datos):
    """Valida la entrada y devuelve (n, catálogo, clave)."""
    n, clave = int(datos["n"]), int(datos["key"])
    costos = {int(m): int(c) for m, c in datos["catalog"]}
    if not 2 <= n <= N_MAX:
        raise ValueError(f"n debe estar entre 2 y {N_MAX}")
    if not 0 <= clave < n:
        raise ValueError("la clave debe estar entre 0 y n − 1")
    if any(c <= 0 for c in costos.values()):
        raise ValueError("los costos deben ser positivos")
    return n, costos, clave


def resolver(n, costos, clave):
    """Resultado del diseño y la ejecución del ataque, listo para JSON."""
    mejor, orden = dijkstra(n, costos)
    if 1 not in mejor:
        return {"ok": False, "pair": par_ambiguo(n, costos), "dijkstra": orden}
    costo, plan = mejor[1]
    pasos = pasos_ataque(n, plan, crear_estacion(n, clave))
    return {
        "ok": True, "plan": plan, "cost": costo, "dijkstra": orden,
        "verified": verificar_todas(n, plan),
        "steps": [{"m": m, "c": c, "keys": claves} for m, c, claves in pasos],
    }


def correr_prueba(prueba):
    """Ejecuta una prueba y devuelve su resultado, listo para JSON."""
    inicio = time.perf_counter()
    try:
        prueba()
        ok, error = True, ""
    except Exception as e:  # una prueba fallida no debe tumbar el servidor
        ok, error = False, f"{type(e).__name__}: {e}"
    ms = (time.perf_counter() - inicio) * 1000
    titulo, _, doc = (inspect.getdoc(prueba) or prueba.__name__).partition("\n\n")  # 1.ª línea = nombre
    return {"name": prueba.__name__, "title": titulo, "doc": doc, "ok": ok, "error": error, "ms": round(ms, 1)}


def correr_pruebas():
    """Corre todas las funciones test_* de test_main.py.

    Se importa desde cero (no con reload) para que las pruebas borradas desaparezcan.
    """
    sys.modules.pop("test_main", None)
    modulo = importlib.import_module("test_main")
    pruebas = [getattr(modulo, n) for n in dir(modulo) if n.startswith("test_")]
    pruebas.sort(key=lambda prueba: prueba.__code__.co_firstlineno)
    return [correr_prueba(prueba) for prueba in pruebas]


class Manejador(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/tests":
            self.responder(200, json.dumps(correr_pruebas()).encode(), "application/json")
        elif self.path == "/styles.css":
            self.responder(200, ESTILOS.read_bytes(), "text/css; charset=utf-8")
        else:
            self.responder(200, PAGINA.read_bytes(), "text/html; charset=utf-8")

    def do_POST(self):
        try:
            cuerpo = self.rfile.read(int(self.headers["Content-Length"]))
            salida, estado = resolver(*leer_peticion(json.loads(cuerpo))), 200
        except (ValueError, KeyError, TypeError) as e:
            salida, estado = {"error": str(e)}, 400
        self.responder(estado, json.dumps(salida).encode(), "application/json")

    def responder(self, estado, cuerpo, tipo):
        self.send_response(estado)
        self.send_header("Content-Type", tipo)
        self.end_headers()
        self.wfile.write(cuerpo)


if __name__ == "__main__":
    print("Abrir http://localhost:8000")
    HTTPServer(("localhost", 8000), Manejador).serve_forever()
