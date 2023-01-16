#!/bin/bash

function check_space {
    echo "Checking Space"
    for zip in $(find . -type f -name "*.zip"); do
        ((total_space += $(unzip -Zt $zip | awk '{print $6}')))
    done
}

function unzip_time {
    mkdir -p unzipped
    # If the total uncompressed space is less than 70% of the remaining disk space don't start unzipping
    if [ $((DISK_SPACE * 90 / 100)) -gt $total_space ] || [ IGNORE_SPACE_CHECK = true ] then
        echo "Starting to unzip"
        cd /Volumes/Camera\ Roll/fb/
        for zip in $(find . -type f -name "*.zip"); do
            FILE=${zip%.zip*}
            echo "Unzipping $FILE"
            unzip -q $zip -d /Volumes/Camera\ Roll/fb/unzipped/$FILE
        done
    else
        echo $DISK_SPACE
        echo $total_space
        echo "Not enough disk space"
    fi
}

function merging_time {
    cd /Volumes/Camera\ Roll/fb/
    mkdir -p merged
    echo "Starting the merge"
    for folder in unzipped/*; do
        echo "Copying $folder"
        cp -R $folder/ merged
    done
}

function rezip {
    echo "Rezipping"
    zip -r merged-export.zip merged/*
}

function tidy_up {
    echo "Tidying up"
    rm -rf merged unzipped
}

# Would need to be tweaked to make it work on Linux
DISK_SPACE=$(diskutil info /dev/disk3s1s1 | grep 'Container Free Space' | awk '{print substr($6,2) }')
IGNORE_SPACE_CHECK=true

[[ -z "$1" ]] && {
    echo "Pass in a directory to scan, i.e. $HOME/Documents/folder"
    exit 1
}
cd $1

total_space=0

# Comment and uncomment as you go to only run certain functions
check_space
# unzip_time
# merging_time
# rezip
# tidy_up
