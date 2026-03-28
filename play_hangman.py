from hangman_logic import choose_word, get_user_char, replace_chars
from hangman_display import load_pics, show_welcome_message, show_game_state, show_feedback ,show_game_over




def main():

    show_welcome_message()
    obrazky = load_pics()

    seznam_tajnych_slov = ["python", "programovani", "hangman", "parametr", "funkce"]
    vybrane_slovo = choose_word(seznam_tajnych_slov)

    stav_hry = "_" * len(vybrane_slovo)
    pocet_neuspesnych_pokusu = 0
    zadana_pismena = []
    vitezstvi = False

    while pocet_neuspesnych_pokusu != len(obrazky):

        show_game_state(stav_hry, obrazky, pocet_neuspesnych_pokusu, zadana_pismena)
        pismeno, zadana_pismena = get_user_char(zadana_pismena)

        if pismeno in vybrane_slovo:
            show_feedback(True)
            stav_hry = replace_chars(stav_hry, vybrane_slovo, pismeno)
            if stav_hry == vybrane_slovo:
                vitezstvi = True
                break

        else:
            show_feedback(False)
            pocet_neuspesnych_pokusu += 1

    show_game_over(vitezstvi, vybrane_slovo)