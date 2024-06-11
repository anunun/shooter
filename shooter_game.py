from tkinter.tix import Tree
from typing import Any
from pygame import *
from random import randint
from time import time as timer #імпортуємо функцію для засікання часу, щоб інтерпретатор не шукав цю функцію в pygame модулі time, даємо їй іншу назву самі

mixer.init()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))


img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_non_killable_enemy = "asteroid.png"
img_mega_ufo= "mega_ufo.png"
img_lazer_1="lazer_1.png"
img_lazer_2="lazer_2.png"

score = 0
lost = 0
goal = 1
max_lost = 3
life = 100
asteroid_x=40
asteroid_y=0
ast = True
ast_2=0
mega_ufo=True
hits =10
hits_sec=0
hit=True
black = (255, 0, 0)
lazer_1 =False
lazer_t1=0
lazer_t2=0
lazer_cx=0
lazer_cy=0
lazer_cx2=0
lazer_cy2=0
num=0
rand=0
start=False
start2=0
# monster = GameSprite(img_enemy, 100, 100, 80, 50, 0)
# monsters.add(monster)


class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, sixe_y , sprite_speed_x ,sprite_speed_y):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(size_x, sixe_y))
        self.speed_x = sprite_speed_x
        self.speed_y = sprite_speed_y
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        global lazer_cx,lazer_cy
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed_x
        if keys[K_d] and self.rect.x < win_width - 30:
            self.rect.x += self.speed_x
        if keys[K_w] and self.rect.y > 100:
            self.rect.y -= self.speed_y
        if keys[K_s] and self.rect.y < win_height - 30:
            self.rect.y += self.speed_y
        lazer_cx=self.rect.centerx
        lazer_cy=self.rect.centery
    def fire(self):
        global lazer_1,lazer_cx2,lazer_cy2,lazer2,lazer1,num
        num=0
        lazer1 = Lazer("lazer_2.png", lazer_cx -3, lazer_cy -150, 6, 300,80,0)
        lazer1.add(lazers_2)
        lazer2 = Lazer("lazer_2.png", lazer_cx -150, lazer_cy+2 , 300, 6,80,0)
        lazer2.add(lazers_2)
        lazer_cx2=lazer_cx
        lazer_cy2=lazer_cy
        lazer_1=True


    # def fire(self):
    #     bullet = Bullet("bullet.png", self.rect.centerx - 7, self.rect.top, 15, 20, -15,0)
    #     bullets.add(bullet)

class Lazer(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed, sprite_speed_y):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed, sprite_speed_y)
    def spawn(self):
        global lazer_1,lazer_cx2,lazer_cy2,lazer2,lazer1,lazer_t1
        lazer1 = Lazer("lazer_2.png", lazer_cx -3, lazer_cy -150, 6, 300,80,0)
        lazer1.add(lazers_2)
        lazer2 = Lazer("lazer_2.png", lazer_cx -150, lazer_cy+2 , 300, 6,80,0)
        lazer2.add(lazers_2)
        lazer_cx2=lazer_cx
        lazer_cy2=lazer_cy
        lazer_1=True
        lazer_t1=0
                
            




class Asteroid(GameSprite):
    def update(self):
        global asteroid_x,ast,ast_2,mega_ufo,start2
        self.rect.y += self.speed_x
        if self.rect.y > win_height:
            if ast_2 <= 116:  
                self.rect.x = asteroid_x
                self.rect.y = 0
            else:
                self.kill()
            ast_2 +=1
        if asteroid_x >= 640 and ast:
            asteroid_x= -80
            ast= False
        elif asteroid_x >= 640 and ast==False:
            asteroid_x=-40
            ast=True
        asteroid_x+=80
        if ast_2==162 and mega_ufo:
            superMonster = SuperUfo(img_mega_ufo, 235, 0, 250, 100, 0,0,hits)
            superMonsters.add(superMonster)
            start2=1
            mega_ufo=False
        
class SuperUfo(GameSprite):
    direction ="LEFT"
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed,sprite_speed_y, max_hits):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed,sprite_speed_y)
        self.max_hits = max_hits
    def update(self):
        if self.direction =="LEFT" and self.rect.x>=0:
            self.rect.x -=2
        elif self.direction=="LEFT" and self.rect.x<=0:
            self.direction="RIGHT"
        elif self.direction=="RIGHT" and self.rect.x<=470:
            self.rect.x +=2
        elif self.direction=="RIGHT" and self.rect.x>=470:
            self.direction="LEFT"
        text_a = font1.render(str(hits), 1, (0, 150, 0))
        window.blit(text_a, (344, 465))    
    def gotHit(self):
        if self.isVictible:
            self.max_hits -= 1
    def isKilled(self):
        if(self.max_hits <= 0):
            self.kill()
            return True
        else: return False

class Bullet(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed_x,sprite_speed_y):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed_x,sprite_speed_y)
    def update(self):
        self.rect.y += self.speed_x
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()

win_width = 720
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

player = Player(img_hero, 345, win_height - 100, 30, 30, 5 ,5)




bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
superMonsters = sprite.Group()
lazers_1 = sprite.Group()
lazers_2 = sprite.Group()

for i in range(5):
    for i in range(9):
        asteroid = Asteroid(img_non_killable_enemy, asteroid_x , asteroid_y, 40, 25,80,0)
        asteroids.add(asteroid)
        asteroid_x+=80
    if ast:
        asteroid_x =0
        ast = False
    else:
        asteroid_x =40
        ast = True
    asteroid_y-=100


run = True
finish = False
clock = time.Clock()
FPS = 30 


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and not finish:
            if e.key == K_SPACE:
                fire_sound.play()
                # player.fire()


    if not finish:
        window.blit(background, (0, 0))
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        superMonsters.update()


        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        superMonsters.draw(window)
        lazers_1.draw(window)
        lazers_2.draw(window)

        
        for superMonster in superMonsters:
            if sprite.spritecollide(superMonster, bullets, True):
                superMonster.gotHit()
                hits-=1
                superMonster.isKilled()

        if sprite.spritecollide(player,lazers_1,False):
            life = life - 1


        # якщо спрайт торкнувся ворога зменшує життя
        if sprite.spritecollide(player, asteroids, False):
            life = life - 1

        if hits==0 and hits_sec == 2:
            finish = True
            window.blit(win, (200, 200))
        
        if hit and hits==0:
            hits_sec+=1
        
        if start2>=1:
            start2+=1
            if start2>=40:
                start2=0
                start=True
                rand=randint(1,1)


        if start and rand==1:    
            lazer1 = Lazer("lazer_2.png", lazer_cx -3, lazer_cy -150, 6, 300,80,0)
            lazer1.add(lazers_2)
            lazer2 = Lazer("lazer_2.png", lazer_cx -150, lazer_cy+2 , 300, 6,80,0)
            lazer2.add(lazers_2)
            lazer_cx2=lazer_cx
            lazer_cy2=lazer_cy
            lazer_1=True
            start=False       
        
        
        #перша атака
        if lazer_1:
            lazer_t1 +=1
            if lazer_t1==10:
                lazer3 = Lazer("lazer_1.png", lazer_cx2 -3, lazer_cy2 -150, 6, 300,80,0)
                lazer3.add(lazers_1)
                lazer4 = Lazer("lazer_1.png", lazer_cx2 -150, lazer_cy2+2 , 300, 6,80,0)
                lazer4.add(lazers_1)
                lazer1.kill()
                lazer2.kill()
            elif lazer_t1==15:
                lazer3.kill()
                lazer4.kill()
                lazer_1=False 
                num+=1
                if num!=5:    
                    lazer1.spawn()
                else:
                    lazer_t1=0
                    start=False
                    num=0
                    start2=1

        #програш
        if life == 0:
            finish = True 
            window.blit(lose, (200, 200))
        
        text_life = font1.render(str(life), 1, (0, 150, 0))
        window.blit(text_life, (650, 10))

        display.update()

    clock.tick(FPS)