#!/usr/bin/env python3

import signal
import sys
import subprocess
from xbox360controller import Xbox360Controller


class XdotoolManager(object):

    def __init__(self):
        pass
          
    def xdo(self, *commands):
        result = subprocess.run(["/usr/bin/xdotool"] + list(commands), capture_output=True, encoding="utf8")
        if result.returncode != 0:
            print(result)
            raise Exception('xdotool problem')
        return result.stdout
        
    def close_current_window(self):
        return self.xdo("getactivewindow", "windowclose")
        
        
    def kill_current_window(self):
        return self.xdo("getactivewindow", "windowkill")
        
    def get_current_window_name(self):
        return self.xdo("getactivewindow", "getwindowname")
    
    def get_current_window_pid(self):
        return self.xdo("getactivewindow", "getwindowpid")
    


class Emulators(object):

    def __init__(self):
        pass
        
        
    def close_all_emulators(self):
    
    	xdoman = XdotoolManager()
    	window_name = xdoman.get_current_window_name()
    	
    	if "cemu" in window_name.lower():
    	    # Cemu dectedted
    	    xdoman.kill_current_window()


    	if "dolphin" in window_name.lower():
    	    # Cemu dectedted
    	    xdoman.kill_current_window()


"""
retroarch/libretro common hotkeys
======================================================
Hotkey Combination	    Action
======================================================
Hotkey+Start	        Exit
Hotkey+Right Shoulder	Save
Hotkey+Left Shoulder	Load
Hotkey+Right	        Input State Slot Increase
Hotkey+Left	Input State Slot Decrease
Hotkey+X	            RGUI Menu
Hotkey+B	            Reset
======================================================
"""


class CustomHotkeys(object):

    def __init__(self):
        self.hotkey_button = "mode"
        self.hotkey_active = False

    def on_hotkey_pressed(self, button):
        print('HOTKEY ACTIVE')
        self.hotkey_active = True
    
    
    def on_hotkey_released(self, button):
        print('HOTKEY INACTIVE')
        self.hotkey_active = False

    def on_start_pressed(self, button):
        if self.hotkey_active:
            self.exit_emulators()
    

    def exit_emulators(self):
        Emulators().close_all_emulators()


    def run(self):
        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            #controller.button_a.when_pressed = self.on_button_pressed
            #controller.button_a.when_released = self.on_button_released
            hotkey_button = getattr(controller, f"button_{self.hotkey_button}")
            hotkey_button.when_pressed = self.on_hotkey_pressed
            hotkey_button.when_released = self.on_hotkey_released
            controller.button_start.when_pressed = self.on_start_pressed
    
            signal.pause()


def main():
    try:
        CustomHotkeys().run()
    except KeyboardInterrupt:
        return 0
    

if __name__ == '__main__':
    sys.exit(main())
