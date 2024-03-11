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
python src/dt_format_message_data.py $HOME/path/to/zip/files/merged
```

```bash
python src/dt_group_message_data.py $HOME/path/to/zip/files/merged
```

---

### dt_rename_messenger_folders

`dt_rename_messenger_folders` renames the folders from their original name to more readable one. Then appends an increment number to the end just to avoid duplicates.
For example if the title of the chat is "Group Chat With Lots of People" it would become "GroupChatWithLotsofPeople-1"

There's no sort of error handling so if it fails to find a `message_1.json` file it just renames it to `-<N>` (N being whatever increment the script is on).

You can run the `dt_rename_messenger_folders.sh` before running the `dt_format_message_data.py`/`dt_group_message_data.py`.

```bash
./src/dt_rename_messenger_folders.sh $HOME/path/to/zip/files/merged
```

---

### dt_sort_media

The last bit of data transformation you can do run is the `dt_sort_media.py`. This renames all the media in a groups folder to be the sender name and timestamp of the message, it's not totally necessary howver if you're running one of the result generator scripts it makes the output a bit nicer to read.

```bash
python src/dt_sort_media.py $HOME/path/to/specific/group/chat/folder
```

## Result Generators

These scripts take a few common params for them to be able to run, those are:

-   `--file`
    -   Is a path to the json file you want to read.
        -   Bad name really as you can pass it a directory and it'll read all `message.json` in there.
    -   type = `string`
    -   required = `true`
-   `--multichat`
    -   If you want to read multiple group chats you can set this to `true`
        -   Doing so will change the function of `--file`, that file you pass in needs be a json file that is just an array of paths to read. Like this:
            -   `["/path/to/group/chat/folder-a/", "/path/to/group/chat/folder-b/", ... ]`
    -   type = `boolean`
    -   required = `false`
-   `--drstart`
    -   If you want to limit the results to certain dates you can pass a date into this `date range start` value.
        -   The format needs to be in `yyyy-mm` format, like so `2000-12`.
    -   You don't need to pass in both a date range start and date range end for this to work.
        -   It defaults to using `2000-01`.
    -   type = `boolean`
    -   required = `false`
-   `--drend`
    -   If you want to limit the results to certain dates you can pass a date into this `date range end` value.
        -   The format needs to be in `yyyy-mm` format, like so `2020-12`.
    -   You don't need to pass in both a date range start and date range end for this to work.
        -   It defaults to using the current year and month.
    -   type = `boolean`
    -   required = `false`

### rg_activity_monitor

The `rg_activity_monitor` script does a handful of smaller functions to get specific answers to things, the availble functions at the moment are:

-   longest-message
    -   Gets the longest message sent to the chat.
-   most-active
    -   Gets the most active participant in the chat.
-   yearly-message-count
-   -   Gets the number of messages sent a year, for each year from the first message to the current year.
-   average-messages
    -   Gets the average number of messages a day.
-   busiest-day
    -   Gets the total message sent on each day.

It doesn't write these to results files like the others.

```bash
python src/rg_activity_monitor.py /path/to/group/chat/folder/
```

**Additional Params**

-   `--function`
    -   Choices string to select your function.
        -   `longest-message`, `most-active`, `yearly-message-count`, `average-messages`, `busiest-day`.
    -   type = `boolean`
    -   required = `false`

---

### rg_media_mogul

The `rg_media_mogul` script reads through the messages and counts up how much media has been sent, including a break down of what media (photos, videos, etc.). Then it reports back who's sent the most for each of the media types.

Writes the results to `media_mogul_results.json` when it's finished.

```bash
python src/rg_media_mogul.py /path/to/group/chat/folder/
```

**Additional Params**

-   `--participant`
    -   Get a certain participants media.
    -   type = `string`
    -   required = `false`
-   `--mediatype`
    -   Choices string to choose a specific media type.
        -   `photos`, `videos`, `files`, `audio`,`gifs`.
    -   Defaults to all media types.
    -   type = `string`
    -   required = `false`

---

### rg_nicknamers

This script gathers a handful of stats about the nicknames that have been set in group chat.

-   Counts how many nickanmes a participant has had as well as how many they've set.
-   All nicknames each participant has.
-   The 3 oldest nicknames.

Writes the results to `media_mogul_results.json` when it's finished.

```bash
python src/rg_nicknamers.py /path/to/group/chat/folder/
```

**Additional Params**

_None_

---

### rg_potty_patrol

The `rg_potty_patrol` script reads through the message data and counts how many times certain words appear in the messages.
It returns 2 data sets:

-   How many times each word appears across the message data.
-   How many times each participant has said each word.

Writes the results to `potty_patrol_results.json` when it's finished.

```bash
python src/rg_potty_patrol.py /path/to/group/chat/folder/
```

**Additional Params**

-   `--pottyfile`
    -   Path to where your list of potty words live.
        -   Needs to be in json array format, like this:
            -   `["foo","bar"]`
    -   type = `string`
    -   required = `true`

---

### rg_reactionator

The `rg_reactionator` script gathers up information about messages that have been reacted to.
It returns a list of all reacted messages along with:

-   How many times each participant has reacted in total.
-   How many times each participant has reacted using a specific emoji.
-   For each participant a count of how many times each participant has reacted to them.

When you're selecting your emoji, it breaks the choice down into these emojis:

-   laugh
    -   😅, 😂, 🤣, 😆
-   heart
    -   😍, ❤, 💜, 💗, 🥰, 💛, 💙, 💚
-   thumb
    -   👍, 👍🏻 ,👍🏾, 👍🏽, 👍🏼, 👍🏿
-   shock
    -   😲, 🤯, 😮
-   anger
    -   🤬, 😠

Writes the results to `reactionator_results.json` when it's finished.

```bash
python src/rg_reactionator.py /path/to/group/chat/folder/
```

**Additional Params**

-   `--emojis`
    -   Choices string to select which emoji to count.
        -   `laugh`, `heart`, `thumb`, `shock`, `anger`
    -   default = `laugh`
    -   type = `string`
    -   required = `false`
-   `--saveallreacts`
    -   Save all the reacted messages in the json.
    -   default = `false`.
    -   type = `boolean`
    -   required = `false`
-   `--saveallemojis`
    -   Save all the emojis messages in the json.
    -   Defaults to `false`.
    -   type = `boolean`
    -   required = `false`

---

### rg_unique_words

This script needs a bunch more time in the oven, it does a word count on all the messages and prints a list of them all along with their count.

```bash
python src/rg_unique_words.py /path/to/group/chat/folder/
```

**Additional Params**

_None_

## TODO

-   Update date readme with the correct files that get generated
-   Add the black heart to the heart emojis
-   Fix the disk size check in the unzip and merge script
-   update emojis in the list
