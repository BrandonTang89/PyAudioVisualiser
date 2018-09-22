# pyaudiovisualiser
Using scipy and pygame to create an audio visualiser which uses multiple fast fourier transforms to visualise an audio file.

<b>Dependencies</b>:<ol>
<li>Python 3.7</li>
<li>Scipy</li>
<li>Pygame</li>
</ol>

The first 5 variables can be edited to suit your viewing experience.<ul>
<li>songs_file                   #Directory To Search For Songs :) [the path finding is relative to this]</li>
<li>screen_w                     #Screen Width</li>
<li>screen_h                     #Screen Height</li>
<li>percentage_displayed_f       #Percentage of frequencies to show (Removes higher frequencies) Range = [0, 1]</li>
<li>max_height_percentile        #Pecentile of amplitude that fills the entire height of screen Range = (0, 100]</li>
</ul>

File path is written relative to the songs_file (which defaults as '' meaning the file path is relative to the audio visualiser GUI.py file)
