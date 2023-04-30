# Messenger Interactionator

## Messenger Nickname Parser

This is a simple script that is designed to read in a json dump of a Facebook messenger group chat then pull the nicknames out so you can see who's been called what

It's supposed to be a bit of fun between me and some friends but thought I'd share it incase anyone else fancied using it

```bash
python3 messenger_nickname_parser.py /path/to/messages.json
```

## Unzippa

When you do export your data from Facebook it gives it to you in a tonne of smallish (around 2 to 3 gb) zips files
This script unzips them all and merges them all into one folder
Then it can rezip up the merged folder and delete the extra stuff it created along the way
Comment and uncomment the function calls to dictate which ones are ran

```bash
./unzippa.sh $HOME/path/to/zip/files
```

## Groupa

Takes all the messages files and combines them all into combined_messages.json
Also makes sure emojis are encoded properly
Renames the audio_files key to just audio
Adds a timestamp_converted key with a readable timestamp

```bash
python3 groupa.py path/to/the/merged/folder/made/by/unzippa
```

## Media sorta

Goes through the photos, gifs, videos, files and audio folder and renames them to be the timestamp and senders names
Also updates the combined_messages.json file with the new names

```bash
python3 media_sorta.py path/to/the/chat/folder/maybe/messages/inbox/chat

OR

python3 media_sorta.py path/to/the/chat/folder/maybe/messages/inbox/ -a
```

## Renamed ya

Renames all the chats in indox to their chat name (using the title field in combined_messages.json)
Adds an increment number to the end incase of duplcates
Doesn't handle errors really so will just rename a folder to the increment number if there is no combined_messages file

```bash
./renamed_ya.sh path/to/the/folder/inside/the/merged/messenger/folder
```

## Unique words

Bit of a WIP but just does a word count on all the messages and prints a list of them all along with their count

```bash
python3 unique_words.py /path/to/messages.json
```

# Order of play

-   Uncomment the functions you want in `unzippa.sh`
    -   By default you'd probably want `unzip_time` and `merging_time`
-   Now you want to run the `groupa.py` on the `merged` folder that gets created in the previous step
-   After `combined_messages.json` has been generated you want to run `renamed_ya.sh` to give all the message groups nicer names
-   Finally you can run `media_sorter.py` on all the messenger groups to rename all the media
-   If you really want you can uncomment `rezip` and `tidy_up` and comment out `unzip_time` and `merging_time` in `unzippa.sh`
