"""Pruebas del correo P2 (Marco Cedeño · Transporte) sobre src/dijkstra.py.

Ejecutar desde la raíz del repo:
    python -m pytest tests/test_dijkstra_p2.py -v
"""
import math
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dijkstra import (TRAMOS_P2, _dijkstra_nucleo, dijkstra,  # noqa: E402
                      existe_ruta_con_costo_max, leer_grafo, ruta_minima)


@pytest.fixture
def red():
    return leer_grafo(TRAMOS_P2, dirigido=True)


def costo_de(grafo, ruta):
    """Verificador independiente: suma los pesos de una ruta dada."""
    total = 0
    for u, v in zip(ruta, ruta[1:]):
        pesos = [w for x, w in grafo[u] if x == v]
        assert pesos, f"no existe el tramo {u} -> {v}"
        total += min(pesos)
    return total


# ----------------------------------------------------------- casos normales
def test_distancias_desde_quito(red):
    dist, _ = dijkstra(red, "Quito")
    assert dist == {"Quito": 0, "Latacunga": 2, "Ambato": 5, "Guayaquil": 8}


def test_ruta_reportada_a_guayaquil(red):
    assert ruta_minima(red, "Quito", "Guayaquil") == (8, ["Quito", "Latacunga", "Guayaquil"])


def test_empate_de_costo_8(red):
    # Las dos rutas del expediente cuestan lo mismo: ambas son óptimas.
    assert costo_de(red, ["Quito", "Latacunga", "Guayaquil"]) == 8
    assert costo_de(red, ["Quito", "Ambato", "Guayaquil"]) == 8


def test_desempate_no_depende_del_orden_de_entrada():
    # Aunque Ambato se lea primero, Latacunga (dist 2) sale antes de la cola,
    # fija dist[Guayaquil] = 8 y, por el '<' estricto, Ambato no lo reemplaza.
    red_inv = leer_grafo(list(reversed(TRAMOS_P2)), dirigido=True)
    assert ruta_minima(red_inv, "Quito", "Guayaquil") == (8, ["Quito", "Latacunga", "Guayaquil"])


def test_version_de_decision(red):
    assert existe_ruta_con_costo_max(red, "Quito", "Guayaquil", 8) is True
    assert existe_ruta_con_costo_max(red, "Quito", "Guayaquil", 7) is False


# -------------------------------------------------------------- casos límite
def test_origen_igual_a_destino(red):
    assert ruta_minima(red, "Quito", "Quito") == (0, ["Quito"])


def test_sin_ruta_en_sentido_contrario(red):
    # Los tramos son dirigidos: no hay ruta de Guayaquil hacia Quito.
    assert ruta_minima(red, "Guayaquil", "Quito") == (math.inf, None)
    assert existe_ruta_con_costo_max(red, "Guayaquil", "Quito", 10**9) is False


def test_peso_cero_permitido():
    g = leer_grafo([("Quito", "Latacunga", 0), ("Latacunga", "Guayaquil", 6)], dirigido=True)
    assert ruta_minima(g, "Quito", "Guayaquil") == (6, ["Quito", "Latacunga", "Guayaquil"])


# ----------------------------------------------------------- casos inválidos
def test_rechaza_peso_negativo():
    with pytest.raises(ValueError, match="peso negativo"):
        leer_grafo([("Quito", "Ambato", -1)], dirigido=True)


@pytest.mark.parametrize("peso, error", [("5", TypeError), (True, TypeError),
                                          (math.nan, ValueError), (math.inf, ValueError)])
def test_rechaza_pesos_no_validos(peso, error):
    with pytest.raises(error):
        leer_grafo([("Quito", "Ambato", peso)], dirigido=True)


def test_rechaza_nodo_inexistente(red):
    with pytest.raises(ValueError, match="no pertenece"):
        ruta_minima(red, "Quito", "Cuenca")


def test_rechaza_limite_no_numerico(red):
    with pytest.raises(TypeError):
        existe_ruta_con_costo_max(red, "Quito", "Guayaquil", "8")


# ------------------------------------- contraejemplo con peso negativo (§5)
def test_contraejemplo_peso_negativo_sin_validar():
    # Quito->A (1), Quito->B (2), B->A (-2): la ruta real Quito->B->A cuesta 0,
    # pero el núcleo sin validación finaliza A con 1 y ya no lo corrige.
    g = {"Quito": [("A", 1), ("B", 2)], "B": [("A", -2)], "A": []}
    dist, _ = _dijkstra_nucleo(g, "Quito")
    assert dist["A"] == 1          # respuesta incorrecta (la correcta es 0)
