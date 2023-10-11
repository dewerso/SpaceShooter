from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update (self):
        self.rect.y+= self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:   
            self.kill()

#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))


player = Player('rocket.png',5,win_height-100 ,80, 100, 10)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font

FPS = 60
clock = time.Clock()
finish = False

score = 0
lost = 0

game = True

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png',randint(80,win_height-80), -40, 80, 50, randint(1,3))
    monsters.add(monster)

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)

bullets = sprite.Group()   

num_fire = 0
rel_time = False


meteors = sprite.Group()
for i in range(1,3):
    meteor = Enemy('asteroid.png',randint(80,win_height-80), -40, 80, 50, randint(1,3))
    meteors.add(meteor)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire+=1 
                    fire_sound.play()
                    player.fire()
                if num_fire>=5 and rel_time == False:
                    time_m1 = timer()
                    rel_time = True


    
    if finish !=True:
        window.blit(background,(0,0))

        text_lose = font1.render('Счёт: '+ str(score), 1, (255,255,255))
        window.blit(text_lose,(10,20))

        text_lose = font2.render('Пропущено: '+ str(lost), 1, (255,255,255))
        window.blit(text_lose,(10,50))

        sprite_list = sprite.groupcollide(monsters,bullets,True,True )

        for c in sprite_list:
            score+=1
            monster = Enemy('ufo.png',randint(80,win_height-80), -40, 80, 50, randint(1,3))
            monsters.add(monster)

        if sprite.spritecollide(player,monsters,False) or lost >= 3:
            finish = True
            text_pro = font1.render('ВЫ ПРОИГРАЛИ',True,(255,255,255))
            window.blit(text_pro,(200,200))

        if score == 11:
            finish = True
            text_win = font2.render('ВЫ ПОБЕДИЛИ', True,(255,255,255))
            window.blit(text_win,(200,200))

        if rel_time == True:
            time_m2 = timer()
            if time_m2 - time_m1 < 2:
                text_pere = font2.render('ПОДОЖДИТЕ', True,(255,255,255))
                window.blit(text_pere,(100,200))
            else:
                num_fire = 0
                rel_time = False



        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        meteors.update()
        meteors.draw(window)
 
    display.update()
    clock.tick(FPS)