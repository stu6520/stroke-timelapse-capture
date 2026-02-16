from pynput import mouse, keyboard
import pyautogui
import pygetwindow as gw
import os
import time
import sys

APP = "RETAS STUDIO"    # Drawing program
TRIGGER = 2     # Take a screenshot every 2 strokes
SAVE = r"output/" # Screenshots' directory, auto-create if not already existed
JPG_QUALITY = 35
SCALE = 0.5   # 0.5 = Screenshots at 50% size


os.makedirs(SAVE, exist_ok=True)

count = 0
idx = 0
press_time = 0
running = True
paused = False
auto_paused = False


def get_window():
    w = gw.getActiveWindow()
    if w and APP.lower() in w.title.lower():
        return w
    return None


def check_auto_pause():
    global auto_paused, paused
    w = get_window()

    if w is None or w.isMinimized:
        if not auto_paused:
            auto_paused = True
            paused = True
            print("Auto-paused (window inactive/minimized)")
    else:
        if auto_paused:
            auto_paused = False
            paused = False
            print("Auto-resumed")


def save_jpg(path):
    img = pyautogui.screenshot()
    w, h = img.size
    img = img.resize((int(w*SCALE), int(h*SCALE)))

    img.save(path, "JPEG", quality=30, subsampling=2)



def on_click(x, y, button, pressed):
    global count, idx, press_time

    if not running:
        return False

    check_auto_pause()

    if paused:
        return

    if button != mouse.Button.left:
        return

    if pressed:
        press_time = time.time()
    else:
        if time.time() - press_time > 0.05:
            count += 1

            if count >= TRIGGER:
                filename = f"Rec_{idx:06d}.jpg"
                path = os.path.join(SAVE, filename)

                save_jpg(path)

                idx += 1
                count = 0


def on_press(key):
    global running, paused, auto_paused

    if key == keyboard.Key.esc:
        print("Exiting...")
        running = False
        return False

    if key == keyboard.Key.f8:
        if not auto_paused:
            paused = not paused
            print("Paused" if paused else "Resumed")


print("Running")
print("F8 = Pause/Resume")
print("ESC = Exit")

mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()
keyboard_listener.start()

keyboard_listener.join()
mouse_listener.stop()

print("Exited.")
sys.exit()

