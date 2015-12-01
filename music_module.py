#!/usr/bin/python

from subprocess import call
import os
from time import sleep
from engine import TextWriter

"""Module: music_module.py"""

def Init(SystemState):
  SystemState.current_song = 0
  SystemState.music_state = "Stopped"
  SystemState.music_position = 0
  pygame = SystemState.pygame
  SystemState.all_music = [os.path.join('media', dir) for dir in os.listdir('./media')]
  pygame.mixer.music.set_volume(1)
  SystemState.music_count = len(SystemState.all_music)
  return SystemState

def Process(SystemState):
  button = str(SystemState.pressed_button)
  pygame = SystemState.pygame
  screen = SystemState.screen
  
  if button == 'play':
    if SystemState.music_state == 'Cannot Play':
      song_name = ChangeSong(SystemState, 1)
    else:
      song_name = LoadSong(SystemState)  
    if SystemState.music_state == 'Paused' and SystemState.music_position > 1:
      pygame.mixer.music.play(0, SystemState.music_position)
    else:
      pygame.mixer.music.play(0, 0)
    SystemState.music_state = 'Now Playing'
    SystemState.next_screen_mode = 2
  
  if button == 'pause':
    song_name = FetchSongName(SystemState) 
    pygame.mixer.music.pause()
    SystemState.music_position = SystemState.music_position + pygame.mixer.music.get_pos()/1000.0
    print SystemState.music_position
    SystemState.music_state = 'Paused'
    SystemState.next_screen_mode = 1
  
  if button == 'stop':
    song_name = FetchSongName(SystemState) 
    pygame.mixer.music.stop()
    SystemState.music_state = 'Stopped'
    if SystemState.screen_mode == 2:
      SystemState.next_screen_mode = 1
    elif SystemState.screen_mode == 3:
      SystemState.next_screen_mode = 3

  if button == 'backward':
    song_name = ChangeSong(SystemState, -1) #The Name of the current song
    if SystemState.music_state == 'Now Playing':
      pygame.mixer.music.play(0, SystemState.music_position)
  
  if button == 'forward':
    song_name = ChangeSong(SystemState, 1) #The Name of the current song
    if SystemState.music_state == 'Now Playing':
      pygame.mixer.music.play(0, SystemState.music_position)
 
  if button == 'alt':
    song_name = FetchSongName(SystemState)
    if SystemState.screen_mode == 1 or SystemState.screen_mode == 2:
      SystemState.next_screen_mode = 3
    elif SystemState.screen_mode == 3:
      if SystemState.music_state == 'Now Playing':
        SystemState.next_screen_mode = 2
      else:
        SystemState.next_screen_mode = 1

  if button == 'volume_up':
    song_name = FetchSongName(SystemState)
    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)

  if button == 'repeat':
    song_name = FetchSongName(SystemState)

  if button == 'volume_down':
    song_name = FetchSongName(SystemState)
    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
  
  #if SystemState.music_state == 'Cannot Play':
  #  song_name = FetchSongName(SystemState)

  UpdateMusicText(SystemState, song_name)
  return SystemState


def Refresh(SystemState):
  SystemState.pressed_button = ''
  SystemState.pressed_buttons = ''
  song_name = FetchSongName(SystemState)
  UpdateMusicText(SystemState, song_name)
  return SystemState


def FetchSongName(SystemState):
  song_name = os.path.basename(SystemState.all_music[SystemState.current_song]) 
  return song_name

def LoadSong(SystemState):
  song_name = FetchSongName(SystemState) 
  try:
    SystemState.pygame.mixer.music.load(SystemState.all_music[SystemState.current_song])
    if SystemState.music_state == "Cannot Play":
        song_name = FetchSongName(SystemState) 
        pygame.mixer.music.stop()
  except:
    SystemState.music_state = "Cannot Play"
  
  return song_name

def ChangeSong(SystemState, direction): 
  SystemState.current_song += direction
  if SystemState.music_count == SystemState.current_song:
    SystemState.current_song = 0
  if SystemState.current_song < 0:
    SystemState.current_song = SystemState.music_count - 1
  song_name = LoadSong(SystemState)
  SystemState.pygame.mixer.music.stop()
  SystemState.music_position = 0
  return song_name

def UpdateMusicText(SystemState, song_name):
  # Text and Returns
  title = SystemState.music_state
  TextWriter.Write(
        state=SystemState,
        text=title,
        text_type = "message"
      )
  subtitle = str(SystemState.current_song + 1) + ". " + song_name
  TextWriter.Write(
        state=SystemState,
        text=subtitle,
        text_type = "subtext"
      )

