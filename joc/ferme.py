import pygame
import random

class Numara:
    def __init__(self):
        self.numara = 1

    def actualizeaza(self, numara):
        self.numara = numara


class Ferme:
    def __init__(self, frames2, drum_x, latime_drum, latime, inaltime, contor):
        self.contor = contor
        self.frames = frames2
        self.durata_baza = 3000
        self.durata = self.durata_baza
        self.prob_uscat = 0.30
        self.prob_gandaci = 0.10
        self.cost_seminte = 50
        self.venit = 150
        self.plantare_sfx = pygame.mixer.Sound("Sunete/Plantare_grau.mp3")
        self.cultivare_sfx = pygame.mixer.Sound("Sunete/taiere.flac")
        self.udare_sfx = pygame.mixer.Sound("Sunete/Apa.flac")

        fl, fi = frames2[0].get_size()
        centru_stanga = drum_x // 2
        centru_dreapta = (drum_x + latime_drum + latime) // 2

        self.pozitii = []
        for rand in range(3):
            fy = inaltime * (rand + 1) // 4 - fi // 2
            for centru in (centru_stanga, centru_dreapta):
                self.pozitii.append((centru - fl // 2, fy))

        self.reseteaza()

    def reseteaza(self):
        n = len(self.pozitii)
        self.stadii = [0] * n
        self.problema = [0] * n
        self.timp_stadiu = [0] * n

    def actualizeaza(self, acum):
        self.durata = self.durata_baza // max(1, self.contor.numara)
        for i in range(len(self.pozitii)):
            if (1 <= self.stadii[i] < 4 and self.problema[i] == 0
                    and acum - self.timp_stadiu[i] >= self.durata):
                sansa = random.random()
                if sansa < self.prob_uscat:
                    self.problema[i] = 1
                elif sansa < self.prob_uscat + self.prob_gandaci:
                    self.problema[i] = 2
                else:
                    self.stadii[i] += 1
                    self.timp_stadiu[i] = acum

    def cadru(self, i):
        if self.problema[i] == 1:
            return 4 + self.stadii[i]
        if self.problema[i] == 2:
            return 8 + self.stadii[i]
        return self.stadii[i]

    def deseneaza(self, ecran):
        for i, poz in enumerate(self.pozitii):
            ecran.blit(self.frames[self.cadru(i)], poz)

    def interactioneaza(self, ecran, jucator, x, y, keys, z, t, bani, acum, buton):
        for i, poz in enumerate(self.pozitii):
            hitbox = self.frames[self.cadru(i)].get_rect(topleft=poz).inflate(120, 120)
            if not (jucator.colliderect(hitbox) and y > 80):
                continue

            ecran.blit(buton, (x - 28, y - 105))
            if not (keys[pygame.K_e] and t >= 15):
                continue

            if self.problema[i] == 1 and z == 4:
                self.udare_sfx.play()
                self.problema[i] = 0
                self.timp_stadiu[i] = acum
                t = 0
            elif self.problema[i] == 2 and z == 3:
                self.udare_sfx.play()
                self.problema[i] = 0
                self.timp_stadiu[i] = acum
                t = 0
            elif self.stadii[i] == 0 and z == 2 and bani >= self.cost_seminte:
                self.plantare_sfx.play()
                bani -= self.cost_seminte
                self.stadii[i] = 1
                self.timp_stadiu[i] = acum
                t = 0
            elif self.stadii[i] == 4 and z == 1:
                self.cultivare_sfx.play()
                self.stadii[i] = 0
                bani += self.venit
                t = 0
                
        return bani, t