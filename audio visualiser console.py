import os
import scipy
import scipy.io.wavfile
import scipy.signal
import time
import pygame

#music_file_name = r""
songs_file = "songs"
music_file_name = input("Song Title: ")
if music_file_name[len(music_file_name)-4:] != '.wav':
    music_file_name += '.wav'
music_file_name = songs_file + "//" + music_file_name

percentage_displayed_f = 0.9
screen_w = 1000
screen_h = 750
percentage_displayed_f = 0.7                                                                                #Percentage of frequencies to show (Removes higher frequencies) Range = [0, 1]
max_height_percentile = 99.8
fftlength = 2048                                                                                            #Number of samples per DFT (better to be a power of 2) (higher: > frequency resolution, < time resolution)

try:
    sr, original_signal = scipy.io.wavfile.read(music_file_name)
except:
    raise Exception('Sound file does not exist within songs file')

print("Found File")
#print("Stereo to Mono Conversion")
music = scipy.mean(original_signal, axis=1)                                                                 #Combining both ears (computationally intensive)

#print('Fourier Transform')                                                                                 #f, t are axis, Sxx is 2d array
f, t, Sxx = scipy.signal.spectrogram(music, sr,nperseg=fftlength)                                           #Sxx[frequency][time]
no_of_displayed_f = int(len(f)*percentage_displayed_f+0.5)
Sxx = Sxx[:no_of_displayed_f-2].transpose()                                                                 #Sxx[time][frequency] Last Frequency at 10163.671875
f = f[:no_of_displayed_f-2]


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

while not done:
        cur_time = time.time() - start_time

        timer = myfont.render(str(int(cur_time))+ "s", False, (0, 255, 255))                                #Timer
        screen.blit(timer,(10,screen_h - 60))                                                               #Puts timer on screen
        screen.blit(title, (10, screen_h -30))                                                              #Puts sound file name on screen
        
        main_time_index = cur_time//dt
        if int(main_time_index) >= len(Sxx):
            pygame.display.quit()
            pygame.mixer.music.stop()
            done = True

        try:
            for index, frequency in enumerate(Sxx[int(main_time_index)]):
                proportion_of_tleft = main_time_index - int(main_time_index)
                height = max(proportion_of_tleft*frequency + (1- proportion_of_tleft)*Sxx[int(main_time_index)+1][index], 400)
                #Draws rectangles where height combines 2 nearest time bins by proportion for each frequency (height of 2px if no amplitude)
                
                pygame.draw.rect(screen, colours[index], pygame.Rect((index+1)*screen_w/no_of_displayed_f, 20, screen_w/no_of_displayed_f, height*rect_scale_factor))
        except:
            print("Finished/ Error")
            pygame.mixer.music.stop()
            pygame.display.quit()


        pygame.display.flip()
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if done:
                    pygame.display.quit()
                    pygame.mixer.music.stop()
        




