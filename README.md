This is a work-in-progress (WIP) release of a local server that allows you to play your Springfield in the "The Simpsons: Tapped Out" mobile app. 

# How to Setup and Use (Docker)

Before you run this program, you will need a few things:

[Docker](https://www.docker.com/get-started/) needs to be setup and operational.


1) Optional: A copy of your existing world (see [teamtsto.org](https://teamtsto.org/) for making a backup of your town) or a backup of your friends' town (see [tsto_friend_puller](https://github.com/tjac/tsto_friend_puller)). Save the file to the "towns" directory WITHOUT any file extension.
2) Create a folder called `tsto`
3) Download [docker-compose.yml](https://raw.githubusercontent.com/d-fens/tsto_server/refs/heads/master/docker-compose.yml), [config.json](https://raw.githubusercontent.com/d-fens/tsto_server/refs/heads/master/config.json) and [.env](https://raw.githubusercontent.com/d-fens/tsto_server/refs/heads/master/.env) to the `tsto` folder.
4) Download a copy of the APK of the [The Simpsons: Tapped Out game](https://apkpure.com/the-simpsons%E2%84%A2-tapped-out/com.ea.game.simpsons4_row) and place within the `tsto` folder. Make sure it is named 'Tapped Out.apk'
5) Edit the `.env` file and replace the APK name with the name; and the IP address with your machines IP.
6) Run `docker-compose up -d` from a command prompt in the `tsto` folder.
7) Install the APK on an Android phone or tablet. Optionally, you can play the game on your PC by using [BlueStacks](https://www.bluestacks.com/download.html) or equivalent emulator.
8) Optional: Run `docker compose logs -f` to see issues with containers. 

## How Update

1) Go back into the folder `tsto` and open a command prompt
2) Run `docker compose pull`
3) Run `docker compose up -d`

# How to Setup and Use (Python)

Note: Not working currently, requires work on changing the flask app to a more standard way of being called e.g. `create_app` or `make_app` factory and/or changes to the `config.json`. Work needed to add scripts for calling the server more cleanly too e.g. `tsto-server`.

1. `pip install -U -e git+https://github.com/d-fens/tsto_server#egg=tsto_server`
2. Download `https://raw.githubusercontent.com/d-fens/tsto_server/refs/heads/master/config.json` and place in a directory.
3. Run `flask --app tsto_server run` in the same directory as the `config.json`

# How to play

The system currently leverages the login AND anonymous play system to allow users to select different worlds to play. By default, clicking the "Tap to play anonymously" will load the "mytown" world. If the user wants to play a different town, they should click the EA Login button, then enter an email address that has the username equal to the town's filename in the towns directory. For example, if you want to load a town with the filename "mysupertown" then you would enter "mysupertown@a.a". The @ and . are required by the TSTO application, so any random domain will work. On the next screen, after pressing the "Log In" button, enter any 5 digit code and press "Verify". This will place the user back at the main screen. At this point pressing the "Tap to play anonymously" will load the newly selected world.

Users of the server have the ability to modify the `config.json` file to change certain behaviours of the system. Feel free to experiment with those options.

Admittedly this is a fragile system. It is definitely a work-in-progress.

# Current state

# Running old events
You can run past The Simpsons: Tapped Out events. If you navigate to the server at ```http://x.x.x.x/dashboard``` you will find a simple dashboard that lets you trigger old events/quest lines. This works by tricking the app into thinking the current date is far in the past (specifically the date at the beginning of the selected event). This is generally not a huge problem except if you have running tasks. If you have Homer doing something and then activate an event that was 2 years ago, it will cost ~7800 donuts to complete the task. Donuts are free now, so not a huge deal. But its best to have your citizens NOT in tasks when you make this change. Also, it is recommended to close the app BEFORE you change to a new event. Just makes the transition easier. 

With this feature you can now replay the last 12 years of the game... do individual events when you want. Or, you can reset to the beginning and play the entire 12 years over again in real time!

# Current state:
* Only works with Android since you need to modify the APK to point to the new server.
* This is still alpha. There are bugs and the code is fragile. Please [report](https://github.com/tjac/tsto_server/issues) any bugs you find.
  
# Change log:
* [2024/12/24] - Initial release
* [2025/1/1]   - Refactored code. Established framework for persistent configs. Multiple towns can be played by using the login system in the app
* [2025/1/6]   - Save functionality! Big thanks to [d-fens](https://github.com/d-fens) for setting the framework necessary to dockerize the server.
* [2025/1/30]  - Added dashboard for adjusting which event is running. Minor changes. More framework improvements for version 2.
