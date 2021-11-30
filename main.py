import matplotlib.pyplot as plt
import math
import random
import time


class Coord:
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color


def draw(init, i):
    red, green, blue, purple = init

    plt.scatter([x.x for x in red], [y.y for y in red], c='#ff0000')
    plt.scatter([x.x for x in green], [y.y for y in green], c='#00ff00')
    plt.scatter([x.x for x in blue], [y.y for y in blue], c='#0000ff')
    plt.scatter([x.x for x in purple], [y.y for y in purple], c='#800080')
    plt.show()
    # plt.savefig(f'img/plot{i}.png')


def euclid_distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


def is_near(x1, y1, x2, y2, koef):
    if ((x1 - koef) < x2 < (x1 + koef)) and ((y1 - koef) < y2 < (y1 + koef)):
        return True
    return False


def knn(init, x, y, k):
    red, green, blue, purple = init
    # result = init[0] + init[1] + init[2] + init[3]
    all_elements = init[0] + init[1] + init[2] + init[3]
    result: list[Coord] = []
    i = (10000//(len(all_elements)*2))*k+100
    # i = 10
    while len(result) < k:
        result = [a for a in all_elements if is_near(x, y, a.x, a.y, i)]
        # i *= 2
        i += 150
    result = sorted(result, key=lambda a: euclid_distance(a.x, a.y, x, y))
    first_k = []
    for i in range(k):
        first_k.append(result[i].color)
    most_frequent = max(set(first_k), key=first_k.count)
    if most_frequent == 'r':
        red.append(Coord(x, y, 'r'))
    elif most_frequent == 'g':
        green.append(Coord(x, y, 'g'))
    elif most_frequent == 'b':
        blue.append(Coord(x, y, 'b'))
    elif most_frequent == 'p':
        purple.append(Coord(x, y, 'p'))


def generate_random(colors, last_color):
    while True:
        color = random.choice(colors)
        if color != last_color:
            break
    if random.uniform(0, 1) < .99:
        if color == 'r':
            x = random.randint(-5000, 0)
            y = random.randint(-5000, 0)
        elif color == 'g':
            x = random.randint(0, 5000)
            y = random.randint(-5000, 0)
        elif color == 'b':
            x = random.randint(-5000, 0)
            y = random.randint(0, 5000)
        else:
            x = random.randint(0, 5000)
            y = random.randint(0, 5000)
    else:
        x = random.randint(-5000, 5000)
        y = random.randint(-5000, 5000)
    return x, y, color


def main():
    red = [(-4500, -4400), (-4100, -3000), (-1800, -2400), (-2500, -3400), (-2000, -1400)]
    green = [(+4500, -4400), (+4100, -3000), (+1800, -2400), (+2500, -3400), (+2000, -1400)]
    blue = [(-4500, +4400), (-4100, +3000), (-1800, +2400), (-2500, +3400), (-2000, +1400)]
    purple = [(+4500, +4400), (+4100, +3000), (+1800, +2400), (+2500, +3400), (+2000, +1400)]
    red = [Coord(item[0], item[1], 'r') for item in red]
    green = [Coord(item[0], item[1], 'g') for item in green]
    blue = [Coord(item[0], item[1], 'b') for item in blue]
    purple = [Coord(item[0], item[1], 'p') for item in purple]

    colors = ['r', 'g', 'b', 'p']
    last_color = ''
    start = time.time()
    for i in range(20000):
        if i % 100 == 0:
            print(i)
            # draw((red, green, blue, purple), i)
        x, y, last_color = generate_random(colors, last_color)
        knn((red, green, blue, purple), x, y, 3)
    draw((red, green, blue, purple), 'last')
    end = time.time()
    print(f'Time: {end-start}')


if __name__ == '__main__':
    main()
