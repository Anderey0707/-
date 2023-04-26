from matplotlib import pyplot as plt                                           
from scipy.fft import fft, fftfreq                                              
import numpy as np                                                              
from scipy.io import wavfile     
import tkinter as tk         
import time                                      


def next_note(wav_fname):
    G = 1500 # разница между громкостью нот
    volume = []
    vol_viborka = []


    samplerate, data = wavfile.read(wav_fname)
    data1 = [data[i][0] for i in range(len(data))]



    k = 1000 # частота выборки в точках/сек(Гц)

    for i in range(int(len(data1) / k)): 
        volume += [data1[(i * k) : (i * k + (k - 1))]]

    for i in volume:
        i = np.array(i)
        i = np.abs(i)
        vol_viborka.append(np.max(i))

    start_end = []
    pred = 0
    for x in range(len(vol_viborka) - 1):
        if vol_viborka[x + 1] - vol_viborka[x] >= G:
            if pred != x:
                start_end.append([pred * 10**3, x * 10**3, x - pred])
                pred = x + 1
    start_end.append([pred * 10**3, x * 10**3, x - pred])
    return start_end


music_book = {'DO':(127.1, 134.6),'DO#':(134.6, 142.6), 
          'RE':(142.6, 150.1),'RE#':(150.1, 160.1), 
          'MI':(160.1, 169.7),'FA':(169.7, 179.8), 
          'FA#':(179.8, 190.5),'SOL':(190.5, 201.8), 
          'SOL#':(201.8, 213.8),'LA':(213.8, 226.5), 
          'LA#':(226.5, 239.9),'SI':(239.9, 254.2),
          'DO1':(254.2, 269.3),'DO#1':(269.3, 285.3), 
          'RE1':(285.3, 301.8),'RE#1':(301.8, 321.8), 
          'MI1':(321.8,337),'FA1':(337, 361.2), 
          'FA#1':(361.2,377),'SOL1':(377, 407.9), 
          'SOL#1':(407.9, 423.3),'LA1':(423.3, 455.1), 
          'LA#1':(455.1, 477.6),'SI1':(477.6, 508.9)}


# wav_fname = 'проект\гамма wav.wav'
wav_fname = 'проект\morning2.wav'
samplerate, data = wavfile.read(wav_fname) 

from_nextnote = next_note(wav_fname)


notes = []
for k in range(len(from_nextnote)):

    start = from_nextnote[k][0]
    end = from_nextnote[k][1]

    y = [data[i][0] for i in range(start, end)]
    yf = fft(y)
    xf = fftfreq(end - start, 1 / samplerate)

    yf = yf.real ** 2 + yf.imag ** 2
    yf = list(yf)
    i = yf.index(np.max(yf))
    freq = abs(xf[i]).round(2)
    notes.append(freq)
print(*notes)

end_notes = []
for x in notes:
    for key in music_book: 
        st, fin = music_book[key] 
        if st < x < fin:
            end_notes.append(key)
            # print(key, end=' ')
print(*end_notes)

def highlight_next_note(notes, index):
    if index < len(notes):
        canvas.create_image(0, 0, anchor=tk.NW, image=piano_img)
        canvas.create_oval(click_note[notes[index]], fill="red")
        root.after(650, highlight_next_note, notes, index+1)


root = tk.Tk()
root.title("Ноты на пианино")
canvas = tk.Canvas(root, width=1000, height=400)
canvas.pack()

# Загрузите изображение пианино и создайте координаты овала
piano_img = tk.PhotoImage(file="проект\piano.png")
canvas.create_image(0, 0, anchor=tk.NW, image=piano_img)
notes = ['DO', 'RE','MI','FA','SOL','LA','SI', 
         'DO1','RE1','MI1','FA1','SOL1','LA1','SI1']
click_note = {}
for i in range(len(notes)): 
    click_note[notes[i]] = (15 + 68.5 * i, 225, 65 + 68.5 * i, 275) 


highlight_next_note(end_notes, 0)



root.mainloop()