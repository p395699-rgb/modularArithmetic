"""Recuperar la clave k de c = m·k mod n al menor costo."""
import heapq
from math import gcd

N = 60
COSTO = {6: 2, 10: 2, 15: 2, 7: 9}  # mensaje -> costo


def gcd_acumulado(n, mensajes):
    """gcd de n y los mensajes."""
    return gcd(n, *mensajes)


def distingue_todas(n, mensajes):
    """True si el gcd es 1."""
    return gcd_acumulado(n, mensajes) == 1


def distingue_por_respuesta(n, mensajes):
    """True si cada clave da respuestas distintas."""
    vectores = {tuple(m * k % n for m in mensajes) for k in range(n)}
    return len(vectores) == n


def par_ambiguo(n, mensajes):
    """Dos claves que no se distinguen."""
    g = gcd_acumulado(n, mensajes)
    return None if g == 1 else (0, n // g)


def dijkstra(n, costos):
    """Camino más barato de n a 1."""
    mejor, cola, orden = {n: (0, [])}, [(0, n)], []
    while cola:
        costo, g = heapq.heappop(cola)
        if costo > mejor[g][0]:  # ya visto
            continue
        orden.append((g, costo))
        if g == 1:
            break
        for m, c in costos.items():
            h = gcd(g, m)
            if h not in mejor or costo + c < mejor[h][0]:
                mejor[h] = (costo + c, mejor[g][1] + [m])
                heapq.heappush(cola, (costo + c, h))
    return mejor, orden


def plan_minimo(n, costos):
    """(costo, plan) o None."""
    mejor, _ = dijkstra(n, costos)
    return mejor.get(1)



def crear_estacion(n, clave):
    """Cifra con una clave secreta."""
    return lambda m: m * clave % n


def claves_compatibles(n, respuestas):
    """Claves que dan esas respuestas."""
    return [k for k in range(n) if all(m * k % n == c for m, c in respuestas)]


def pasos_ataque(n, plan, estacion):
    """(mensaje, cifrado, claves) por paso."""
    respuestas, pasos = [], []
    for m in plan:
        respuestas.append((m, estacion(m)))
        pasos.append((m, respuestas[-1][1], claves_compatibles(n, respuestas)))
    return pasos


def ejecutar_ataque(n, plan, estacion, mostrar=True):
    """Devuelve la clave encontrada."""
    pasos = pasos_ataque(n, plan, estacion)
    if mostrar:
        for m, c, restantes in pasos:
            print(f"  mensaje {m:>3} -> {c:>3}  | claves compatibles: {len(restantes)}")
    restantes = pasos[-1][2] if pasos else list(range(n))
    return restantes[0] if len(restantes) == 1 else None


def verificar_todas(n, plan):
    """True si funciona con todas las claves."""
    return all(ejecutar_ataque(n, plan, crear_estacion(n, k), mostrar=False) == k for k in range(n))


def resolver(n, costos, clave_secreta):
    print(f"n = {n}, catálogo = {costos}")
    resultado = plan_minimo(n, costos)
    if resultado is None:
        print(f"  Catálogo insuficiente. Claves indistinguibles: {par_ambiguo(n, costos)}")
        return
    costo, plan = resultado
    print(f"  Plan óptimo: {plan} (costo {costo})")
    clave = ejecutar_ataque(n, plan, crear_estacion(n, clave_secreta))
    print(f"  Clave recuperada: {clave} | costo total: {costo}")


def main():
    resolver(N, COSTO, clave_secreta=37)
    print()
    reducido = {m: c for m, c in COSTO.items() if m not in (7, 15)}
    resolver(N, reducido, clave_secreta=37)


if __name__ == "__main__":
    main()
