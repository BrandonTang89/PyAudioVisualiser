# pyaudiovisualiser
Using scipy and pygame to create an audio visualiser which uses multiple fast fourier transforms to visualise an audio file.

<b>Dependencies</b>:<ol>
<li>Python 3.7</li>
<li>Scipy</li>
<li>Pygame</li>
</ol>

The first 6 variables can be edited to suit your viewing experience.
<pre>
songs_file                   #Directory To Search For Songs :) [the path finding is relative to this]
screen_w                     #Screen Width
screen_h                     #Screen Height
percentage_displayed_f       #Percentage of frequencies to show (Removes higher frequencies) Range = [0, 1]
max_height_percentile        #Pecentile of amplitude that fills the entire height of screen Range = (0, 100]
fftlength                    #Number of samples per DFT (better to be a power of 2) 
                             #Longer fftlength results in greater frequency resolution but worse time resolution
</pre>

File path is written relative to the songs_file <br>(which defaults as '' meaning the file path is relative to the audio visualiser GUI.py file)

AudioVisualiserGUI.pyw allows for GUI file name input (unfortunately does not support copy and paste)
AudioVisualiserConsole.py uses a command line for name input 

<b>NOTE: Python only accepts sound files encoded in .wav format</b><br>
One can use the conole lame.exe application to convert mp3 files to wav files using the following command in the terminal
<pre> lame.exe some_mp3.mp3 some_wav.wav</pre>
