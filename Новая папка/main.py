from random import randint
from pygame import*


class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y,player_speed,width=65,height=65):
        super().__init__()
        self.image=transform.scale(image.load(player_image),(width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Player(GameSprite):
    def  update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 85:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, -15, 15, 20,)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_weight - 80)
            self.rect.y = 0
            lost = lost + 1

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.png'), (win_width, win_height))

player = Player('rocket.png', 5, win_height - 100, 20 ,80 ,100)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80),  -40, randint(1, 5), 80, 50)
    monsters.add(monster)

bullets = sprite.Group()

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))

score = 0  # збито кораблів
lost = 0  # пропущено кораблів
game = True  # прапорець скидається кнопкою закриття вікна
finish = False  # змінна "гра закінчилася"

clock = time.Clock()
FPS = 20


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
        
    if not finish:
        window.blit(background, (0,0))
        player.update()
        monsters.update()
        bullets.update()
        
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        

        text = font1.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        if sprite.groupcollide(monsters, bullets, True, True):
            score = score + 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, randint(1, 5), 80, 50)
            monsters.add(monster)


        if sprite.spritecollide(player, monsters, False) or lost >= 20:
            finish = True
            window.blit(lose, (200, 200))


        if score >= 20:
            finish = True
            window.blit(win, (200, 200))

        display.update()

    clock.tick(FPS)







            
