#!/bin/sh
# Turn a Google Flow clip into web banner files for the site (needs ffmpeg).
# Usage:  sh _builder/encode_video.sh <input.mp4> <name> <start-seconds> <end-seconds>
# Example: sh _builder/encode_video.sh ~/Downloads/Jodhpur_lanes_1080p.mp4 jodhpur 0.8 7.9
# Makes:  website/assets/video/<name>-hd.mp4 (1280x720) and <name>-sm.mp4 (768x432, phones)
#         website/assets/img/poster-<name>(.webp/.avif) and poster-<name>-sm(.webp/.avif), shown while the video loads
# - Crops a 16:9 frame that stops just before the Flow sparkle mark in the bottom-right corner
#   (the mark sits at x 1704-1776, y 864-936 on 1920x1080 clips). Set CROP=none to keep the full frame.
# - The last 0.8 s fades back into the start, so the clip loops without a jump.
# - Pick start/end to skip any morph or cut that Flow adds at the beginning of a clip.
set -e
IN="$1"; NAME="$2"; A="$3"; B="$4"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/website/assets/video"; IMG="$ROOT/website/assets/img"
mkdir -p "$OUT"
F=0.8
OFF=$(awk "BEGIN { print $B - $A - 2 * $F }")
if [ "${CROP:-flow}" = "none" ]; then PRE=""; else PRE="crop=1696:954:0:63,"; fi
for spec in 1280:720:hd:27:1800k 768:432:sm:28:750k; do
  W=$(echo "$spec" | cut -d: -f1); H=$(echo "$spec" | cut -d: -f2); TAG=$(echo "$spec" | cut -d: -f3)
  CRF=$(echo "$spec" | cut -d: -f4); MAX=$(echo "$spec" | cut -d: -f5)
  ffmpeg -v error -y -i "$IN" -filter_complex \
    "[0:v]trim=start=$A:end=$B,setpts=PTS-STARTPTS,fps=24,${PRE}scale=$W:$H:flags=lanczos,format=yuv420p,split[x][y];[x]trim=start=$F,setpts=PTS-STARTPTS[main];[y]trim=end=$F,setpts=PTS-STARTPTS[head];[main][head]xfade=transition=fade:duration=$F:offset=$OFF[v]" \
    -map "[v]" -an -c:v libx264 -profile:v high -preset veryslow -tune film -crf "$CRF" -maxrate "$MAX" -bufsize "$MAX" -g 48 \
    -movflags +faststart -pix_fmt yuv420p "$OUT/$NAME-$TAG.mp4"
done
ffmpeg -v error -y -i "$OUT/$NAME-hd.mp4" -frames:v 1 -c:v libwebp -quality 62 -compression_level 6 "$IMG/poster-$NAME.webp"
ffmpeg -v error -y -i "$OUT/$NAME-sm.mp4" -frames:v 1 -c:v libwebp -quality 62 -compression_level 6 "$IMG/poster-$NAME-sm.webp"
ffmpeg -v error -y -i "$OUT/$NAME-hd.mp4" -frames:v 1 -c:v libaom-av1 -still-picture 1 -crf 35 -cpu-used 5 -pix_fmt yuv420p "$IMG/poster-$NAME.avif"
ffmpeg -v error -y -i "$OUT/$NAME-sm.mp4" -frames:v 1 -c:v libaom-av1 -still-picture 1 -crf 33 -cpu-used 5 -pix_fmt yuv420p "$IMG/poster-$NAME-sm.avif"
echo "done: $NAME"
