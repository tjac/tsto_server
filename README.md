This is a VERY alpha release of a local server that allows you to play your Springfield in the Simpsons: Tapped Out mobile app. 

# How to Use
Before you run this program, you will need a few things:

1) A copy of your world (see teamtsto.org for making a backup of your town) or a backup of your friends' town (see [tsto_friend_puller](https://github.com/tjac/tsto_friend_puller)). Save the file to the "towns" directory WITHOUT any file extension.
2) Rename the town's file to mytown.pb and store it in the same directory as this script.
3) Install the required packages using the pip command:
   - ```pip install -r requirements.txt```
4) Download a copy of the APK of the game (https://apkpure.com/the-simpsons%E2%84%A2-tapped-out/com.ea.game.simpsons4_row)
5) Modify the APK to point to your local computer (use [Patch-Apk](https://github.com/TappedOutReborn/Patch-Apk)) for the NEW_GAMESERVER_URL (e.g. ```http://1.1.1.1```) but leave the NEW_DLCSERVER_URL as ```http://oct2018-4-35-0-uam5h44a.tstodlc.eamobile.com/netstorage/gameasset/direct/simpsons/dlc/``` (for now)

Once you have done the above, execute the server by using the following command:

```python tsto_server.py 1.1.1.1 ```

where 1.1.1.1 is the IP address of the computer hosting the server.

Run your modified APK on your Android device.

# How to play
The system currently leverages the login vs. anonymous play system to allow users to select different worlds to play. By default, clicking the "Tap to play anonymously" will load the "mytown" world. If the user wants to play a different town, they should click the EA Login button, then enter an email address that has the username equal to the town's filename in the towns directory. For example, if you want to load a town with the filename "mysupertown" then you would enter "mysupertown@a.a". The @ and . are required by the TSTO application, so any random domain will work. On the next screen, after pressing the "Log In" button, enter any 5 digit code and press "Verify". This will place the user back at the main screen. At this point pressing the "Tap to play anonymously" will load the newly selected world.

Admittedly this is a fragile system. It is definitely a work in progress.

# Current state:
* Only works with Android since you need to modify the APK to point to the new server.
* Any changes you make to your town will not be saved. It will reset to the original state each time.
* This is SUPER alpha. There are bugs and the code is fragile. Please report any bugs you find.
  
# Change log:
* [2024/12/24] - Initial release
* [2025/1/1] - Refactored code. Established framework for persistent configs. Multiple towns can be played by using the login system in the app