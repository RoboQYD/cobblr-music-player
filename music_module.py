#!/usr/bin/python
import os
import signal
from time import sleep
from engine import Menu
from engine import Utilities
from engine import TextWriter
from engine import SystemState
from subprocess import call

"""Module: music_module.py"""

signal.signal(signal.SIGINT, Utilities.GracefulExit)

class MusicState(object):
    pass

def Init():
  
  SystemState.MusicState = MusicState
  pygame = SystemState.pygame

  # Variables relating to the music player
  SystemState.MusicState.player_state = "Stopped"
  pygame.mixer.music.set_volume(1)
  
  # Variables relating to the song archive
  SystemState.MusicState.song_path = "media/music/"
  SystemState.MusicState.song_index = 0
  SystemState.MusicState.song_position = 0
 
  # Creating the path for the song
  MakeMusicPath()

  # More variables related to song archive
  SystemState.MusicState.song_archive = sorted([os.path.join('media/music/', dir) for dir in os.listdir('media/music/')])
  SystemState.MusicState.song_count = len(SystemState.MusicState.song_archive)
  SystemState.MusicState.song_id = SystemState.MusicState.song_archive[SystemState.MusicState.song_index]
  SystemState.MusicState.song_name = SystemState.MusicState.song_id.split(SystemState.MusicState.song_path)[1]

def MakeMusicPath():
  if os.path.exists(SystemState.MusicState.song_path) == False:
    os.makedirs(SystemState.MusicState.song_path)
  os.chown(SystemState.MusicState.song_path, SystemState.uid, SystemState.gid)


def Process():
  button = str(SystemState.pressed_button)
  pygame = SystemState.pygame
  screen = SystemState.screen
  back_pressed = 0

  if button == 'play' and len(SystemState.MusicState.song_archive) > 0:
    if SystemState.MusicState.player_state == 'Cannot Play':
      ChangeSong(1)
    else:
      LoadSong()
    if SystemState.MusicState.player_state == 'Paused' and SystemState.MusicState.song_position > 1:
      pygame.mixer.music.play(0, SystemState.MusicState.song_position)
    else:
      pygame.mixer.music.play(0, 0)
    SystemState.MusicState.player_state = 'Now Playing'
    Menu.JumpTo(screen_mode=2, toggle=True)

  if button == 'pause':
    pygame.mixer.music.pause()
    SystemState.MusicState.song_position = SystemState.MusicState.song_position + pygame.mixer.music.get_pos()/1000.0
    SystemState.MusicState.player_state = 'Paused'
    Menu.JumpTo(screen_mode=1, toggle=True)
  
  if button == 'stop':
    pygame.mixer.music.stop()
    SystemState.MusicState.player_state = 'Stopped'
    if SystemState.screen_mode == 2:
      Menu.JumpTo(screen_mode=1)
    elif SystemState.screen_mode == 3:
      Menu.JumpTo(screen_mode=3, toggle=True)

  if button == 'backward':
    ChangeSong(-1)
    if SystemState.MusicState.player_state == 'Now Playing':
      pygame.mixer.music.play(0, SystemState.MusicState.song_position)
  
  if button == 'forward':
    ChangeSong(1)
    if SystemState.MusicState.player_state == 'Now Playing':
      pygame.mixer.music.play(0, SystemState.MusicState.song_position)
 
  if button == 'alt':
    if SystemState.screen_mode == 1 or SystemState.screen_mode == 2:
      Menu.JumpTo(screen_mode=3, toggle=True)
    elif SystemState.screen_mode == 3:
      if SystemState.MusicState.player_state == 'Now Playing':
        Menu.JumpTo(screen_mode=2, toggle=True)
      else:
        Menu.JumpTo(screen_mode=1, toggle=True)

  if button == 'volume_up':
    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)

  if button == 'repeat':
    pass

  if button == 'volume_down':
    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)

  if button == 'go_back':
    back_pressed = 1
    Menu.Back()

  if back_pressed == 0:
    UpdateMusicText()

def LoadSong():
  try:
    SystemState.pygame.mixer.music.load(SystemState.MusicState.song_id)
    if SystemState.MusicState.player_state == "Cannot Play":
        pygame.mixer.music.stop()
  except:
    SystemState.MusicState.player_state = "Cannot Play"
  
def ChangeSong(direction): 
  SystemState.MusicState.song_index += direction
  if SystemState.MusicState.song_count == SystemState.MusicState.song_index:
    SystemState.MusicState.song_index = 0
  if SystemState.MusicState.song_index < 0:
    SystemState.MusicState.song_index = SystemState.MusicState.song_count - 1
  SystemState.MusicState.song_id = SystemState.MusicState.song_archive[SystemState.MusicState.song_index]
  SystemState.MusicState.song_name = SystemState.MusicState.song_id.split(SystemState.MusicState.song_path)[1]
  SystemState.pygame.mixer.music.stop()
  SystemState.MusicState.song_position = 0
  LoadSong()

def UpdateMusicText():
  title = SystemState.MusicState.player_state
  TextWriter.Write(
        state=SystemState,
        text=title,
        text_type = "message"
      )
  subtitle = str(SystemState.MusicState.song_index + 1) + ". " + str(SystemState.MusicState.song_name)
  TextWriter.Write(
        state=SystemState,
        text=subtitle,
        text_type = "subtext"
      )
