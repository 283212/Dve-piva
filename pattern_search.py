import json


def load_fasta(filepath):
    """
        Každá funkce musí obsahovat dokumentační řetězec (docstring) --> !!TROJE UVOZOVKY!!
        V docstringu se popisuje účel funkce, vstupní parametry a výstup.

        Načtení dat ... Funkce přijme cestu k souboru a soubor načte. Výstupem je slovník, kde klíčem je název biologické sekvence/vzorku a hodnotou řetěz písmen (nukleové báze).
    """
    with open(filepath, 'r') as f:

        lines = f.readlines()
        slovnik = {}


        for line in lines:

            if line[0] == ">":
                klic = line[1:].strip()
                slovnik[klic] = ""
            else:
                retez = line.strip()
                slovnik[klic] = slovnik[klic] + retez

    return slovnik




def preprocessing(sekvence, vzor):
    """
        Předzpracování - výběr kandidátních oken
        Vstupuje sekvence a vzor, který v sekvenci hledáme. V této funkci hledáme pouze potenciální shody, dá se říci okna.
        Okno je úsek v sekvenci, který má stejnou délku, písmeno na začátku a písmeno na konci, jako vzor.
        Výstupem je seznam indexů počátků těchto oken.
    """
    indexy_kandidatnich_pocatku = []

    for index, pismeno in enumerate(sekvence):

        if pismeno == vzor[0] and sekvence[index + len(vzor) -1] == vzor[-1]:
            indexy_kandidatnich_pocatku.append(index)

        if index == len(sekvence) - len(vzor):
            break

    return indexy_kandidatnich_pocatku




def match_pattern(indexy_kandidatu, sekvence, vzor):
    """
        Vstupuje sekvence, vzor a seznam indexů počátků oken v sekvenci.
        Zde hledáme úplné shody mezi okny a vzorem.
        Výstupem je nový seznam obsahující indexy počátků úseků sekvence plně shodných se vzorem.
    """
    indexy_shod = []


    for index in indexy_kandidatu:
        zacatek = index + 1                      # +1 ... prvni písmeno je již ověřené, zaciname od druheho
        shoda = True

        for i in range(len(vzor) - 2):           # -2 ... Nemusime ověřovat zacatek a konec

            if sekvence[zacatek + i] == vzor[i+1]:
                continue
            else:
                shoda = False
                break

        if shoda == True:
            indexy_shod.append(index)

    return indexy_shod




def find_patterns(slovnik_sekvenci, slovnik_vzory):
    """
        Přijme slovník se sekvencemi (jméno sekvence: sekvence) a slovník se vzory (jméno vzoru: vzor).
        Vytvoří seznam slovníků, tedy seznam s prvky, kde každý prvek představuje informace o dvojici "sekvence, vzor".
        Dvojice pro sekvenci s názvem "sequence_1" je "pattern_1" atd.
        Vytvořený seznam je výstupem funkce (VÝSLEDEK pro JSON).
    """
    seznam_slovniku = []


    for i in range(len(slovnik_sekvenci)):
        prvek_info = {}

        klic_sekvence = "sequence_" + str(i)
        klic_vzoru = "pattern_" + str(i)
        prvek_info["sequence_name"] = klic_sekvence
        prvek_info["sequence"] = slovnik_sekvenci[klic_sekvence]
        prvek_info["pattern_name"] = klic_vzoru
        prvek_info["pattern"] = slovnik_vzory[klic_vzoru]

        indexy_pocatku = preprocessing(slovnik_sekvenci[klic_sekvence], slovnik_vzory[klic_vzoru])

        prvek_info["matches"] = match_pattern(indexy_pocatku, slovnik_sekvenci[klic_sekvence], slovnik_vzory[klic_vzoru])

        seznam_slovniku.append(prvek_info)

    return seznam_slovniku





def write_json(filename, vysledky):
    """
        Přijme výsledek a název budoucího souboru.
        Vytvoří JSON soubor s výsledkem.
    """
    with open(filename, 'w') as f:
        f.write(json.dumps(vysledky))



def main(filepath_sekvence, filepath_vzory, filepath_vystup):
    """
        Přijme soubor se sekvencemi a soubor se vzory a vytvoří JSON soubor s konečným výsledkem.
    """
    slov_sekvence = load_fasta(filepath_sekvence)    # {sequence_0:AGCCCAA, sequence_1:CAA..}
    slov_vzory = load_fasta(filepath_vzory)        # {pattern_0:AGCCCAA, pattern_1:CAA..}

    seznam_slovniku = find_patterns(slov_sekvence, slov_vzory)

    write_json(filepath_vystup, seznam_slovniku)
