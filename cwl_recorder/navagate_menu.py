from utils import *
from time import sleep
from recording import record_replay
import os
from dataclasses import dataclass

@dataclass
class RecordSettings:
    speed_factor: int
    resolution: str
    path: str
    day: int | None

locations = {
    "cwl_menu": (105, 877),
    "close_popup": (2270, 82),
    "center_of_screen": (1282, 651),
    "return_home": (155, 1282),
    "first_enemy_base": (1486, 899),
    "replay_button": (931, 1265),
    "next_base": (1896, 1142),
    "3rd_star": (1018, 1182, 255, 221, 77)
}

days = {
    1: (670,1301),
    2: (877,1294),
    3: (1083,1296),
    4: (1293,1296),
    5: (1495,1292),
    6: (1694,1294),
    7: (1908,1293),
}

def wait_for_cwl_menu_to_load():
    sleep(0.5) # make sure the clouds have actually came

    while not find_location_on_screen("cwl_info.png"): pass

def scroll_to_top():
    move_mouse_to(*locations["center_of_screen"])
    while not check_color_of_pixel(0, 0, 0, 0, 0, 3):
        scroll(1)
    sleep(.5) # let the screen settle

def record_all_replays(settings: RecordSettings) -> None:
    '''
    open cwl menu

    for day in 1 to 7
        click on day

        for attack in 1 to 15
            if file does not exist
                record attack
            go to next attack
    '''
    click_on_screen(*locations["cwl_menu"])
    wait_for_cwl_menu_to_load()
    click_on_screen(*locations["close_popup"])

    for day in range(1, 8):
        if settings.day is not None:
            day = settings.day

        click_on_screen(*locations["center_of_screen"])
        click_on_screen(*days[day])
        wait_for_cwl_menu_to_load()
        scroll_to_top()
        click_on_screen(*locations["first_enemy_base"])
        
        day_path = os.path.join(settings.path, f"day_{day}")

        for attack in range(1, 16):
            video_file = os.path.join(day_path, f"attack_{attack}")

            if not check_if_recording_exists(video_file):
                click_on_screen(*locations["replay_button"], min_delay=0.1, max_delay=0.2, min_press_time=0.05, max_press_time=0.1)
                
                record_replay(video_file, settings.speed_factor)

                click_on_screen(*locations["return_home"])
                wait_for_cwl_menu_to_load()
                if find_location_on_screen("red_x.png"):
                    click_on_screen(*locations["close_popup"])
            
            click_on_screen(*locations["next_base"])

        if settings.day is not None:
            break

def check_if_recording_exists(video_file):
    if os.path.exists(video_file + ".mp4"):
        return True
    
    print(f"file `{video_file}` does not exist")
    return False
