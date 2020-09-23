#========Import modules==============
import pygame
import random
import time
#=========Full screen settings=========
global fullscreen
fullscreen=False

def toggle_screen(display):
    global fullscreen    
    if pygame.display.get_driver()=='x11':
        pygame.display.toggle_fullscreen()
    else:
        acopy=game_display.copy()                    
        if fullscreen:
            pygame.display.set_mode(display)
            fullscreen=False
        else:
            pygame.display.set_mode(display, pygame.FULLSCREEN)
            fullscreen= True
            game_display.blit(acopy, (0,0))                    
            pygame.display.update()

#=========Get pygame started===========
pygame.init()
#============Set global variables====
global figurinhas, repetidas, página_atual, pacotinhos, pos_figurinhas, pos_repetidas,mostrar, folio, p_banca, background, pet, seta, seta_dir, set_esq, banca,pack, font, sub_font, figs, counter, switch, fat, x_pet, y_pet

#=======Open bios====================
bios=open('bios.txt',encoding='latin-1')
scientists=[i.split('|') for i in bios.readlines()]
bios.close()
#======Open questions================
quest=open('questions.txt',encoding='latin-1')
quest_lines=quest.readlines()
quest.close()
questões=[]
while len(quest_lines)>0:
    car=[]
    for i in range(6):
        car.append(quest_lines[0].replace('\n',''))
        del quest_lines[0]
    questões.append(car)
#==================================
figurinhas=[]
repetidas=[]
já_respondidas=[]
página_atual=1
pacotinhos=0
pos_figurinhas=0
pos_repetidas=0
erros=0
acertou=False
cl_troc=False
mostrar=[False for i in range(len(scientists))]
ok,always=True,False
selected=None


#============Set values==============
display_width=1024
display_height=768
pygame.display.set_caption('Bio Folio')
pygame.display.set_icon (pygame.image.load("icon.png"))
game_display=pygame.display.set_mode((display_width,display_height))
clock=pygame.time.Clock()
clock.tick(100)
white=(255,255,255)
black=(0,0,0)
#==========Load images and font==============
#pet=pygame.image.load('pet.png')
folio=pygame.image.load('projeto inicial.png')
p_banca=pygame.image.load('projeto banca.png')
background=pygame.image.load('universo.png')
pet=pygame.image.load('pet.png')
seta=pygame.image.load('seta.png')
seta_dir=pygame.transform.rotate(seta, -90)
seta_esq=pygame.transform.rotate(seta, 90)
pack=pygame.image.load('pacotinho.png')
banca=pygame.image.load('banca.png')
n_sel=pygame.image.load('n_sel.png')
sel=pygame.image.load('sel.png')
album=pygame.image.load('album.png')
conf=pygame.image.load('confirmar.png')
ball=pygame.image.load('balao.png')
trocar=pygame.image.load('trocar.png')

font=pygame.font.Font("FreeMono.ttf",25)
sub_font=pygame.font.Font('FreeMono.ttf',12)
sub_font2=pygame.font.Font('FreeMono.ttf',18)
figs=[pygame.image.load(str(i+1)+'.png') for i in range(len(scientists))]
#======Element at mouse's tip function=================
def we(dictionary):
    elemento_atual=None
    pressed=False
    if pygame.mouse.get_pressed()==(1,0,0): pressed=True
            
    x,y=pygame.mouse.get_pos()
    for elemento,coordenada in dictionary.items():
        if coordenada[0]<=x<=coordenada[1] and coordenada[2]<=y<=coordenada[3]:
            elemento_atual=elemento
            
    return(elemento_atual,pressed)    
#=========Text formating function===========
def blit_text(text, surface, pos, font=font, color=black, display=game_display):
    splited_lines=[line.split() for line in text.splitlines()]
    space=font.size(' ')[0]
    max_width, max_height = surface
    x, y = pos
    for splited_line in splited_lines:
        for word in splited_line:
            word_surface=font.render(word,0,color)
            word_width,word_height = word_surface.get_size()
            if x+word_width >= max_width:
                x=pos[0]
                y+=word_height
            display.blit(word_surface,(x,y))
            x+=word_width+space
        x=pos[0]
        y+=word_height
#=======RotateCenter===================
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
#=======Endereços===========================




def main():
    global figurinhas, repetidas, página_atual, pacotinhos, pos_figurinhas, pos_repetidas,mostrar, folio, p_banca, background, pet, seta, seta_dir, set_esq, banca,pack, font, sub_font, figs, counter, switch, fat, x_pet, y_pet, c
    endereços={
    'figurinhas':(30,30+137,50,50+181),
    'repetidas':(30,30+137,302,302+181),
    'pacotinhos':(31,31+137,552,552+181),
    'fig_esq':(25,25+20,244,244+20),
    'fig_dir':(50,50+20,244,244+20),
    'rep_esq':(25,25+20,496,496+20),
    'rep_dir':(50,50+20,496,496+20),
    'folio_esq':(289,289+20,365,365+20),
    'folio_dir':(900,900+20,365,365+20),
    'banca':(219,219+70,589,589+70),
    }

    
    #-----------------------------
    #Blit images------------------
    game_display.blit(folio,(0,0))
    if len(figurinhas)>0:
        game_display.blit(figs[figurinhas[pos_figurinhas]-1],(31,51))
    if len(repetidas)>0:
        game_display.blit(figs[repetidas[pos_repetidas]-1],(31,303))
    game_display.blit(seta_esq,(25,244))
    game_display.blit(seta_dir,(50,244))
    game_display.blit(seta_esq,(25,496))
    game_display.blit(seta_dir,(50,496))
    game_display.blit(seta_esq,(289,365))
    game_display.blit(seta_dir,(900,365))
    game_display.blit(banca,(219,589))
    if pacotinhos>0:
        game_display.blit(pack,(31,552))
    
    
    #Get events----------------------
##    for event in pygame.event.get():
##        if event.type==pygame.MOUSEMOTION:
##            print(pygame.mouse.get_pos())
            #print (we(endereços))
    #------Packs Mechanics--------------
    if we(endereços)==('fig_dir',True) and pos_figurinhas<len(figurinhas)-1:
        pos_figurinhas+=1
    elif we(endereços)==('rep_dir',True) and pos_repetidas<len(repetidas)-1:
        pos_repetidas+=1
    elif we(endereços)==('fig_esq',True) and pos_figurinhas>0:
        pos_figurinhas-=1
    elif we(endereços)==('rep_esq',True) and pos_repetidas>0:
        pos_repetidas-=1
    elif we(endereços)==('pacotinhos',True) and pacotinhos>0:
        pacotinhos-=1
        sorteada=random.randint(1,len(scientists))
        if sorteada not in figurinhas and mostrar[sorteada-1]==False :
            figurinhas.append(sorteada)
            figurinhas.reverse()
        else:
            repetidas.append(sorteada)
            repetidas.reverse()
    elif we(endereços)==('folio_esq',True) and página_atual>1:
        página_atual-=1
    elif we(endereços)==('folio_dir',True) and página_atual<len(scientists):
        página_atual+=1


    
    if len(figurinhas)!=0:
        blit_text(str(pos_figurinhas+1)+'/'+str(len(figurinhas)),(200,265),(75,240),color=white)
    else:
        blit_text(('0/0'),(200,265),(75,240),color=white)    
    if len(repetidas)!=0: 
        blit_text(str(pos_repetidas+1)+'/'+str(len(repetidas)),(200,265),(75,494),color=white)
    else:
        blit_text(('0/0'),(200,265),(75,494),color=white)

    blit_text(str(pacotinhos),(400,400),(181,708),color=white)
    #-------------------------------------------------
    screen_text=font.render(str(página_atual),True,white)
    text_rect=screen_text.get_rect()
    text_rect.center=600,440
    game_display.blit(screen_text,text_rect)
    #-------------------------------------------------

    if len(figurinhas)>0:
        if we(endereços)==('figurinhas',True) and figurinhas[pos_figurinhas]==página_atual:
            mostrar[figurinhas[pos_figurinhas]-1]=True
            del figurinhas[pos_figurinhas]

    for scientist in scientists:
        if mostrar[int(scientist[0])-1]==True and página_atual==int(scientist[0]):
            game_display.blit(figs[int(scientist[0])-1],(532,224))

            screen_text=font.render(scientist[1],True,black)
            text_rect=screen_text.get_rect()
            text_rect.center=600,500
            game_display.blit(screen_text,text_rect)
            blit_text(scientist[2],(815,754),(408,521))
    #--------------------------------------------------

    if we(endereços)==('banca',True):
        switch=1
#===============================================
def f_banca():
    endereços_2={
    'alt_1':(83,83+500,275+70*0,275+70*0+60),
    'alt_2':(83,83+500,275+70*1,275+70*1+60),
    'alt_3':(83,83+500,275+70*2,275+70*2+60),
    'alt_4':(83,83+500,275+70*3,275+70*3+60),
    'alt_5':(83,83+500,275+70*4,275+70*4+45),
    'album':(837,837+70,426,426+70),
    'confirmar':(344,344+100,607,607+60),
    'trocar':(837,837+70,336,336+70)
        }
    global já_respondidas, div, resto, cl_troc, x_pet,y_pet, fat, n_sel, sel, ok, n_sort, always, selected, album, switch, conf, erros, pacotinhos, ball, acertou, trocar, repetidas
    game_display.blit(p_banca,(0,0))
    game_display.blit(pet,(x_pet,y_pet))
    game_display.blit(album, (837,426))
    game_display.blit(conf,(344,607))
    game_display.blit(trocar,(837,336))
    
    y_pet+=fat*0.4
    if y_pet<0:
        y_pet=0
        fat*=-1
    elif y_pet>5:
        y_pet=5
        fat*=-1

    if we(endereços_2)==('trocar',True):
        cl_troc=True
        
        resto=len(repetidas)%5
        div=int(len(repetidas)/5)
        for i in range(len(repetidas)-resto):
            del repetidas[0]
        pacotinhos+=div
            

            
            

    for i in range(5):
        game_display.blit(n_sel,(83,275+70*i))

    if len(já_respondidas)==len(questões): já_respondidas=[]

    if ok==True:
        while True:
            n_sort=random.randint(0,len(questões)-1)
            if n_sort not in já_respondidas:
                já_respondidas.append(n_sort)
                ok=False
                break
    blit_text(questões[n_sort][0],(690,188),(67,51))
    for i in range(5):
         blit_text(questões[n_sort][i+1].replace('*',''),(697,392+70*i),(118,272+70*i))
         if we(endereços_2)==('alt_'+str(i+1),True):  selected=i
         if questões[n_sort][i+1].startswith('*'): correta=i

    for i in range(5):
        if selected==i: game_display.blit(sel,(83,275+70*i))

    if selected==correta: acertou=True
    else: acertou=False

    if we(endereços_2)==('album',True): switch=0

    if we(endereços_2)==('confirmar',True):
        if selected!=None:
            selected=None
            ok=True
            if acertou:
                pacotinhos+=1
                #c=0
                

            else:
                erros+=1
                if erros%2==0:
                    pacotinhos-=1


            
            
        
        
#=========Starting the loop============
counter=0
global setar,c,falhou
c=0
falhou=False
setar=False
switch=0
fat=1
x_pet,y_pet=700,0
while True:
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
                   
        if event.type==pygame.MOUSEMOTION:
            c+=1
            if c>=20:
                setar=False
                falhou=False
                cl_troc=False
            #print(pygame.mouse.get_pos())
            #print (we(endereços))

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                toggle_screen((display_width,display_height))
                
    counter+=0.1
    if counter==360: counter=0
    bg=rot_center(background,counter)
    game_display.blit(bg,(-128,-256))


    if switch==0:
        try:
            main()
        except:
            pass

    if switch==1:
        try:
            f_banca()
            if acertou and ok==True: setar=True
            if ok==True and not acertou: falhou=True 
            if setar==True:
                game_display.blit(ball,(780,119))
                blit_text('Parabéns! Você ganhou um pacotinho!',(790+126,200+122),(790,200),font=sub_font2)
            if falhou==True:
                game_display.blit(ball,(780,119))
                if erros%2!=0:
                    blit_text('Vish! Você errou!',(790+120,200+122),(790,200),font=sub_font2)
                else:
                    blit_text('Você errou duas vezes! Perdeu um pacotinho...',(790+120,200+122),(790,200),font=sub_font2)
            if cl_troc==True:
                game_display.blit(ball,(780,119))
                blit_text('Você trocou %d repetidas em %d pacotinhos.'%(div*5,div),(790+126,200+122),(790,200),font=sub_font2)
        except:
            pass
        
    pygame.display.update()
#=======Close pygame============
pygame.quit()
