#!/bin/bash

[[ -z "$1" ]] && {
    echo "Pass in a directory to scan, i.e. $HOME/Documents/folder"
    exit 1
}

count=0
for folder in $1/messages/inbox/*; do
    CHAT_NAME=$(cat $folder/combined_messages.json | grep '"title":' | cut -d '"' -f4)
    NEW_NAME=$(echo $CHAT_NAME | tr -cd '[:alnum:][:cntrl:]')
    NEW_NAME+="-"
    NEW_NAME+=$count
    echo "Moving $folder to $NEW_NAME"
    mv $folder $1/messages/inbox/$NEW_NAME
    ((count++))
done
