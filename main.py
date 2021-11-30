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

    plt.scatter([x[0] for x in red], [y[1] for y in red], c='#ff0000')
    plt.scatter([x[0] for x in green], [y[1] for y in green], c='#00ff00')
    plt.scatter([x[0] for x in blue], [y[1] for y in blue], c='#0000ff')
    plt.scatter([x[0] for x in purple], [y[1] for y in purple], c='#800080')
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
    result = []
    i = 10
    while len(result) < k:
        result = [(a[0], a[1]) for a in all_elements if is_near(x, y, a[0], a[1], i)]
        i += 150
    result = sorted(result, key=lambda a: euclid_distance(a[0], a[1], x, y))
    # my_red = [item for item in red if is_near(x, y, item[0], item[1], i)]
    # my_green = [item for item in green if is_near(x, y, item[0], item[1], i)]
    # my_blue = [item for item in blue if is_near(x, y, item[0], item[1], i)]
    # my_purple = [item for item in purple if is_near(x, y, item[0], item[1], i)]
    first_k = []
    for i in range(k):
        if result[i] in red:
            first_k.append('r')
        elif result[i] in green:
            first_k.append('g')
        elif result[i] in blue:
            first_k.append('b')
        elif result[i] in purple:
            first_k.append('p')
    most_frequent = max(set(first_k), key=first_k.count)
    if most_frequent == 'r':
        red.append((x, y))
    elif most_frequent == 'g':
        green.append((x, y))
    elif most_frequent == 'b':
        blue.append((x, y))
    elif most_frequent == 'p':
        purple.append((x, y))


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
    colors = ['r', 'g', 'b', 'p']
    last_color = ''
    start = time.time()
    for i in range(10000):
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
