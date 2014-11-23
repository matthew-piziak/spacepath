convert -delay 2 -loop 0 *screen.png $1
convert $1 -resize %50 $1
gnome-open $1
