#!/bin/bash

video_recorder="selenoid/video-recorder:latest-release"
browsers=("selenoid/chrome:latest")

download_browsers() {
    for browser in "${browsers[@]}"; do
        docker pull "${browser}"
    done
}

if [ "$1" = "up" ]; then
    mkdir -p "reports/video/" -p "reports/logs/" || echo 'win'
    docker pull ${video_recorder}
    download_browsers
    docker-compose -f selenoid-compose.yml up --detach
elif [ "$1" = "down" ]; then
    docker-compose -f selenoid-compose.yml down -v
elif [ "$1" = "update" ]; then
    download_browsers
elif [ "$1" = "clean" ]; then
    docker system prune -af
else
    echo "Command '$1' not found"
fi
