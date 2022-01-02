from sys import exit
from os import listdir, path
from PIL import ImageGrab
import pywinauto
import win32gui
from pynput.keyboard import Key, Controller
import time
import cv2
import numpy as np
import random
import ctypes
import telebot
import os.path
import yaml

SETTINGS_FILE = 'settings.yaml'
settings = None
if os.path.isfile(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as stream:
        settings = yaml.safe_load(stream)

BOT_TOKEN = ''
OWNER_USER_ID = ''
if settings and settings.get('bot_token'):
    BOT_TOKEN = settings['bot_token']
if settings and settings.get('tg_user_id'):
    OWNER_USER_ID = settings['tg_user_id']
if BOT_TOKEN != '':
    TB = telebot.TeleBot(BOT_TOKEN)

BUTTONS_LOCATION = './images/buttons'
TESTS_LOCATION = './images/test_windows'
THRESHOLD = 0.79
SOURCE_WINDOW_NAME = 'Fortnite  '

FPS = 1
SCALE_FACTOR = 0.5
GAMES_PLAYED = 0
BOT_LAUNCHED = time.time()

keyboard = Controller()
scale = 1/SCALE_FACTOR
frame_delay = 1000/FPS

MONITOR = None


def focus_window(hwd):
    try:
        win32gui.SetForegroundWindow(hwd)
    except Exception:
        pass


def tg_send_image(image, caption):
    if BOT_TOKEN == '':
        return
    TB.send_chat_action(OWNER_USER_ID, 'upload_photo')
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    data = cv2.imencode('.jpg', image)[1].tobytes()
    TB.send_photo(OWNER_USER_ID, data, caption)


def random_animation(window_rect):
    #randX = random.randint(window_rect[0]+20,window_rect[2]-20)
    #randY = random.randint(window_rect[1]+20,window_rect[3]-20)
    #print(' -> Random animation! '+str(window_rect)+' '+str((randX, randY)))
    random_key = str(random.randint(1,8))
    print(' -> Random animation '+random_key)
    keyboard.press('b')
    time.sleep(random.uniform(0.5,1.5))
    #pywinauto.mouse.move(coords=(randX, randY))
    keyboard.press(random_key)
    time.sleep(random.uniform(0.2,0.5))
    keyboard.release(random_key)
    time.sleep(random.uniform(0.1,0.3))
    keyboard.release('b')
    time.sleep(random.uniform(0.5,1))


def click_button(topLeft, botttomRight, windowRect):
    randX = windowRect[0]+random.randint(topLeft[0]*scale+5, botttomRight[0]*scale-5)
    randY = windowRect[1]+random.randint(topLeft[1]*scale+5, botttomRight[1]*scale-5)
    pywinauto.mouse.click(button='left', coords=(randX, randY))


def do_random_move(topLeft, botttomRight, windowRect):
    keyboard_button = random.choice('wasd12')
    print('Random keyboard: %s' % keyboard_button)
    press_time = random.uniform(0.2,2)
    if keyboard_button == '1':
        time.sleep(press_time)
        return
    if keyboard_button == '2':
        keyboard_button = 'space'
    keyboard.press(keyboard_button)
    time.sleep(press_time)
    keyboard.release(keyboard_button)
    

def do_finish(topLeft, botttomRight, windowRect):
    global GAMES_PLAYED
    print('[!] Game finished, closing to main menu...')
    keyboard.press('e')
    time.sleep(random.uniform(1.5,2.5))
    keyboard.release('e')
    time.sleep(0.1)
    print('    Done')
    GAMES_PLAYED = GAMES_PLAYED + 1
    if GAMES_PLAYED > 0:
        current_time = time.time()
        avg_minutes = round((current_time - BOT_LAUNCHED)/60/GAMES_PLAYED, 2)
        print()
        print(' -- ' + str(GAMES_PLAYED) + ' games played, ' + str(avg_minutes) + ' minutes per game --')
        print()
        print('    Sleeping...')
        time.sleep(random.uniform(5,15))


def do_cancel(topLeft, botttomRight, windowRect):
    print('[!] Level upped! Closing to main menu...')
    keyboard.press(Key.esc)
    time.sleep(random.uniform(1.1,2.1))
    keyboard.release(Key.esc)
    time.sleep(random.uniform(2,4))
    print('    Done')


def do_start(topLeft, botttomRight, windowRect):
    print('[!] Starting game from main menu...')
    time.sleep(random.uniform(0.5,3))
    caption = None
    if GAMES_PLAYED > 0:
        current_time = time.time()
        avg_minutes = round((current_time - BOT_LAUNCHED)/60/GAMES_PLAYED, 2)
        caption = str(GAMES_PLAYED) + ' games played, ' + str(avg_minutes) + ' minutes per game'
    tg_send_image(MONITOR, caption)
    click_button(topLeft, botttomRight, windowRect)
    time.sleep(0.2)
    print('    Done')


def do_get_reward(topLeft, botttomRight, windowRect):
    print('[!] Got reward, resuming...')
    time.sleep(random.uniform(2,4))
    click_button(topLeft, botttomRight, windowRect)
    time.sleep(0.2)
    print('    Done')


def do_resume(topLeft, botttomRight, windowRect):
    print('[!] Something failed, resuming...')
    time.sleep(random.uniform(5,15))
    click_button(topLeft, botttomRight, windowRect)
    time.sleep(0.5)
    print('    Done')


def do_vote(topLeft, botttomRight, windowRect):
    print('[!] Voting detected! Voting...')
    keyboard.press('f')
    time.sleep(random.uniform(1.5,4.5))
    keyboard.release('f')
    print('    Done')

def do_maingame(topLeft, bottomRight, windowRect):
    do_random_move(topLeft, bottomRight, windowRect)


events = {
    'finished_blue': do_finish,
    'finished_red': do_finish,
    'menu': do_cancel,
    'levelup': do_cancel,
    'news': do_cancel,
    'start': do_start,
    'start_light': do_start,
    'get_reward': do_get_reward,
    'resume': do_resume,
    'vote': do_vote,
    'maingame': do_maingame
}


def main():

    last_random_animated = 0
    last_frame_captured = 0
    source_hwd = win32gui.FindWindow(None, SOURCE_WINDOW_NAME)

    #source_hwd = None
    #def winEnumHandler(hwnd, ctx):
    #    if win32gui.IsWindowVisible(hwnd):
    #        window_title = win32gui.GetWindowText(hwnd)
    #        print (hex(hwnd), window_title, window_title.encode('unicode-escape'))
    #        if SOURCE_WINDOW_NAME in window_title:
    #            print('Found')
    #            global source_hwd
    #            source_hwd = hwnd
    #win32gui.EnumWindows( winEnumHandler, None )
    
    #print(source_hwd)
    #exit(0)
    
    #print('Finished '+str(source_hwd))

    if not source_hwd:
        print('Failed to find source window')
        exit(1)
        
    focus_window(source_hwd)
    
    # Prevent windows from sleeping
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
    # This will cancel previous command:
    # ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
    
    print()
    print('    FPS Lock: ' + str(FPS))
    print('    Process ID: ' + str(source_hwd))
    print()

    buttons = []
    for filename in listdir(BUTTONS_LOCATION):
        filepath = path.join(BUTTONS_LOCATION, filename)
        name = filename.split('.')[0]
        image = cv2.imread(filepath)
        height, width = image.shape[:2]
        width = round(width/scale)
        height = round(height/scale)
        image = cv2.resize(image, (width, height))
        buttons.append({
            'name': name,
            'filepath': filepath,
            'image': image,
            'height': height,
            'width': width,
        })
        print('    Button '+filename+' loaded')

    print()
    print('  ----------- BOT LAUNCHED -----------')
    print()
    while True:
        if time.time()-last_frame_captured < frame_delay:
            time.sleep((frame_delay-(time.time()-last_frame_captured))/1000)
        last_frame_captured = time.time()
        if random.randint(0,10) == 5:
            focus_window(source_hwd)
        window_rect = win32gui.GetWindowPlacement(source_hwd)[4]
        image = cv2.cvtColor(np.array(ImageGrab.grab(window_rect)), cv2.COLOR_BGR2RGB)
        global MONITOR
        MONITOR = image
        #source_image = image.copy()
        image_height, image_width = image.shape[:2]
        image_width = round(image_width/scale)
        image_height = round(image_height/scale)
        image = cv2.resize(image, (image_width, image_height))
        submitted_events = []
        found_buttons = []
        for button in buttons:
            result = cv2.matchTemplate(image, button['image'], cv2.TM_CCOEFF_NORMED)
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
            quality = round(maxVal, 3)
            if quality > THRESHOLD:
                topLeft = maxLoc
                botttomRight = (topLeft[0] + button['width'], topLeft[1] + button['height'])
                print('    Found "'+button['name']+'" with confidence '+str(quality))
                cv2.rectangle(image, topLeft, botttomRight, (0, 255, 0), 2)
                cv2.putText(image, button['name']+' '+str(quality), topLeft, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                found_buttons.append(button['name'])
                
                if button['name'] == 'get_reward' and 'levelup' in found_buttons:
                    continue
                if button['name'] == 'levelup' and 'get_reward' in found_buttons:
                    continue
                    
                submitted_events.append([button['name'], topLeft, botttomRight, window_rect])
                
        cv2.imshow('monitor', image)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
        #if (cv2.waitKey(1) & 0xFF) == ord('s'):
        #    print(' -> Screenshot created!')
        #    cv2.imwrite('./screenshot.png', source_image)
        for event in submitted_events:
            focus_window(source_hwd)
            events[event[0]](event[1], event[2], event[3])
        if (time.time()-last_random_animated) > (25 + random.uniform(0,15)):
            last_random_animated = time.time()
            random_animation(window_rect)


if __name__ == '__main__':
    main()
