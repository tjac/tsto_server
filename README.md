This is a work-in-progress (WIP) release of a local server that allows you to play your Springfield in the "The Simpsons: Tapped Out" mobile app. 

# How to Setup and Use (Docker)

Before you run this program, you will need a few things:

[Docker](https://www.docker.com/get-started/) needs to be setup and operational.


1) Optional: A copy of your existing world (see [teamtsto.org](https://teamtsto.org/) for making a backup of your town) or a backup of your friends' town (see [tsto_friend_puller](https://github.com/tjac/tsto_friend_puller)). Save the file to the "towns" directory WITHOUT any file extension.
2) Create a folder called `tsto`
3) Download [docker-compose.yml](https://raw.githubusercontent.com/d-fens/tsto_server/refs/heads/master/docker-compose.yml) and [.env](https://raw.githubusercontent.com/d-fens/tsto_server/refs/heads/master/.env) to the `tsto` folder.
4) Download a copy of the APK of the [The Simpsons: Tapped Out game](https://apkpure.com/the-simpsons%E2%84%A2-tapped-out/com.ea.game.simpsons4_row) and place within the `tsto` folder. Make sure it is named 'Tapped Out.apk'
5) Edit the .env file and replace the APK with the name and the IP address with your machine IP.
6) Install the APK on an Android phone or tablet. Optionally, you can play the game on your PC by using [BlueStacks](https://www.bluestacks.com/download.html) or equivalent emulator.
7) Run `docker-compose up -d` from a command prompt in the `tsto` folder.
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

* Only works with Android since you need to modify the APK to point to the new server.
* This is SUPER alpha. There are bugs and the code is fragile. Please report any bugs you find.
