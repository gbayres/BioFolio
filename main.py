############ Importing Modules ###############

import pygame, random, os
from functions import *
from time import sleep

#=========Get pygame started===========
pygame.init()
root = os.getcwd() #Set root path

#========= Starting mixer =============
pygame.mixer.init()
pygame.mixer.music.load(root + '/Resources/Songs/The Stork.mp3')
pygame.mixer.music.play(-1)

########### Loading elements ##############

#===============Load bios==================
descriptions = load_bios()
#============Load questions================
questions = load_questions()
#============Load stickers=================
cmp = load_components()
os.chdir('../Stickers')
figs = [pygame.image.load(str(i + 1)+'.png') for i in range(len(descriptions))]
os.chdir(root)

############# Declaring variables ###################

page = "album" #Current page of the application

new_stickers = [] #Sequence of new stickers
rep_stickers = [] #Sequence of repeated stickers
answered_questions = [] #List of questions that were already answered

new_sticker_position = 0 #Current position at 'new stickers' section
rep_sticker_position = 0 #Current position at 'repeated stickers' section
current_album_page = 1 
number_of_packs = 0

correct_selected = 0 #True if correct alternative is marked
clicked_trade = 0 #True if the user clicked 'trade'
show = [0 for i in range(len(descriptions))]
    #True for each sticker which must be shown

selected = -1 #Which alternative has been marked
confirmed = 1 #True if a new question must be set 
                    
missed = 0 #True if user missed
hit = 0 #True if user got it right
misses = 0 #Counting of misses
#NOTE: hit != not missed

#------- Doesn't need to load ------------
angle = 0 #Angle which background is blitted
cicles = 0 #Prevents balloons from disappearing instantly
pet_direction = 1 #Defines if the pet goes up or down
x_pet, y_pet = 700, 0 #Pet starting position

#-----------------------------------------

############# Defining save and load functions ################

def save_or_load(option='save'):
    global page, new_stickers, rep_stickers, answered_questions, \
           new_sticker_position, rep_sticker_position, current_album_page, \
           number_of_packs, correct_selected, clicked_trade, show, \
           selected, misses

    if option == 'save':
        
        with open(root + '/Data/save.txt', 'w') as f:
            for variable in [page, new_stickers, rep_stickers, answered_questions,
                             new_sticker_position, rep_sticker_position,
                             current_album_page, number_of_packs, correct_selected,
                             clicked_trade, show, selected, misses]:

                    to_write = variable

                    if isinstance(variable, bool):
                        to_write = int(to_write)

                    f.write(str(to_write) + '\n')

    elif option == 'load':

        with open(root + '/Data/save.txt') as f:
            l = [i.replace('\n','') for i in f.readlines()]

        page                 =         l[ 0]
        new_stickers         = to_list(l[ 1])
        rep_stickers         = to_list(l[ 2])
        answered_questions   = to_list(l[ 3])
        new_sticker_position =     int(l[ 4])
        rep_sticker_position =     int(l[ 5])
        current_album_page   =     int(l[ 6])
        number_of_packs      =     int(l[ 7])
        correct_selected     =     int(l[ 8])
        clicked_trade        =     int(l[ 9])
        show                 = to_list(l[10])
        selected             =     int(l[11])
        misses               =     int(l[12])

try:
    save_or_load('load')               
except:
    pass


############# Window-related variables ##############

display_width, display_height = (1024, 768)

pygame.display.set_caption('BioFolio')

pygame.display.set_icon(
    pygame.image.load(
        root + "/Resources/Components/icon.png"
        )
    )

game_display = pygame.display.set_mode(
    (
        display_width,
        display_height
        )
    )

#Setting clock
clock = pygame.time.Clock()
clock.tick(100)

#Defining colors
white = (255, 255, 255)
black = (  0,   0,   0)

##########################################################
'''                       Pages                     '''
##########################################################

def main_page():

    global new_stickers, rep_stickers, current_album_page, number_of_packs,\
           new_sticker_position, rep_sticker_position, show, \
           pack, figs, angle, page
    
    ########### Blits the components of the album page ############
    
    game_display.blit(
        cmp['projeto inicial'],
        (0, 0)
        )

    if new_stickers: 
        game_display.blit(
            figs[new_stickers[new_sticker_position] - 1],
            (31, 51)
            )
        
    if len(rep_stickers) > 0: 
        game_display.blit(
            figs[rep_stickers[rep_sticker_position] - 1],
            (31, 303)
            )

    [game_display.blit(*i) for i in origin_map(cmp, 0)]

    if number_of_packs > 0:
        game_display.blit(
            cmp['pacotinho'],
            (31, 552)
            )

    ############# Events regarding which component was clicked ##########

    #------ Wait a little ------
    if which_element(0)[1]:
        sleep(0.09)
    #---------------------------
        
    if which_element(0) == ('fig_dir', True) and \
       new_sticker_position < len(new_stickers) - 1:
            new_sticker_position += 1
            
    elif which_element(0) == ('rep_dir', True) and \
         rep_sticker_position < len(rep_stickers) - 1:
            rep_sticker_position += 1
            
    elif which_element(0) == ('fig_esq', True) and \
         new_sticker_position > 0:
            new_sticker_position -= 1
            
    elif which_element(0) == ('rep_esq', True) and \
         rep_sticker_position > 0:
            rep_sticker_position -= 1
            
    elif which_element(0) == ('pacotinhos', True) and \
         number_of_packs > 0:
            number_of_packs -= 1

            sorteada = random.randint(1, len(descriptions))
            if sorteada not in new_stickers and \
               show[sorteada - 1] == False:
                    new_stickers.append(sorteada)
                    new_stickers.reverse()
            else:
                    rep_stickers.append(sorteada)
                    rep_stickers.reverse()
                
    elif which_element(0) == ('folio_esq', True) and \
         current_album_page > 1:
            current_album_page -= 1
            
    elif which_element(0) == ('folio_dir', True) and \
         current_album_page < len(descriptions):
            current_album_page += 1


    #################### Blits number of new stickers #####################

    if len(new_stickers) != 0:
        blit_text(str(new_sticker_position + 1) + '/' + str(len(new_stickers)),
                  (200, 265),
                  ( 75, 240),
                  fnt(25),
                  game_display,
                  white)
    else:
        blit_text(('0/0'),
                  (200, 265),
                  ( 75, 240),
                  fnt(25),
                  game_display,
                  white)

    ################## Blits number of repeated stickers ##############

    if len(rep_stickers) != 0: 
        blit_text(str(rep_sticker_position + 1) + '/' + str(len(rep_stickers)),
                  (200, 265),
                  ( 75, 494),
                  fnt(25),
                  game_display,
                  white)
    else:
        blit_text(('0/0'),
                  (200, 265),
                  ( 75, 494),
                  fnt(25),
                  game_display,
                  white)

    ################# Blits number of sticker packs ###################
        
    blit_text(str(number_of_packs),
              (400, 400),
              (181, 708),
              fnt(25),
              game_display,
              white)
    
    ############### Blits current page of the album ##############
    
    screen_text = fnt(25).render(
        str(current_album_page), True, white
        )
    
    text_rect = screen_text.get_rect()
    text_rect.center = 600, 440
    game_display.blit(screen_text, text_rect)
    
    ########## Events after clicking on a sticker #################

    if new_stickers:
        if which_element(0) == ('figurinhas', True) \
           and new_stickers[new_sticker_position] == current_album_page:
                show[new_stickers[new_sticker_position] - 1] = 1
                del new_stickers[new_sticker_position]

    ########## Blits description of current sticker ###############

    for description in descriptions:
        if show[int(description[0]) - 1] == True \
           and current_album_page == int(description[0]):

                game_display.blit(
                    figs[int(description[0]) - 1],
                    (532, 224)
                    )

                screen_text = fnt(25).render(
                    description[1], True, black
                    )

                text_rect = screen_text.get_rect()
                text_rect.center = 600, 510
                game_display.blit(screen_text, text_rect)

                blit_text(description[2],
                          (815, 754),
                          (408, 525),
                          fnt(20),
                          game_display)
    
    ######### Change to newsstand if user clicks "album" button #########

    if which_element(0) == ('banca', True):
        page = "newsstand"

#####################################################################

def page_banca():
    
    '''Newsstand page'''

    global answered_questions, div, resto, clicked_trade, x_pet, y_pet, pet_direction,\
           n_sel, sel, confirmed, n_sort, selected, album, page, cicles, \
           conf, misses, number_of_packs, ball, correct_selected, rep_stickers

    ########## Blits basic elements of the screen ###################

    [game_display.blit(*i) for i in origin_map(cmp, 1)]

    #Blits pet
    game_display.blit(cmp['pet'], (x_pet, int(y_pet)))
    
    ######### Controls the movement of the pet ######################

    y_pet += pet_direction * 0.4

    if y_pet < 0:
        y_pet = 0
        pet_direction *= -1
        
    elif y_pet > 5:
        y_pet = 5
        pet_direction *= -1

    ######## Events after user clicks "trade" ########################

    if which_element(1) == ('trocar', True):
        clicked_trade = True
        resto = len(rep_stickers) % 5
        div = int(len(rep_stickers) / 5)
        for i in range(len(rep_stickers) - resto):
            del rep_stickers[0]
        number_of_packs += div

    ######## Blits unmarked radio buttons ############################        

    for i in range(5):
        game_display.blit(cmp['n_sel'],
                          (83, 275 + 70 * i))

    #### Resets the questions if all of them are already answered ####

    if len(answered_questions) == len(questions):
        answered_questions = []

    ##################### Starting another question ##################

    if confirmed:
        cicles = 0 #Reset balloon stand time
        while True:
            n_sort = random.randint(0, len(questions) - 1)
            if n_sort not in answered_questions:
                answered_questions.append(n_sort)
                confirmed = False
                break

    ################## Draw a question and blits it ################        

    blit_text(questions[n_sort][0],
              (690, 188),
              (67, 51),
              fnt(20),
              game_display)

    ################# Blits the alternatives of the question ############

    for i in range(5):
         blit_text(questions[n_sort][i + 1].replace('*',''),
                   (697, 392 + 70 * i),
                   (118, 272 + 70 * i),
                   fnt(18),
                   game_display)
         
         if which_element(1) == ('alt_' + str(i + 1), True):
             selected = i
             
         if questions[n_sort][i + 1].startswith('*'):
             correta = i

    ########## Blits unmarked radio buttons #############################

    for i in range(5):
        if selected == i:
            game_display.blit(
                cmp['sel'],
                (83, 275 + 70 * i))

    ######### Checks if the user has got it right #######################
    
    if selected == correta:
        correct_selected = True
    else:
        correct_selected = False

    ######### Change to main page if user clicks "album" button #########

    if which_element(1) == ('album', True):
        page = "album"

    ######### Events after user clicks "confirm" ########################

    if which_element(1) == ('confirmar', True):
        if selected != -1:
            selected = -1
            confirmed = True
            if correct_selected:
                number_of_packs += 1                
            else:
                misses += 1
                if misses % 2 == 0:
                    number_of_packs -= 1

################################ MAIN ###################################

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_or_load()
            pygame.quit()
            quit()
                   
        if event.type == pygame.MOUSEMOTION:
            cicles += 1
            if cicles >= 150:
                hit = False
                missed = False
                clicked_trade = False
                cicles = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                toggle_screen((display_width, display_height),
                              game_display)

    ############## Blits and spins the background ##############         

    angle += 0.1
    if angle == 360:
        angle = 0

    bg = rot_center(cmp['universo'], angle)

    game_display.blit(bg, (-128, -256))
    
    ############## Running current page ###########################

    if page == "album":
        #try:
            main_page()
        #except:
            #pass

    if page == "newsstand":
        #try:
            page_banca()
            if confirmed and correct_selected:
                hit = True

            if confirmed and not correct_selected:
                missed = True 

            ############## balloon when the user hits #################
                
            if hit:
                game_display.blit(cmp['balao'],
                                  (780, 119))

                blit_text('Parabéns! Você ganhou um pacotinho!',
                          (790 + 126, 200 + 122),
                          (790, 200),
                          fnt(17),
                          game_display)

            ############### balloon when the user misses ###############
                
            if missed:
                game_display.blit(cmp['balao'],
                                  (780, 119))
                
                if misses % 2 != 0:
                    blit_text('Vish! Você errou!', 
                              (790 + 120, 200 + 122),
                              (790, 200),
                              fnt(18),
                              game_display)
                    
                else:
                    blit_text('Você errou duas vezes! Perdeu um pacotinho...',
                              (790 + 120, 200 + 122),
                              (790, 200),
                              fnt(17),
                              game_display)

            ############### balloon when the user clicks "Trade" ############

            if clicked_trade:
                game_display.blit(cmp['balao'],
                                  (780, 119))
                
                blit_text(f'Você trocou {div*5} repetidas em {div} pacotinhos.',
                          (790 + 126, 200 + 122),
                          (790, 200),
                          fnt(18),
                          game_display)
        #except:
           # pass
        
    pygame.display.update()
############### Close pygame ###################
pygame.quit()
