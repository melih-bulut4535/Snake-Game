import sys
import math
from random import randrange
import pygame as pg


class Ball(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(groups)
        self.image = pg.Surface((30, 30), pg.SRCALPHA)
        col = randrange(256), randrange(256), randrange(256)
        pg.draw.circle(self.image, col, (15, 15), 15)
        self.rect = self.image.get_rect(center=pos)
        self.vel = pg.math.Vector2(8, 0).rotate(randrange(360))
        self.pos = pg.math.Vector2(pos)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if self.rect.left < 0 or self.rect.right > 640:
            self.vel.x *= -1
        if self.rect.top < 0 or self.rect.bottom > 480:
            self.vel.y *= -1


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    sprite_group = pg.sprite.Group()
    ball = Ball((320, 240), sprite_group)

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                sprite_group.add(Ball((320, 240)))

        sprite_group.update()
        screen.fill((30, 30, 30))
        sprite_group.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()