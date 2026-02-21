# Requirements: pip install pydirectinput
#               pip install keyboard   (for clean exit with ESC)

import pydirectinput
import time
import random
import keyboard  # only used to exit cleanly with ESC

# Make sure to run this AFTER Roblox is open and in focus
# (or click inside Roblox window right after starting the script)

pydirectinput.PAUSE = 0.08          # small delay between actions (more human-like)
pydirectinput.FAILSAFE = True       # move mouse to top-left to emergency stop

print("Anti-AFK started. Press ESC anytime to stop.")
print("Make sure Roblox window is active / focused.")
print("Will press random movement + jump every 4–6 minutes.\n")

try:
    while True:
        if keyboard.is_pressed('esc'):
            print("ESC pressed → stopping script.")
            break

        # Random delay between 240–360 seconds (4–6 min)
        wait_time = random.uniform(240, 360)
        print(f"Waiting {wait_time//60:.0f} min {wait_time%60:.0f} sec...")
        time.sleep(wait_time)

        # Small sequence to look "active"
        keys = ['w', 'a', 's', 'd', 'space']
        
        # Press 4–8 random keys quickly
        for _ in range(random.randint(4, 8)):
            key = random.choice(keys)
            pydirectinput.keyDown(key)
            time.sleep(random.uniform(0.06, 0.18))
            pydirectinput.keyUp(key)
            time.sleep(random.uniform(0.15, 0.45))  # small pause between presses

        print("→ Did a short movement/jump burst")

except KeyboardInterrupt:
    print("\nStopped via Ctrl+C")

print("Script ended.")