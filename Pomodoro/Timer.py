from time import *
import threading
from tkinter import messagebox
import pygame
import Settings
import GUI


def get_minutes(time):
    return time // 60


def get_seconds(time):
    return time - 60 * get_minutes(time)


def format_min_sec(time):
    if get_minutes(time) < 10 and get_seconds(time) < 10:
        return f'0{get_minutes(time)}:0{get_seconds(time)}'
    elif get_minutes(time) < 10 and get_seconds(time) >= 10:
        return f'0{get_minutes(time)}:{get_seconds(time)}'
    elif get_minutes(time) >= 10 and get_seconds(time) < 10:
        return f'{get_minutes(time)}:0{get_seconds(time)}'
    else:
        return f'{get_minutes(time)}:{get_seconds(time)}'


def start_timer(t):
    tm = t
    Settings.to_pass = t
    if not Settings.terminate_timer:
        while t >= 0 and not Settings.terminate_timer:
            if Settings.run:
                Settings.g_time = format_min_sec(t)
                Settings.passed += 1
                if tm == Settings.STUDY_TIME:
                    Settings.time_passed_stat += 1
                t -= 1
                sleep(1)
            else:
                sleep(0.7)
    else:
        pass


def get_threads():
    for thread in threading.enumerate():
        print(thread.name)


def finish_timer():
    Settings.passed = -1
    Settings.terminate_timer = True
    Settings.run = False
    GUI.settings_button["state"] = "normal"
    GUI.start_button["command"] = GUI.threads
    GUI.start_button["image"] = GUI.start_img
    GUI.terminate_timer_button["state"] = "disabled"
    Settings.g_time = format_min_sec(Settings.STUDY_TIME)


def kill_timer():
    if messagebox.askyesno("Stop timer", "Do you want stop the timer?"):
        finish_timer()
    # sleep(0.5)


def pause_timer():
    print("paused")
    Settings.run = False


def resume_timer():
    print("resumed")
    Settings.run = True


def pause_resume():
    if Settings.run:
        pause_timer()
    else:
        resume_timer()


def play_start_sound():
    if Settings.play_sounds and not Settings.terminate_timer:
        pygame.mixer.music.load('./sounds/ping-82822.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=0)
        pygame.mixer.music.fadeout(2000)


def play_brake_sound():
    if Settings.play_sounds and not Settings.terminate_timer:
        pygame.mixer.music.load('./sounds/bell-chord1-83260.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=0)
        pygame.mixer.music.fadeout(2000)


def study_time():
    play_start_sound()
    start_timer(Settings.STUDY_TIME)
    if not Settings.terminate_timer:
        Settings.points += 1
    Settings.passed = -1


def short_brake_time():
    play_brake_sound()
    start_timer(Settings.SHORT_BREAK_TIME)
    Settings.passed = -1


def long_brake_time():
    play_brake_sound()
    start_timer(Settings.LONG_BREAK_TIME)
    Settings.passed = -1


def learning_loop():
    study_time()
    short_brake_time()
    study_time()
    short_brake_time()
    study_time()
    short_brake_time()
    study_time()
    long_brake_time()
    if not Settings.terminate_timer:
        finish_timer()
