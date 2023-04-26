import tkinter as tk
from dataclasses import dataclass
import random
import heapq
from bst import Node
WIDTH = 1600
HEIGHT = 900
line_y = 500
points = []


@dataclass
class point:
    x: int
    y: int
    radius: int


@dataclass
class edge:
    p1: point
    p2: point


class arc:
    def __init__(self, apex: point):
        self.apex = apex

    # apex (h, k)
    # focus (h, k + p)
    def f(self, x):
        x1 = self.apex.x
        y1 = self.apex.y
        
        return (1/((2*(y1-line_y)))    *    ((x-x1)**2 + y1**2 - line_y**2))
        #return ((x1**2  -  2*x1*x   +    4*y1*p+x**2)/4/p)


def generate_points(n: int) -> list[point]:
    global points
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
        

def update_line(liney):
    global line_y 
    line_y = int(liney)
    draw(points)


def draw_line():
    canvas.create_line(0,line_y,WIDTH,line_y)


def generate_all_edges(points: list[point]) -> list[edge]:
    edges = []
    for point1 in points:
        for point2 in points:
            edges.append(edge(point1, point2))
    return edges


def calc_parabolas(points:list[point], line: int):
    parabolas = []
    for pt in points:
        parabolas.append(arc(pt))
    return parabolas


def draw_parabolas(parabolas:list[arc]):
    for parabola in parabolas:
        if parabola.apex.y < line_y:
            for i in range(0, WIDTH, 10):
                x = i
                y = parabola.f(x)
                if y > 0:
                    canvas.create_line(x, y, x+10, parabola.f(x+10), fill='black')


def draw(points):
    canvas.delete('all')
    draw_points(points)
    parabolas = calc_parabolas(points, line_y)
    draw_parabolas(parabolas)
    draw_line()

def sort_points_by(points: list[point], axis: str) -> list[point]:
    match axis:
        case 'x':
            points.sort(key=lambda p: p.x)
        case 'y':
            points.sort(key=lambda p: p.y)

    return points




def generate_new_pattern_diagram():
    points = generate_points(int(entry.get()))
    points = sort_points_by(points, 'x')

    draw(points)
    

    '''Q = []
        for point in points:
            heapq.heappush(Q,'site')

        beachline = Node(0)


        while Q:
            event = heapq.heappop()
             match event:
                case 'site':

                case 'vertex':

        edges = generate_all_edges(points)'''


    # Loop through the range of x values, plot each point on the canvas
    draw(points)
    # draw_edges(edges)
    canvas.pack()


window = tk.Tk()



canvas = tk.Canvas(window, width=1600, height=900)
canvas.pack()


button = tk.Button(window, text="Generate new pattern",
                   command=generate_new_pattern_diagram)
button.place(x=WIDTH-button.winfo_reqwidth()-10,
             y=HEIGHT-button.winfo_reqheight()-10)

entry = tk.Entry(window, width=5)

entry.place(x=WIDTH-button.winfo_x()-button.winfo_reqwidth() -
            50, y=HEIGHT-entry.winfo_reqheight()-10)

slider = tk.Scale(window, from_=0, to=HEIGHT,length=400, orient=tk.HORIZONTAL, command=update_line)
slider.pack()

window.mainloop()
