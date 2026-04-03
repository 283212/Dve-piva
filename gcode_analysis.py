import math

# Rychlost rychlého přesunu (G0) v mm/min:
TRAVEL_SPEED_MM_PER_MIN = 6000.0

# Rychlost pracovního pohybu (G1) v mm/min:
PRINT_SPEED_MM_PER_MIN = 1500.0


# Ukázka G-code řádků:
# "G1 X50.0 Y0.0 Z0.0"
# "G0 X100.0 Y100.0 Z50.0"
#
# Rozparsované řádky (slovníky):
# {'cmd': 'G1', 'X': 50.0, 'Y': 0.0, 'Z': 0.0}
# {'cmd': 'G0', 'X': 100.0, 'Y': 100.0, 'Z': 50.0}

def parse_line(radek):

    radek = radek.strip()
    if radek == "" or radek[0] == ";":
     return None


    hodnoty = radek.split(" ")
    xyz = []
    slovnik = {}
    slovnik["cmd"] = hodnoty[0]

    for prvek in hodnoty[1:]:
        cislo = prvek[1:]
        cislo = float(cislo)
        xyz.append(cislo)

    slovnik["X"] = xyz[0]
    slovnik["Y"] = xyz[1]
    slovnik["Z"] = xyz[2]

    return slovnik




def read_gcode(file):

    prikazy = []

    with open(file, "r", encoding="utf-8") as file:
        for line in file:
            prikaz = parse_line(line)

            if prikaz != None:
                prikazy.append(prikaz)

        return prikazy




def get_move_time(prvni_bod_slovnik, druhy_bod_slovnik, rychlost):

    prevedena = rychlost/60

    vzdalenost = (((druhy_bod_slovnik["X"] - prvni_bod_slovnik["X"]) ** 2) + ((druhy_bod_slovnik["Y"] - prvni_bod_slovnik["Y"]) ** 2) + ((druhy_bod_slovnik["Z"] - prvni_bod_slovnik["Z"]) ** 2)) ** 0.5
    cas = float(vzdalenost / prevedena)

    return cas




def analyze_time(prikazy):

    # Rychlost rychlého přesunu (G0) v mm/min:
    # TRAVEL_SPEED_MM_PER_MIN = 6000.0

    # Rychlost pracovního pohybu (G1) v mm/min:
    # PRINT_SPEED_MM_PER_MIN = 1500.0

    cas_prace = 0.0
    cas_presunu = 0.0
    slovnik = {}

    pocatecnipozice = {"X": 0.0, "Y": 0.0, "Z": 0.0}
    for prikaz in prikazy:
        if prikaz["cmd"] == "G1":
            cas = get_move_time(pocatecnipozice, prikaz, PRINT_SPEED_MM_PER_MIN)
            cas_prace += cas
        if prikaz["cmd"] == "G0":
            cas = get_move_time(pocatecnipozice, prikaz, TRAVEL_SPEED_MM_PER_MIN)
            cas_presunu += cas
        pocatecnipozice = prikaz

    slovnik["work_time_s"] = cas_prace
    slovnik["travel_time_s"] = cas_presunu
    slovnik["total_time_s"] = cas_prace + cas_presunu
    return slovnik




def get_bounding_box(prikazy):

    x = 0
    y = 0
    z = 0
    slovnik = {}

    for prikaz in prikazy:
        if prikaz["X"] > x:
            x = prikaz["X"]
        if prikaz["Y"] > y:
            y = prikaz["Y"]
        if prikaz["Z"] > z:
            z = prikaz["Z"]

    slovnik["x_min"] = 0
    slovnik["x_max"] = x
    slovnik["y_min"] = 0
    slovnik["y_max"] = y
    slovnik["z_min"] = 0
    slovnik["z_max"] = z

    return slovnik




def main(filename):

    prikazy = read_gcode(filename)
    slovnik_cas = analyze_time(prikazy)
    box = get_bounding_box(prikazy)

    print(f"G-code soubor: {filename}")
    print(f"Pracovní čas: {slovnik_cas['work_time_s']:.3f} s")
    print(f"Čas přesunů: {slovnik_cas['travel_time_s']:.3f} s")
    print(f"Celkový čas: {slovnik_cas['total_time_s']:.3f} s")
    print(f"""Bounding box:
  X: {box['x_min']:.3f} .. {box['x_max']:.3f}
  Y: {box['y_min']:.3f} .. {box['y_max']:.3f}
  Z: {box['z_min']:.3f} .. {box['z_max']:.3f}""")






if __name__ == "__main__":
    parse_line("; Layer 1")
    parse_line("G0 X0.0 Y0.0 Z0.0")
    parse_line("G1 X0.0 Y40.0 Z5.0")