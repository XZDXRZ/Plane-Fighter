import pygame, sys, random

size = (1000,650)
bg_color = (255,255,255)
tick = 10

# Game var
MAXENERMY = 3
MAXSPEED = 3
MAXPLAYERBULLET = 30
PLAYERBULLETDELAY = 500
player_bullet_num = 0
enermy_num = 0
player_bullet_delay = 100

# Score
score = 0
miss = 0

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./pic/player.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (100,50)

    def move(self):
        self.pos = pygame.mouse.get_pos()
        self.height = self.rect.bottom - self.rect.top
        self.weith = self.rect.right - self.rect.left
        self.pos = list(self.pos)
        self.pos[0] -= self.weith/2
        self.pos[1] -= self.height/2
        if self.pos[0]<0:
            self.pos[0]=0
        if self.pos[0]>size[0]:
            self.pos[0]=size[0]
        if self.pos[1]<0:
            self.pos[1]=0
        if self.pos[1]>size[1]:
            self.pos[1]=size[1]
        self.rect.left, self.rect.top = self.pos

    def get_pos(self):
        #return [self.rect.left, self.rect.top]
        return [(self.pos[0]+self.weith/2),(self.pos[1]+self.height/2)]

    def death(self):
        if pygame.sprite.spritecollide(self, enermies, True):
            return True
        return False

class Enermy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./pic/enermy.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (random.randint(1,size[0]-(self.rect.right-self.rect.left)),-100)
        self.t = [0,random.randint(1,MAXSPEED)]

    def move(self):
        self.rect = self.rect.move(self.t)

    def out(self):
        if self.rect.top > size[1]:
            return True
        return False

class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./pic/player_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.t = [0,-7]

    def move(self):
        self.rect = self.rect.move(self.t)

    def out(self):
        if self.rect.bottom < 0:
            return True
        return False

    def hit(self):
        if pygame.sprite.spritecollide(self, enermies, True):
            return True
        return False

def animate():
    global enermy_num, player_bullet_num, player_bullet_delay, score, miss, font
    screen.fill(bg_color)
    # Enermy
    for enermy in enermies:
        enermy.move()
        screen.blit(enermy.image, enermy.rect)
        if enermy.out():
            enermies.remove(enermy)
            enermy_num -= 1
            miss += 1
    # Player Bullet
    for player_bullet in player_bullets:
        player_bullet.move()
        if player_bullet.hit():
            score += 1
            enermy_num -= (enermy_num - len(enermies))
            player_bullets.remove(player_bullet)
            player_bullet_num -= 1
            continue
        screen.blit(player_bullet.image, player_bullet.rect)
        if player_bullet.out():
            player_bullets.remove(player_bullet)
            player_bullet_num -= 1
    # Player
    player.move()
    if player.death():
        pygame.quit()
        sys.exit()
    screen.blit(player.image, player.rect)
    # Other Generation
    for i in range(enermy_num, MAXENERMY):
        enermies.add(Enermy())
        enermy_num += 1
    for i in range(player_bullet_num, MAXPLAYERBULLET):
        if player_bullet_delay >= PLAYERBULLETDELAY:
            player_bullets.add(Player_Bullet(player.get_pos()))
            player_bullet_num += 1
            player_bullet_delay = 0
        player_bullet_delay += 1
    # Font
    hitting = font.render('Score: '+str(score),False,(0,233,233))
    screen.blit(hitting, (10,10))
    missing = font.render('Miss: '+str(miss),False,(233,233,0))
    screen.blit(missing, (10,45))
    pygame.display.flip()
    pygame.time.delay(tick)

screen = pygame.display.set_mode(size)
screen.fill(bg_color)

running = True
font = pygame.font.SysFont('arial', 40)
player = Player()
enermies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()

while running:
    animate()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
sys.exit()