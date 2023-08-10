import tkinter as tk
from ttkthemes import ThemedTk
import Settings

BG_COL = '#464646'
TXT_COL = '#c1c1c1'


def draw_window():
    global statsWindow
    statsWindow = ThemedTk(theme="adapta")
    statsWindow.title("Stats")
    statsWindow.geometry('450x200')
    statsWindow['background'] = BG_COL
    statsWindow.resizable(False, False)


def get_hours_stat(time):
    return time // 3600


def get_minutes_stat(time):
    return (time // 60) - 60 * get_hours_stat(time)


def format_min_sec2(time):
    if get_hours_stat(time) < 10 and get_minutes_stat(time) < 10:
        return f'0{get_hours_stat(time)}:0{get_minutes_stat(time)}'
    elif get_hours_stat(time) < 10 and get_minutes_stat(time) >= 10:
        return f'0{get_hours_stat(time)}:{get_minutes_stat(time)}'
    elif get_hours_stat(time) >= 10 and get_minutes_stat(time) < 10:
        return f'{get_hours_stat(time)}:0{get_minutes_stat(time)}'
    else:
        return f'{get_hours_stat(time)}:{get_minutes_stat(time)}'


def get_rank():
    global rank
    studied_hours = get_hours_stat(Settings.time_passed_stat)
    if studied_hours < 10:
        rank = "Preschool"
    elif 10 <= studied_hours < 20:
        rank = "Elementary school"
    elif 20 <= studied_hours < 30:
        rank = "Middle school"
    elif 30 <= studied_hours < 40:
        rank = "High school"
    elif 40 <= studied_hours < 50:
        rank = "Bachelor"
    elif 50 <= studied_hours < 60:
        rank = "Master's Degree"
    elif 60 <= studied_hours < 70:
        rank = "PhD"
    else:
        rank = "Professor"


def draw_labels():
    global studied_label
    global rank_label

    txt = f'You have studied for {get_hours_stat(Settings.time_passed_stat)} hours and {get_minutes_stat(Settings.time_passed_stat)} minutes'
    studied_label = tk.Label(statsWindow, text=txt, bg=BG_COL, font=('Arial', 15), fg=TXT_COL)
    studied_label.pack()

    rank_label = tk.Label(statsWindow, text=f'Rank: {rank}', bg=BG_COL, font=('Arial', 19), fg=TXT_COL)
    rank_label.pack()


# def update_labels():
#     studied_label["text"] = Settings.time_passed_stat
#     statsWindow.after(10, update_labels)


def init_stats():
    draw_window()
    get_rank()
    draw_labels()
    # update_labels()
