import pygame

class Model:
    def __init__(self, latime, inaltime, tile, drum_x, pamant, drum,
                 margine_stanga, margine_dreapta, masa,
                 secera, seminte, insecticid, stropitoare):

        self.fundal = pygame.Surface((latime, inaltime))
        for rand in range(inaltime // tile + 1):
            y1 = rand * tile
            for coloana in range(latime // tile + 1):
                self.fundal.blit(pamant, (coloana * tile, y1))
            self.fundal.blit(margine_stanga, (drum_x, y1))
            self.fundal.blit(drum, (drum_x + tile, y1))
            self.fundal.blit(drum, (drum_x + 2 * tile, y1))
            self.fundal.blit(margine_dreapta, (drum_x + 3 * tile, y1))

        poz_mese = [
            (drum_x + tile - 5, 0),
            (drum_x + 2 * tile + 5, 0),
            (drum_x + tile - 5, inaltime - tile),
            (drum_x + 2 * tile + 5, inaltime - tile),
        ]
        for poz in poz_mese:
            self.fundal.blit(masa, poz)

        x2, x3 = latime // 2 - tile, latime // 2
        x4, x5 = latime // 2 - tile, latime // 2
        y_sus, y_jos = 0, inaltime - tile
        self.mese = [
            masa.get_rect(topleft=(x2, y_sus)),
            masa.get_rect(topleft=(x3, y_sus)),
            masa.get_rect(topleft=(x4, y_jos)),
            masa.get_rect(topleft=(x5, y_jos)),
        ]

        self.zone = {
            1: masa.get_rect(topleft=(x2, y_sus)).inflate(0, 60),
            2: masa.get_rect(topleft=(x3, y_sus)).inflate(0, 60),
            3: masa.get_rect(topleft=(x4, y_jos - 60)),
            4: masa.get_rect(topleft=(x5, y_jos - 60)),
        }

        self.secret1 = masa.get_rect(topright=(drum_x + tile * 2 + 10, -20))
        self.secret2 = masa.get_rect(topright=(drum_x + tile * 2 + 10, inaltime - 70))

        self.imagini_unelte = {1: secera, 2: seminte, 3: insecticid, 4: stropitoare}
        self.repaus = {
            1: (drum_x + tile - 5, 0),
            2: (drum_x + 2 * tile + 5, 0),
            3: (drum_x + tile - 5, inaltime - tile - 10),
            4: (drum_x + 2 * tile, inaltime - tile - 20),
        }
        self.decalaj = {1: 30, 2: 30, 3: 30, 4: 10}

    def deseneaza_fundal(self, ecran):
        ecran.blit(self.fundal, (0, 0))

    def blocheaza(self, jucator, keys, x, y, viteza):
        if any(jucator.colliderect(m) for m in self.mese):
            if keys[pygame.K_w]:
                y += viteza
            elif keys[pygame.K_s]:
                y -= viteza
            elif keys[pygame.K_d]:
                x -= viteza
            elif keys[pygame.K_a]:
                x += viteza
        return x, y

    def interactioneaza(self, ecran, jucator, x, y, keys, z, t, buton):
        for unealta, zona in self.zone.items():
            if jucator.colliderect(zona) and z in (0, unealta):
                ecran.blit(buton, (x - 28, y - 105))
                if keys[pygame.K_e] and t >= 15:
                    z = unealta if z == 0 else 0
                    t = 0
        return z, t

    def deseneaza_unelte(self, ecran, x, y, z):
        for unealta, imagine in self.imagini_unelte.items():
            if z == unealta:
                poz = (x + self.decalaj[unealta], y)
            else:
                poz = self.repaus[unealta]
            ecran.blit(imagine, poz)

    def secret(self, jucator):
        return jucator.colliderect(self.secret1) or jucator.colliderect(self.secret2)