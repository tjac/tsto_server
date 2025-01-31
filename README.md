This is a VERY alpha release of a local server that allows you to play your Springfield in the Simpsons: Tapped Out mobile app. 

# How to Setup and Use
Before you run this program, you will need a few things:

1) A copy of your world. Save the file to the "towns" directory WITHOUT any file extension. If you don't have your town it is too late to get it. You can leave the towns directory empty and start over with a new world... this time with a LOT of donuts.
2) Make a directory named "gameassets" in the server's directory and copy ALL of the DLC to this directory. The Internet Archive has a [copy](https://archive.org/details/tsto-dlc-cdn-oct2024)
3) Install the required packages using the pip command: ```pip install -r requirements.txt```
4) Download a copy of the APK of the [The Simpsons: Tapped Out game](https://apkpure.com/the-simpsons%E2%84%A2-tapped-out/com.ea.game.simpsons4_row)
5) Modify the APK to point to your instance of the TSTO server (see APK generation below)
6) Install the APK on your Android phone or tablet. Optionally, you can play the game on your PC by using [BlueStacks](https://www.bluestacks.com/download.html).
7) Modify the config.json file to point to your IP address (change 10.10.10.10 to your IP address!):
```
  "server_url": "http://10.10.10.10"
```

Once you have done the above, execute the server by using the following command:

```python tsto_server.py```

Run your modified APK on your Android device.

# APK generation
In order to use this server, you will need to modify the game APK to point to your local computer. The TappedOutReborn group has provided a very handy tool for generating the modified APK here: [Patch-Apk](https://github.com/TappedOutReborn/Patch-Apk). When using the install.sh script set both the NEW_GAMESERVER_URL to the IP address or domain of the machine hosting your server (e.g. ```http://x.x.x.x```) and NEW_DLCSERVER_URL to the same but with /gameassets/ appended (e.g. ```http://x.x.x.x/gameassets/```). Do not use 127.0.0.1 or localhost for your server's address.


# How to play
The system currently leverages the login AND anonymous play system to allow users to select different worlds to play. By default, clicking the "Tap to play anonymously" will load the "mytown" world. If the user wants to play a different town, they should click the EA Login button, then enter an email address that has the username equal to the town's filename in the towns directory. For example, if you want to load a town with the filename "mysupertown" then you would enter "mysupertown@a.a". The @ and . are required by the TSTO application, so any random domain will work. On the next screen, after pressing the "Log In" button, enter any 5 digit code and press "Verify". This will place the user back at the main screen. At this point pressing the "Tap to play anonymously" will load the newly selected world.

Users of the server have the ability to modify the config.json file to change certain behaviors of the system. Feel free to experiement with those options.

Admittedly this is a fragile system. It is definitely a work in progress.

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
