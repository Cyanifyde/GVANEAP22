import pygame
import random
pygame.init()
pygame.display.set_caption('NEA')
screen = pygame.display.set_mode([0,0],pygame.FULLSCREEN) #pygame.FULLSCREEN is a flag that allows the game to be put into fullscreen mode
clock = pygame.time.Clock()
size=screen.get_size()
from threading import Thread
from queue import Queue
import time
import string
alphabet = list(string.ascii_lowercase)

class people_set: #a class to hold and controll the "person" class
    def __init__(self):
        self.people_list=[] #a list of all people in existance
        self.moveing_list=[] #a list of all people currently in motion
    def summon_person(self):# function to be called when a person is being created
        x=list(house_list.houses.keys())[random.randint(0,len(house_list.houses)-1)] # picks a random house for their initial house to be set at
        new_p=person(x,len(self.people_list)) #creates the person
        self.people_list.append(new_p) # adds that person to a list of people
    def move_person(self): # picks a random person in the list of all people and asign them a house to go to
        if len(self.people_list)>=1: # makes sure there is at least 1 person before chosing someone or it will throw errors
            num=random.randint(0,len(self.people_list)-1)
            persons=self.people_list[num]
            if persons not in self.moveing_list:
                self.moveing_list.append(persons)
                running=True
                while running==True: # makes sure the house for destination is not the same one as the current location
                    num=random.randint(0,len(house_list.houses)-1)
                    x=list(house_list.houses.keys())[num]
                    if x !=persons.loc:
                        persons.dest=x
                        running=False

class person: #person class for holding and controlling all neccessry code for them to function
    def __init__(self,loc,tag):
        self.loc=loc
        self.tag=tag
        self.house=loc
        self.dest=None
        self.infected=False 
        self.coords=[[-1,0],[0,-1],[0,1],[1,0]] # coordinates of all possible movement vectors
        self.home=False
    def dist(self,x,y): # gets the distance between 2 points
        return (x[0]-y[0])**2+(x[1]-y[1])**2
        
    def move(self): #gets the distance from the end to itself and sees what vector from self.coords would be more beneficial
        lowest_dist=self.dist(self.loc,self.dest)
        if lowest_dist==0:
            self.home=True
        lowest=self.loc

        for x in self.coords:
            new_loc=(self.loc[0]+x[0],self.loc[1]+x[1])
            out=self.dist(new_loc,self.dest)
            if out<=lowest_dist:
                lowest=new_loc
        self.loc=lowest

    def draw(self): #draws the circle on the screen
        pygame.draw.circle(screen, "orange", self.loc, 2, 0)

class keys: # a class to control all functions to update change and use keybinds
    def __init__(self):
        self.all_keys={
            "q":pygame.K_q,"w":pygame.K_w,"e":pygame.K_e,"r":pygame.K_r,
            "t":pygame.K_t,"y":pygame.K_y,"u":pygame.K_u,"i":pygame.K_i,
            "o":pygame.K_o,"p":pygame.K_p,"a":pygame.K_a,"s":pygame.K_s,
            "d":pygame.K_d,"f":pygame.K_f,"g":pygame.K_g,"h":pygame.K_h,
            "j":pygame.K_j,"k":pygame.K_k,"l":pygame.K_l,"z":pygame.K_z,
            "x":pygame.K_x,"c":pygame.K_c,"v":pygame.K_v,"b":pygame.K_b,
            "n":pygame.K_n,"m":pygame.K_m
        } # a dictionary to hold and compare all possible keyboard inputs I want
        self.default_keybinds={
            "save":["s",pygame.K_s],
            "summon_house":["q",pygame.K_q],
            "summon_person":["w",pygame.K_w],
            "interact":["i",pygame.K_i],
            "zoom_in":["b",pygame.K_EQUALS],
            "zoom_out":["v",pygame.K_MINUS],
            "increase_sim_speed":["q",pygame.K_h],
            "decrease_sim_speed":["g",pygame.K_g],
            "menu":["m",pygame.K_m],
            "camera_mode_change":["c",pygame.K_c],
            "pause":["p",pygame.K_p]
        } # a dictionary to hold all the default keybinds.
        self.get_keys_set() 
    def get_keys_set(self): # sets gets all currently used keybinds to self.current to be used
        self.current=[]
        for x in self.default_keybinds:
            self.current.append(self.default_keybinds[x][1])

key_group=keys()
gui_font = pygame.font.Font(None,30)# sets the UI font and size
class Button:# a class for holding all button related code and function
    # text : a string that will be displalyed on the screen
    # width : a number (int) that denotes the number of pixels wide the button must be
    # height : a number (int) that denotes the number of pixels high the button must be
    # x : a number (int) that denotes the number of pixels along the screen the button must be
    # y : a number (int) that denotes the number of pixels high the button must be
    # function : a passable reference to a function that can be activated by the code for when the button is pressed
    # arg : a variabe with no set type that can be used by the function above for various reasons
    # box : an bool used to controll whether the button will be rendered and interactable
    def __init__(self,text,width,height,x,y,function=None,box=True,arg=None): 

        if box==True:
            self.text_colour="#0A0908"
        else:
            self.text_colour="#FFFFFF"
        self.function=function 
        self.pressed = False # bool to say if the button is pressed
        self.pos=[x,y] # records where it is in the screen (from 0,0)
        self.rect = pygame.Rect([x,y],(width,height))  # creates a pygame rect object
        self.rect.center=[x,y]
        self.colour = '#40C9A2'
        self.text = text
        self.text_surface = gui_font.render(text,True,self.text_colour)
        self.text_rect = self.text_surface.get_rect(center = self.rect.center)
        self.box=box # a true or false to say whether the button will be rendered or not
        self.arg=arg # if some details need to be passed int the function, it is done here

    def change_text(self,text):# changes the text on the button
        self.text=text
        self.text_surface=gui_font.render(text,True,self.text_colour)
        self.text_rect = self.text_surface.get_rect(center = self.rect.center)

    def draw(self):#draws the button and the text and checks if the button is pressed
        if self.box==True:
            pygame.draw.rect(screen,self.colour, self.rect)
        screen.blit(self.text_surface, self.text_rect)
        if self.box!=True:
            self.check_click()

    def check_click(self):# cheks if the button is pressed, if it is it returns true and runs a functon
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.colour = '#e5f9e0' # actuve colour
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                return True
            else:
                if self.pressed == True:
                    self.pressed = False
                    self.function(self)
                return False
        else:
            self.colour = '#40C9A2' # non active colour
            return False

class scene_1_set: # scene 1 
    def __init__(self):
        self.buttons=[]
    def setup(self):
        self.buttons.append(Button('Simulation',200,40,screen.get_width()//2,screen.get_height()//2-150,box=False))
        self.buttons.append(Button('Keybinds',200,40,screen.get_width()//2,screen.get_height()//2-100,function=change_to_keybinds))
        self.buttons.append(Button('Settings',200,40,screen.get_width()//2,screen.get_height()//2-50,function=change_to_settings))
        self.buttons.append(Button('Start Simulation',200,40,screen.get_width()//2,screen.get_height()//2,function=change_to_game))
        self.buttons.append(Button('Quit',200,40,screen.get_width()//2,screen.get_height()//2+50,exit))
    def delete_self(self):
        for x in self.buttons:
            del x
        del self
    def update(self):
        for x in self.buttons:
            x.draw()

class scene_2_set:
    def __init__(self):
        self.buttons=[]
    def setup(self):
        #group 1
        x=screen.get_width()//4
        y=screen.get_height()//2-250
        for i in range(7):
            l=list(key_group.default_keybinds.keys())[i]
            y+=50
            self.buttons.append(Button(l,200,40,x,y,box=False))
        #group 2
        x=screen.get_width()//2-screen.get_width()//8
        y=screen.get_height()//2-250
        for i in range(7):
            l=list(key_group.default_keybinds.keys())[i]
            y+=50
            self.buttons.append(Button(key_group.default_keybinds[l][0],200,40,x,y,function=change_text,arg=l))
        #group 3
        x=screen.get_width()//2
        y=screen.get_height()//2-250
        for i in range(7,len(key_group.default_keybinds)):
            l=list(key_group.default_keybinds.keys())[i]
            y+=50
            self.buttons.append(Button(l,200,40,x,y,box=False))
        #group 4
        x=screen.get_width()//2+screen.get_width()//8
        y=screen.get_height()//2-250
        for i in range(7,len(key_group.default_keybinds)):
            l=list(key_group.default_keybinds.keys())[i]
            y+=50
            self.buttons.append(Button(key_group.default_keybinds[l][0],200,40,x,y,function=change_text,arg=l))
        x=screen.get_width()//2+screen.get_width()//4
        y=screen.get_height()//2-200
        self.buttons.append(Button("main menu",200,40,x,y,change_to_main))
    def delete_self(self):
        for x in self.buttons:
            del x
        del self
    def update(self):
        for x in self.buttons:
            x.draw()

class scene_3_set():

    def __init__(self):
        self.buttons=[]
    def setup(self):
        x=screen.get_width()//2+screen.get_width()//4
        y=screen.get_height()//2-200
        self.buttons.append(Button("main menu",200,40,x,y,function=change_to_main))
    def update(self):
        for x in self.buttons:
            x.draw()

class game_settings():
    def __init__(self):
        self.it=None

def get_keys(object):
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                text = event.unicode
                if text in alphabet:
                    object.change_text(text)
                    key_group.default_keybinds[object.arg]=[text,key_group.all_keys[text]]
                    key_group.get_keys_set()
                    running=False
        time.sleep(0.2)

def exit(arg):
    pygame.quit()

def change_to_keybinds(arg):
    global scenemain
    scenemain=False
    global scene
    scene=scene_2_set()
    scene.setup()

def change_to_main(arg):
    global scenemain
    scenemain=False
    global scene
    scene=scene_1_set()
    scene.setup()

def change_to_settings(arg):
    global scenemain
    scenemain=False
    global scene
    scene=scene_3_set()
    scene.setup()

def change_to_game(arg):
    global scenemain
    scenemain=True
    m=Thread(target=person_loop,daemon=True)
    m.start()


def change_text(item):
    item.change_text("please press a key")
    item.draw()
    m=Thread(target=get_keys(item))
    m.start()
    m.join()

scene=scene_1_set()
scene.setup()

class game:
    def __init__(self) -> None:
        objects=[]

class houses:
    def __init__(self) -> None:
        self.houses={}

    def create_house(self):
        m=Thread(target=check_m_col_house)
        m.start()
        m.join()
        if q1.get()==1:
            house_created=house()
            self.houses[house_created.loc]=house_created

    def draw(self):
        for x in self.houses:
            object=self.houses[x]
            pygame.draw.rect(screen,"blue",pygame.Rect(object.loc[0], object.loc[1], 5,5))

import random
class house:
    def __init__(self) -> None:
        
        self.loc=pygame.mouse.get_pos()
        self.tag=str(self.loc)
        self.object=pygame.Rect(self.loc,[5,5])

def check_m_col_house():
    loc=pygame.mouse.get_pos()
    found=False
    for x in house_list.houses:
        if loc[0]>=house_list.houses[x].loc[0]-5 and loc[0] <=house_list.houses[x].loc[0]+5:
            if loc[1] >=house_list.houses[x].loc[1]-5 and loc[1] <=house_list.houses[x].loc[1]+5:
                q1.put(house_list.houses[x])
                found=True
    
    if found==False:
        q1.put(1)

def check_clicks():
    for x in buttons_game.buttons_house:
        x.check_click()

def create_path():
    pass

q1=Queue()
selected=None
def delete_house(arg):
    try:
        del house_list.houses[selected.loc]
    except KeyError:
        pass
    
class game_buttons:
    def __init__(self) -> None:
        self.buttons_house=[]
        self.buttons_house.append(Button("delete",200,40,100,20,function=delete_house))
        self.buttons_house_draw=False
    def draw(self):
        if self.buttons_house_draw:
            for x in self.buttons_house:
                x.draw()


buttons_game=game_buttons()
house_list=houses()
scenemain=False
people_list=people_set()
def person_loop():
    running=True
    while running==True:
        time.sleep(0.001)
        if random.random()>0.001:
            people_list.move_person()
        for x in people_list.moveing_list:
            x.move()
            if x.home:
                people_list.moveing_list.remove(x)
                x.home=False

while 1:
    screen.fill("black")
    if scenemain:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key==key_group.default_keybinds["summon_house"][1]:
                    house_list.create_house()
                if event.key==key_group.default_keybinds["summon_person"][1]:
                    people_list.summon_person()
                if event.key==key_group.default_keybinds["camera_mode_change"][1]:
                    for x in range(300):
                        people_list.summon_person()
            if event.type == pygame.MOUSEBUTTONDOWN:
                loc=pygame.mouse.get_pos()
                m=Thread(target=check_m_col_house)
                m.start()
                m.join()
        m=Thread(target=check_clicks)
        m.start()
        m.join()
        try:
            q1_get=q1.get_nowait()
        except:
            q1_get=None
        if q1_get!=1 and q1_get:
            selected=q1_get
            buttons_game.buttons_house_draw=True
        elif q1_get==1:
            buttons_game.buttons_house_draw=False
        house_list.draw()  
        buttons_game.draw()         
        for x in people_list.moveing_list:
            x.draw() 
        pygame.display.update()
        clock.tick()

    else:
        scene.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        for x in scene.buttons:
            x.check_click()
        pygame.display.update()
        clock.tick()
