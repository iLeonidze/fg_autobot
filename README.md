# fg_autobot
This bot will play Fortnite for you 24/7

## How to install
1. Download latest python3
1. Open CMD, navigate to directory where you want to download repo
1. `git clone https://github.com/iLeonidze/fg_autobot.git`
1. `cd fg_autobot`
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
1. Edit `main.py` file, fill bot token in `BOT_TOKEN`, fill your ID in `OWNER_USER_ID`. Example:
   ```
   BOT_TOKEN = '1234567890:ABCDEFGABCDEFGABCDEFGABCDEFGABCDEFGAB'
   OWNER_USER_ID = '123456789'
   ```

## How to start
1. Close all unnecessary processes, nothing should pop-up
1. Open Fortnite, go to Battle Royale game
1. Select "Impostors" game mode
1. Navigate to repo in CMD
1. `python3 main.py`
1. Make shure you selected english keyboard layout
1. Make sure nothing is visially blocking the Fortnite window
1. Do not shutdown your monitor

## How to stop
1. Ctrl+C in CMD
