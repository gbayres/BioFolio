from pygame import *
import os

##########################################################
fullscreen = False
def toggle_screen(screen, game_display):

    '''Alternates between fullscreen and window'''

    global fullscreen
    try:
        if display.get_driver() == 'x11':
            display.toggle_fullscreen()
        else:
            acopy = game_display.copy()
            if fullscreen:
                display.set_mode(screen)
                fullscreen = False
            else:
                display.set_mode(screen, FULLSCREEN)
                game_display.blit(acopy, (0, 0))
                display.update()
                fullscreen = True
    except:
        print("Incompatible with fullscreen")

##########################################################
        
def load_bios():

    '''Loads stickers descriptions'''
    
    with open(os.getcwd() + '/Data/bios.txt',
              encoding='latin-1') as f:
        return [i.split('|') for i in f.readlines()]

##########################################################
    
def slices_of_6(lst):

    ''' Wrapper to divide a list in chunks of 6 '''
    
    def wrapper():
        return [lst()[i: i + 6] for i in range(0, len(lst()), 6)]
    return wrapper

@slices_of_6
def load_questions():

    '''Loads questions'''
    
    with open(os.getcwd() + '/Data/questions.txt',
              encoding = 'latin-1') as f:
        return f.readlines()

##########################################################

def right(img):

    '''Turns a picture to the right'''
    
    return transform.rotate(img, -90)

def left(img):

    'Turns a picture to the left'''
    
    return transform.rotate(img, 90)

##########################################################

def load_components():

    '''Loads components of the page'''
    
    os.chdir(os.getcwd()+'/Resources/Components/')
    files = os.listdir()
    loads = map(image.load, files)
    components = [os.path.splitext(i)[0] for i in files]

    cmp = dict(zip(components,loads))
    cmp['seta_esq'] = left(cmp['seta'])
    cmp['seta_dir'] = right(cmp['seta'])

    return cmp 

##########################################################

def origin_map(cmp, page):

    '''Returns the positions of the page components'''
    
    return [
        [
            (cmp['seta_esq'], ( 25, 244)),
            (cmp['seta_dir'], ( 50, 244)),
            (cmp['seta_esq'], ( 25, 496)),
            (cmp['seta_dir'], ( 50, 496)),
            (cmp['seta_esq'], (289, 365)),
            (cmp['seta_dir'], (900, 365)),
            (cmp['banca']   , (219, 589))
        ],

        [
            (cmp['projeto banca'], (  0,   0)),
            (cmp['album']        , (837, 426)),
            (cmp['confirmar']    , (344, 607)),
            (cmp['trocar']       , (837, 336)),
        ]
            ][page]

##########################################################

def position_map():

    ''' Returns the limits of each element '''
    
    return [
    {
        'figurinhas' : ( 30, 30 + 137,  50,  50 + 181),
        'repetidas'  : ( 30, 30 + 137, 302, 302 + 181),
        'pacotinhos' : ( 31, 31 + 137, 552, 552 + 181),
        'fig_esq'    : ( 25, 25 +  20, 244, 244 +  20),
        'fig_dir'    : ( 50, 50 +  20, 244, 244 +  20),
        'rep_esq'    : ( 25, 25 +  20, 496, 496 +  20),
        'rep_dir'    : ( 50, 50 +  20, 496, 496 +  20),
        'folio_esq'  : (289, 289 + 20, 365, 365 +  20),
        'folio_dir'  : (900, 900 + 20, 365, 365 +  20),
        'banca'      : (219, 219 + 70, 589, 589 +  70)
    },

    {
        'alt_1'    : ( 83,  83 + 500, 275 + 70 * 0, 275 + 70 * 0 + 60),
        'alt_2'    : ( 83,  83 + 500, 275 + 70 * 1, 275 + 70 * 1 + 60),
        'alt_3'    : ( 83,  83 + 500, 275 + 70 * 2, 275 + 70 * 2 + 60),
        'alt_4'    : ( 83,  83 + 500, 275 + 70 * 3, 275 + 70 * 3 + 60),
        'alt_5'    : ( 83,  83 + 500, 275 + 70 * 4, 275 + 70 * 4 + 45),
        'album'    : (837, 837 +  70, 426, 426 + 70),
        'confirmar': (344, 344 + 100, 607, 607 + 60),
        'trocar'   : (837, 837 +  70, 336, 336 + 70)
    }]

##########################################################

def which_element(page):

    '''Returns the element where the cursor is over and if
       the right mouse button was clicked '''
    
    current_element = None
    pressed = False

    if mouse.get_pressed() == (1,0,0):
        pressed = True

    x, y = mouse.get_pos()

    for element, coordinate in position_map()[page].items():
        if coordinate[0] <= x <= coordinate[1] and\
           coordinate[2] <= y <= coordinate[3]:
            current_element = element

    return (current_element, pressed)

##########################################################

def rot_center(image, angle):

    '''Rotates an image while keeping its center and size'''

    orig_rect = image.get_rect()
    rot_image = transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

##########################################################

def fnt(size):

    '''Returns a font element of a given size'''
    
    return font.Font(os.getcwd() + '/Resources/Font/FreeMono.ttf',
                     size) 

##########################################################

def blit_text(text,
              surface,
              pos,
              font,
              display,
              color = (0, 0, 0)):

    '''Blits a text on the screen'''
    
    splited_lines = [line.split() for line in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = surface
    x, y = pos
    for splited_line in splited_lines:
        for word in splited_line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            display.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height

#############################################################

def to_list(string):

    '''Converst a string to list of integers'''

    lst = []
    for i in string[1 : -1].split(', '):
        if i != '':
            lst.append(int(i))

    return lst
    
