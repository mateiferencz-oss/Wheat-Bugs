import pygame
import joc.sprite_sheet as sprite_sheet
folder = "Spriteuri"

def incarca(nume, cadre, marime):
    imagine = pygame.image.load(f"{folder}/{nume}")
    coala = sprite_sheet.SpriteSheet(imagine, cadre)
    return [coala.imagine(i, marime) for i in range(cadre)]


def incarca_tot():
    coale = [
        ("Player.png", 9, 7),
        ("Coala_Ferma_noua.png", 13, 7),
        ("Coala_Meniu.png", 9, 9),
    ]

    spriteuri = [
        ("Iarba.png", 3), ("Drum.png", 3),
        ("Margine_Stanga_Drum.png", 3), ("Margine_Dreapta_Drum.png", 3),
        ("Buton.png", 4), ("Ban.png", 6), ("Spate_Ban.png", 11),
        ("Masa.png", 3), ("Secera.png", 3), ("Seminte.png", 3),
        ("Insecticid.png", 3), ("Stropitoare.png", 4), ("Gandaci.png", 4),
        ("Spate_Roi.png", 5), ("Margine_Dreapta_Roi.png", 5),
        ("Margine_Spate_Roi.png", 5), ("Buton_Space.png", 8), ("Mort.png", 5),
    ]

    liste = [incarca(nume, cadre, marime) for nume, cadre, marime in coale]
    imagini = [incarca(nume, 1, marime)[0] for nume, marime in spriteuri]

    return (*liste, *imagini)