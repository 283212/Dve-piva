import math
PI = math.pi
SHAPE_KRUH = 'kruh'
SHAPE_OBDELNIK = 'obdelnik'
SHAPE_PRAVOUHLY_TROJUHELNIK = 'pravouhly trojuhelnik'

def get_shapes_and_areas(parametry):

    tvary = []
    obsahy = []

    for rozmery in parametry: #(4)
        if len(rozmery) == 1:
            tvary.append("kruh")
            obsah = rozmery[0] ** 2 * PI
            obsahy.append(obsah)
        if len(rozmery) == 2:  #(4, 6)
            tvary.append("obdelnik")
            obsah = rozmery[0] * rozmery[1]
            obsahy.append(obsah)
        if len(rozmery) == 3:
            tvary.append("pravouhly trojuhelnik")
            obsah = rozmery[0] * rozmery[1] /2
            obsahy.append(obsah)
    print(tvary, obsahy)
    return tvary, obsahy


#get_shapes_and_areas([(6,), (3, 5), (5, 3), (3,), (3, 1), (3, 4, 5), (5, 12, 13)])


def check_if_can_get_through_hole(parametry, tvary, prumer):

    prumer = float(prumer)
    ano_ne = []

    for parametry, tvary in zip(parametry, tvary):
        if tvary == "kruh":
            if parametry[0] <= prumer/2:
                ano_ne.append(True)
                continue
        if tvary == "obdelnik":
            if (parametry[0] ** 2 + parametry[1] ** 2) ** 0.5 <= prumer:
                ano_ne.append(True)
                continue
        if tvary == "pravouhly trojuhelnik":
            if parametry[2] <= prumer:
                ano_ne.append(True)
                continue

        ano_ne.append(False)

    return ano_ne



def count_area_weighted_letters(tvary, obsahy, ano_ne, pismeno):

    nasobky = []

    for tvar in tvary:
        pocet = tvar.count(pismeno)
        nasobky.append(pocet)

    suma_tvaru = 0.0

    for obsahy, ano_ne, nasobek in zip(obsahy, ano_ne, nasobky):
        if ano_ne == True:
            suma_tvaru += obsahy * nasobek

    return suma_tvaru


def main(parametry, prumer, pismeno, pravda_lez_vraceni=False):

    tvary, obsahy = get_shapes_and_areas(parametry)
    ano_ne = check_if_can_get_through_hole(parametry, tvary, prumer)
    suma_tvaru = count_area_weighted_letters(tvary, obsahy, ano_ne, pismeno)

    if pravda_lez_vraceni == True:
        return suma_tvaru, tvary
    else:
        return suma_tvaru










#if __name__ == '__main__':
   # shapes_parameters = [(6,), (3, 5), (5, 3), (3,), (3, 1), (3, 4, 5), (5, 12, 13)]
   # hole_diameter = 5
   # letter = 'j'

  #  main(shapes_parameters, hole_diameter, letter)
    # main(shapes_parameters, hole_diameter, letter, True)

