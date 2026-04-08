from haversine_utils import haversine


# Ukázka dat z CSV souboru:
# data_example = [(0, 50.07380, 14.43780), (5, 50.07385, 14.43790), ...]
#
# Každá trojice je: (čas_v_sekundách, zeměpisná_šířka, zeměpisná_délka)
#
# Příklad výpočtu vzdálenosti:
# vzdalenost_m = haversine(50.07380, 14.43780, 50.07385, 14.43790)

def read_run_data(file):
    trojice = []
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            line = line.split(",")
            a = (line[0])
            b = (line[1])
            c = (line[2])
            trojica = (float(a), float(b), float(c))
            trojice.append((trojica))
    return trojice




def get_total_distance(trojice):

    celkova = 0
    for i in range(len(trojice)-1):
        vzdalenost = haversine(float(trojice[i][1]), float(trojice[i][2]), float(trojice[i + 1][1]), float(trojice[i + 1][2]))
        celkova += vzdalenost

    # pociatok = trojice[0]
    # koniec =  trojice[-1]
    # lat1, lon1 = float(pociatok[1]), float(pociatok[2])
    # lat2, lon2 = float(koniec[1]), float(koniec[2])
    return celkova




def get_total_time(trojice):
    koniec = trojice[-1]
    cas1 = koniec[0]
    return float(cas1)




def get_average_speed(celkova_vzdalenost_m, cas_s):
    cas_m = cas_s / 3600
    celkova_vzdalenost_km = celkova_vzdalenost_m / 1000
    priemerna_rychlost = celkova_vzdalenost_km / cas_m

    return float(priemerna_rychlost)




def get_max_speed(trojice):
    max_speed = 0
    for i in range(len(trojice)-1):
        vzdalenost = haversine(float(trojice[i][1]), float(trojice[i][2]), float(trojice[i+1][1]), float(trojice[i+1][2]))
        cas = float(trojice[i+1][0]) - float(trojice[i][0])
        if max_speed < (vzdalenost / cas):
            max_speed = (vzdalenost/cas)

    return max_speed * 3.6



def main(filepath):
    trojice = read_run_data(filepath)
    vzdialenost = get_total_distance(trojice) /1000
    celkovy_cas = get_total_time(trojice)
    priemerna_rychlost = get_average_speed(vzdialenost, celkovy_cas) * 1000
    max_speed = get_max_speed(trojice)
    print(f"GPS soubor: {filepath}")
    print(f"Celková vzdálenost: {vzdialenost:.03f} km")
    minuty = int(celkovy_cas/60)
    s = int(celkovy_cas % 60)
    print(f"Celkový čas: {minuty}:{s}")
    print(f"Průměrná rychlost: {priemerna_rychlost:.03f} km/h")
    print(f"Maximální rychlost: {max_speed:.03f} km/h")
