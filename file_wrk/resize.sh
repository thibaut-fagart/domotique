# ! /bin/sh
echo "starting script"
for f in * ;do
echo "converting $f ..."
convert $f -resize 1280x1024 -quality 100 $f
done
