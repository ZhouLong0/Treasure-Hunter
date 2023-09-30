import pygame

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
RED = (255, 0, 0)
HIDDEN = (255, 0, 255)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, type) -> None:
        super().__init__()
        images = [
            pygame.image.load("./graphics/player.png").convert_alpha(),
            pygame.image.load("./graphics/obstacle.png").convert_alpha(),
            pygame.image.load("./graphics/treasure.png").convert_alpha(),
        ]
        arrows = [
            pygame.image.load("./graphics/arrows/arrow_up.png").convert_alpha(),
            pygame.image.load("./graphics/arrows/arrow_down.png").convert_alpha(),
            pygame.image.load("./graphics/arrows/arrow_left.png").convert_alpha(),
            pygame.image.load("./graphics/arrows/arrow_right.png").convert_alpha(),
        ]
        self.coordinates = (x, y)
        self.image = pygame.Surface([96, 96])
        self.image.set_colorkey(HIDDEN)
        self.image.fill(WHITE)

        if type == 0:
            self.image.fill(HIDDEN)
        elif type == 1:
            self.image = images[0]
        elif type == 9:
            self.image = images[2]
        elif type == 4:
            self.image = images[1]

        elif type == "u":
            self.image = arrows[0]
        elif type == "d":
            self.image = arrows[1]
        elif type == "l":
            self.image = arrows[2]
        elif type == "r":
            self.image = arrows[3]

        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = type

    def update(self):
        ...
