from pygame import *
from random import randint
from time import time as timer
run = True
rel_time = False
num_fie = 0
wid = 700
hit = 500

font.init()
font1 = font.SysFont('Arial',80)
font2 = font.SysFont('Arial',36)
win = font1.render("НЩГ ЦШТ!!!",True,(255,255,255))
lose = font1.render("ТЫ ЛОХ!!",True,(100,0,0))

ing_enemy = "asteroid.png"
ing_roket = "rocket.png"
ing_bullet = "bullet.png"
ing_ufo = 'ufo.png'

window = display.set_mode((wid,hit))
display.set_caption('Wars')
background = transform.scale(
    image.load("galaxy.jpg"),
    (700,500))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()


class Roket(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))




class Player(Roket):
    def KEY(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(ing_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Bullet(Roket):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

goal = 100
score = 0
lost = 0
max_lost = 3

class Enemy(Roket):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > wid:
            self.rect.x = randint(80 ,620)
            self.rect.y = 0
            lost = lost + 1
    
Rockett = Player(ing_roket,5,400,80,100,10)
monsters = sprite.Group()
bullets = sprite.Group()
ufos = sprite.Group()

for i in range(1,6):
    monster = Enemy(ing_enemy,randint(80, 620),-40,80,50,randint(1,3))
    monsters.add(monster)

for i in range(1,3):
    ufo = Enemy(ing_ufo,randint(80, 620),-40,80,50,randint(1,3))
    ufos.add(ufo)





finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fie < 5 and rel_time == False:
                    num_fie = num_fie + 1
                    #fire_sound.play()
                    Rockett.fire()
                
                if num_fie >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background,(0,0))
        Rockett.KEY()
        Rockett.reset()
        monsters.update()
        monsters.draw(window)
        ufos.update()
        ufos.draw(window)

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score = score + 1
            monster = Enemy(ing_enemy,randint(80, 620),-40,80,50,randint(1,3))
            monsters.add(monster)

        if sprite.spritecollide(Rockett,monsters,False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200,20))

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Я перезаряжаюсь...', 1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fie = 0
                rel_time = False

        if score >= goal:
            finish = True
            window.blit(win, (200,200))

        text = font2.render("Счет:" + str(score), 1,(255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render("Пропущенные:" + str(lost), 1,(255,255,255))
        window.blit(text_lose,(10,50)) 
        bullets.update()
        bullets.draw(window)
    display.update()
    time.delay(50)