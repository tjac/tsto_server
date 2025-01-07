This is a VERY alpha release of a local server that allows you to play your Springfield in the Simpsons: Tapped Out mobile app. 

# How to Setup and Use
Before you run this program, you will need a few things:

1) A copy of your world (see teamtsto.org for making a backup of your town) or a backup of your friends' town (see [tsto_friend_puller](https://github.com/tjac/tsto_friend_puller)). Save the file to the "towns" directory WITHOUT any file extension.
3) Install the required packages using the pip command: ```pip install -r requirements.txt```
4) Download a copy of the APK of the [The Simpsons: Tapped Out game](https://apkpure.com/the-simpsons%E2%84%A2-tapped-out/com.ea.game.simpsons4_row)
5) Modify the APK to point to your instance of the TSTO server (see APK generation below)
6) Install the APK on your Android phone or tablet. Optionally, you can play the game on your PC by using [BlueStacks](https://www.bluestacks.com/download.html).

Once you have done the above, execute the server by using the following command:

```python tsto_server.py http://x.x.x.x ```

again where ```x.x.x.x``` is the IP address or domain name of the computer hosting the server.

Run your modified APK on your Android device.

# APK generation
In order to use this server, you will need to modify the game APK to point to your local computer. The TappedOutReborn group has provided a very handy tool for generating the modified APK here: [Patch-Apk](https://github.com/TappedOutReborn/Patch-Apk).  When using the install.sh script set the NEW_GAMESERVER_URL (e.g. ```http://x.x.x.x```) to the IP address or domain of the machine hosting your server and set NEW_DLCSERVER_URL as ```http://oct2018-4-35-0-uam5h44a.tstodlc.eamobile.com/netstorage/gameasset/direct/simpsons/``` Note that the NEW_DLCSERVER_URL is still using the EA servers for now. This will be changed in the next release. Do not use 127.0.0.1 or localhost for your server's address.


# How to play
The system currently leverages the login AND anonymous play system to allow users to select different worlds to play. By default, clicking the "Tap to play anonymously" will load the "mytown" world. If the user wants to play a different town, they should click the EA Login button, then enter an email address that has the username equal to the town's filename in the towns directory. For example, if you want to load a town with the filename "mysupertown" then you would enter "mysupertown@a.a". The @ and . are required by the TSTO application, so any random domain will work. On the next screen, after pressing the "Log In" button, enter any 5 digit code and press "Verify". This will place the user back at the main screen. At this point pressing the "Tap to play anonymously" will load the newly selected world.

Users of the server have the ability to modify the config.json file to change certain behaviors of the system. Feel free to experiement with those options.

Admittedly this is a fragile system. It is definitely a work in progress.

# Current state:
* Only works with Android since you need to modify the APK to point to the new server.
* Any changes you make to your town will not be saved. It will reset to the original state each time.
* This is SUPER alpha. There are bugs and the code is fragile. Please report any bugs you find.
  
# Change log:
* [2024/12/24] - Initial release
* [2025/1/1] - Refactored code. Established framework for persistent configs. Multiple towns can be played by using the login system in the app
* [2025/1/6] - Save functionality! Big thanks to [d-fens](https://github.com/d-fens) for setting the framework necessary to dockerize the server.