import asyncio
import pygame
import random
import joc.sprite as sprite
import joc.ferme as ferme
import joc.model as model


async def main():
    pygame.init()
    ecran = pygame.display.set_mode((1536, 864))
    ceas = pygame.time.Clock()

    font = pygame.font.Font("freesansbold.ttf", 60)
    font_gandaci = pygame.font.Font("freesansbold.ttf", 40)

    latime, inaltime = ecran.get_size()

    (frames, frames2, meniu,
     pamant, drum, margine_drum_stanga, margine_drum_dreapta,
     buton, ban, spate,
     masa, secera, seminte,
     insecticid, stropitoare, gandaci,
     roi, roi2, roi3, space, mort) = sprite.incarca_tot()

    bluescreen = pygame.image.load("Spriteuri/Bluescreen.png").convert_alpha()
    bluescreen = pygame.transform.scale(bluescreen, (latime, inaltime))
    frames_mari = sprite.incarca("Player.png", 9, 14)

    interval_roi = 90000
    scadere_roi = 15000
    urmatorul_roi = pygame.time.get_ticks() + interval_roi
    roi_pana = 0
    game_over = False

    x, y = latime // 2, inaltime // 2
    frame = 8
    acum = 0
    z = 0
    t = 0
    m = 0
    bani = 250
    bariera = 10

    viteza = 8
    viteza_normala = 8
    viteza_diagonala = 6
    crestere_viteza = 1

    l = latime // 500
    k = inaltime // 500

    tile = 96
    nrtile_latime = latime // tile
    latime_drum = 4 * tile
    drum_x = (latime - latime_drum) // 2

    contor = ferme.Numara()
    ferme_joc = ferme.Ferme(frames2, drum_x, latime_drum, latime, inaltime, contor)

    model_joc = model.Model(latime, inaltime, tile, drum_x, pamant, drum,
                            margine_drum_stanga, margine_drum_dreapta, masa,
                            secera, seminte, insecticid, stropitoare)

    elemente_meniu = [
        (2, 11, 4), (7, 11, 2), (0, 11, 0),
        (3, 0, 4),  (5, 0, 2),  (1, 0, 0),
        (6, 3, 0),  (6, 5, 0),  (6, 8, 0),
        (4, 3, 4),  (4, 5, 4),  (4, 8, 4),
        (8, 3, 2),  (8, 5, 2),  (8, 8, 2),
    ]

    latime_meniu = max(c * tile + meniu[i].get_width() for i, c, r in elemente_meniu)
    inaltime_meniu = max(r * tile + meniu[i].get_height() for i, c, r in elemente_meniu)

    meniu_x = (latime - latime_meniu) // 2
    meniu_y = (inaltime - inaltime_meniu) // 2

    # textele care nu se schimbă, create o singură dată
    tutorial = font.render("Invazile de gandaci devin tot mai frecvente, "
                           "asa ca trebuie sa cumperi un Aparat Anti-Gandac 3000. "
                           "Problema este ca costa 3000 de bani si tu ai 250. "
                           "Cultiva destule plante inainte ca invazile sa devina "
                           "prea frecvente si repara ferma cand este atacata de gandaci.",
                           True, "black", None, 1370)
    victorie = font.render("Ai castigat", True, "green")
    pierdere = font.render("Ai pierdut", True, "red")

    run = True
    while run:
        ceas.tick(60)
        t += 1
        my_text = font.render(str(bani), True, "yellow")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and keys[pygame.K_d]:
            viteza = viteza_diagonala
            y -= viteza
            x += viteza
            frame = 0
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            viteza = viteza_diagonala
            y -= viteza
            x -= viteza
            frame = 1
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            viteza = viteza_diagonala
            y += viteza
            x += viteza
            frame = 3
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            viteza = viteza_diagonala
            y += viteza
            x -= viteza
            frame = 2
        elif keys[pygame.K_w]:
            viteza = viteza_normala
            y -= viteza
            frame = 7
        elif keys[pygame.K_s]:
            viteza = viteza_normala
            y += viteza
            frame = 6
        elif keys[pygame.K_a]:
            viteza = viteza_normala
            x -= viteza
            frame = 4
        elif keys[pygame.K_d]:
            viteza = viteza_normala
            x += viteza
            frame = 5
        else:
            frame = 8

        corp = frames[frame].get_bounding_rect()
        x = max(bariera - corp.left, min(x, latime - corp.right - bariera))
        y = max(bariera - corp.top, min(y, inaltime - corp.bottom - bariera))

        jucator = frames[frame].get_rect(topleft=(x, y))

        model_joc.deseneaza_fundal(ecran)
        x, y = model_joc.blocheaza(jucator, keys, x, y, viteza)
        z, t = model_joc.interactioneaza(ecran, jucator, x, y, keys, z, t, buton)

        if m == 1:
            acum = pygame.time.get_ticks()

        if acum >= urmatorul_roi and not game_over:
            ferme_joc.reseteaza()
            bani = max(0, bani - 100)
            roi_pana = acum + 2000
            interval_roi -= scadere_roi
            contor.numara += 0.25
            viteza_normala += crestere_viteza
            viteza_diagonala = int(viteza_normala * 0.7)
            if interval_roi <= 0:
                game_over = True
            else:
                urmatorul_roi = acum + interval_roi

        ferme_joc.actualizeaza(acum)

        ferme_joc.deseneaza(ecran)
        bani, t = ferme_joc.interactioneaza(ecran, jucator, x, y, keys, z, t, bani, acum, buton)

        ecran.blit(frames[frame], (x, y))

        if acum < roi_pana:
            for _ in range(40):
                ecran.blit(gandaci, (random.randint(0, latime - gandaci.get_width()),
                                     random.randint(0, inaltime - gandaci.get_height())))

        model_joc.deseneaza_unelte(ecran, x, y, z)

        if not game_over:
            secunde = max(0, (urmatorul_roi - acum) // 1000)
            text_roi = font_gandaci.render(f"Roi de gandaci in: {secunde}s", True, "red")
            ecran.blit(roi, (70, 10))
            ecran.blit(roi, (230, 10))
            ecran.blit(roi, (300, 10))
            ecran.blit(roi3, (30, 10))
            ecran.blit(roi2, (340, 10))
            ecran.blit(text_roi, (50, 30))

        ecran.blit(spate, ((nrtile_latime - l) * tile - 70, -120))
        ecran.blit(my_text, ((nrtile_latime - l) * tile, 25))
        ecran.blit(ban, ((nrtile_latime - l) * tile - 150, -45))

        if m == 0:
            for index, c, r in elemente_meniu:
                ecran.blit(meniu[index], (meniu_x + c * tile, meniu_y + r * tile))
            ecran.blit(space, (6.7 * tile, 5.5 * tile))
            ecran.blit(tutorial, (tile + 40, tile + 20))
            if keys[pygame.K_SPACE]:
                m = 1
                urmatorul_roi = pygame.time.get_ticks() + interval_roi

        if game_over:
            for index, c, r in elemente_meniu:
                ecran.blit(meniu[index], (meniu_x + c * tile, meniu_y + r * tile))
            ecran.blit(space, (6.7 * tile, 5.5 * tile))

            if bani >= 2900:
                ecran.blit(victorie, (latime // 2 - 150, inaltime // 2 - 150))
                ecran.blit(frames_mari[8], (latime // 2 - 70, inaltime // 2 - 50))
            else:
                ecran.blit(pierdere, (latime // 2 - 150, inaltime // 2 - 150))
                ecran.blit(mort, (latime // 2 - 80, inaltime // 2 - 50))

            if keys[pygame.K_SPACE]:
                run = False

        if model_joc.secret(jucator):
            ecran.blit(bluescreen, (0, 0))
            run = False

        pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())