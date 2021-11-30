import matplotlib.pyplot as plt
import math
import random
import time


class Coord:
    """
    Trieda Coord vytvara objekty, ktore maju x hodnotu, y hodnotu a farbu
    objekt reprezentuje jeden bod
    """
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color


def draw(init, i):
    """
    Funkcia draw vvykresli graf pomocou kniznice matplotlib
    Graf pripadne ulozi
    :param init: pole bodov v grafe (red, green, blue, purple)
    :param i: poradie (na nazvoslovie suboru)
    """
    red, green, blue, purple = init

    plt.scatter([x.x for x in red], [y.y for y in red], c='#ff0000')
    plt.scatter([x.x for x in green], [y.y for y in green], c='#00ff00')
    plt.scatter([x.x for x in blue], [y.y for y in blue], c='#0000ff')
    plt.scatter([x.x for x in purple], [y.y for y in purple], c='#800080')
    plt.show()
    # plt.savefig(f'img/plot{i}.png')


def euclid_distance(x1, y1, x2, y2):
    """
    Funkcia vyrata euklidovsku vzdialenost dvoch bodov v suradnicovej sustave
    :param x1: x prveho bodu
    :param y1: y prveho bodu
    :param x2: x druheho bodu
    :param y2: y druheho bodu
    :return: vzdialenost
    """
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


def is_near(x1, y1, x2, y2, koef):
    """
    Funkcia vrati True, ak su dva zadanie body dostatocne blizko
    Nerata euklidovsku vzdialenost, ale akysi stvorec okolo jedneho bodu
    Dostatocne blizko znamena vzdialene menej ako koef na x alebo y osi
    :param x1: bod 1
    :param y1: bod 1
    :param x2: bod 2
    :param y2: bod 2
    :param koef: vzdialenost
    :return: boolean
    """
    if ((x1 - koef) < x2 < (x1 + koef)) and ((y1 - koef) < y2 < (y1 + koef)):
        return True
    return False


def classify(init, x, y, k):
    """
    Funkcia classify sluzi na samotne zaradenie bodu pomocou algoritmu KNN
    Funkcia najskor spoji vsetky body do jedneho pola, vygeneruje nejaku vzdialenost,
    v akej ma hladat najblizsie body (pomocou funkcie is_near).
    Tato vzdialenost je vacsia pre malo bodov a mensia pre vela bodov v grafe,
    snazi sa odhadnut idealnu v zdialenost v ktorej najde k (+3) bodov
    Nasledne tieto body zoradi podla euklidovej vzdialenosti a zoberie prvych k.
    Najde najviac frekventovanu farbu z tychto k bodov, a priradi ju aj novemu bodu.
    Tento bod potom zaradi do prislusnej skupiny.
    :param init: Pole bodov (red, green, blue, purple)
    :param x: x suradnica noveho bodu
    :param y: y suradnica anoveho bodu
    :param k: koeficient k
    """
    red, green, blue, purple = init
    # result = init[0] + init[1] + init[2] + init[3]
    all_elements = init[0] + init[1] + init[2] + init[3]
    result: list[Coord] = []
    i = (10000//(len(all_elements)*2))*k+100
    # i = 10
    while len(result) < k+3:
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
    return most_frequent


r, g, b, p, o = 0, 0, 0, 0, 0


def generate_random(colors, last_color):
    """
    Funkcia nahodne generuje, v ktorej stvrtine sa vygeneruje bod.
    Nikdy sa bod nevygeneruje v rovnakej stvrtine 2 krat za sebou (okrem 0.01% nahody).
    Nasledne sa s 99% pravdepodobnostou bod vygeneruje v danej stvrtine, inak sa vygeneruje
    nahodne
    :param colors: pole farieb ('r', 'g', 'b', 'p')
    :param last_color: posledne vygenerovana farba
    :return: bod (x, y) a farba
    """
    global r, g, b, p, o
    while True:
        color = random.choice(colors)
        if color != last_color:
            break
    if random.uniform(0, 1) < .99:
        if color == 'r':
            x = random.randint(-5000, 0)
            y = random.randint(-5000, 0)
            r += 1
        elif color == 'g':
            x = random.randint(0, 5000)
            y = random.randint(-5000, 0)
            g += 1
        elif color == 'b':
            x = random.randint(-5000, 0)
            y = random.randint(0, 5000)
            b += 1
        else:
            x = random.randint(0, 5000)
            y = random.randint(0, 5000)
            p += 1
    else:
        x = random.randint(-5000, 5000)
        y = random.randint(-5000, 5000)
        o += 1
    return x, y, color


def run(red, green, blue, purple, k, n):
    """
    Funkcia run vygeneruje a klasifikune n krat bod
    Funkcia taktiez stopuje cas za ktory sa vykona
    :param red: pole cervenych bodov
    :param green: pole zelenych bodov
    :param blue: pole modrych bodov
    :param purple: pole fialovych bodov
    :param k: koeficient k (v algoritme knn)
    :param n: pocet bodov ktore sa maju vygenerovat
    """
    colors = ['r', 'g', 'b', 'p']
    last_color = ''
    success = 0
    start = time.time()
    for i in range(n):
        if i % 1000 == 0:
            print(i)
            # draw((red, green, blue, purple), i)
        x, y, last_color = generate_random(colors, last_color)
        is_color = classify((red, green, blue, purple), x, y, k)
        if last_color == is_color:
            success += 1
    draw((red, green, blue, purple), 'last')
    end = time.time()
    print(f'Time: {end - start}')
    print(f'Success: {success} / {n}')
    print(f'r {r}, g {g}, b {b}, p {p}, o {o}')


def main():
    """
    Funkcia main inicializuje pociatocne body a zavola funkciu run
    """
    red = [(-4500, -4400), (-4100, -3000), (-1800, -2400), (-2500, -3400), (-2000, -1400)]
    green = [(+4500, -4400), (+4100, -3000), (+1800, -2400), (+2500, -3400), (+2000, -1400)]
    blue = [(-4500, +4400), (-4100, +3000), (-1800, +2400), (-2500, +3400), (-2000, +1400)]
    purple = [(+4500, +4400), (+4100, +3000), (+1800, +2400), (+2500, +3400), (+2000, +1400)]
    red = [Coord(item[0], item[1], 'r') for item in red]
    green = [Coord(item[0], item[1], 'g') for item in green]
    blue = [Coord(item[0], item[1], 'b') for item in blue]
    purple = [Coord(item[0], item[1], 'p') for item in purple]

    # draw((red, green, blue, purple), 0)

    # run(red, green, blue, purple, k=1, n=20000)
    # run(red, green, blue, purple, k=3, n=20000)
    # run(red, green, blue, purple, k=7, n=20000)
    run(red, green, blue, purple, k=15, n=20000)
    return 0


if __name__ == '__main__':
    main()
