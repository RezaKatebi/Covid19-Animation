#------------------------------------------------------
#   
#   Shell script to make a movie
#   (c) Katebi&Rezaie Co.
#   
#   Steps
#           1. make frames in png
#           2. use ffmpeg to combine them into mp4
#
#------------------------------------------------------

# Choose the theme: options are `dark` or `light`
theme=dark
echo "theme: "${theme}

# Run app.py
python app.py -m -t ${theme} 

# Run ffmpeg
dir=${PWD}/frames
output_name=Covid19_${theme}.mp4
echo "movie : "${output_name}

echo "change to "${dir}
cd ${dir}
#ffmpeg -pattern_type glob -framerate 6 -i ${theme}_"**.png" -c:v h264 -r 10 -s 1920x1080 -pix_fmt yuv420p ${output_name}
