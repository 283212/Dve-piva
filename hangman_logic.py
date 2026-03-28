import random

def choose_word(seznam_slov):

    tajne_slovo = random.choice(seznam_slov)
    return tajne_slovo




def get_user_char(hadane_pismena):

    while True:
        pismeno = input(f"Hádejte jedno písmeno: ").lower()
        if len(pismeno) != 1:
            print("CHYBA: pokus není jedno písmeno")
            continue

        if not pismeno.isalpha():
            print("CHYBA: pokus není písmeno")
            continue

        if pismeno in hadane_pismena:
            print("CHYBA: písmeno již bylo hádáno")
            continue

        hadane_pismena.append(pismeno)
        return pismeno, hadane_pismena




def replace_chars(stav_hry, tajne_slov , zadane_pismeno):

    indexy = []
    retez = ""
    for i, x in enumerate(tajne_slov):
        if tajne_slov[i] == zadane_pismeno:
            indexy.append(i)

    for u in range(len(tajne_slov)):
        if u not in indexy:
            retez += stav_hry[u]
            continue
        retez += tajne_slov[u]

    stav_hry = retez
    return stav_hry







if __name__ == "__main__":
    replace_chars("", "kokopadlo", "p")