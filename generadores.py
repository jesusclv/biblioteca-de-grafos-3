import math
import random
from typing import List, Set
from grafo import Grafo

# ===================================================================
# Script encargado de generar grafos de diferentes tipos y tamaños.
# ===================================================================

class GeneradorGrafos:
    @staticmethod
    def _peso_aleatorio(min_p: float = 1.0, max_p: float = 25.0) -> float:
        return round(random.uniform(min_p, max_p), 2)

    @staticmethod
    def malla(m: int, n: int, dirigido: bool = False) -> Grafo:
        g = Grafo(dirigido)
        for i in range(m):
            for j in range(n):
                actual = f"nodo_{i}_{j}"
                g.agregar_nodo(actual)
                if i < m - 1: g.agregar_arista(actual, f"nodo_{i+1}_{j}", GeneradorGrafos._peso_aleatorio())
                if j < n - 1: g.agregar_arista(actual, f"nodo_{i}_{j+1}", GeneradorGrafos._peso_aleatorio())
        return g

    @staticmethod
    def erdos_renyi(n: int, m: int, dirigido: bool = False) -> Grafo:
        g = Grafo(dirigido)
        for i in range(n): g.agregar_nodo(f"nodo_{i}")
        
        aristas_creadas = 0
        max_aristas = n * (n - 1) if dirigido else n * (n - 1) // 2
        m = min(m, max_aristas)

        while aristas_creadas < m:
            u, v = f"nodo_{random.randint(0, n - 1)}", f"nodo_{random.randint(0, n - 1)}"
            if u != v and v not in g.aristas[u]:
                g.agregar_arista(u, v, GeneradorGrafos._peso_aleatorio())
                aristas_creadas += 1
        return g

    @staticmethod
    def gilbert(n: int, p: float, dirigido: bool = False) -> Grafo:
        g = Grafo(dirigido)
        for i in range(n): g.agregar_nodo(f"nodo_{i}")
            
        for i in range(n):
            inicio_j = 0 if dirigido else i + 1
            for j in range(inicio_j, n):
                if i != j and random.random() < p:
                    g.agregar_arista(f"nodo_{i}", f"nodo_{j}", GeneradorGrafos._peso_aleatorio())
        return g

    @staticmethod
    def geografico(n: int, r: float, dirigido: bool = False) -> Grafo:
        g = Grafo(dirigido)
        for i in range(n):
            g.agregar_nodo(f"nodo_{i}", x=random.uniform(0, 1), y=random.uniform(0, 1))

        for i in range(n):
            for j in range(i + 1, n):
                id_u, id_v = f"nodo_{i}", f"nodo_{j}"
                n1, n2 = g.nodos[id_u], g.nodos[id_v]
                dist = math.hypot(n1.atributos['x'] - n2.atributos['x'], n1.atributos['y'] - n2.atributos['y'])
                if dist <= r:
                    peso_geo = round(max(dist * 100, 0.01), 2)
                    g.agregar_arista(id_u, id_v, peso_geo)
                    if dirigido: g.agregar_arista(id_v, id_u, peso_geo)
        return g

    @staticmethod
    def barabasi_albert(n: int, d: int, dirigido: bool = False) -> Grafo:
        g = Grafo(dirigido)
        for i in range(d): g.agregar_nodo(f"nodo_{i}")
        for i in range(d):
            for j in range(i + 1, d): g.agregar_arista(f"nodo_{i}", f"nodo_{j}", GeneradorGrafos._peso_aleatorio())
                
        for i in range(d, n):
            nuevo_nodo = f"nodo_{i}"
            g.agregar_nodo(nuevo_nodo)
            grados_nodos: List[str] = []
            for idx_previo in range(i):
                id_previo = f"nodo_{idx_previo}"
                grados_nodos.extend([id_previo] * len(g.aristas[id_previo]))
                    
            objetivos: Set[str] = set()
            while len(objetivos) < d and len(objetivos) < i:
                obj = random.choice(grados_nodos)
                if obj != nuevo_nodo: objetivos.add(obj)
                    
            for obj in objetivos: g.agregar_arista(nuevo_nodo, obj, GeneradorGrafos._peso_aleatorio())
        return g

    @staticmethod
    def dorogovtsev_mendes(n: int, dirigido: bool = False) -> Grafo:
        g = Grafo(dirigido)
        if n < 3: return g
        for i in range(3): g.agregar_nodo(f"nodo_{i}")
        g.agregar_arista("nodo_0", "nodo_1", GeneradorGrafos._peso_aleatorio())
        g.agregar_arista("nodo_1", "nodo_2", GeneradorGrafos._peso_aleatorio())
        g.agregar_arista("nodo_2", "nodo_0", GeneradorGrafos._peso_aleatorio())
        
        for i in range(3, n):
            nuevo_nodo = f"nodo_{i}"
            g.agregar_nodo(nuevo_nodo)
            arista_aleatoria = random.choice(g.obtener_todas_las_aristas())
            g.agregar_arista(nuevo_nodo, arista_aleatoria.fuente.id, GeneradorGrafos._peso_aleatorio())
            g.agregar_arista(nuevo_nodo, arista_aleatoria.destino.id, GeneradorGrafos._peso_aleatorio())
        return g