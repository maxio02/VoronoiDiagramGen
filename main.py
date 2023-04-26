import tkinter as tk
from dataclasses import dataclass
import random
import heapq
from bst import Node
from math import sqrt
import itertools
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

    def f(self, x):
        x1 = self.apex.x
        y1 = self.apex.y
        
        return (1/((2*(y1-line_y)))    *    ((x-x1)**2 + y1**2 - line_y**2))
        #return ((x1**2  -  2*x1*x   +    4*y1*p+x**2)/4/p)

    def intersect(self, other):
            x1 = self.apex.x
            y1 = self.apex.y
            x2 = other.apex.x
            y2 = other.apex.y
            
            a1 = 1/(2*(y1-line_y))
            b1 = -x1/(y1-line_y)
            c1 = (x1**2 + y1**2 - line_y**2)/(2*(y1-line_y))
            
            a2 = 1/(2*(y2-line_y))
            b2 = -x2/(y2-line_y)
            c2 = (x2**2 + y2**2 - line_y**2)/(2*(y2-line_y))
            
            a = a1 - a2
            b = b1 - b2
            c = c1 - c2
            
            discriminant = b**2 - 4*a*c
            
            if discriminant < 0:
                return []  
            else:
                x_intersects = [(-b + sqrt(discriminant)) / (2*a), (-b - sqrt(discriminant)) / (2*a)]
                intersection_points = []
                for x in x_intersects:
                    y = self.f(x)
                    if abs(y - other.f(x)) < 1e-6: 
                        intersection_points.append(point(x, y,5))
                return intersection_points
                                                                

def generate_points(n: int) -> list[point]:
    global points
    points = []
    for i in range(n):
        points.append(point(random.randint(15, WIDTH-15),
                      random.randint(15, HEIGHT-15), 5))
    return points


def draw_points(points: list[point], color):
    for point in points:
        canvas.create_oval(point.x - point.radius, point.y-point.radius,
                           point.x+point.radius, point.y+point.radius, fill=color)


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
        if line_y > pt.y:
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

def calc_intersection_points(parabolas:list[arc]):
    intersection_points = []
    pairs = list(itertools.combinations(parabolas, 2))

    for pair in pairs:
        intersection_points.extend(pair[0].intersect(pair[1]))
    return intersection_points

def draw(points):
    canvas.delete('all')
    draw_points(points, 'red')
    parabolas = calc_parabolas(points, line_y)
    draw_parabolas(parabolas)
    intersection_points = calc_intersection_points(parabolas)
    draw_points(intersection_points, 'black')
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


    
    draw(points)
    
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
