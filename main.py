import random,pygame,os


game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,'img')
snd_folder = os.path.join(game_folder,'music')

WIDTH = 1200
HEIGHT = 700
FPS = 80

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


colors = [BLACK,WHITE,RED,GREEN,BLUE]


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('my game')
clock = pygame.time.Clock()

shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder,'pew.wav'))



explotions_music_options=[]
explotions_music_options.append(pygame.mixer.Sound(os.path.join(snd_folder,'expl6.wav')))
explotions_music_options.append(pygame.mixer.Sound(os.path.join(snd_folder,'expl3.wav')))



background = pygame.transform.smoothscale(pygame.image.load(os.path.join(img_folder,"starfield.png")).convert(), (WIDTH,HEIGHT))
background_rect = background.get_rect()

player_img = pygame.image.load(os.path.join(img_folder,'player.png')).convert()
player_img.set_colorkey(BLACK)
mini_player_img = pygame.transform.scale(player_img,(25,19))




bullet_images=[]
bullet_images.append(pygame.image.load(os.path.join(img_folder,'laserBlue16.png')).convert())
bullet_images.append(pygame.image.load(os.path.join(img_folder,'laserRED02.png')).convert())
bullet_images[0].set_colorkey(BLACK)
bullet_images[1].set_colorkey(BLACK)

explotions_anim={}
explotions_anim['lg'] = []
explotions_anim['sm'] = []
explotions_anim['player'] = []
for i in range(9):
	img = pygame.image.load(os.path.join(img_folder,'regularExplosion0{}.png'.format(i))).convert()
	img.set_colorkey(BLACK)
	explotions_anim['lg'].append(pygame.transform.scale(img,(75,75)))
	explotions_anim['sm'].append(pygame.transform.scale(img,(35,35)))
	img = pygame.image.load(os.path.join(img_folder,'sonicExplosion0{}.png'.format(i))).convert()
	img.set_colorkey(BLACK)
	explotions_anim['player'].append(img)



Ranking=[]
for i in range(12):
	img = pygame.image.load(os.path.join(img_folder,"rank0{:02}.png".format(i))).convert()
	img.set_colorkey(BLACK)
	Ranking.append(pygame.transform.scale(img,(32,32)))

Ranking_conditions = [1000,2000,4000,8000,16000,32000,64000,100000,250000,500000,1000000,5000000]

Ranking_upgrades ={}
Ranking_upgrades['n_bullets'] = [0,1,1,1,2,2,2,2,3,3,3,3]
Ranking_upgrades['bullet_speed'] = [0,10,10,11,12,13,14,15,16,17,18,20]
Ranking_upgrades['shooting_speed'] =   [0,7,8,9,10,11,12,13,14,15,16,17]
Ranking_upgrades['max_health'] = [0,100,110,115,125,130,140,150,160,170,220,300]


levels={}

levels['conditions'] = [0,50,100,200] 


levels['score_gain']     	= [0,25,50,100]
levels['bullet_speed']   	= [0,7,8,10]
levels['shooting_speed']  	= [0,0.5,1,3]
levels['speed_y']         	= [0,2,3,4]
levels['dir']         		= [0,5,5,6]
levels['lives']            	= [0,1,2,3] 
levels['image']          	= []

enemy_image = pygame.image.load(os.path.join(img_folder,'enemy_1.png')).convert()
levels['image'].append(pygame.transform.scale(enemy_image,(51,42)))
enemy_image = pygame.image.load(os.path.join(img_folder,'enemy_2.png')).convert()
levels['image'].append(pygame.transform.scale(enemy_image,(48,42)))
enemy_image = pygame.image.load(os.path.join(img_folder,'enemy_3.png')).convert()
levels['image'].append(pygame.transform.scale(enemy_image,(50,50)))


monster={}

monster['score_gain']     	= [0,250,500,1000]
monster['bullet_speed']   	= [0,7,8,10]
monster['shooting_speed']  	= [0,1,3,5]
monster['lives']            = [0,50,100,150]
monster['dir']         		= [0,6,6,8]
monster['n_bullets']     	= [0,3,5,7]
monster['image']=[]

for i in range(1,4):
	monster['image'].append(pygame.image.load(os.path.join(img_folder,'Monster_{}.png'.format(i))).convert())



power_up = {}
power_up['live']   = mini_player_img
power_up['shield'] = pygame.image.load(os.path.join(img_folder,'shield_gold.png')).convert()
power_up['shield'].set_colorkey(BLACK)

	


CUR_LEVEL = 1
score=0;

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf,x,y,health,max_health,color):
	health = max(health,0)
	rect = pygame.Rect(x,y,max_health,10)
	fill_rect = pygame.Rect(x,y,health,10)
	pygame.draw.rect(surf,color,fill_rect)
	pygame.draw.rect(surf,WHITE,rect,2)



def level_progress(surf,x,y,progress,max_progress):
	progress = int((progress/max_progress)*100)
	rect = pygame.Rect(x,y,100,10)
	fill_rect = pygame.Rect(x,y,progress,10)
	pygame.draw.rect(surf,GREEN,fill_rect)
	pygame.draw.rect(surf,WHITE,rect,2)





def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x - 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)



def show_go_screen(case='start'):
	screen.blit(background,background_rect)
	if case=='win':
		draw_text(screen,"Congratulation",50,WIDTH/2,HEIGHT/4)
		draw_text(screen,"You Won",50,WIDTH/2,HEIGHT/2)
		draw_text(screen,"Score : "+str(score),40,WIDTH/2,HEIGHT*3/4)
		draw_text(screen,"Press (S) to play again",15,WIDTH/2,HEIGHT-50)
	elif case=='game over':
		draw_text(screen,"GAME OVER",64,WIDTH/2,HEIGHT/4)
		draw_text(screen,"Score : "+str(score),40,WIDTH/2,HEIGHT/2)
		draw_text(screen, "Press (S) to Start", 18, WIDTH / 2, HEIGHT * 3 / 4)	
	else:
		draw_text(screen, "Space War", 64, WIDTH / 2, HEIGHT / 4)
		draw_text(screen, "Arrow keys move, Space to fire", 22,WIDTH / 2, HEIGHT / 2)
		draw_text(screen, "Press (S) to Start", 18, WIDTH / 2, HEIGHT * 3 / 4)

	pygame.display.flip()


	while 1:
		clock.tick(FPS)
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		if keys[pygame.K_s]:
			break;



class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,speed_y,Type=0,speed_x=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_images[Type]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y-10)
        self.speed_y = speed_y
        self.speed_x = speed_x

    def update(self):
        self.rect.y-=self.speed_y
        self.rect.x+=self.speed_x
        if(self.rect.top>=HEIGHT or self.rect.bottom<=0 or self.rect.right<=0 or self.rect.left >=WIDTH):
            self.kill()




class Pow(pygame.sprite.Sprite):
	def __init__(self,Type,center):
		pygame.sprite.Sprite.__init__(self)
		self.type = Type
		self.image = power_up[self.type]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speed = 2

	def update(self):
		self.rect.y +=self.speed
		if(self.rect.top>=HEIGHT):
			self.kill()



class Explotions(pygame.sprite.Sprite):
	def __init__(self,size,center):
		pygame.sprite.Sprite.__init__(self)
		self.size=size
		self.image = explotions_anim[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame=0
		self.last_update = pygame.time.get_ticks()
		self.update_rate = 50;

	def update(self):
		now = pygame.time.get_ticks()
		if(now - self.last_update > self.update_rate):
			self.last_update = now
			self.frame+=1
			if(self.frame == len(explotions_anim[self.size])):
				self.kill()
			else:
				self.image = explotions_anim[self.size][self.frame]
				center = self.rect.center
				self.rect = self.image.get_rect()
				self.rect.center = center



class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)        
		self.image = pygame.transform.scale(player_img,(56,38))
		#self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2,HEIGHT/2)
		self.rect.bottom = HEIGHT-10
		self.speed_x=0
		self.last_shoot=pygame.time.get_ticks()
		self.radius = 20;
		self.shooting_speed=5  # can be changed
		self.health=100
		self.max_health=100  # can be changed
		self.lives = 3;
		self.hide_timer=1000
		self.hidden = False
		self.rank=0
		self.bullet_speed=10 # can be changed
		self.n_bullets=1     # can be changed


	def shoot(self):
		now = pygame.time.get_ticks()
		if(now - self.last_shoot >=(1000/self.shooting_speed)):
			self.last_shoot = now    
			shoot_sound.play()
			if(self.n_bullets==1):
				b = Bullet(self.rect.center[0],self.rect.center[1],self.bullet_speed)
				bullets.add(b)
				all_sprites.add(b)
			elif(self.n_bullets==2):
				a = Bullet(self.rect.left,self.rect.center[1],self.bullet_speed)
				b = Bullet(self.rect.right,self.rect.center[1],self.bullet_speed)
				bullets.add(a);bullets.add(b)
				all_sprites.add(a);all_sprites.add(b)
			else:
				a = Bullet(self.rect.center[0],self.rect.center[1],self.bullet_speed)
				b = Bullet(self.rect.left,self.rect.center[1],self.bullet_speed)
				c = Bullet(self.rect.right,self.rect.center[1],self.bullet_speed)
				bullets.add(a);bullets.add(b);bullets.add(c)
				all_sprites.add(a);all_sprites.add(b);all_sprites.add(c)


	def update(self):


		if(Ranking_conditions[self.rank] <=score and self.rank<len(Ranking_conditions)-1):
			self.rank+=1
			self.n_bullets = Ranking_upgrades['n_bullets'][self.rank]
			self.bullet_speed = Ranking_upgrades['bullet_speed'][self.rank]
			self.max_health = Ranking_upgrades['max_health'][self.rank]
			self.shooting_speed = Ranking_upgrades['shooting_speed'][self.rank]



		if(self.hidden and pygame.time.get_ticks() - self.hide_timer >=1000):
			self.hidden=False
			self.rect.center = (WIDTH/2,HEIGHT-40)



		if(self.health<=0):
			self.health=self.max_health
			self.lives-=1
			expl = Explotions('player',self.rect.center)
			all_sprites.add(expl)
			self.hide()

		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT] and self.rect.left > 10:
			self.speed_x-=8
		if keystate[pygame.K_RIGHT] and self.rect.right<WIDTH-10:
			self.speed_x+=8

		if keystate[pygame.K_SPACE] :
			self.shoot()
		self.rect.x += self.speed_x



	def hide(self):
		self.hidden=True
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (WIDTH/2,HEIGHT+200)





class Mobs(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = levels['image'][CUR_LEVEL-1] # can be changed
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = -100
		self.dir = random.choice([-1,1]) * levels['dir'][CUR_LEVEL] # can be changed
		self.speed_y = levels['speed_y'][CUR_LEVEL] # can be changed
		self.radius = (self.rect.width*0.85)//2
		self.last_shoot=pygame.time.get_ticks()
		self.shooting_speed = levels['shooting_speed'][CUR_LEVEL] # can be changed
		self.bullet_speed = levels['bullet_speed'][CUR_LEVEL] # can be changed
		self.score_gain = levels['score_gain'][CUR_LEVEL] # can be changed
		self.lives = levels['lives'][CUR_LEVEL]
		self.max_height = random.choice([10,110,210])
		self.type=0



	def shoot(self):
		now = pygame.time.get_ticks()
		if(now - self.last_shoot >=(1000/self.shooting_speed)):
			b = Bullet(self.rect.center[0],self.rect.center[1],-self.bullet_speed,1)
			enemy_bullets.add(b)
			all_sprites.add(b)
			self.last_shoot = now  




	def update(self):
		self.rect.y+=self.speed_y
		self.rect.x +=self.dir
		if(self.rect.right>WIDTH or self.rect.left<0):self.dir*=-1
		if(self.rect.top>=self.max_height):
			self.speed_y = 0
		self.shoot();




class Monster(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = monster['image'][CUR_LEVEL-1] # can be changed
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = -500
		self.dir = random.choice([-1,1]) * monster['dir'][CUR_LEVEL] # can be changed
		self.speed_y = 10 # can be changed
		self.radius = (self.rect.width*0.85)//2
		self.last_shoot=pygame.time.get_ticks()
		self.shooting_speed = monster['shooting_speed'][CUR_LEVEL] # can be changed
		self.bullet_speed = monster['bullet_speed'][CUR_LEVEL] # can be changed
		self.score_gain = monster['score_gain'][CUR_LEVEL] # can be changed
		self.lives = monster['lives'][CUR_LEVEL]   # can be changed
		self.max_height = 50
		self.type=1
		self.n_bullets = monster['n_bullets'][CUR_LEVEL]




	def shoot(self):
		now = pygame.time.get_ticks()
		if(now - self.last_shoot >=(1000/self.shooting_speed)):
			for i in range(-(self.n_bullets//2),(self.n_bullets//2)+1):
				b = Bullet(self.rect.center[0],self.rect.center[1],-self.bullet_speed,1,i)
				enemy_bullets.add(b)
				all_sprites.add(b)
			self.last_shoot = now  




	def update(self):
		self.rect.y+=self.speed_y
		self.rect.x +=self.dir
		if(self.rect.right>WIDTH or self.rect.left<0):self.dir*=-1
		if(self.rect.top>=self.max_height):
			self.speed_y = 0
		self.shoot();






all_sprites = pygame.sprite.Group()

mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()


player = Player()
M = Monster()
all_sprites.add(player)



pygame.mixer.music.load(os.path.join(snd_folder,'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

score=0
DEAD=0



MONSTER_MODE = 0

RUNNING= True

game_case = 'start'

while RUNNING:

	if game_case!='running':
		show_go_screen(game_case)
		game_case = 'running'
		MONSTER_MODE=0;score=0;DEAD=0;CUR_LEVEL=1;
		all_sprites = pygame.sprite.Group()
		mobs = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		enemy_bullets = pygame.sprite.Group()
		powers = pygame.sprite.Group()
		player = Player()
		M = Monster()
		all_sprites.add(player)



	clock.tick(FPS)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			RUNNING=False

	if(player.lives==0 ):
		game_case = 'game over'

	all_sprites.update()



	if levels['conditions'][CUR_LEVEL] <= DEAD :
		DEAD=0
		for i in mobs:
			expl = Explotions('lg',i.rect.center)
			all_sprites.add(expl)
			i.kill()

		MONSTER_MODE = 1
		M = Monster()
		mobs.add(M)
		all_sprites.add(M)
		
	

	if(not MONSTER_MODE):
		for i in range(len(mobs),12):
			m = Mobs()
			mobs.add(m)
			all_sprites.add(m)


	player_and_mobs = pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
	mobs_and_bullets = pygame.sprite.groupcollide(mobs, bullets, False, True)
	player_and_bullets = pygame.sprite.spritecollide(player, enemy_bullets, True)
	player_and_powers = pygame.sprite.spritecollide(player, powers, True)


	for hit in  mobs_and_bullets:
		hit.lives-=1
		random.choice(explotions_music_options).play()
		if(hit.lives==0):
			if(hit.type==0):
				k = random.randrange(100)
				if(k>=95):
					p = Pow('shield',hit.rect.center)
					powers.add(p)
					all_sprites.add(p)
			
				score+= hit.score_gain
				expl = Explotions('lg',hit.rect.center)
				all_sprites.add(expl)
				hit.kill()
				DEAD+=1
			else:
				expl = Explotions('player',hit.rect.center)
				all_sprites.add(expl)
				hit.kill()
				score+= hit.score_gain
				p1 = Pow('shield',hit.rect.center)
				powers.add(p1)
				all_sprites.add(p1)
				p2 = Pow('shield',(hit.rect.x,hit.rect.y))
				powers.add(p2)
				all_sprites.add(p2)
				p3 = Pow('live',(hit.rect.x-hit.rect.width,hit.rect.y))
				powers.add(p3)
				all_sprites.add(p3)
				MONSTER_MODE=0
				if(CUR_LEVEL==3):
					game_case = 'win'
				else:
					CUR_LEVEL+=1



		else:
			expl = Explotions('sm',hit.rect.center)
			all_sprites.add(expl)
		


	for hit in  player_and_bullets :
		random.choice(explotions_music_options).play()
		player.health-=10
		expl = Explotions('sm',hit.rect.center)
		all_sprites.add(expl)



	for hit in player_and_mobs:
		random.choice(explotions_music_options).play()
		player.health-=20;
		expl = Explotions('lg',hit.rect.center)
		all_sprites.add(expl)


	for hit in player_and_powers:
		if(hit.type == "live"):
			player.lives+=1
		if(hit.type == 'shield'):
			player.health = min(player.max_health,player.health+50)



	screen.blit(background, background_rect)
	


	all_sprites.draw(screen)

	draw_text(screen, str(score), 18, WIDTH / 2, 10)
	draw_lives(screen,WIDTH / 2-10,30,1,Ranking[player.rank])     # draw lives
	draw_shield_bar(screen,5,5,player.health,player.max_health,GREEN)   # draw shield bar
	level_progress(screen,5,100,DEAD,levels['conditions'][CUR_LEVEL])   # draw level progress
	draw_lives(screen,WIDTH-40,20,player.lives,mini_player_img)   # drawing the rank

	if(MONSTER_MODE):
		draw_shield_bar(screen,5,50,M.lives*2,monster['lives'][CUR_LEVEL]*2,RED) # monster shield bar 
	
	pygame.display.flip()

pygame.quit()