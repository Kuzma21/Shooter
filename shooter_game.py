from pygame import *
from random import randint

win_widht = 700
win_height = 500
window = display.set_mode((win_widht, win_height))
display.set_caption('COSMOS')
background = transform.scale(image.load('F2.jpg'),(win_widht, win_height))
mixer.init()
mixer.music.load('Inferno.mp3')
mixer.init()
shoot = mixer.Sound('shoot.ogg')


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = 'left'
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT]:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("X1.png", self.rect.centerx, self.rect.top, 20, 20, 15)
        Bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lose
        if self.rect.y > 500:
            lose += 1
            self.rect.y = 0
            self.rect.x = randint(80,620)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

Bullets = sprite.Group()

lose = 0

Monsters = sprite.Group()
for i in range(5):
    Monsters.add(Enemy("enemy" + str(i + 1) + ".png", randint(80,620), 0, 65, 65, randint(2,3)))


player = Player("K1.png", 300, 440, 65, 65, 11)


clock = time.Clock()
FPS = 60
game = True

font.init()
font1 = font.Font("arial.ttf", 36)
text_lose = font1.render("Пропущено " + str(lose), 1, (255, 255, 255))



score = 0




while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                shoot.play()
                player.fire()
    if lose > 2  or sprite.spritecollide(player, Monsters, False):
        game = False          

    sprites_list = sprite.groupcollide(Monsters,  Bullets, True, True)
    for s in sprites_list:
        score += 1
        Monsters.add(Enemy("enemy" + str(randint(1,5)) + ".png", randint(80,620), 0, 65, 65, randint(2,3)))

    
    window.blit(background,(0,0))
    player.reset()
    player.update()
    Monsters.draw(window)
    Monsters.update()
    Bullets.draw(window)
    Bullets.update()




    font1 = font.Font("arial.ttf", 36)
    window.blit(text_lose, (10, 10))
    text_lose = font1.render("Пропущено " + str(lose), 1, (255, 255, 255))
    text_score = font1.render("Убито " + str(score), 1, (255, 255, 255))
    window.blit(text_score, (10, 40))



    clock.tick(FPS)
    display.update()
    