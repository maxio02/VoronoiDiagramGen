import tkinter as tk
from dataclasses import dataclass
import random

WIDTH = 1600
HEIGHT = 900


@dataclass
class point:
    x: int
    y: int
    radius: int


@dataclass
class edge:
    p1: point
    p2: point


def generate_points(n: int) -> list[point]:
    points = []
    for i in range(n):
        points.append(point(random.randint(15, WIDTH-15),
                      random.randint(15, HEIGHT-15), 5))
    return points


def draw_points(points: list[point]):
    for point in points:
        canvas.create_oval(point.x - point.radius, point.y-point.radius,
                           point.x+point.radius, point.y+point.radius, fill='black')


def draw_edges(edges: list[edge]):
    for edge in edges:
        canvas.create_line(edge.p1.x, edge.p1.y, edge.p2.x,
                           edge.p2.y, fill='black')


def generate_all_edges(points: list[point]) -> list[edge]:
    edges = []
    for point1 in points:
        for point2 in points:
            edges.append(edge(point1, point2))
    return edges

def generate_new_pattern_diagram():
    
    canvas.delete('all')
    points = generate_points(int(entry.get()))
    edges = generate_all_edges(points)
    draw_points(points)
    draw_edges(edges)
    canvas.pack()

window = tk.Tk()


canvas = tk.Canvas(window, width=1600, height=900)
canvas.pack()



button = tk.Button(window, text="Generate new pattern", command=generate_new_pattern_diagram)
button.place(x=WIDTH-button.winfo_reqwidth()-10, y=HEIGHT-button.winfo_reqheight()-10)

entry = tk.Entry(window,width=5)

entry.place(x=WIDTH-button.winfo_x()-button.winfo_reqwidth()-50, y=HEIGHT-entry.winfo_reqheight()-10)


window.mainloop()


