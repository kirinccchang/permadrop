#!/bin/bash

# Optimized script to create GIF from static screenshots for documentation
# Best settings: 1s delay, 256 colors, loop, consistent sizing

if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg is not installed. Install with: brew install ffmpeg"
    exit 1
fi

if [ $# -lt 2 ]; then
    echo "Usage: $0 <input_image1> <input_image2> ... <output.gif>"
    exit 1
fi

output="${@: -1}"
inputs=("${@:1:$#-1}")

# Build input args
input_args=""
for img in "${inputs[@]}"; do
    input_args="$input_args -i $img"
done

# Optimized: framerate 1 (1s per frame), scale to 800px, 256 colors, loop
eval "ffmpeg -y $input_args -filter_complex \"concat=n=$(( $# - 1 )):v=1:a=0,scale=800:-1:force_original_aspect_ratio=decrease,pad=800:ih:(ow-iw)/2\" -r 1 -colors 256 -loop 0 \"$output\""

echo "Optimized GIF created: $output (1s per frame, 256 colors, looped)"