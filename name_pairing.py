REMOVE_CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " ", ".", ",", "-", "_"]
REPLACE_CHARS = {"ě": "e", "š": "s", "č": "c", "ř": "r", "ž": "z", "ý": "y",
                 "á": "a", "í": "i", "é": "e", "ú": "u", "ů": "u", "ď": "d",
                 "ť": "t", "ň": "n", "ó": "o"}


def standardize_names(seznam_jmen):

    novy_seznam = []
    for jmeno in seznam_jmen:

        jmeno = jmeno.lower()
        upravene_jmeno = ""
        for char in jmeno:
            if char in REPLACE_CHARS:
                pismeno = REPLACE_CHARS[char]
                upravene_jmeno += pismeno

            elif char in REMOVE_CHARS:
                    continue

            else:
                upravene_jmeno += char

        novy_seznam.append(upravene_jmeno)

    return novy_seznam




def get_similarity(prvni_jmeno, druhe_jmeno):

    similarita1 = 0
    similarita2 = 0
    for char in prvni_jmeno:
        if char in druhe_jmeno:
            similarita1 += 1

    for char in druhe_jmeno:
        if char in prvni_jmeno:
            similarita2 += 1

    return (similarita1 + similarita2) / (len(prvni_jmeno) + len(druhe_jmeno))




def pair_names(reference_seznam, names_to_assign):

    seznam_dvojic = []

    for jmeno1 in reference_seznam:
        predchozi_podobnost = 0
        for jmeno2 in names_to_assign:
            podobnost = get_similarity(jmeno1, jmeno2)
            if podobnost > predchozi_podobnost:
                predchozi_podobnost = podobnost
                dvojice = (jmeno1, jmeno2)

        seznam_dvojic.append(dvojice)

    return seznam_dvojic




def main(filename_to_assign, filename_reference):

    #to_assign = []
    reference = []

    with open(filename_to_assign, "r", encoding="utf-8") as file1:
        for radek in file1:
            cisty = radek.strip()
            to_assign = cisty.split(";")
          #  to_assign.append(cisty)

        #to_assign = file1.readlines()

    with open(filename_reference, "r", encoding= "utf-8") as file2:
        for radek in file2:
            cisty = radek.strip()
            reference.append(cisty)

        #reference = file2.readlines()

    to_assign = standardize_names(to_assign)
    reference = standardize_names(reference)

    return pair_names(to_assign, reference)









if __name__ == "__main__":
    # Ukázkové seznamy jmen
    names_reference = ["Kateřina Šabatová", "Tomas Vi4ar", "Jiří Chmelík", "Smíšek Radoan"]
    names_to_assign = ["Katerina Sabatoova", "Radovan, Smíšek", "Jiri Chmelik", "Tomas Vičar", "Radovan Simsek"]