# Rec Room Discord Rich Presence
> A **cross-platform** Discord rich presence for Rec Room made with Python! As long as the program is running in the background while Discord is open, it will broadcast your in-game activity to Discord no matter which platform you play on!

## Showcase
The program supports all rooms, including dorm rooms!

![image](https://user-images.githubusercontent.com/13438202/199005404-a6f60f95-bbcd-41b5-a35e-e4bdcd1c845b.png) 

Don't worry if you're in a private room, the program detects that and hides it for you!

![image](https://user-images.githubusercontent.com/13438202/199005024-2e7e4c0b-07da-4e7e-98e5-f3cafb67a128.png)

It can also tell if a game or a quest has begun and how long it has elapsed!

![image](https://user-images.githubusercontent.com/13438202/199006616-68322f8c-054f-4aec-aade-dd0affe3d428.png)

![image](https://user-images.githubusercontent.com/13438202/199006629-98e23d02-43c3-48b1-8c39-1094cf38bae9.png)

It can also tell which platform you are playing on. (PCVR, Screen Mode (PC & consoles), Quest 1 or Quest 2)

As you can see, it's not limited to only PC. As long as the program is running on your PC with Discord open, all in-game activity on the set account will be broadcasted on your Discord!

![image](https://user-images.githubusercontent.com/13438202/199006465-13153f0f-ec77-4a50-9164-fd49d711497a.png)

## Usage
Install the latest release from https://github.com/Jegarde/RecRoomDiscordRPC/releases.

You can either run it as a Python script or a Windows executable!

There are instructions on the `README.txt` provided with the files.

Although 2FA is supported, if you are not interested in inputting an authenticator code each time you run the program, feel free to fill in an alt account's credentials

If you do decide to use an alt account, please input your alt account's username in the provided .env's `ALT_USERNAME` slot.

## Contributing
If you'd like, you can add yours or others rooms on the [supported room JSON](https://github.com/Jegarde/RecRoomDiscordRPC/blob/master/supported_rooms.json)!

It lets you have unique pre-game and in progress statuses for each room.

Make sure you format it correctly!
