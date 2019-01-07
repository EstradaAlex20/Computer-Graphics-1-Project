from ctypes import *
from sdl2 import *
from sdl2.keycode import *
from gl import *
from glconstants import *
import array
from Buffer import *
from Program import *
import random
import math
import traceback
from sdl2.sdlmixer import *
import os.path
from math3d import *
from Bullet import *
from Texture import *
from Sampler import *
from Ship import *
from Enemy import *
from Image import *
from Text import *
from Camera import *
from PowerUp import *
from Mesh import *
from Asteroid import *

bulletList = []
enemyList = []
enemyList1 = []
powerup_list = []
asteroid_list = []
fade = False
red = 0.0
green = 0.0
blue = 0.0
amountOfPointsOnShape = 10
keys = set()
speed = 0.01
bulletSpeed = 0.0005
enemySpeed = 0.0005
addedMS = 0
frames = 0
frames1 = 0

def squaredDistance(x1, y1, x2, y2):
    return (x1-x2)**2 + (y1-y2)**2

def setup():
    global starAmount
    global starsVao
    global quadProg
    global StarProgram
    global ShipProg
    global beep
    global enemyProg
    global enemy1Prog
    global backgroundProg
    global main_program
    global monster_program
    global ship
    global fire
    global enemy
    global enemy1
    global nebula
    global powerup
    global powerup1
    global cam
    global monster
    global starList
    global bullet1
    global myShip
    global skyboxProg
    global skybox
    global skyboxTexture

    beep = Mix_LoadWAV(os.path.join("assets","Beep-09.ogg").encode())

    glEnable(GL_MULTISAMPLE)
    glClearColor(0.0,0.0,0.0,1.0)

    starAmount = 50
    starList = []
    star_points = []
    for i in range(starAmount):
        starList.append(Star())

    for i in range(len(starList)):
        star_points.append(starList[i].x)
        star_points.append(starList[i].y)

    A = array.array("f", star_points)
    b = Buffer(A)
    tmp = array.array("I", [0])
    glGenVertexArrays(1, tmp)
    starsVao = tmp[0]
    glBindVertexArray(starsVao)
    b.bind(GL_ARRAY_BUFFER)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, False, 2*4, 0)
    glBindVertexArray(0)

    myShip = Ship()

    cam = Camera(myShip.pos, myShip.up, myShip.facing)

    for i in range(3):
        asteroid_list.append(Asteroid(vec4(0,0,0,0)))



    skyboxTexture = ImageTextureCube("nebula-%04d.jpg")
    skybox = Mesh("cube.obj.mesh")
    skybox.materials[0].tex = skyboxTexture



    skyboxProg = Program("skyboxVertexShader.txt", "skyboxFragmentShader.txt")
    StarProgram = Program("StarsVertexShader.txt", "StarsFragmentShader.txt")
    main_program = Program("MainVS.txt", "MainFS.txt")

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    Program.setUniform("lightPos", vec3(0,1,-1) + myShip.pos.xyz) #vec3(0,1,-1)
    Program.updateUniforms()


    print("Setup Done")



def update(updateMesc):
    global fade
    global red
    global speed
    global bulletSpeed
    global enemySpeed
    global addedMS
    global frames
    global frames1
    global myText

    myShip.angle = 0

    if fade:
        red += 0.01
        myText.setText(vec2(0,0), str(red)[0:4])

    else:
        red = 0.0
        myText.setText(vec2(0,0), str(red)[0:4])

    ev = SDL_Event()
    addedMS += updateMesc
    if addedMS >= 250:
        addedMS = 0
        frames += 1
        frames1 += 1

    for i in asteroid_list:
        i.update(updateMesc)

    Program.setUniform("lightPos", myShip.up.xyz + myShip.pos.xyz) #vec3(0, 1, -1
    Program.updateUniforms()

    i = 0
    while(i < len(bulletList)):
        bulletList[i].update(updateMesc, myShip)
        if bulletList[i].lifetime <= 0:
            x = bulletList.pop()
            if i < len(bulletList):
                bulletList[i] = x
        else:
            i += 1

    if 119 in keys:
        # W Pressed
        myShip.pitch(-0.01)

    if 97 in keys:
        # a Pressed
        myShip.turn(0.01)

    if 115 in keys:
        # s Pressed
        myShip.pitch(0.01)

    if 100 in keys:
        # d Pressed
        myShip.turn(-0.01)

    if 13 in keys:
        #Enter Pressed, turbo mode
        myShip.x += speed * 4

    if 88 in keys:
        fade = False
        bulletList.append(Bullet(myShip))
        if Mix_PlayChannel(-1, beep, 0) < 0:
            print(Mix_GetError())


    while 1:
        if not SDL_PollEvent(byref(ev)):
            break
        if ev.type == SDL_QUIT:
            SDL_Quit()
            sys.exit(0)
        elif ev.type == SDL_KEYDOWN:
            k = ev.key.keysym.sym
            keys.add(k)
            if k == 32:
                fade = True
            if k == SDLK_q:
                SDL_Quit()
                sys.exit(0)
        elif ev.type == SDL_KEYUP:
            k = ev.key.keysym.sym
            keys.discard(k)
            if k == 32:
                fade = False
                bulletList.append(Bullet(myShip))
                if Mix_PlayChannel(-1, beep, 0) < 0:
                    print(Mix_GetError())
    myShip.update(updateMesc)
    cam.lookAt(myShip.pos, myShip.up, myShip.pos + myShip.facing+myShip.up*0.5) # coi, up, eye

def draw():
    global frames
    global frames1
    global enemy
    Program.setUniform("frames1", frames1%8)
    Program.setUniform("frames", frames%4)
    cam.setUniforms()
    Program.updateUniforms()
    glClearColor(red, green, blue, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)

    StarProgram.use()
    glBindVertexArray(starsVao)
    for i in range(len(starList)):
        Program.setUniform("worldMatrix", starList[i].worldMatrix)
        Program.updateUniforms()
        glDrawArrays(GL_POINTS, 0, starAmount)

    ###Drawing the bulets
    main_program.use()
    for i in range(len(bulletList)):
        bulletList[i].draw()

    Program.setUniform("enemyAlpha", 1)
    for i in range(len(asteroid_list)):
        asteroid_list[i].draw()

    myShip.draw()

    skyboxProg.use()
    skyboxTexture.bind(3)
    skybox.draw(myShip.worldView)

    Text.prog.use()
    glBindVertexArray(myText.vao)
    myText.samp.bind(0)
    myText.tex.bind(0)

def debugCallback( source, msgType, msgId, severity, length, message, param ):
    print(msgId,":",message)
    if severity == GL_DEBUG_SEVERITY_HIGH:
        for x in traceback.format_stack():
            print(x,end="")

def main():
    global red
    global green
    global blue
    global fade
    global myText

    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO)
    TTF_Init()
    Mix_Init(MIX_INIT_OGG | MIX_INIT_MP3)
    Mix_OpenAudio(22050, MIX_DEFAULT_FORMAT, 1, 4096)

    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
    SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION,4)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION,3)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS,SDL_GL_CONTEXT_DEBUG_FLAG)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS,1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES,4)
    
    win = SDL_CreateWindow( b"ETGG",20,20, 512,512, SDL_WINDOW_OPENGL)
    if not win: 
        print("Could not create window")
        return

    rc = SDL_GL_CreateContext(win)
    if not rc:
        print("Cannot create GL context")
        raise RuntimeError()

    glDebugMessageCallback(debugCallback, None)
    # Source, type, severity, count, ids, enabled
    glDebugMessageControl(GL_DONT_CARE, GL_DONT_CARE, GL_DONT_CARE,
                          0, None, True)
    glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS)
    glEnable(GL_DEBUG_OUTPUT)

    setup()

    MSEC_PER_FRAME = 16
    TICKS_PER_FRAME = int(SDL_GetPerformanceFrequency() * MSEC_PER_FRAME / 1000)
    last = SDL_GetPerformanceCounter()
    ticksPerSecond = SDL_GetPerformanceFrequency()
    targetRate = 16/1000*ticksPerSecond #in ticks
    update_Msec = 5
    accumlated_Update = 0


    Program.setUniform("screenSize", vec4(512,512,1/512,1/512))
    Program.updateUniforms()


    myText = Text("Charmonman-Regular.ttf", 100)
    myText.setText(vec2(100,200), "YEET")

    while 1:

        now = SDL_GetPerformanceCounter()
        elapsedTicks = now-last
        last = now
        elapsedMsec = int(elapsedTicks/ticksPerSecond * 1000)
        accumlated_Update +=  elapsedMsec
        while accumlated_Update >= update_Msec:
            update(update_Msec) #update(elapsedMsec)
            accumlated_Update -= update_Msec
        draw()
        SDL_GL_SwapWindow(win)
        tmp = SDL_GetPerformanceCounter()
        T = tmp - now
        leftoverT = targetRate-T
        if leftoverT > 0:
            SDL_Delay(int((leftoverT/ticksPerSecond)*1000))

main()
