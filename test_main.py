from itertools import combinations

from main import (
    COSTO, N, par_ambiguo, pasos_ataque, gcd_acumulado, dijkstra, distingue_todas,
    distingue_por_respuesta, crear_estacion, plan_minimo, ejecutar_ataque, verificar_todas,
)


def test_plan_optimo_gana_al_7():
    """Plan de costo mínimo

    El plan más barato es {6, 10, 15} con costo 6; el mensaje 7 solo cuesta 9.
    """
    costo, plan = plan_minimo(N, COSTO)
    assert costo == 6
    assert sorted(plan) == [6, 10, 15]


def test_recupera_las_60_claves():
    """Recuperación de las 60 claves

    El plan recupera cualquiera de las 60 claves.
    """
    _, plan = plan_minimo(N, COSTO)
    for clave in range(N):
        assert ejecutar_ataque(N, plan, crear_estacion(N, clave), mostrar=False) == clave
    assert verificar_todas(N, plan)


def reproduce(clave, respuestas):
    """True si la clave produce exactamente cada respuesta c recibida."""
    return all(m * clave % N == c for m, c in respuestas)


def revisar_paso(secreta, respuestas, claves):
    """Comprueba las claves compatibles reportadas tras una respuesta."""
    g = gcd_acumulado(N, [m for m, _ in respuestas])
    assert secreta in claves
    assert all((k in claves) == reproduce(k, respuestas) for k in range(N))
    assert len(claves) == g
    assert claves == [k for k in range(N) if (k - secreta) % (N // g) == 0]


def test_claves_compatibles():
    """Claves compatibles

    Las claves compatibles dan exactamente las respuestas recibidas; las descartadas no.
    """
    _, plan = plan_minimo(N, COSTO)
    for secreta in range(N):
        respuestas = []
        for m, c, claves in pasos_ataque(N, plan, crear_estacion(N, secreta)):
            respuestas.append((m, c))
            revisar_paso(secreta, respuestas, claves)


def test_sin_7_ni_15_es_ambiguo():
    """Catálogo insuficiente

    Sin los mensajes 7 y 15 no alcanza: dos claves distintas dan las mismas respuestas.
    """
    reducido = {6: 2, 10: 2}
    assert plan_minimo(N, reducido) is None
    k1, k2 = par_ambiguo(N, reducido)
    assert k1 != k2
    assert all(m * k1 % N == m * k2 % N for m in reducido)


def test_criterio_gcd_igual_a_definicion():
    """Criterio del gcd

    La regla gcd = 1 da lo mismo que comparar las respuestas de todas las claves.
    """
    for tamano in range(len(COSTO) + 1):
        for subconjunto in combinations(COSTO, tamano):
            assert distingue_todas(N, subconjunto) == distingue_por_respuesta(N, subconjunto)


def test_dijkstra_costo_creciente():
    """Dijkstra

    Avanza de menor a mayor costo: de 60 (costo 0) a 1 (costo 6).
    """
    _, orden = dijkstra(N, COSTO)
    lista_costos = [costo for _, costo in orden]
    assert lista_costos == sorted(lista_costos)
    assert orden[0] == (N, 0) and orden[-1] == (1, 6)
