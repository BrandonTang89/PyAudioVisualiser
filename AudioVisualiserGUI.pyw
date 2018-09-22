import scipy
import scipy.io.wavfile
import scipy.signal
import time
import pygame
from subprocess import call
from pathlib import Path

songs_file = ''                     #Directory To Search For Songs :) [the path finding is relative to this]
lame_path = 'lame.exe'              #Path to lame.exe
screen_w = 1600                     #Screen Width and height in px
screen_h = 900
percentage_displayed_f = 0.7        #Percentage of frequencies to show (Removes higher frequencies) Range = [0, 1]
max_height_percentile = 99.85       #Pecentile of amplitude that fills the entire height of screen Range = (0, 100]
fftlength = 2048                    #Number of samples per DFT (better to be a power of 2) (higher: > frequency resolution, < time resolution)
entertainment = False               #Just for aesthetics, centers the lowest frequencies in the centers and higher ones at the end then wraps around


class InputBox:                                                                                             #Class for Input Box

    def __init__(self, x, y, w, h, text='Enter Music File Path'):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
                self.color = COLOR_ACTIVE
                if self.text == 'Enter Music File Path':
                    self.text = ''
                
            # Change the current color of the input box.
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print("Try file path",self.text)
                    music_file_name = self.text
    
                    if songs_file != '':
                        music_path = (songs_file + "//" + music_file_name)
                    else:
                        music_path = (music_file_name)

                    if music_path[len(music_path)-4:] == '.mp3' and Path(lame_path).is_file():             #if mp3, convert if possible   
                            self.text = 'Attempting to convert mp3 file into wav'
                            refresh()
                            
                            call(["lame", "--decode", music_path, music_path[:len(music_path)-4]+'.wav'], shell=True)
                            music_path = music_path[:len(music_path)-4]+'.wav'
                    elif music_path[len(music_path)-4:] != '.wav':
                            music_path += '.wav'
                        
                    music_path = Path(music_path)
                    if music_path.is_file():                                                                #if file is wav
                        self.text = 'File Found! Now Loading...'
                        refresh()
                        return (True, music_path,music_file_name)
                    else:
                        self.text = 'Invalid File'
                        refresh()
                        return (False, '', '')
                    
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
        return (False, '','')

    def draw(self, screen):
        # Blit the text.
        self.txt_surface = FONT.render(self.text, True, self.color)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+10))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2+self.active*2)


#PREPARING PYGAME ENVT
pygame.init()
screen = pygame.display.set_mode((screen_w, screen_h))#creates main screen surface

#Getting font ready
pygame.font.init()
myfont = pygame.font.SysFont('Verdana', 20)
 
#INPUT BOX SCREEN-----------------------------------------------------------------------
COLOR_INACTIVE = pygame.Color('white')                                                                      #Parameters for Input Box
COLOR_ACTIVE = ((0,255,255))
FONT = myfont

#Initialising Title
title_font = pygame.font.SysFont('Verdana', 50)
logo = title_font.render("Brandon's Audio Visualiser", True, (0,255,255))
logo_rect = logo.get_rect(center=(screen_w/2, screen_h/4))

instruction = myfont.render("Enter Soundfile Path", True, (0,250,250))
instruction_rect = instruction.get_rect(center=(screen_w/2, 2*screen_h/5))

del_x = myfont.render("X", True, (255,255,255))
#Creating an input box
input_box = InputBox(0.1*screen_w,screen_h/2, 0.8*screen_w, 40)
del_box = del_x.get_rect(center=(0.9*screen_w - 25, screen_h/2+20))

def refresh():
    input_box.draw(screen)                                                                                  #Drawing all boxes and text
    screen.blit(del_x, del_box)
    screen.blit(logo, logo_rect)
    screen.blit(instruction, instruction_rect)
    pygame.display.flip()
    screen.fill((30, 30, 30))
#Starting Screen
done = False
while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                raise SystemExit

            try:                                                                                            #Protect agasint crashing due to char input
                done,music_path,music_file_name = input_box.handle_event(event)
                del_x = myfont.render("X", True, COLOR_ACTIVE if input_box.active else COLOR_INACTIVE)      #Colour of del x follows colour of input box
            except:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if del_box.collidepoint(event.pos):                                                         #If the user clicked on the delete box / x 
                    input_box.text = ''
            refresh()
        
#CALCULATION----------------------------------------------------------------------------
try:
    sr, original_signal = scipy.io.wavfile.read(music_path)
except:
    raise Exception('Error Parsing Sound File')

print("Found File")
print("Stereo to Mono Conversion")
music = scipy.mean(original_signal, axis=1)                                                                 #Combining both channels by averaging

print('Fourier Transform')                                                                                  #f, t are axis, Sxx is 2D array
f, t, Sxx = scipy.signal.spectrogram(music, sr,nperseg=fftlength)                                           #Sxx[frequency][time]
no_of_displayed_f = int(len(f)*percentage_displayed_f+0.5)
Sxx = Sxx[:no_of_displayed_f-2].transpose()                                                                 #Sxx[time][frequency] Last Frequency at 10163.671875
f = f[:no_of_displayed_f-2]

#STARTS ANTIMATION-----------------------------------------------------------------------
title = myfont.render(music_file_name, False, (0, 255, 255))                                                #Display name of soundfile
rect_scale_factor = screen_h/scipy.percentile(Sxx, max_height_percentile)                                   #Scale factor for height of rectangles
dt= t[1] - t[0]

#Initialising colour array for rectangles
colours = []
colour_f = 0.05                                                                                             #Colour Frequency
for i in range(no_of_displayed_f):
    green   = scipy.sin(colour_f*i + 0) * 127 + 128
    blue = scipy.sin(colour_f*i + 2) * 127 + 128
    red  = scipy.sin(colour_f*i + 4) * 127 + 128
    colours.append((red, green, blue))
    
#Initialising timer and music
pygame.mixer.music.load(str(music_path))                                                                    #Load and play music
pygame.mixer.music.play(1)
start_time = time.time()                                                                                    #Starts timer immediately after music starts

#Precalulations to make animation smoother
Sxx_len = len(Sxx)
rect_width = screen_w/no_of_displayed_f
done = False
#Animation Loop
while not done:
    try:
        cur_time = time.time() - start_time

        timer = myfont.render(str(int(cur_time))+ "s", False, (0, 255, 255))                                #Timer
        screen.blit(timer,(10,screen_h - 60))                                                               #Puts timer on screen
        screen.blit(title, (10, screen_h -30))                                                              #Puts sound file name on screen
        
        main_time_index = int(cur_time//dt)

        for index, frequency in enumerate(Sxx[(main_time_index)]):
            proportion_of_tleft = main_time_index - (main_time_index)
            height = max(proportion_of_tleft*frequency + (1- proportion_of_tleft)*Sxx[(main_time_index)+1][index], 2/rect_scale_factor)
            #Draws rectangles where height combines 2 nearest time bins by proportion for each frequency (height of 2px if no amplitude)
            if entertainment:
                multiplication_factor = 1 if index%2 else -1
                pygame.draw.rect(screen, colours[(index*multiplication_factor)%len(colours)], pygame.Rect((screen_w/2+multiplication_factor*0.5*(index+1)*screen_w/no_of_displayed_f), 20, screen_w/no_of_displayed_f, height*rect_scale_factor))
            else:
                pygame.draw.rect(screen, colours[index], pygame.Rect((index+1)*rect_width, 20, rect_width, height*rect_scale_factor))

        pygame.display.flip()
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.mixer.music.stop()
                    break

    except:
        pygame.display.quit()
        pygame.mixer.music.stop()
        break
        




