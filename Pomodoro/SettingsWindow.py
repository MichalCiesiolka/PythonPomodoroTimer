import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import Settings
import GUI

LINE1 = '-------------------------TIME SETTINGS--------------------------------------------'
LINE2 = '-----------------------OTHER SETTINGS--------------------------------------------'
BG_COL = '#464646'
TXT_COL = '#c1c1c1'


def disable_buttons():
    GUI.start_button["state"] = "disabled"


def enable_buttons():
    GUI.start_button["state"] = "normal"


def enable_dev_buttons():
    GUI.info_button.pack()
    GUI.threads_button.pack()
    GUI.font_button.pack()
    GUI.info_button.place(x=25, y=450)
    GUI.threads_button.place(x=165, y=450)
    GUI.font_button.place(x=305, y=450)
    dev_button['command'] = disable_dev_buttons


def disable_dev_buttons():
    GUI.info_button.pack_forget()
    GUI.threads_button.pack_forget()
    GUI.font_button.pack_forget()
    dev_button['command'] = enable_dev_buttons


def draw_settings():
    global settingsWindow
    # settingsWindow = tk.Toplevel()
    settingsWindow = ThemedTk(theme="equilux")
    settingsWindow.title("Settings")
    settingsWindow.geometry('450x520')
    settingsWindow['background'] = BG_COL
    settingsWindow.resizable(False, False)


def draw_buttons():
    global save_button
    global cancel_button
    global dev_button
    save_button = tk.Button(settingsWindow, text="SAVE", command=save_changes, width=4, height=1)
    save_button.pack()
    save_button.place(x=310, y=480)

    cancel_button = tk.Button(settingsWindow, text="CANCEL", command=cancel_changes, width=4, height=1)
    cancel_button.pack()
    cancel_button.place(x=380, y=480)

    dev_button = ttk.Button(settingsWindow, text='DEV FUNCTIONS', command=enable_dev_buttons)
    dev_button.pack()
    dev_button.place(x=5, y=190)


def draw_labels():
    global study_time_label
    global short_brake_time_label
    global long_brake_time_label

    line1 = tk.Label(settingsWindow, text=LINE1, bg=BG_COL, font=('Arial', 14), fg=TXT_COL)
    line1.pack()
    line1.place(x=1, y=1)

    study_time_label = tk.Label(settingsWindow, text=f'Work: {int(study_slider.get())}', height=1, bg=BG_COL,
                                font=('Arial', 14), fg=TXT_COL)
    study_time_label.pack()
    study_time_label.place(x=201, y=42)

    short_brake_time_label = tk.Label(settingsWindow, text=f'Break: {int(short_brake_slider.get())}', height=1,
                                      bg=BG_COL, font=('Arial', 14), fg=TXT_COL)
    short_brake_time_label.pack()
    short_brake_time_label.place(x=201, y=82)

    long_brake_time_label = tk.Label(settingsWindow, text=f'Long break: {int(long_brake_slider.get())}', height=1,
                                     bg=BG_COL, font=('Arial', 14), fg=TXT_COL)
    long_brake_time_label.pack()
    long_brake_time_label.place(x=201, y=122)

    line2 = tk.Label(settingsWindow, text=LINE2, bg=BG_COL, font=('Arial', 14), fg=TXT_COL)
    line2.pack()
    line2.place(x=1, y=160)


def update_scale_labels(e):
    try:
        study_time_label.config(text=f'Work: {int(study_slider.get())}')
        short_brake_time_label.config(text=f'Break: {int(short_brake_slider.get())}')
        long_brake_time_label.config(text=f'Long break: {int(long_brake_slider.get())}')
    except:
        pass


def draw_sliders():
    global study_slider
    global short_brake_slider
    global long_brake_slider
    study_slider = ttk.Scale(settingsWindow, from_=15, to=35, length=200, orient=tk.HORIZONTAL,
                             command=update_scale_labels)
    study_slider.set(Settings.STUDY_TIME // 60)
    study_slider.pack()
    study_slider.place(x=1, y=41)

    short_brake_slider = ttk.Scale(settingsWindow, from_=5, to=10, orient=tk.HORIZONTAL, length=200,
                                   command=update_scale_labels)
    short_brake_slider.set(Settings.SHORT_BREAK_TIME // 60)
    short_brake_slider.pack()
    short_brake_slider.place(x=1, y=81)

    long_brake_slider = ttk.Scale(settingsWindow, from_=15, to=30, orient=tk.HORIZONTAL, length=200,
                                  command=update_scale_labels)
    long_brake_slider.set(Settings.LONG_BREAK_TIME // 60)
    long_brake_slider.pack()
    long_brake_slider.place(x=1, y=121)


def draw_checkboxes():
    global var
    var = tk.BooleanVar(settingsWindow)
    c = ttk.Checkbutton(settingsWindow, text='Play sounds', variable=var)
    c.pack()
    c.place(x=5, y=230)
    if Settings.play_sounds:
        c.invoke()


def change_play_sounds():
    if var.get() == 1:
        Settings.play_sounds = True
    else:
        Settings.play_sounds = False


def save_changes():
    change_play_sounds()
    Settings.STUDY_TIME = int(study_slider.get()) * 60
    Settings.SHORT_BREAK_TIME = int(short_brake_slider.get()) * 60
    Settings.LONG_BREAK_TIME = int(long_brake_slider.get()) * 60
    Settings.g_time = GUI.format_min_sec(Settings.STUDY_TIME)


def cancel_changes():
    study_slider.set(Settings.STUDY_TIME // 60)
    short_brake_slider.set(Settings.SHORT_BREAK_TIME // 60)
    long_brake_slider.set(Settings.LONG_BREAK_TIME // 60)


def on_close():
    save_changes()
    enable_buttons()
    settingsWindow.destroy()


def read_from_config():
    cfg = open("config.txt", "r+")
    config = {line.split()[0]: int(line.split()[2]) for line in cfg}
    Settings.STUDY_TIME = config['STUDY_TIME']
    Settings.SHORT_BREAK_TIME = config['SHORT_BREAK_TIME']
    Settings.LONG_BREAK_TIME = config['LONG_BREAK_TIME']
    Settings.points = config['points']
    Settings.time_passed_stat = config['time_passed_stat']
    cfg.close()


def save_to_config():
    cfg = open("config.txt", "w")
    cfg.write(f"STUDY_TIME = {Settings.STUDY_TIME}\n")
    cfg.write(f"SHORT_BREAK_TIME = {Settings.SHORT_BREAK_TIME}\n")
    cfg.write(f"LONG_BREAK_TIME = {Settings.LONG_BREAK_TIME}\n")
    cfg.write(f"points = {Settings.points}\n")
    cfg.write(f'time_passed_stat = {Settings.time_passed_stat}\n')
    cfg.close()


def init_settings():
    disable_buttons()
    draw_settings()
    draw_buttons()
    draw_sliders()
    draw_labels()
    draw_checkboxes()

    settingsWindow.protocol("WM_DELETE_WINDOW", on_close)
    settingsWindow.mainloop()
