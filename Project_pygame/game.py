import pygame
import os
import time as t
import random

pygame.font.init()

count=0
width=700
height=700
fps=60 #frame per second
i=0#for counter
enemy_vel=1
win1=pygame.display.set_mode([width,height])
bg=pygame.transform.scale(pygame.image.load(os.path.join("imgs","png-night.png")),(width,height))
ship = pygame.transform.scale(pygame.image.load(os.path.join("imgs","sprite.png")),(70,70))
enemy_ship=pygame.transform.scale(pygame.image.load(os.path.join("imgs","ship_enemy.png")),(40,40))
fire_b=pygame.transform.scale(pygame.image.load(os.path.join("imgs","fire.png")),(20,20))
hero_fire=pygame.transform.scale(pygame.image.load(os.path.join("imgs","missile.png")),(22,22))
pygame.display.set_caption("Shoot Game")
label1=pygame.font.SysFont("comicsans",30)
label2=pygame.font.SysFont("comicsans",50)
count_t=0
Time = pygame.time.Clock() # set interval time or frame per second
Life=10
level=6
level_count=0
a=[i for i in range(0,-400,-1)]
class ship1():
    def __init__(self,x,y,w,img):
        self.x=x
        self.y=y
        self.w=w
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)
    
    def update(self):
        self.w.blit(self.img,(self.x,self.y))
        
class laser():
    def __init__(self,x,y,win,p_width,img1):
        self.imgs=img1
        self.mask=l=pygame.mask.from_surface(self.imgs)
        self.win2=win
        self.x=x
        self.y=y
        self.p_width=p_width
        
    def refresh_laser(self):
        self.win2.blit(self.imgs,(self.x+(self.p_width/2)-10,self.y))


class Enemy():
    def __init__(self,x,y,e_img,w):
        self.x=x
        self.y=y
        self.win3=w
        self.img=e_img
        self.mask=pygame.mask.from_surface(self.img)
    def refresh_enemy(self):
        self.win3.blit(self.img,(self.x,self.y))


def count(limit,i):
    if i>limit:
        i=0
        return True
    else:
        return False

def collide(obj1,obj2):
    x3=obj1.x-obj2.x
    y3=obj2.y-obj1.y
    return obj2.mask.overlap(obj1.mask,(x3,y3))!= None

def refresh_dis():
    player.update()# call player
    pygame.display.update()

player=ship1(width/2,height-(ship.get_height()),win1,ship)
run=True
fire=False
laser_fire=[]
enemies=[]
ene_laser=[]

start_msg=label1.render("PRESS 's' TO START",1,(255,255,255))
won = label1.render("Congrts..You Won",1,(255,255,255))
end=label1.render("You Lost",1,(255,255,255))
st=True
st_status=False
while run:
    Time.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            
    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP] and (player.y-2)>0:
        player.y=player.y-2
    if keys[pygame.K_DOWN] and (player.y+2+ship.get_width()) < width:
        player.y=player.y+2
    if keys[pygame.K_LEFT] and (player.x-2) >0:
        player.x=player.x-2
    if keys[pygame.K_RIGHT] and (player.x+2+ ship.get_width())< height:
        player.x=player.x+2
    if keys[pygame.K_s]:
        st_status=True
    win1.blit(bg,(0,0))
    if st_status:
        if keys[pygame.K_SPACE] and count(10,i):
            f1=laser(player.x,player.y,win1,ship.get_width(),hero_fire)
            laser_fire.append(f1)
            i=0
        i=i+1

        for bullet in laser_fire:
            bullet.y-=2
            if bullet.y < 0:
                laser_fire.remove(bullet)
            bullet.refresh_laser()
            for enemy_ind in enemies:
                if collide(enemy_ind,bullet):
                    enemies.remove(enemy_ind)
                    laser_fire.remove(bullet)
                    level_count+=1
                    if level_count > 25:
                        level_count=0
                        level-=1
                        if level<=0:
                            level=1
                            win1.blit(won,((width/2) - 20,height/2))
                            refresh_dis()
                            t.sleep(1)
                            
        y_dir=random.choice(a)
        if random.randrange(0,level*50)==1:
            ene=Enemy(random.randint(0,width-(enemy_ship.get_width())-10),y_dir,enemy_ship,win1)
            enemies.append(ene)
        for enemy_ind in enemies:
            enemy_ind.y+= enemy_vel
            if random.randrange(0,5*fps)==1:
                ene_l=laser(enemy_ind.x,enemy_ind.y+(enemy_ship.get_height()/2)-3,win1,enemy_ship.get_width(),fire_b)
                ene_laser.append(ene_l)
            if collide(player,enemy_ind):
                Life-=1
                enemies.remove(enemy_ind)
            enemy_ind.refresh_enemy()
            if enemy_ind.y > height:
                enemies.remove(enemy_ind)
        for enel in ene_laser:
            enel.y+=enemy_vel+1
            enel.refresh_laser()
            if collide(enel,player):
                Life-=1
                ene_laser.remove(enel)
            if enel.y > height:
                ene_laser.remove(enel)

    else:
        win1.blit(start_msg,((width/2)-60,height/2))

    lab1=label1.render("Life:{}".format(Life),1,(255,255,255))
    lab2=label1.render("Level:{}".format(7-level),1,(255,255,255))
    lab3=label2.render("You Lost",1,(255,255,255))
    
    win1.blit(lab1,(width-(lab1.get_width())-10,20 ))
    win1.blit(lab2,(width-(lab2.get_width())-10,(lab1.get_height()+20)))
    if Life<=0:
        win1.blit(lab3,(win1.get_width()/2,win1.get_height()/2))
        break
    refresh_dis()
pygame.quit()
