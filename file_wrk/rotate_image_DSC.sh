# ! /bin/sh
echo "starting script"
for f in DSC* ;do
echo "rotating $f ..."
convert $f -auto-orient -quality 100 $f
done
