import json


def load_pics(filename="hangman.json"):

    with open(filename) as file:
        obrazky = json.load(file)
        print(len(obrazky))
        return obrazky




def show_welcome_message():
    print("Vítej ve hře šibenice!")
    print("Zadávej písmena a pokus se uhodnout tajné slovo. Ale pozor, ať neskončíš na šibenici!")




def show_game_state(stav_hry, obrazky, pocet_neuspesnych_pokusu, zadane_pismena):

    print(obrazky[pocet_neuspesnych_pokusu])
    print(f"Slovo: {stav_hry}")
    vypis_pismen = ", ".join(zadane_pismena)
    print(f"Použitá písmena: {vypis_pismen}")




def show_feedback(ano_ne):

    if ano_ne == True:
        print("Správně! 👍")
    else:
        print("Špatně! ❌")




def show_game_over(win, tajne_slovo):

    if win == True:
        print(f"Gratuluji! Uhodl jsi slovo: {tajne_slovo}")
    else:
        print(f"Konec hry! Tajné slovo bylo: {tajne_slovo}")

if __name__ == "__main__":
    obrazky = load_pics()
    show_game_state("_____", obrazky, 7, ["i","i","i","i""i","i"])