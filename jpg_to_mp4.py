import cv2
import os
import re
import sys
import numpy as np
import traceback

try:
    # === base directory (where exe/script is) ===
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # === ask folder ===
    user_input = input("Enter folder path OR folder name(Default output/: ").strip()
    if not user_input:
        raise Exception("Input cannot be empty")

    # absolute path → use directly
    if os.path.isabs(user_input):
        input_folder = user_input
        video_name = os.path.basename(os.path.normpath(user_input))
    else:
        # relative name → assume inside output/
        input_folder = os.path.join(base_dir, "output", user_input)
        video_name = user_input

    output_video = os.path.join(base_dir, f"{video_name}.mp4")

    # === fps ===
    try:
        fps = float(input("Enter FPS (default 30): ") or 30)
    except:
        fps = 30

    # === folder check ===
    if not os.path.exists(input_folder):
        raise Exception(f"Folder not found:\n{input_folder}")

    # === collect images ===
    files = [f for f in os.listdir(input_folder)
             if f.lower().endswith((".jpg",".jpeg",".png"))]

    def extract_num(name):
        m = re.search(r'(\d+)', name)
        return int(m.group(1)) if m else -1

    files.sort(key=extract_num)

    if not files:
        raise Exception("No images found in folder")

    # === first frame ===
    first_path = os.path.join(input_folder, files[0])
    first = cv2.imdecode(np.fromfile(first_path, dtype=np.uint8), cv2.IMREAD_COLOR)

    if first is None:
        raise Exception("Cannot read first image")

    h, w, _ = first.shape

    # === video writer ===
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_video, fourcc, fps, (w, h))

    print("Processing", len(files), "images...")

    for f in files:
        path = os.path.join(input_folder, f)
        img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

        if img is None:
            print("Skipped:", f)
            continue

        if img.shape[:2] != (h, w):
            img = cv2.resize(img, (w, h))

        video.write(img)

    video.release()
    print("Done! Saved:", output_video)

except Exception as e:
    print("\nERROR:", e)
    print(traceback.format_exc())
    input("Press Enter to exit...")


