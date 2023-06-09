#!/usr/bin/bash
function view_image {
  feh "$1" -g 640x480 -.
}

if [[ $# -ne 1 ]]; then
    echo "Usage: ./ViewImage.sh <path_to_image_file>" 
    exit 1
fi

view_image "$1"

