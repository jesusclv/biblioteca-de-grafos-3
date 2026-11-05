import heapq
import itertools
from collections import deque
from typing import Dict, List, Any, Set, Tuple, Union, Optional

# ===================================================================
# Script encargado de representar grafos y sus algoritmos asociados.
# ===================================================================

class Nodo:
    """Representa un vértice dentro del grafo."""
    def __init__(self, id_nodo: Union[int, str], **kwargs: Any):
        self.id = id_nodo
        self.atributos: Dict[str, Any] = kwargs

    def __str__(self) -> str:
        return str(self.id)


class Arista:
    """Representa la conexión entre dos nodos."""
    def __init__(self, fuente: Nodo, destino: Nodo, dirigido: bool = False, peso: float = 1.0):
        self.fuente = fuente
        self.destino = destino
        self.dirigido = dirigido
        self.peso = peso

    def __str__(self) -> str:
        conector = "->" if self.dirigido else "--"
        return f"{self.fuente.id} {conector} {self.destino.id} ({self.peso:.2f})"


class Grafo:
    def __init__(self, dirigido: bool = False):
        self.dirigido: bool = dirigido
        self.nodos: Dict[Union[int, str], Nodo] = {}
        self.aristas: Dict[Union[int, str], Dict[Union[int, str], Arista]] = {}

    def agregar_nodo(self, id_nodo: Union[int, str], **kwargs: Any) -> None:
        if id_nodo not in self.nodos:
            self.nodos[id_nodo] = Nodo(id_nodo, **kwargs)
            self.aristas[id_nodo] = {}

    def agregar_arista(self, id_fuente: Union[int, str], id_destino: Union[int, str], peso: float = 1.0) -> None:
        self.agregar_nodo(id_fuente)
        self.agregar_nodo(id_destino)
        
        if id_destino in self.aristas[id_fuente]:
            return
            
        nueva_arista = Arista(self.nodos[id_fuente], self.nodos[id_destino], self.dirigido, peso)
        self.aristas[id_fuente][id_destino] = nueva_arista
        
        if not self.dirigido:
            self.aristas[id_destino][id_fuente] = nueva_arista

    def obtener_todas_las_aristas(self) -> List[Arista]:
        todas: List[Arista] = []
        visitadas: Set[Tuple[str, str]] = set()
        
        for origen, conexiones in self.aristas.items():
            for destino, arista in conexiones.items():
                if not self.dirigido:
                    conexion = tuple(sorted([str(origen), str(destino)]))
                    if conexion not in visitadas:
                        todas.append(arista)
                        visitadas.add(conexion)
                else:
                    todas.append(arista)
        return todas

    def exportar_dot(self, nombre_archivo: str, mostrar_peso_arista: bool = True) -> None:
        tipo_grafo = "digraph" if self.dirigido else "graph"
        conector = "->" if self.dirigido else "--"

        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(f"{tipo_grafo} G {{\n")
            for id_nodo in self.nodos:
                f.write(f'  "{id_nodo}";\n')
            
            for arista in self.obtener_todas_las_aristas():
                if mostrar_peso_arista:
                    f.write(
                        f'  "{arista.fuente.id}" {conector} "{arista.destino.id}" '
                        f'[weight={arista.peso:.2f}, label="{arista.peso:.2f}"];\n'
                    )
                else:
                    f.write(f'  "{arista.fuente.id}" {conector} "{arista.destino.id}";\n')
            f.write("}\n")

    #* Algoritmos de búsqueda (BFS y DFS)
    def BFS(self, s: Union[int, str]) -> 'Grafo':
        if s not in self.nodos: raise ValueError(f"El nodo '{s}' no existe.")
        arbol = Grafo(dirigido=self.dirigido)
        visitados: Set[Union[int, str]] = {s}
        cola: deque = deque([s])
        arbol.agregar_nodo(s, **self.nodos[s].atributos)

        while cola:
            u = cola.popleft()
            for v, arista in self.aristas[u].items():
                if v not in visitados:
                    visitados.add(v)
                    arbol.agregar_nodo(v, **self.nodos[v].atributos)
                    arbol.agregar_arista(u, v, arista.peso)
                    cola.append(v)
        return arbol

    def DFS_R(self, s: Union[int, str]) -> 'Grafo':
        if s not in self.nodos: raise ValueError(f"El nodo '{s}' no existe.")
        arbol = Grafo(dirigido=self.dirigido)
        visitados: Set[Union[int, str]] = set()

        def _dfs(u: Union[int, str]) -> None:
            visitados.add(u)
            arbol.agregar_nodo(u, **self.nodos[u].atributos)
            for v, arista in self.aristas[u].items():
                if v not in visitados:
                    arbol.agregar_nodo(v, **self.nodos[v].atributos)
                    arbol.agregar_arista(u, v, arista.peso)
                    _dfs(v)

        _dfs(s)
        return arbol

    def DFS_I(self, s: Union[int, str]) -> 'Grafo':
        if s not in self.nodos: raise ValueError(f"El nodo '{s}' no existe.")
        arbol = Grafo(dirigido=self.dirigido)
        visitados: Set[Union[int, str]] = set()
        pila: List[Tuple[Optional[Union[int, str]], Union[int, str], float]] = [(None, s, 1.0)]

        while pila:
            padre, u, peso = pila.pop()
            if u not in visitados:
                visitados.add(u)
                arbol.agregar_nodo(u, **self.nodos[u].atributos)
                if padre is not None: arbol.agregar_arista(padre, u, peso)
                for v, arista in self.aristas[u].items():
                    if v not in visitados:
                        pila.append((u, v, arista.peso))
        return arbol

    #* Algoritmo de Dijkstra
    def Dijkstra(self, s: Union[int, str]) -> 'Grafo':
        if s not in self.nodos: raise ValueError(f"El nodo '{s}' no existe.")

        distancias: Dict[Union[int, str], float] = {nodo: float('inf') for nodo in self.nodos}
        padres: Dict[Union[int, str], Optional[Union[int, str]]] = {s: None}
        peso_arista_padre: Dict[Union[int, str], float] = {}
        visitados: Set[Union[int, str]] = set()

        distancias[s] = 0.0
        contador = itertools.count() 
        cola_prioridad: List[Tuple[float, int, Union[int, str]]] = [(0.0, next(contador), s)]

        while cola_prioridad:
            dist_u, _, u = heapq.heappop(cola_prioridad)
            if u in visitados: continue
            visitados.add(u)

            for v, arista in self.aristas[u].items():
                if v not in visitados:
                    nueva_dist = dist_u + arista.peso
                    if nueva_dist < distancias[v]:
                        distancias[v] = nueva_dist
                        padres[v] = u
                        peso_arista_padre[v] = arista.peso
                        heapq.heappush(cola_prioridad, (nueva_dist, next(contador), v))

        arbol = Grafo(dirigido=self.dirigido)
        mapa_etiquetas: Dict[Union[int, str], str] = {}

        for u in visitados:
            etiqueta = f"{u} ({distancias[u]:.2f})"
            mapa_etiquetas[u] = etiqueta
            arbol.agregar_nodo(etiqueta, distancia=round(distancias[u], 2), **self.nodos[u].atributos)

        for v in visitados:
            u_padre = padres.get(v)
            if u_padre is not None:
                arbol.agregar_arista(mapa_etiquetas[u_padre], mapa_etiquetas[v], peso=peso_arista_padre[v])

        return arbol