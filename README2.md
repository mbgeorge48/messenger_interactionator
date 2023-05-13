# Messenger Interactionator

This is a collection of scripts that do various things to the JSON data you can export from Facebook Messenger

It's supposed to be a bit of fun between me and some friends but thought I'd share it incase anyone else fancied using it

It's split into 2 types of script:

-   Data Transformations
    -   Prefixed with `dt_`
-   Result Generators
    -   Prefixed with `rg_`

Two of the scripts are shell scripts because it just felt easier to do it that way

| [Data Transformations](#data-transformations)               | [Result Generators](#result-generators)           |
| ----------------------------------------------------------- | ------------------------------------------------- |
| [dt_unzip_and_merge](#dt_unzip_and_merge)                   | [rg_activity_monitor.py](#rg_activity_monitor.py) |
| [dt_format_message_data](#dt_format_message_data)           | [rg_media_mogul.py](#rg_media_mogul.py)           |
| [dt_rename_messenger_folders](#dt_rename_messenger_folders) | [rg_nicknamers.py](#rg_nicknamers.py)             |
| [dt_sort_media](#dt_sort_media)                             | [rg_potty_patrol.py](#rg_potty_patrol.py)         |
|                                                             | [rg_reactionator.py](#rg_reactionator.py)         |
|                                                             | [rg_unique_words.py](#rg_unique_words.py)         |

---

## Data Transformations

### dt_unzip_and_merge

These exist to make getting the results easier. If you've you Facebook Messenger and ever downloaded your data you'll probably know that Facebook give it to you in a handful of bitesized chunks.
The `dt_unzip_and_merge.sh` script takes all the all the zip files, unzips them and pushes them all together to make one bit `merged` folder.

If you're following along at home you want to start with that one. You can do so by running:

```bash
./src/dt_unzip_and_merge.sh $HOME/path/to/zip/files/
```

The script can do other stuff but tbh they're more of an after thought so don't fully work, e.g. it can zip up the `merged` folder then delete all the left over files.

---

### dt_format_message_data

After you've unzipped everything you'd want to run either `dt_format_message_data.py` or `dt_group_message_data.py`, these just add a few quality of life changes to the script.

-   Encodes all the emojis so you can see what they actually are.
-   Renames the audio media key from `audio_files` to just `audio`.
-   Adds a timestamp_converted key with a readable timestamp.

I'll eventaully combine the two scripts into one, as the only real difference is `dt_group_message_data` groups all the messenger data into `combined_messages.json`.
You don't need to do that anymore, when I originally made all these scripts it used the grouped up data to get the results.

```bash
./src/dt_format_message_data.py $HOME/path/to/zip/files/merged
```

```bash
./src/dt_group_message_data.py $HOME/path/to/zip/files/merged
```

---

### dt_rename_messenger_folders

`dt_rename_messenger_folders` renames the folders from their original name to more readable one. Then appends an increment number to the end just to avoid duplicates.
For example if the title of the chat is "Group Chat With Lots of People" it would become "GroupChatWithLotsofPeople-1"

There's no sort of error handling so if it fails to find a `message_1.json` file it just renames it to `-<N>` (N being whatever increment the script is on)

You can run the `dt_rename_messenger_folders.sh` before running the `dt_format_message_data.py`/`dt_group_message_data.py`.

```bash
./src/dt_rename_messenger_folders.sh $HOME/path/to/zip/files/merged
```

---

### dt_sort_media

The last bit of data transformation you can do run is the `dt_sort_media.py`. This renames all the media in a groups folder to be the sender name and timestamp of the message, it's not totally necessary howver if you're running one of the result generator scripts it makes the output a bit nicer to read.

```bash
./src/dt_sort_media.py $HOME/path/to/specific/group/chat/folder
```

It's also not 100% tested at the time of writing...

## Result Generators

These scripts take a few common params for them to be able to run, those are:

-   `--file`
    -   Is a path to the json file you want to read
        -   Bad name really as you can pass it a directory and it'll read all `message.json` in there
    -   type = `string`
    -   required = `true`
-   `--multichat`
    -   If you want to read multiple group chats you can set this to `true`
        -   Doing so will change the function of `--file`, that file you pass in needs be a json file that is just an array of paths to read. Like this:
            -   EXAMPLE NEEDED
    -   type = `boolean`
    -   required = `false`
-   ## `--drstart`
    -   1111
    -   type = `boolean`
    -   required = `false`
-   ## `--drend`
    -   2222
    -   type = `boolean`
    -   required = `false`

### rg_activity_monitor

The `rg_activity_monitor` script does a handful of smaller functions to get specific answers to things, the availble functions at the moment are:

-   longest-message
    -   Gets the longest message sent to the chat
-   most-active
    -   Gets the most active participant in the chat
-   yearly-message-count
-   -   Gets the number of messages sent a year, for each year from the first message to the current year
-   average-messages
    -   Gets the average number of messages a day

It doesn't write these to results files like the others.

---

### rg_media_mogul

---

### rg_nicknamers

---

### rg_potty_patrol

---

### rg_reactionator

---

### rg_unique_words

---

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
