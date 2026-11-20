# Recuperación de una clave al menor costo

Repo: https://github.com/p395699-rgb/modularArithmetic

Una estación cifra cada mensaje `m` con una clave secreta `k`: `c = (m · k) mod n`.
Cada mensaje del catálogo tiene un costo. Hay que elegir, sin ver respuestas, qué mensajes
enviar para identificar **cualquier** clave con el **menor costo total**.

## Idea clave

Un conjunto de mensajes `S` distingue todas las claves **si y solo si** `gcd(n, S) = 1`.
Si `g = gcd(n, S) > 1`, las claves `0` y `n/g` dan las mismas respuestas (testigo de ambigüedad).

## Algoritmo

Los estados son los divisores de `n`. Se empieza en `g = n`; enviar `m` lleva a `gcd(g, m)`
pagando su costo. El objetivo es llegar a `1` al menor costo, y eso lo resuelve
**Dijkstra** (`dijkstra` en `main.py`).

## Ejemplo (`n = 60`)

| Mensaje | 6 | 10 | 15 | 7 |
|---|--:|--:|--:|--:|
| Costo   | 2 | 2  | 2  | 9 |

- El 7 solo basta (`gcd(7, 60) = 1`), pero cuesta 9.
- **Plan óptimo: {6, 10, 15}, costo 6.** Claves compatibles tras cada respuesta: 6 → 2 → 1.
- Sin 7 ni 15, `gcd(60, 6, 10) = 2`: las claves 0 y 30 no se distinguen.

## Cómo ejecutar

```bash
git clone https://github.com/p395699-rgb/modularArithmetic.git
cd modularArithmetic
python3 main.py        # plan y ataque para n = 60
python3 app.py         # UI en http://localhost:8000
python3 -m pytest      # pruebas (requiere pytest)
```
