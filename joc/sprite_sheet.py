import pygame

class SpriteSheet:
    def __init__(self, image, numar_cadre):
        self.sheet = image
        self.latime = image.get_width() // numar_cadre
        self.inaltime = image.get_height()

    def imagine(self, frame, marime):
        image = pygame.Surface((self.latime, self.inaltime), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (frame * self.latime, 0, self.latime, self.inaltime))
        return pygame.transform.scale(image, (self.latime * marime, self.inaltime * marime))