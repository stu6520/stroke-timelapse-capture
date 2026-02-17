from pynput import mouse, keyboard
import pyautogui
import pygetwindow as gw
import os
import time
import sys

APP = "RETAS STUDIO"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_SAVE = os.path.join(SCRIPT_DIR, "output")
TRIGGER = 2
JPG_QUALITY = 35
SCALE = 0.5

# ---------- PROJECT NAME ----------
project = input("Enter project name: ").strip()
if not project:
    print("Project name required.")
    sys.exit()

SAVE = os.path.join(BASE_SAVE, project)
os.makedirs(SAVE, exist_ok=True)

# ---------- FIND NEXT INDEX ----------
existing = [f for f in os.listdir(SAVE) if f.endswith(".jpg")]
if existing:
    nums = [int(f.split("_")[1].split(".")[0]) for f in existing if "_" in f]
    idx = max(nums) + 1 if nums else 0
else:
    idx = 0

print("Saving to:", SAVE)
print("Starting index:", idx)

# ---------- STATE ----------
count = 0
press_time = 0
running = True
paused = False


# ---------- WINDOW ----------
def get_window():
    w = gw.getActiveWindow()
    if w and APP.lower() in w.title.lower():
        return w
    return None


# ---------- SCREENSHOT ----------
def save_jpg(path):
    w = get_window()
    if not w:
        return

    bbox = (w.left, w.top, w.right, w.bottom)
    img = pyautogui.screenshot(region=bbox)

    w0, h0 = img.size
    img = img.resize((int(w0 * SCALE), int(h0 * SCALE)))

    img.save(path, "JPEG", quality=JPG_QUALITY, optimize=True, progressive=True)


# ---------- MOUSE ----------
def on_click(x, y, button, pressed):
    global count, idx, press_time

    if not running or paused:
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


# ---------- KEYBOARD ----------
def on_press(key):
    global running, paused

    if key == keyboard.Key.esc:
        running = False
        return False

    elif key == keyboard.Key.f8:
        paused = not paused
        print("Paused" if paused else "Resumed")


# ---------- RUN ----------
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
