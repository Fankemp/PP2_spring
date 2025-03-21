import pygame
import os
import time

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((640, 480))

current_track = 0
tracks = []

def load_tracks(directory):
    global tracks
    tracks = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp3')]
    print(f"Загруженные треки: {tracks}")

def play_track(track_name):
    pygame.mixer.music.load(track_name)
    pygame.mixer.music.play()
    print(f"Играет {track_name}")

def stop_track():
    pygame.mixer.music.stop()
    print("Музыка остановлена.")

def next_track():
    global current_track
    current_track += 1
    if current_track >= len(tracks):
        current_track = 0
    play_track(tracks[current_track])

def previous_track():
    global current_track
    current_track -= 1
    if current_track < 0:
        current_track = len(tracks) - 1
    play_track(tracks[current_track])

load_tracks(r'D:\PP2\PP2_spring\lab7\controller\music')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not pygame.mixer.music.get_busy():
                    play_track(tracks[current_track])
                else:
                    print("Музыка уже играет.")
            elif event.key == pygame.K_s:
                stop_track()
            elif event.key == pygame.K_n:
                next_track()
            elif event.key == pygame.K_b:
                previous_track()
            elif event.key == pygame.K_q:
                pygame.quit()
                exit()
    
    time.sleep(0.1)
