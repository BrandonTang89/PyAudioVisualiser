# pyaudiovisualiser
Using scipy and pygame to create an audio visualiser which uses multiple fast fourier transforms to visualise an audio file.

<b>Dependencies</b>:<ol>
  <li>Python 3.7+</li>
  <li>Scipy</li>
  <li>Pygame</li>
  <li>Pathlib</li>
</ol>

Python 3.7+ can be installed from <pre> https://www.python.org/downloads </pre>

Scipy, Pygame and Pathlib are python libraries which can be installed using pip in the terminal (after downloading python 3.7+)
<pre> pip install scipy pygame pathlib</pre>

Note: The GUI and EXE versions only work (properly) on windows
# Getting Started
<b>Variations</b>

AudioVisualiserGUI.pyw
<ul>
  <li>Allows for GUI file name input</li>
  <li>Does not support copy and paste</li>
</ul>

AudioVisualiserGUI.exe 
<ul>
  <li>Available in the release</li>
  <li>Can be used without the required dependencies</li>
  <li>Doesn't allow customisation of variables :( </li>
 </ul>
 
AudioVisualiserConsole.py
<ul>
  <li>Uses a command line for name input</li>
  <li>Works with linux and OS X (file path must be enclosed with quotation marks)</li>
</ul>

<b>Writing Filepath</b><br>
File path is written relative to the songs_file variable which defaults as '' (meaning the file path is relative to the main AudioVisualiser file).

If no extension of file path is given, the program assumes it to be wav.<br>
If the file path ends with .mp3, the program attempts to convert it with lame.

<b>NOTE: Python only natively accepts sound files encoded in .wav format</b><br>
Download lame.exe and link its path to the AudioVisualiser for mp3 input.<br>
By default, the program looks for lame in the same directory as itself.

# Customising the Visualiser
The first 7 variables can be edited to suit your viewing experience.
<pre>
songs_file = ''              #Directory To Search For Songs :) [the path finding is relative to this]
lame_path = 'lame.exe'       #Path to lame.exe
screen_w                     #Screen Width
screen_h                     #Screen Height
percentage_displayed_f       #Percentage of frequencies to show (Removes higher frequencies) Range = [0, 1]
max_height_percentile        #Pecentile of amplitude that fills the entire height of screen Range = (0, 100]
fftlength                    #Number of samples per DFT (better to be a power of 2) 
                             #Longer fftlength results in greater frequency resolution but worse time resolution
</pre>

