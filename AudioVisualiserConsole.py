import scipy
import scipy.io.wavfile
import scipy.signal
import time
import pygame
from pathlib import Path
from subprocess import call
#music_file_name = r""
songs_file = ''
lame_path = 'lame.exe'
percentage_displayed_f = 0.9
screen_w = 1000
screen_h = 750
percentage_displayed_f = 0.7                                                                                #Percentage of frequencies to show (Removes higher frequencies) Range = [0, 1]
max_height_percentile = 99.8
fftlength = 2048
entertainment = False


print("--------------------------------------------")
print("BRANDON's AUDIO VISUALISER")
print("--------------------------------------------")
while True:                                                                                                 #While no valid file
    try:
        music_file_name = input("Song Title: ")
        if music_file_name[len(music_file_name)-4:] == '.mp3' and Path(lame_path).is_file():                #if mp3, convert if possible   
            print('Attempting to convert mp3 file into wav')
            call(["lame", "--decode", music_file_name, music_file_name[:len(music_file_name)-4]+'.wav'], shell=True)
            music_file_name = music_file_name[:len(music_file_name)-4]+'.wav'
        elif music_file_name[len(music_file_name)-4:] != '.wav':
            music_file_name += '.wav'

        if songs_file != '':
            music_file_name = songs_file + "//" + music_file_name
            
        sr, original_signal = scipy.io.wavfile.read(music_file_name)
        break
    except:
        print("invalid file")
        

print("Found File!")
print("Stereo to Mono Conversion")
music = scipy.mean(original_signal, axis=1)                                                                 #Combining both ears (computationally intensive)

print('Fourier Transform')                                                                                  #f, t are axis, Sxx is 2d array
f, t, Sxx = scipy.signal.spectrogram(music, sr,nperseg=fftlength)                                           #Sxx[frequency][time]
no_of_displayed_f = int(len(f)*percentage_displayed_f+0.5)
Sxx = Sxx[:no_of_displayed_f-2].transpose()                                                                 #Sxx[time][frequency] Last Frequency at 10163.671875
f = f[:no_of_displayed_f-2]

print("Playing...")
pygame.init()
screen = pygame.display.set_mode((screen_w, screen_h))                                                      #creates main screen surface
rect_scale_factor = screen_h/scipy.percentile(Sxx, max_height_percentile)
done = False
dt= t[1] - t[0]

#Printing clock and title on bottom right
pygame.font.init()
myfont = pygame.font.SysFont('Verdana', 20)
title = myfont.render(music_file_name, False, (0, 255, 255))  

#Initialising colour array for rectangles
colours = []
colour_f = 0.05                                                                                             #Colour Frequency
for i in range(no_of_displayed_f):
    green   = scipy.sin(colour_f*i + 0) * 127 + 128
    blue = scipy.sin(colour_f*i + 2) * 127 + 128
    red  = scipy.sin(colour_f*i + 4) * 127 + 128
    colours.append((red, green, blue))
    
#Initialising timer and music
start_time = time.time()
pygame.mixer.music.load(music_file_name)                                                                    #Load and play music
pygame.mixer.music.play(1)

#Precalulations to make animation smoother
Sxx_len = len(Sxx)
rect_width = screen_w/no_of_displayed_f
done = False
while not done:
        cur_time = time.time() - start_time

        timer = myfont.render(str(int(cur_time))+ "s", False, (0, 255, 255))                                #Timer
        screen.blit(timer,(10,screen_h - 60))                                                               #Puts timer on screen
        screen.blit(title, (10, screen_h -30))                                                              #Puts sound file name on screen
        
        main_time_index = int(cur_time//dt)
        if (main_time_index) >= Sxx_len:
            pygame.display.quit()
            pygame.mixer.music.stop()
            break

        try:
            for index, frequency in enumerate(Sxx[(main_time_index)]):
                proportion_of_tleft = main_time_index - (main_time_index)
                height = max(proportion_of_tleft*frequency + (1- proportion_of_tleft)*Sxx[(main_time_index)+1][index], 2/rect_scale_factor)
                #Draws rectangles where height combines 2 nearest time bins by proportion for each frequency (height of 2px if no amplitude)
                if entertainment:
                    multiplication_factor = 1 if index%2 else -1
                    pygame.draw.rect(screen, colours[(index*multiplication_factor)%len(colours)], pygame.Rect((screen_w/2+multiplication_factor*0.5*(index+1)*screen_w/no_of_displayed_f), 20, screen_w/no_of_displayed_f, height*rect_scale_factor))
                else:
                    pygame.draw.rect(screen, colours[index], pygame.Rect((index+1)*rect_width, 20, rect_width, height*rect_scale_factor))
        except:
            print("Finished/ Error")
            pygame.mixer.music.stop()
            pygame.display.quit()


        pygame.display.flip()
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.display.quit()
                    pygame.mixer.music.stop()
        




