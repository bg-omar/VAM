@echo off
echo Converting all .gif to .png (first frame only) using ImageMagick...

for %%f in (*.gif) do (
    echo Processing %%f...
    magick "%%f[0]" "%%~nf.png"
)

echo Done.
pause
