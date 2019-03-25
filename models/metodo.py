from pygame import mouse


def crear_arista(todos_los_nodos):
    lista = []
    while len(lista) < 2:
        mouse_clicked = mouse.get_pressed()
        mouse_pos = mouse.get_pos()

        for nodo in todos_los_nodos:
            if (
                nodo.x < mouse_pos[0] < nodo.x + nodo.width
                and nodo.y < mouse_pos[1] < nodo.y + nodo.height
                and mouse_clicked
            ):
                lista.append(nodo)
