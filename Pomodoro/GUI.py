import sys
from Timer import *
from SettingsWindow import *
from StatisticsWindow import *
from tkinter import font
import pygame

BG_COL = '#464646'
TXT_COL = '#c1c1c1'


def draw_window():
    global window
    global style
    global fonts
    window = ThemedTk(theme="equilux")
    # window = tk.Tk()
    window.title('Pomodoro Timer')
    window.geometry('450x520')
    window['background'] = BG_COL
    window.resizable(False, False)
    fonts = list(font.families())


def draw_labels():
    global label1
    global points_label
    global act_font
    label1 = ttk.Label(window, text="00:00", font=('Ramabhadra', 140), background=BG_COL, foreground=TXT_COL)
    label1['text'] = format_min_sec(Settings.STUDY_TIME)
    label1.pack()
    label1.place(relx=0.5, rely=0.4, anchor='center')


def get_window_info():
    print(f'WINDOW HEIGHT:{window.winfo_height()} WINDOW WIDTH:{window.winfo_width()}')
    print(f'BUTTONS HEIGHT:{start_button.winfo_height()} BUTTONS WIDTH:{start_button.winfo_width()}')


def change_font():
    label1['font'] = (fonts[Settings.i], 120)
    print(fonts[Settings.i])
    Settings.i += 1


def load_button_images():
    global start_img
    global pause_img
    global stop_img
    global settings_img
    global stats_img
    start_img = tk.PhotoImage(file='images/START.png')
    pause_img = tk.PhotoImage(file='./images/PAUSE.png')
    stop_img = tk.PhotoImage(file='./images/STOP.png')
    settings_img = tk.PhotoImage(file='./images/SETTINGS.png')
    stats_img = tk.PhotoImage(file='./images/STATS.png')


def draw_buttons():
    global start_button
    global settings_button
    global font_button
    global terminate_timer_button
    global stats_button
    global info_button
    global threads_button

    start_button = tk.Button(window, command=threads, borderwidth=0, image=start_img)
    start_button.pack()
    start_button.place(x=25, y=300)

    # settings_button = tk.Button(window, image=btn_img, command=init_settings, borderwidth=0, width=50, height=50)
    settings_button = tk.Button(window, text='SETTINGS', command=init_settings, borderwidth=0, image=settings_img)
    settings_button.pack()
    settings_button.place(x=238, y=300)

    stats_button = tk.Button(window, text='STATS', command=init_stats, borderwidth=0, image=stats_img)
    stats_button.pack()
    stats_button.place(x=343, y=300)

    terminate_timer_button = tk.Button(window, command=kill_timer, state="disabled", borderwidth=0, image=stop_img)
    terminate_timer_button.pack()
    terminate_timer_button.place(x=133, y=300)

    info_button = ttk.Button(window, text="INFO", command=get_window_info, state="normal")
    # info_button.pack()

    threads_button = ttk.Button(window, text="THREADS", command=get_threads)
    # threads_button.pack()

    font_button = ttk.Button(window, command=change_font, text='CHANGE FONT')
    #font_button.pack()


def threads():
    global learnLoop
    terminate_timer_button["state"] = "normal"
    Settings.terminate_timer = False
    learnLoop = threading.Thread(target=learning_loop)
    learnLoop.daemon = True
    learnLoop.start()
    Settings.run = True
    settings_button["state"] = "disabled"
    start_button["command"] = pause_resume


def draw_progress_bar():
    global progress_bar
    progress_bar = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=420, mode='determinate')
    progress_bar.pack()
    progress_bar.place(x=15, y=45)
    #progress_bar['value'] = int((Settings.g_time / Settings.STUDY_TIME) * 100)


def update_labels():
    label1["text"] = Settings.g_time
    progress_bar['value'] = int(((Settings.to_pass - Settings.passed) / Settings.to_pass) * 100)
    # points_label["text"] = Settings.points
    if not Settings.terminate_timer:
        if Settings.run:
            start_button['image'] = pause_img
        else:
            start_button['image'] = start_img
    else:
        start_button["text"] = "START"
    window.after(2, update_labels)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        save_to_config()
        sys.exit()


def initWindow():
    pygame.mixer.init()
    draw_window()
    load_button_images()
    draw_labels()
    draw_buttons()
    draw_progress_bar()
    update_labels()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()
