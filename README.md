
# Nasa-discord Bot 🚀

This Python script is a Discord bot designed to bring the wonders of space right to your Discord server! 🌌 Built using the `discord.py` library, this bot interacts with various NASA APIs to fetch and display space-related information and images. Get ready to explore the cosmos with commands that are both educational and entertaining! 🌠

**Main Features:**
1. **Curiosity Rover Images 📸:**
   - Command: `!cur [sol date] [camera]`
   - Fetches stunning images taken by the Curiosity rover on Mars based on the specified sol (Martian day) and camera.
   - Valid cameras: FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM.

2. **Astronomy Picture of the Day (APOD) 🌠:**
   - Command: `!apod`
   - Retrieves and displays the mesmerizing Astronomy Picture of the Day from NASA's APOD API.

3. **International Space Station (ISS) Information 🛰️:**
   - Command: `!iss location` - Provides the current location, velocity, and other cool details of the ISS.
   - Command: `!iss people` - Lists the astronauts currently aboard the ISS. 👩‍🚀👨‍🚀

4. **Miscellaneous Commands 🎉:**
   - `!motd [message]` - Change the bot's status message to keep it fresh! 📝
   - `!say [message]` - Make the bot say whatever you want in the channel. Yep, anything! 🗣️
   - `!sendmsg` - Send direct messages to specified user IDs. 💌
   - `!deside [option1] [option2]` - Can't decide? Let the bot choose for you! 🤔
   - `!tts [message]` - Use text-to-speech to play a message in a voice channel. 🎙️
   - `!play` - Play MP3 files from a local folder in a voice channel. 🎵
   - `!dc` - Disconnect the bot from the voice channel. 👋

**Error Handling 🛠️:**
- Includes error handling for missing required arguments in commands, providing helpful feedback to users. 🛡️

**Configuration ⚙️:**
- The bot's configuration is stored in a `config.ini` file, which includes settings for the bot name, profile picture, default activity, Twitch username, bot secret, command prefix, and NASA API key. Customize it to suit your needs!

**Usage 🚀:**
- Customize the `config.ini` file with your desired settings, restart the bot, and embark on your interstellar journey! 🌌

---

This description adds a fun and engaging touch to the functionalities of the Discord bot script. 
