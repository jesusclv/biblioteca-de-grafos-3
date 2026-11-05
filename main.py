import os
import sys
import math
import subprocess
from generadores import GeneradorGrafos

# ==================================================================
# Punto de entrada del generaddor de grafos
# ==================================================================

# Ampliar límite de recursión por si utilizas DFS_R en pruebas
sys.setrecursionlimit(2000)

def renderizar_imagenes_graphviz(carpeta_origen: str, carpeta_destino: str) -> None:
    os.makedirs(carpeta_destino, exist_ok=True)
    for archivo in sorted(os.listdir(carpeta_origen)):
        if archivo.endswith(".gv"):
            ruta_gv = os.path.join(carpeta_origen, archivo)
            ruta_png = os.path.join(carpeta_destino, archivo.replace(".gv", ".png"))
            comando = ["sfdp", "-Tpng", "-Goverlap=prism", ruta_gv, "-o", ruta_png]
            try:
                subprocess.run(comando, check=True)
                print(f"  [PNG] Imagen generada: {ruta_png}")
            except FileNotFoundError:
                print("  [Aviso] 'sfdp' no encontrado. Verifica tu instalación de Graphviz.")
                break

if __name__ == "__main__":
    dir_generados = os.path.join("archivos_gv", "generados")
    dir_calculados = os.path.join("archivos_gv", "calculados")
    dir_img_generados = os.path.join("imagenes", "generados")
    dir_img_calculados = os.path.join("imagenes", "calculados")

    os.makedirs(dir_generados, exist_ok=True)
    os.makedirs(dir_calculados, exist_ok=True)

    configuraciones = {
        "pocos_30": {"n": 30, "malla": (6, 5)},
        "muchos_200": {"n": 200, "malla": (20, 10)}
    }

    for etiqueta_tam, params in configuraciones.items():
        tam = params["n"]
        m_filas, n_cols = params["malla"]

        grafos_generados = {
            f"Malla_{etiqueta_tam}": GeneradorGrafos.malla(m_filas, n_cols),
            f"ErdosRenyi_{etiqueta_tam}": GeneradorGrafos.erdos_renyi(tam, tam * 3),
            f"Gilbert_{etiqueta_tam}": GeneradorGrafos.gilbert(tam, 6.0 / tam),
            f"Geografico_{etiqueta_tam}": GeneradorGrafos.geografico(tam, math.sqrt(10 / (math.pi * tam))),
            f"BarabasiAlbert_{etiqueta_tam}": GeneradorGrafos.barabasi_albert(tam, 3),
            f"DorogovtsevMendes_{etiqueta_tam}": GeneradorGrafos.dorogovtsev_mendes(tam)
        }

        for nombre, grafo in grafos_generados.items():
            # Exportar grafo original
            ruta_gv_original = os.path.join(dir_generados, f"{nombre}.gv")
            grafo.exportar_dot(ruta_gv_original)

            # Seleccionar origen y calcular Dijkstra
            nodo_origen = next(iter(grafo.nodos))
            arbol_dijkstra = grafo.Dijkstra(nodo_origen)

            # Exportar árbol
            ruta_gv_dijkstra = os.path.join(dir_calculados, f"{nombre}_Dijkstra.gv")
            arbol_dijkstra.exportar_dot(ruta_gv_dijkstra)

            print(f"[OK] {nombre}: Procesado con Dijkstra.")

    print("\nRenderizando imágenes PNG con Graphviz...")
    renderizar_imagenes_graphviz(dir_generados, dir_img_generados)
    renderizar_imagenes_graphviz(dir_calculados, dir_img_calculados)
    print("\nProceso completado exitosamente.")