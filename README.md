# fg_autobot
This bot will play Fortnite and farm XP for you 24/7

## How to install
1. Install [Git](https://git-scm.com/downloads)
1. Open Windows Settings, go to "Manage app execution aliases" in Apps & Features, then untick the "python.exe" App Installer box.
1. Download latest [python3](https://www.python.org/downloads/)
1. Open CMD, navigate to directory where you want to download repo
1. `git clone https://github.com/iLeonidze/fg_autobot.git`
1. `cd fg_autobot`
1. `python3 -m pip install --upgrade pip`
1. `python3 -m pip install -r requirements.txt`

## Configure system
1. Open Windows settings
1. Disable automatic sleeping
1. Disable automatic monitor disable
1. In monitor settings disable any power-off features

## Configure game
1. Open Fortnite
1. Open Settings, change the following parameters:
   * Video:
      * Window Mode: Windowed
      * Resolution: 1280x680
      * Frame Limit: 30 FPS
      * Quality Presets: Low
      * 3D Resolution: 39%
   * Game:
      * Language: Russian
1. Restart the game

## Connect Telegram bot (Optional)
1. Go to `@botfather` bot in Telegram and create a new bot
1. After creation you will recieve bot token - copy it
1. Go to `@getmyid_bot` bot in Telegram and get your ID
1. Create `settings.yaml` file, fill bot token in `bot_token`, fill your ID in `tg_user_id`. Example:
   ```yaml
   bot_token: '1234567890:ABCDEFGABCDEFGABCDEFGABCDEFGABCDEFGAB'
   tg_user_id: 123456789
   ```

## How to start
1. Disconnect all gamepads
1. Close all unnecessary processes, nothing should pop-up
1. Make shure you selected english keyboard layout before running python script
1. Open Fortnite, go to Battle Royale game
1. Select "Impostors" game mode
1. Ensure you playing in non-private mode
1. Navigate to repo in CMD
1. `python3 main.py`
1. Make sure nothing is visially blocking the Fortnite window
1. Do not shutdown your monitor

## How to stop
1. Ctrl+C in CMD

## How to update
1. Navigate to repo in CMD
1. `git reset --hard HEAD`
1. `git pull`
1. `python3 -m pip install --upgrade pip`
1. `python3 -m pip install -I -r requirements.txt`

## How to uninstall
1. Navigate to repo in CMD
1. `python3 -m pip uninstall -r requirements.txt`
1. `python3 -m pip cache purge`
1. Delete repo directory
1. Optionally uninstall Git

## How to reinstall
1. Navigate to repo in CMD
1. `python3 -m pip uninstall -r requirements.txt`
1. `git reset --hard HEAD`
1. `git pull`
1. `python3 -m pip install --upgrade pip`
1. `python3 -m pip install -r requirements.txt`

## How to build EXE version
1. `python3 -m pip install pyinstaller`
1. `pyinstaller main.spec --noconfirm`
1. Use executable `dist/fg_autobot`

## Q&A
#### Why FPS in "monitor" window is too low?
Low FPS is specially designed to decrease the load on the CPU. It can be changed in `FPS` option, but this is not recommended. 
