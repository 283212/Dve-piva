from stage_simulator import set_position
import json
import csv




def read_stage_config(file):

    with open(file) as f:
        konfigurace = json.load(f)

    return konfigurace




def get_home_position(konfigurace):

    domaci = {}

    domaci["x"] = int((konfigurace["x"]["min"] + konfigurace["x"]["max"]) / 2)
    domaci["y"] = int((konfigurace["y"]["min"] + konfigurace["y"]["max"]) / 2)
    domaci["z"] = int((konfigurace["z"]["min"] + konfigurace["z"]["max"]) / 2)

    return domaci




def set_position_safe(pozadovana, konfigurace):

    if pozadovana["x"] > konfigurace["x"]["max"]:
        pozadovana["x"] = konfigurace["x"]["max"]
    if pozadovana["x"] < konfigurace["x"]["min"]:
        pozadovana["x"] = konfigurace["x"]["min"]

    if pozadovana["y"] > konfigurace["y"]["max"]:
        pozadovana["y"] = konfigurace["y"]["max"]
    if pozadovana["y"] < konfigurace["y"]["min"]:
        pozadovana["y"] = konfigurace["y"]["min"]

    if pozadovana["z"] > konfigurace["z"]["max"]:
        pozadovana["z"] = konfigurace["z"]["max"]
    if pozadovana["z"] < konfigurace["z"]["min"]:
        pozadovana["z"] = konfigurace["z"]["min"]

    set_position(pozadovana["x"], pozadovana["y"], pozadovana["z"])

    return pozadovana   # nepotrebny return ... potrebny jen pro Pytest




def execute_file(file_commands, konfigurace):

    seznam_pozic = []

    with (open(file_commands, "r") as f):
        lines = f.readlines()

        for line in lines[1:]:
            line = line.strip()
            line = line.split(",")

            slovnik = {}
            slovnik["x"] = int(line[0])
            slovnik["y"] = int(line[1])
            slovnik["z"] = int(line[2])

            pozadovana = set_position_safe(slovnik, konfigurace)

            seznam_pozic.append(pozadovana)

    return seznam_pozic    # nepotrebny return (=seznam pozadovanych pozic) ... jen pro Pytest




def plan_grid_scan(konfigurace, krok_x, krok_y, prazdny_soubor):

    #x_min = konfigurace["x"]["min"]
    x_max = konfigurace["x"]["max"]
    y_min = konfigurace["y"]["min"]
    y_max = konfigurace["y"]["max"]
    z = int((konfigurace["z"]["min"] + konfigurace["z"]["max"]) / 2)

    pocet_pozic = 0
    pozice = ["x,y,z"]

    while y_min <= y_max:
        x_min = konfigurace["x"]["min"]
        while x_min <= x_max:

            x, y, z = int(x_min), int(y_min), z
            pozice.append((x, y, z))

            x_min += krok_x
            pocet_pozic += 1

        y_min += krok_y


    with open(prazdny_soubor, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(pozice)

    return pocet_pozic




def main(konfig_soubor, prazdny_soubor_plan):

    konfigurace = read_stage_config(konfig_soubor)
    domaci_pozice = get_home_position(konfigurace)


    set_position_safe(domaci_pozice, konfigurace)

    #Do souboru (např. "prazdny_soubor_plan") napíše prikazy (=vsechny pozice) + vrati pocet_pozic
    pocet_pozic = plan_grid_scan(konfigurace, 1000, 1000 ,prazdny_soubor_plan)

    #Čte soubor s prikazy (pozicemi) a vykonava je tak, že volá set_position() pres set_position_safe()
    execute_file(prazdny_soubor_plan, konfigurace)


    print(f"Počet naplánovaných pozic pro grid scan: {pocet_pozic}")
