import pika
import uuid
import json
from threading import Thread
import pygame
import time
import random
from pygame import mixer
from enum import Enum
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Tanks')


clock = pygame.time.Clock()
form1 = pygame.font.SysFont(None, 30)
text1 = form1.render(":Lives", 1, (255, 17, 0))
form2 = pygame.font.SysFont(None, 30)
text2 = form2.render(":Lives", 1, (100, 150, 250 ))
sound1=r'C:\Users\Аида\Documents\python\tanksgame\start.wav'
pygame.mixer.music.load(sound1)
pygame.mixer.music.play(-1)
sound2=r'C:\Users\Аида\Documents\python\tanksgame\boom.wav'
sound3=r'C:\Users\Аида\Documents\python\tanksgame\bullet.wav'
Walls=[]
def message_to_screen(msg, color, y_displace=0):
    textSurf, textRect = text_objects(msg, color)
    textRect.center = (int(screen_width / 2), int(screen_height / 2) + y_displace)
    screen.blit(textSurf, textRect)

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
   
class Bullet:

    def __init__(self, bx, by, bcolor, bspeed):
        self.bx = bx
        self.by = by
        self.bxspeed = bspeed
        self.byspeed = bspeed
        self.bcolor = bcolor
        self.run = False
        self.r = 5

    def draw(self):
        pygame.draw.circle(screen, self.bcolor, (self.bx, self.by), self.r)
        
  
    def shoot(self):
        if a.direction == Direction.RIGHT:
            self.bx = a.x + 50
            self.by = a.y + 10
            self.bxspeed = 10
            self.byspeed = 0
            self.run = True
                
        if a.direction == Direction.LEFT:
            self.bx = a.x - 20
            self.by = a.y + 20
            self.bxspeed = -10
            self.byspeed = 0
            self.run = True
                
        if a.direction == Direction.UP:
            self.bx = a.x + 20
            self.by = a.y - 20
            self.bxspeed = 0
            self.byspeed = -10
            self.run = True
                
        if a.direction == Direction.DOWN:
            self.bx = a.x + 10
            self.by = a.y + 50
            self.bxspeed = 0
            self.byspeed = 10
            self.run = True
        
    def hit(self):

        if (-45<=(a.x - self.bx)<= 10) and (-45<=(a.y-self.by)<= 45):    
            self.run = False
            a.score -= 1
            pygame.mixer.Sound(sound2).play()
            

        elif (-45<=(a.x - self.bx)<= 10) and (-45<=(a.y-self.by)<= 10):
            self.run = False
            a.score -= 1
            pygame.mixer.Sound(sound2).play()
 
        elif (-45<=(a.x - self.bx)<= 10) and (-10<=(a.y-self.by)<= 45):
            self.run = False
            a.score -= 1
            pygame.mixer.Sound(sound2).play()

        elif (-45<=(a.x - self.bx)<= 10) and (-45<=(a.y-self.by)<= 10):
            self.run = False
            a.score -= 1
            pygame.mixer.Sound(sound2).play()

        elif self.bx > 800 or self.bx < 0 or self.by <0 or self.by > 600:
            self.run = False


bullet1 = Bullet(850, 800, (193, 0, 32), 10)
bullet2 = Bullet(850, 800, (193, 0, 32), 10)
bullets = [bullet1, bullet2]

class Tank:
    global score
    def __init__(self, x, y, speed, color, score, d_right = pygame.K_RIGHT, d_left = pygame.K_LEFT, d_up = pygame.K_UP, d_down = pygame.K_DOWN):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = 45
        self.direction = Direction.RIGHT
        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT, d_up: Direction.UP, d_down: Direction.DOWN} 
        self.score = score

    def draw(self):
        tank_c = (self.x + int(self.width/2), self.y + int(self.width/2))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width), 2)
        pygame.draw.circle(screen, self.color, tank_c, int(self.width/2))

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width + int(self.width/2), self.y + int(self.width/2)), 4)
        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (self.x - int(self.width/2), self.y + int(self.width/2)), 4)
        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width/2), self.y - int(self.width/2)), 4)
        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width/2), self.y + self.width + int(self.width/2)), 4)


                        

    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed
        if self.x > 700:
            self.x = 0
        if self.x < 0:
            self.x = 670
        if self.y < 0:
            self.y = 600
        if self.y > 600:
            self.y = 0
        self.draw()
        

FPS = 30
mainloop = True
tank1 = Tank(200, 200, 2, (255, 17, 0), 3)
tank2 = Tank(100, 100, 2, (100, 150, 250), 3, pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
n = [tank1, tank2]


while mainloop:
    mill = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            
            if event.key in tank1.KEY.keys():
                tank1.change_direction(tank1.KEY[event.key])
            if event.key in tank2.KEY.keys():
                tank2.change_direction(tank2.KEY[event.key])
        
            
    screen.fill((0, 0, 0))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and not bullet2.run:
            a = n[1]
            bullet2.shoot()
            pygame.mixer.Sound(sound3).play()
        if event.key == pygame.K_RETURN and not bullet1.run:
            a = n[0]
            bullet1.shoot()
            pygame.mixer.Sound(sound3).play()
            
    if bullet1.run == True:
        bullet1.bx += bullet1.bxspeed
        bullet1.by += bullet1.byspeed
        bullet1.draw()
        a = n[1]
        bullet1.hit()
        pygame.mixer.Sound(sound3).play()
        
        
    if bullet2.run == True:
        bullet2.bx += bullet2.bxspeed
        bullet2.by += bullet2.byspeed
        bullet2.draw()
        a = n[0]
        bullet2.hit()
        pygame.mixer.Sound(sound3).play()
        
    Size1 = pygame.font.SysFont(None, 30)
    score1 = form1.render(str(tank1.score), 1, (255, 17, 0))
    Size2 = pygame.font.SysFont(None, 30)
    score2 = form2.render(str(tank2.score), 1, (100, 150, 250))
    if tank1.score==0: 
        mainloop=False
    elif tank2.score==0:
        mainloop= False


    tank1.move()
    tank2.move()
    
    
    screen.blit(text1, (110, 550))
    screen.blit(text2, (700, 550))
    screen.blit(score1, (90, 550))
    screen.blit(score2, (680, 550))
    pygame.display.flip()
#pygame.init()
#screen_width = 800
#screen_height = 600
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Tanks')
black=(0,0,0)
wheat=(245,222,179)

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0,0,255)

red = (200, 0, 0)
light_red = (255, 0, 0)

yellow = (200, 200, 0)
light_yellow = (255, 255, 0)

green = (34, 177, 76)
light_green = (0, 255, 0)
Wall=[]
Bullet=[]


class Button:
    def __init__(self, x, y, width, height,func):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.func = func
  
            
    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
        pressed=pygame.key.get_pressed()
        screen=pygame.display.set_mode((800,600))
        screen.fill((0,0,0))
        form = pygame.font.Font(None , 48)
        text = form.render('Welcome to tanks', True, (255,255, 0))
        place = text.get_rect(center = (200,100))
        
        screen.blit(text, place)
        form1 = pygame.font.SysFont(None, 48)
        text1 = form1.render('Single Player mode', True, (255, 255, 0))
        place1 = text1.get_rect(center=(400, 200))
        screen.blit(text1, place1)

        form2 = pygame.font.SysFont(None, 48)
        text2 = form2.render('Multiplayer mode', True, (255, 255, 0))
        place2 = text2.get_rect(center=(400, 300))
        screen.blit(text2, place2)

        form3 = pygame.font.SysFont(None, 48)
        text3 = form.render('Multiplayer AI mode', True, (255, 255, 0))
        place3 = text3.get_rect(center=(400, 400))
        screen.blit(text3, place3)
        if pressed[pygame.K_UP]:
                click_button-=1
        elif pressed[pygame.K_DOWN]:
                click_button+=1
        if pressed[pygame.K_RETURN]:
                screen.fill((0,0,0))
           
def click_button():
    click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()
    if pressed[pygame.K_UP]:
                click_button-=1
    elif pressed[pygame.K_DOWN]:
                click_button+=1
    if pressed[pygame.K_RETURN]:
                screen.fill((0,0,0))   
    
    print('OK')
    



def createWalls():
        if len(Walls)==0:
                Walls.append([random.randint(100,920),random.randint(100,720)])
        maxx=random.randint(8,15)
        while len(Walls)<maxx:
                x=random.randint(100,920)
                y=random.randint(100,720)
                for wall in Walls:
                        if x+80<wall[0] or x>wall[0]+80 :
                                Walls.append([x,y])
                                break
                        elif y+80<wall[1] or y>wall[1]+80:
                                Walls.append([x,y])
def drawWalls(Walls,screen):
        for wall in Walls:
                pygame.draw.rect(screen,(186,150,52) , pygame.Rect(wall[0],wall[1], 80, 80))



clock = pygame.time.Clock()


def score(score):
    text = smallfont.render("Score: " + str(score), True, white)
    screen.blit(text, [0, 0])




class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
   

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:

                    pygame.quit()
                    quit()
        screen.fill(black)
        
        


        screen.fill(black)
        message_to_screen("You won!", white, -100)
        

        button("play Again", 150, 500, 150, 50, wheat, light_green)
        
        
        pygame.display.update()

        clock.tick(15)

    def start_game(self, event):

        self.started = True


IP = '34.254.177.17'
PORT = '5672'
VHOST = 'dar-tanks'
USER = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'




class TankRpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=IP,
        port = PORT,
        virtual_host = VHOST,
        credentials = pika.PlainCredentials(
            username = USER,
            password = PASSWORD
        )))
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue = '',
                                           auto_delete = True,
                                           exclusive = True)
        self.callback_queue = queue.method.queue #очередь куда приходит ответ
        self.channel.queue_bind(
            exchange = 'X:routing.topic',
            queue =  self.callback_queue
        )

        self.channel.basic_consume( 
            queue = self.callback_queue,
            on_message_callback = self.on_response,
            auto_ack = True
        )

        self.response = None
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None
    def on_response(self, ch, method, props, body):#принимает данные
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            print(self.response)


    def call(self, key, message = {}): #отправляет запросы на сервер

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body = json.dumps(message)
        )
        while self.response is None:
            self.connection.process_data_events()
        
    def check_server_status(self): #запрос чтобы узнать статус сервера
        self.call('tank.request.healthcheck')
        return self.response['status'] == '200'

    def obtain_token(self, room_id): 
        message = {
            'roomId': room_id
        }
        self.call('tank.request.register',message)
        if 'token' in  self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']
            return True
        return False

    def turn_tank(self, token,direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

class TankConsumerClient(Thread):
    def __init__(self,room_id):
        super().__init__()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,
                port = PORT,
                virtual_host = VHOST,
                credentials = pika.PlainCredentials(
                    username = USER,
                    password = PASSWORD
        )))
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue = '',
                                           auto_delete = True,
                                           exclusive = True)
        event_listener = queue.method.queue
        self.channel.queue_bind(exchange = 'X:routing.topic',
                                queue = event_listener,
                                routing_key = 'event.state.'+ room_id)
        self.channel.basic_consume(
            queue = event_listener,
            on_message_callback= self.on_response,
            auto_ack = True
        )
        self.response = None
    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)

    def run(self):
        self.channel.start_consuming()
        
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

MOVE_KEYS = {
    pygame.K_w:UP,
    pygame.K_a:LEFT,
    pygame.K_s:DOWN,
    pygame.K_d:RIGHT
}

def draw_tank(x, y, width, height, direction,**kwargs):
    print(kwargs)
    tank_c = (x + int(width / 2), y + int(width / 2))
    pygame.draw.rect(screen, (255, 0, 0),
                    (x, y, width, width), 2)
    pygame.draw.circle(screen, (255, 0, 0),tank_c, int(width / 2))
    for x in state["gamefild"]['tanks']:
        color=(255,255,255)
        if x[id]==id:
            color=(0,0,0)
        pygame.draw()
def boom_bullet(self, token):
    messahe = {
        'token': token
    }
    self.call('tank.request.boom', message)
class Bullet:

    def __init__(self, bx, by, bcolor, bspeed):
        self.bx = bx
        self.by = by
        self.bxspeed = bspeed
        self.byspeed = bspeed
        self.bcolor = bcolor
        self.run = False
        self.r = 5

    def draw(self):
        pygame.draw.circle(screen, self.bcolor, (self.bx, self.by), self.r)

    def shoot(self):
        if a.direction == Direction.RIGHT:
            self.bx = a.x + 50
            self.by = a.y + 10
            self.bxspeed = 10
            self.byspeed = 0
            self.run = True
                
        if a.direction == Direction.LEFT:
            self.bx = a.x - 20
            self.by = a.y + 20
            self.bxspeed = -10
            self.byspeed = 0
            self.run = True
                
        if a.direction == Direction.UP:
            self.bx = a.x + 20
            self.by = a.y - 20
            self.bxspeed = 0
            self.byspeed = -10
            self.run = True
                
        if a.direction == Direction.DOWN:
            self.bx = a.x + 10
            self.by = a.y + 50
            self.bxspeed = 0
            self.byspeed = 10
            self.run = True

def game_start():
    mainloop = True
    font = pygame.font.Font('freesansbold.ttf', 32)
    button = Button(100,100,100,100,click_button)
    while mainloop:
        screen.fill((0, 0, 0))
        
        pos = pygame.mouse.get_pos()
        #print(pos)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                if event.key in MOVE_KEYS:
                    client.turn_tank(client.token, MOVE_KEYS[event.key])

            if event.type == pygame.MOUSEBUTTONDOWN:

                if button.x <= pos[0] <= button.x + button.width and button.y<= pos[1] <= button.y + button.height:
                    button.func()
        button.draw()
        try:            
            remaining_time = event_client.response['remainingTime']
            text = font.render('Remaining Time:{}'.format(remaining_time), True, (255,255,255))
            textRect = text.get_rect()
            textRect.center = (500, 100)
            screen.blit(text, textRect)
            hits = event_client.response['hits']
            bullets = event_client.response['gameField']['bullets']
            winners = event_client.response['winners']
            tanks = event_client.response['gameField']['tanks']
            for tank in tanks:
                # tank_x = tank['x']
                # tank_y = tank['y']
                # tank_width = tank['width']
                # tank_height = tank['height']
                # tank_direction = tank['direction']
                # draw_tank(tank_x, tank_y, tank_width, tank_height, tank_direction)
                draw_tank(**tank)
        except:
            pass
        pygame.display.flip()

    #client.connection.close()
    #pygame.quit()
def game_over():
    game_over = True

    while game_over:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(black)
        message_to_screen("Game Over", white, -100)
        message_to_screen("You loser", wheat, -30)

        button("Play Again", 150, 500, 150, 50, wheat)
        

        pygame.display.update()

        clock.tick(15)
def you_win():
    win = True

    while win:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(black)
        message_to_screen("You won!", white, -100)
        message_to_screen("Congratulations!", wheat, -30)

        button("play Again", 150, 500, 150, 50)
        

        pygame.display.update()

        clock.tick(15)
    client.connection.close()
    pygame.quit()
client = TankRpcClient()
client.check_server_status()
client.obtain_token('room-11')
event_client = TankConsumerClient('room-11')
event_client.start()
game_start()
drawWalls(Walls,screen)
game_intro()
game_over()
