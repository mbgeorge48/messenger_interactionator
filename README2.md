# Messenger Interactionator

This is a collection of scripts that do various things to the JSON data you can export from Facebook Messenger

It's supposed to be a bit of fun between me and some friends but thought I'd share it incase anyone else fancied using it

It's split into 2 types of script:
* Data Transformations
    * Prefixed with `dt_`
* Result Generator
    * Prefixed with `rg_`

Two of the scripts are shell scripts because it just felt easier to do it that way

---

## Data Transformations

These exist to make getting the results easier. If you've you Facebook Messenger and ever downloaded your data you'll probably know that Facebook give it to you in a handful of bitesized chunks.
The `dt_unzip_and_merge.sh` script takes all the all the zip files, unzips them and pushes them all together to make one bit `merged` folder.

If you're following along at home you want to start with that one. You can do so by running:

```bash
./src/dt_unzip_and_merge.sh $HOME/path/to/zip/files/
```

The script can do other stuff but tbh they're more of an after thought so don't fully work, e.g. it can zip up the `merged` folder then delete all the left over files.

After you've unzipped everything you'd want to run `dt_rename_messenger_folders.sh`, this just adds a few quality of life changes to the script.
* Combines all the `message_N.json` into one giant `combined_messages.json` file.
    * You don't actually require this anyone but originally this was used in the result generators.
* Encodes all the emojis so you can see what they actually are.
* Renames the audio media key from `audio_files` to just `audio`.
* Adds a timestamp_converted key with a readable timestamp.

```bash
./src/dt_rename_messenger_folders.sh $HOME/path/to/zip/files//merged
```


## Groupa

Takes all the messages files and combines them all into combined_messages.json
Also makes sure emojis are encoded properly
Renames the audio_files key to just audio

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
