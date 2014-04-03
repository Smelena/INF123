import pygame, math, decimal,random, sys, pickle
from decimal import*
from pygame.locals import *
class DataHandler(object):
    def defaultscore(self):
        self.hiscorename=['Cathy','Kellye','Dwight','Candis','Dorothy','Kym','Farah','Huey','Vonnie','Loyd']
        self.hiscore=[2000,1500,1000,900,800,700,650,600,550,500]
class Objects(object): #main sprite parent
    def screencollision(self,time):
        if self.rect.left>gameinit.width:
            self.rect.right=0
        if self.rect.top>gameinit.height:
            self.rect.bottom=0
        if self.rect.right<0:
            self.rect.left=gameinit.width
        if self.rect.bottom<0:
            self.rect.top=gameinit.height
        self.x=self.rect.centerx+self.x-int(self.x)
        self.y=self.rect.centery+self.y-int(self.y)
class Asteroid(Objects,pygame.sprite.Sprite):
    def __init__(self,location,s,bulletangle,*groups):
        super(Asteroid,self).__init__(*groups)
        self.originalimage=pygame.image.load("img/asteroid.png").convert_alpha()
        width,height= self.originalimage.get_width()*s,self.originalimage.get_height()*s
        self.image=pygame.transform.scale(self.originalimage,(width,height))
        self.rect=pygame.rect.Rect(location,self.image.get_size())
        angle=random.randrange(21)*2*(random.randrange(7)+1)
        realangle=angle*math.pi/180
        if location[0]<= 1:
            self.rect.right=location[0]
        elif location[0]>= gameinit.width:
            self.rect.left=location[0]
        else:
            self.rect.centerx=location[0]
        if location[1]<= 1:
            self.rect.bottom=location[1]
        elif location[1]>= gameinit.height:
            self.rect.top=location[1]
        else:
            self.rect.centery==location[1]
        self.speedx=(random.randrange(1)*2-1)*((random.randrange(70)+5))/(80+30*s)*math.cos(realangle)
        self.speedy=(random.randrange(1)*2-1)*((random.randrange(70)+5))/(80+30*s)*math.sin(realangle)
        if self.speedx<-0.6:
            self.speedx=-0.6
        if self.speedx>0.6:
            self.speedx=0.6
        if self.speedy<-0.6:
            self.speedy=-0.6
        if self.speedy>0.6:
            self.speedy=0.6
        (self.x,self.y)=self.rect.center
        self.size=s
    def destroy(self, angle):
        if self.size>1:
            for object in range(0,3):
                Asteroid((self.rect.x+random.randrange(self.image.get_width()-30)+30,self.rect.y+random.randrange(self.image.get_height()-30)+30),self.size-1,angle,gameinit.sprites, gameinit.asteroids)
        gameinit.score+=15/self.size
        self.kill()
    def update(self,time):
        if gameinit.running:
            if pygame.sprite.collide_circle(self,gameinit.player) and gameinit.player.invincibility<=0.0:
                gameinit.player.explode(time)
        self.x+=0.5*time*self.speedx/(self.size+1)
        self.y+=0.5*time*self.speedy/(self.size+1)
        self.rect.center=(self.x,self.y)
        self.screencollision(time)
            
class Bullet(Objects, pygame.sprite.Sprite):
    def __init__(self,location,angle,*groups):
        super(Bullet,self).__init__(*groups)
        self.image=pygame.image.load("img/bullet.png").convert_alpha()
        self.rect=pygame.rect.Rect(location,self.image.get_size())
        if angle+90>360:
            angle-=360.0
        self.realangle=(angle+90)*math.pi/180
        self.rect.center=location
        self.speedx=1.0*math.cos(self.realangle)
        self.speedy=-1.0*math.sin(self.realangle)
        self.timer=250.0
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy
        (self.x,self.y)=self.rect.center
    def update(self,time):
        if self.timer>0:
            self.timer-=time
            self.x+=self.speedx*time
            self.y+=self.speedy*time
            self.rect.center=(self.x,self.y)
            if self.rect.left>gameinit.width-8:
                self.rect.right=8
            if self.rect.top>gameinit.height-8:
                self.rect.bottom=8
            if self.rect.right<8:
                self.rect.left=gameinit.width-8
            if self.rect.bottom<8:
                self.rect.top=gameinit.height-8
            for object in gameinit.sprites.sprites():
                if gameinit.player!= object and self!=object:
                    if pygame.sprite.collide_circle(self,object):
                        object.destroy(self.realangle)
                        self.kill()
                        break
        else:
            self.kill()
        self.screencollision(time)    
class Ship(Objects,pygame.sprite.Sprite):
    def __init__(self,location,*groups):
        super(Ship,self).__init__(*groups)
        self.originalimage=pygame.image.load("img/ship.png").convert_alpha()
        self.rect=pygame.rect.Rect(location,self.originalimage.get_size())
        (self.rect.centerx,self.rect.centery)=location
        self.rotation=0.0
        self.speedx=0
        self.speedy=0
        self.shot=0
        self.load=200.0
        self.invincibility=0.0
        self.alive=1
        (self.x,self.y)=self.rect.center
    def accelerate(self,angle,x,y):
        realangle=angle+90
        if realangle>360:
            realangle-=360.0
        realangle*=math.pi/180
        rady=-math.sin(realangle)
        radx=math.cos(realangle)
        if (rady<0 and not y<-0.5) or (rady>0 and not y>0.5):
            y+=rady*0.014
        if (radx<0 and not x<-0.5) or (radx>0 and not x>0.5):    
            x+=radx*0.014
        return x,y
    def reverse(self,angle,x,y):
        realangle=angle+90
        if realangle>360:
            realangle-=360.0
        realangle*=math.pi/180
        rady=math.sin(realangle)
        radx=-math.cos(realangle)
        if (rady<0 and not y<-0.3) or (rady>0 and not y>0.3):
            y+=rady*0.011
        if (radx<0 and not x<-0.3) or (radx>0 and not x>0.3):
            x+=radx*0.011
        return x,y
    def shoot(self):
        if self.load>=200.0:
            Bullet(self.rect.center,self.rotation,gameinit.sprites)
            self.load=0.0
    def explode(self,time):
        if gameinit.life>0 and self.alive:
            self.invincibility=2000.0
            self.rotation=0.0
            self.speedx=0
            self.speedy=0
            self.load=200.0
            (self.x,self.y)=(gameinit.width/2,gameinit.height/2)
            gameinit.life-=1
            self.image=pygame.transform.rotate(self.originalimage,self.rotation)
        else:
            gameinit.gameover=1
            self.alive=0
            self.kill()
    def update(self,time):
        if self.load<200.0:
            self.load+=time
        
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rotation+=0.5*time
            if self.rotation>360.0:
                self.rotation-=360.0
        if key[pygame.K_RIGHT]:
            self.rotation-=0.5*time
            if self.rotation<0.0:
                self.rotation+=360.0
        if key[pygame.K_UP]:
            self.speedx,self.speedy=self.accelerate(self.rotation,self.speedx,self.speedy)
        if key[pygame.K_DOWN]:
            self.speedx,self.speedy=self.reverse(self.rotation,self.speedx,self.speedy)
        self.x+=self.speedx*time
        self.y+=self.speedy*time
        self.rect.center=(self.x,self.y)
        if self.invincibility>0.0:
            self.invincibility-=time
            for i in range(40):
                if self.invincibility<=i*50 and self.invincibility>(i-1)*50 and i%2==0:
                    self.rect.center=(self.x,self.y)
                    self.image=pygame.transform.rotate(self.originalimage,self.rotation)
                    self.rect = self.image.get_rect(center=self.rect.center)
                    break
                elif self.invincibility<=i*50 and self.invincibility>(i-1)*50 and i%2!=0:
                    self.image=pygame.Surface((self.rect.width,self.rect.height)).convert_alpha()
                    self.image.fill((255,255,255,255))
        else:
            self.image=pygame.transform.rotate(self.originalimage,self.rotation)
            self.rect = self.image.get_rect(center=self.rect.center)
        
        self.screencollision(time)


class Game(object):
    running=0
    newhiscore=0
    def announcelevel(self,time,screen):
        self.leveltimer-=time
        leveltext=self.fontlarge.render('Level '+str(self.level),True,(0,0,0))
        screen.blit(leveltext,(self.width/2-leveltext.get_width()/2,self.height/2-leveltext.get_height()/2))
    def spawn(self):
        for i in range(self.level+1):
            while True:
                x=random.randrange(self.width)
                y=random.randrange(self.height)
                if x==0 or y==0 or x==self.width or y==self.height:
                    Asteroid((x,y),3,random.randrange(360)+1,self.sprites,self.asteroids)
                    break   
    def main(self, screen):
        self.leveltimer=500.0
        self.score=0
        self.gameover=0
        self.life=3
        getcontext().prec=3
        self.clock=pygame.time.Clock()
        self.running=1
        self.sprites=pygame.sprite.Group()
        self.asteroids=pygame.sprite.Group()
        self.player=Ship((self.width/2,self.height/2),self.sprites)
        self.background=pygame.surface.Surface((self.width,self.height))
        self.background.fill((255,255,255))
        self.font=pygame.font.Font('FreeMono.ttf',20)
        self.fontlarge=pygame.font.Font('FreeMono.ttf',36)
        self.scoretext=self.font.render('Score',True,(0,0,0))
        self.level=1
        self.levelstart=0
        self.lifeimg=pygame.image.load("img/ship.png").convert_alpha()
        self.lifeimg=pygame.transform.scale(self.lifeimg,(self.lifeimg.get_width()/2,self.lifeimg.get_height()/2))
        self.gameovertimer=1500.0
        self.newhiscore=0
        while self.running:
            self.clock.tick(60)
            time = self.clock.tick(60)
            self.event=pygame.event.get()
            for event in self.event:
                if event.type==pygame.QUIT:
                    self.running=0
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN and not self.gameover:
                    if event.key==pygame.K_SPACE:
                        self.player.shoot()
                    if event.key==pygame.K_q:
                        self.score+=600
                        self.life=0
            screen.blit(self.background,(0,0))
            self.sprites.update(time)
            if self.gameover:
                gameovertext=self.fontlarge.render('Game Over', True, (0,0,0))
                screen.blit(gameovertext,(self.width/2-gameovertext.get_width()/2,self.height/2-gameovertext.get_height()/2))
                if self.gameovertimer>0.0:
                    self.gameovertimer-=time
                else:
                    for i in range(len(scoredat.hiscore)):
                        if self.score>scoredat.hiscore[i]:
                            self.newhiscore=1
                            for ii in range(len(scoredat.hiscore)-i):
                                iii=9-ii
                                scoredat.hiscore[iii]=scoredat.hiscore[iii-1]
                                scoredat.hiscorename[iii]=scoredat.hiscorename[iii-1]
                            scoredat.hiscore[i]=self.score
                            scoredat.hiscorename[i]='_'
                            scoredat.rank=i
                            menu.menu[0].selected=1
                            break
                    break
            self.sprites.draw(screen)
            if self.leveltimer>0.0:
                self.announcelevel(self.clock.tick(60),screen)
                self.levelstart=0

            elif self.levelstart==0:
                self.spawn()
                self.levelstart=1
            if len(self.asteroids)==0 and self.levelstart!=0:
                self.leveltimer=500.0
                self.level+=1
            screen.blit(self.scoretext,(gameinit.width-20-self.scoretext.get_width(),10))
            scoredisplay=self.font.render(str(self.score),True,(0,0,0))
            for i in range(self.life):
                screen.blit(self.lifeimg,(15+20*i,20))
            screen.blit(scoredisplay,(gameinit.width-20-scoredisplay.get_width(),30))
            pygame.display.flip()

class Menu(pygame.sprite.Sprite):
    def __init__(self,number,text,*groups):
        super(Menu,self).__init__(*groups)
        self.selected=0
        self.menutext=text
        self.pos=number
        self.rect=pygame.rect.Rect(0,0,0,0)
    def highlight(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    def select(self):
        self.selected=1
    def unselect(self):
        self.selected=0
    def choose(self, screen):
        if self.menutext=='New Game':
            gameinit.main(screen)
        if self.menutext=='Hi-Score':
            menu.menuopen='score'
        if self.menutext=='Exit':
            pygame.quit()
            sys.exit()
    def update(self,time):    
        if self.selected==1:
            text='>'+self.menutext+'<'
        else:
            text=self.menutext
        self.image=menu.fontsmall.render(text,True,(0,0,0))
        self.rect=pygame.rect.Rect((gameinit.width/2-self.image.get_width()/2,80+20*self.pos+gameinit.height*2/3),self.image.get_size())
class MainMenu(object):
    running=0
    menuopen='main'    
    def main(self, screen):
        self.menu={}
        self.running=1
        self.sprites=pygame.sprite.Group()
        self.menus=pygame.sprite.Group()
        self.background=pygame.surface.Surface((gameinit.width,gameinit.height))
        self.background.fill((255,255,255))
        self.clock=pygame.time.Clock()
        self.fontverysmall=pygame.font.Font('FreeMono.ttf',14)
        self.fontsmall=pygame.font.Font('FreeMono.ttf',20)
        self.fontlarge=pygame.font.Font('FreeMono.ttf',50)
        self.title=self.fontlarge.render('Asteroids',True,(0,0,0))
        self.menulist=['New Game','Hi-Score','Exit']
        for i in range(len(self.menulist)):
            self.menu[i]=Menu(i,self.menulist[i],self.menus)   
        self.menu[0].selected=1
        for i in range(0,5):
            angle=0
            Asteroid((random.randrange(gameinit.width),random.randrange(gameinit.height)),3,random.randrange(360)+1,self.sprites)
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=0
                if event.type==pygame.KEYDOWN:
                    if self.menuopen=='main':
                        if event.key==pygame.K_RETURN or event.key==pygame.K_SPACE:
                            for i in self.menu.keys():
                                if self.menu[i].selected==1:
                                    self.menu[i].choose(screen)
                                    break
                            break
                        if event.key==pygame.K_DOWN:
                            for i in self.menu.keys():
                                if self.menu[i].selected==1:
                                    print self.menu[i]
                                    if i+1 in self.menu.keys():
                                        self.menu[i].unselect()
                                        self.menu[i+1].select()
                                        break
                                    elif i-1 in self.menu.keys():
                                        self.menu[i].unselect()
                                        self.menu[i-1].select()
                                        break
                        if event.key==pygame.K_UP:
                            for i in self.menu.keys():
                                if self.menu[i].selected==1:
                                    if i-1 in self.menu.keys():
                                        self.menu[i].unselect()
                                        self.menu[i-1].select()
                                        break
                                    elif i+1 in self.menu.keys():
                                        self.menu[i].unselect()
                                        self.menu[i+1].select()
                                        break
                    if self.menuopen=='score':
                        if not gameinit.newhiscore:
                            if event.key==pygame.K_RETURN or event.key==pygame.K_SPACE or event.key==pygame.K_ESCAPE:
                                self.menuopen='main'
                        else:
                            letter=event.unicode
                            if letter.isalnum():
                                scoredat.hiscorename[scoredat.rank]=scoredat.hiscorename[scoredat.rank][:-1]+letter+'_'
                            elif event.key==pygame.K_BACKSPACE:
                                scoredat.hiscorename[scoredat.rank]=scoredat.hiscorename[scoredat.rank][:-2]+'_'
                            elif event.key==pygame.K_RETURN:
                                scoredat.hiscorename[scoredat.rank]=scoredat.hiscorename[scoredat.rank][:-1]
                                file=open('score.dat','w+')
                                pickle.dump(scoredat,file,pickle.HIGHEST_PROTOCOL)
                                file.close()
                                gameinit.newhiscore=0
                            
            if self.menuopen!='score' and gameinit.newhiscore:
                self.menuopen='score'
            self.sprites.update(self.clock.tick(60))
            if self.menuopen=='main':
                for i in self.menu.keys():
                    if self.menu[i].highlight():
                        self.menu[i].selected=1
                        for ii in self.menu.keys():
                            if ii!=i:
                                self.menu[ii].selected=0
                        if pygame.mouse.get_pressed()[0]==1:
                            self.menu[i].choose(screen)
                self.menus.update(self.clock.tick(60))
            screen.blit(self.background,(0,0))
            self.sprites.draw(screen)
            self.credits=self.fontverysmall.render('Made by Jun wei Zhu 2012',True,(0,0,0))
            screen.blit(self.credits,(screen.get_width()-16-self.credits.get_width(),screen.get_height()-16-self.credits.get_height()))
            if self.menuopen=='main':
                self.menus.draw(screen)
                screen.blit(self.title,(gameinit.width/2-self.title.get_width()/2,gameinit.height/4))
            if self.menuopen=='score':
                scoretitle=['Rank','Name','Hi-Score']
                scoretitletext=self.fontsmall.render(scoretitle[0],True,(0,0,0))
                screen.blit(scoretitletext,(100-scoretitletext.get_width(),148))
                scoretitletext=self.fontsmall.render(scoretitle[1],True,(0,0,0))
                screen.blit(scoretitletext,(128,148))
                scoretitletext=self.fontsmall.render(scoretitle[2],True,(0,0,0))
                screen.blit(scoretitletext,(gameinit.width-128-scoretitletext.get_width(),148))
                scoretitletext=self.fontlarge.render(scoretitle[2],True,(0,0,0))
                screen.blit(scoretitletext,(gameinit.width/2-scoretitletext.get_width()/2,120-scoretitletext.get_height()/2))
                for i in range(len(scoredat.hiscore)):
                    scorenumber=self.fontsmall.render(str(i+1)+'  ', True, (0,0,0))
                    scorename=self.fontsmall.render(scoredat.hiscorename[i],True,(0,0,0))
                    scorescore=self.fontsmall.render(str(scoredat.hiscore[i]),True,(0,0,0))
                    screen.blit(scorenumber,(128-scorenumber.get_width(),176+28*i))
                    screen.blit(scorename,(128,176+28*i))
                    screen.blit(scorescore,(gameinit.width-128-scorescore.get_width(),176+28*i))
            pygame.display.flip()
if __name__=="__main__":
    pygame.init()
    pygame.display.set_caption("Jun's asteroids")
    gameinit=Game()
    try:
        file=open('score.dat','r+')
        scoredat=pickle.load(file)
        file.close()
    except:
        scoredat=DataHandler()
        scoredat.defaultscore()
        file=open('score.dat','w+')
        pickle.dump(scoredat,file,pickle.HIGHEST_PROTOCOL)
        file.close()
    gameinit.width,gameinit.height=800,600
    screen=pygame.display.set_mode((gameinit.width,gameinit.height))
    menu=MainMenu()

    menu.main(screen)