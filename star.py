# coding: utf-8

import sys
import pygame

import time

from pygame.sprite import Sprite

from random import randint

scr_width = 1280
scr_height = 720
scr_size = (scr_width, scr_height)
bg_color = (255, 255, 255)

basket_color = (0, 0, 0)
basket_width = 120
basket_height = 20

moving_right = False
moving_left = False
moving_speed = 3

star_falling_speed = 1


class Basket():
    def __init__(self, main_screen):
        self.main_screen = main_screen
        self.screen_rect = main_screen.get_rect()
        self.rect = pygame.Rect(0, 0, basket_width, basket_height)
        self.rect.x = self.screen_rect.centerx - basket_width / 2
        self.rect.y = scr_height - basket_height

    def update_basket(self):
        pygame.draw.rect(self.main_screen, basket_color, self.rect)


class Star(Sprite):
    def __init__(self, main_screen):
        super().__init__()
        self.main_screen = main_screen
        self.image = pygame.image.load('star.png')
        self.rect = self.image.get_rect()
        self.screen_rect = main_screen.get_rect()
        self.rect.x = randint(0, self.screen_rect.right)
        self.rect.y = 0

    def show_star(self):
        self.main_screen.blit(self.image, self.screen_rect)

    def star_falling(self):
        self.rect.y += star_falling_speed


def moving(basket):
    if moving_right and basket.rect.right < scr_width:
        basket.rect.x += (moving_speed + 1)
    if moving_left and basket.rect.left > 0:
        basket.rect.x -= moving_speed


def get_star(stars):
    for star in stars.sprites():
        return star


def create_stars(main_screen, stars):
    star = Star(main_screen)
    stars.add(star)


def check_falling_distance(main_screen, stars):
    screen_rect = main_screen.get_rect()
    for star in stars.sprites():
        if star.rect.y <= screen_rect.bottom:
            return True
        else:
            return False


def falling(main_screen, stars):
    star = get_star(stars)
    if check_falling_distance(main_screen, stars):
        star.star_falling()
    else:
        create_stars(main_screen, stars)
        print('have new')


def check_spritecollide(basket, stars):
    collisions = pygame.sprite.spritecollide(basket, stars, True)
    if collisions:
        pygame.mixer.music.load("Ding.wav")
        pygame.mixer.music.play()
        print('Get one')


pygame.init()
main_screen = pygame.display.set_mode(scr_size)
pygame.display.set_caption('接星星')

stars = pygame.sprite.Group()

create_stars(main_screen, stars)

basket = Basket(main_screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_LEFT:
                moving_left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False

    main_screen.fill(bg_color)

    moving(basket)

    basket.update_basket()

    falling(main_screen, stars)

    stars.draw(main_screen)

    check_spritecollide(basket, stars)

    for star in stars.copy():
        if star.rect.bottom >= scr_height:
            stars.remove(star)
            print('remove the miss')

    pygame.display.flip()
