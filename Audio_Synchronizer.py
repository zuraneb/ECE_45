# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:14:17 2022

@author: Zura Zura
"""

#Importing 4 different libraries
import pygame as pg
import numpy as np
from time import time
from matplotlib import pyplot as plt

pg.init()
pg.mixer.init()

# Synthesizes the sound and frequency. Makes sure that sampling rate is correct
def synth(frequency, duration=1.5, sampling_rate = 44100):
    frames = int(duration*sampling_rate)
    arr = np.cos(2*np.pi*frequency*np.linspace(0,duration, frames))
    sound = np.asarray([32767*arr,32767*arr]).T.astype(np.int16)
    sound = pg.sndarray.make_sound(sound.copy())
    
    return sound

#Plays the sound using ADSR values provided
def adsr(sound,play_time,attack,decay,sustain,release):
    attack_time = play_time * attack / 100
    decay_time = play_time * decay / 100
    sustain_time = play_time * sustain/100
    release_time = play_time * release/100
    request_time = time()
    run = True
    volume = 0
    
    while(run):
        current_time = time()
        while(current_time < request_time + attack_time):
            current_time = time()
            volume = (current_time - request_time)/attack_time
            sound.set_volume(volume)
            sound.play()
            
            
        while(current_time < request_time + attack_time + decay_time):
            current_time = time()
            volume = 1 - 0.6*((current_time - request_time - attack_time)/decay_time)
            sound.set_volume(volume)
            sound.play()
           
                 
        while(current_time < request_time + attack_time + decay_time + sustain_time):
            current_time = time()
            volume = 0.4
            sound.set_volume(volume)
            sound.play()
            
            
        while(current_time < request_time + play_time):
            current_time = time()
            volume = 0.4 - 0.4*((current_time - request_time - attack_time - sustain_time - decay_time)/release_time)
            sound.set_volume(volume)
            sound.play()
            
          
        if(current_time > request_time + attack_time + decay_time + sustain_time):
            run = False
       

# Plots ADSR chart for better visualization
def plot_adsr(attack,decay,sustain,release):
    plot_list = np.zeros(100)
    attack_step = 1/(int(attack))
    decay_step = -0.6/(int(decay))
    release_step = -0.4/(int(release))

    k = 0
    plot_list[k] = 0
    
    for i in range(int(attack)):
        plot_list[k+1] = plot_list[k] + attack_step
        k = k + 1
    for i in range(int(decay)):
        plot_list[k+1] = plot_list[k] + decay_step
        k = k + 1
    for i in range(int(sustain)):
        plot_list[k+1] = plot_list[k]
        k = k + 1
    for i in range(int(release) - 1):
        plot_list[k+1] = plot_list[k] + release_step
        k = k + 1
        
    plt.plot(plot_list)
    plt.ylabel('Volume')
    plt.xlabel('Time %')
    plt.pause(0.0001)


# Runs the code and asks for user inputs
if __name__ == "__main__":
    
    note_frequencies = [130,146,164,174,196,220,246]  # 7 Primary notes with default ADSR settings
    note_time = 3
    attack_time = 15
    decay_time = 35
    sustain_time = 20
    release_time = 30

    keymod = '0-='
    notes = {} # dict to store samples

    k = 0;

    for i in range(len(note_frequencies)):    # Creates an array with basic notes already synthesized
        
        sample = synth(note_frequencies[k])
        notes[k] = [sample, note_frequencies[k]]
        k = k + 1
    
    
    while True:    # Keeps gatherting input from the user and asking about the modes and what to do
        
        plot_adsr(attack_time,decay_time,sustain_time,release_time)
        print('Current ADSR graph is plotted')
        
        print('You have few mode options')
        print('Mode 1: Just play with the notes like a DJ')
        print('Mode 2: Play your own note')
        print('Mode 3: Adjust the settings for ADSR Values and how long do you want notes in Mode 1 be')
    
        mode_selection = input("Select a Mode  ")
    
    
        if(int(mode_selection) == 1):
            print("You Go DJ")
            print('For C note enter 1')
            print('For D note enter 2')
            print('For E note enter 3')
            print('For F note enter 4')
            print('For G note enter 5')
            print('For A note enter 6')
            print('For B note enter 7')
            print('To Go Back to the Menu enter 0')
        
            z = True
            while z:
                note_to_play = input("")
            
                if(int(note_to_play) == 1):
                    adsr(notes[0][0],note_time,attack_time,decay_time,sustain_time,release_time)
                if(int(note_to_play) == 2):
                    adsr(notes[1][0],note_time,attack_time,decay_time,sustain_time,release_time)
                if(int(note_to_play) == 3):
                    adsr(notes[2][0],note_time,attack_time,decay_time,sustain_time,release_time)
                if(int(note_to_play) == 4):
                    adsr(notes[3][0],note_time,attack_time,decay_time,sustain_time,release_time)
                if(int(note_to_play) == 5):
                    adsr(notes[4][0],note_time,attack_time,decay_time,sustain_time,release_time)
                if(int(note_to_play) == 6):
                    adsr(notes[5][0],note_time,attack_time,decay_time,sustain_time,release_time)
                if(int(note_to_play) == 7):
                    adsr(notes[6][0],note_time,attack_time,decay_time,sustain_time,release_time)
                if(int(note_to_play) == 0):
                    z = False
                
                
                
        if(int(mode_selection) == 2):   
            release = False
            while(not release):
                personal_frequency = float(input('What frequency do you want?(To go to the menu enter 0)? '))
                
                if(int(personal_frequency) == 0):
                    release = True 
                else:
                    new_note = synth(personal_frequency)
                    adsr(new_note,note_time,attack_time,decay_time,sustain_time,release_time)
            
            
        if(int(mode_selection) == 3):
           note_time = float(input("How many seconds do you want the notes to play? "))
           attack_time = float(input("What percentage (0-100) do you want the attack stage to take place? "))
           decay_time = float(input("What percentage (0-100) do you want the decay stage to take place? "))
           sustain_time = float(input("What percentage (0-100) do you want the sustain stage to take place? "))
           release_time = float(input("What percentage (0-100) do you want the release stage to take place? "))
        
           if(int(attack_time + decay_time + sustain_time + release_time) != 100):
                print("Come on man, these percentages don't add up to a 100. Let's try this again")
                release = False
                while(not release):
                    note_time = float(input("How many seconds do you want the notes to play? "))
                    attack_time = float(input("What percentage (0-100) do you want the attack stage to take place? "))
                    decay_time = float(input("What percentage (0-100) do you want the decay stage to take place? "))
                    sustain_time = float(input("What percentage (0-100) do you want the sustain stage to take place? "))
                    release_time = float(input("What percentage (0-100) do you want the release stage to take place? "))
                    if(int(attack_time + decay_time + sustain_time + release_time) != 100):
                        print("Come on man, these percentages don't add up to a 100. Let's try this again")
                    else:
                        print("Noted, thanks for the input. The changes have been made")
                        release = True    
           else:
                print("Noted, thanks for the input. The changes have been made")
                
                
            
     
    '''
    This part I tried to make in mode 4. The idea was for the user to be able to type in multiple notes from Mode 1 and play them simultaiously
    I got to the point where the code was able to read multiple digits from the user. So a user could type 1356 and the code would know that
    the user wants to play note 1,3,5,6 and I even made an array with 7 -values, where whether an index is 0 or 1 represents whether or not
    the user wants to play that note. The plan was to send this array to ADSR function above and play the notes that are marked with '1'
    however, even though I got really close, I encountered an issue with playing multiple notes at the same time because .play function did not really work
    on multiple notes. I spent an hour trying to figure out how to solve it but could not do it, and decided not to implement it hoping that other modes implemented above 
    would be sufficient    
    
    '''       
            
        
    '''
    print('Enter the notes you want to play as a single number:')
    print('For C note enter 1')
    print('For D note enter 2')
    print('For E note enter 3')
    print('For F note enter 4')
    print('For G note enter 5')
    print('For A note enter 6')
    print('For B note enter 7')
    
    user_input = input('Enter the notes you want to play as a single number (You can enter multiple at the same time):')
    digits = [int(a) for a in str(user_input)]
    notes_to_play = [0,0,0,0,0,0,0]
    
    z = 0
    while(z < len(note_frequencies)):
        for t in range(len(digits)):
            if(digits[t]== z+1):
                notes_to_play[z] = 1
                       
        z = z + 1
                
    print(notes_to_play)
    '''
    
    
    #adsr(notes[k][0],3)

    pg.mixer.quit()
    pg.quit()