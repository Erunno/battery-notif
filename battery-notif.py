from time import sleep
from win10toast import ToastNotifier
import keyboard
import psutil

battery = psutil.sensors_battery()
notif_limit_mins = 20
notif_critical_interval_mins = 3


def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%dh %02dm" % (hours, minutes)


def show_battery_status():
    global battery

    battery_perc = battery.percent
    time_left_secs = battery.secsleft

    title = f'Battery {battery_perc}%'
    body = f'Remaining time: {convertTime(time_left_secs)}'

    if battery.power_plugged:
        title = "⚡ " + title + " ⚡"

    toaster = ToastNotifier()
    toaster.show_toast(title, body)


def keep_checking_battery():
    global battery
    while True:
        time_left_mins = battery.secsleft / 60

        if time_left_mins > notif_limit_mins:
            sleep(time_left_mins // 5)
            continue

        if not battery.power_plugged:
            show_battery_status()

        sleep(notif_critical_interval_mins)


keyboard.add_hotkey('ctrl + win + b', show_battery_status)

keep_checking_battery()
