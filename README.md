# Spiral Tiling

Create conformal map visualizations using logarithmic spiral transformations.

This simple tool was inspired by a paper and talk by Craig S. Kaplan:

    Escher-Like Spiral Tilings
    https://isohedral.ca/escher-like-spiral-tilings/

It contains a function you can import or run from the command line as well as a
very rudimentary GUI (built with NiceGUI) that lets you invoke the spiralzing function,
load a new tile from disk, and save (download) generated images.

## Installation

You can just copy the file spiralize.py and use it as long as you have 
matplotlib & numpy installed. If you want to use the GUI, you'll need to
also install the python library NiceGUI (which itself has a whole lot 
of other dependencies), via pip or uv.


## Usage

### GUI (NiceGUI)
```bash
python spiralgui.py
```

### Command Line
```bash
usage: python spiralize.py [-h] [-o OUTFILE] [-a A] [-b B] [-s SIZE SIZE] [--scale SCALE] [-r RANGE] [-t TILE]

Generate Escher-like spiral tiles

options:
  -h, --help            show this help message and exit
  -o, --outfile OUTFILE
                        File to save image to; show image on screen if not specified
  -a A                  Parameter 'a' for scaling/rotating spiral
  -b B                  Parameter 'b' for scaling/rotating spiral
  -s, --size SIZE SIZE  Size in pixels of final image, width height
  --scale SCALE         Scaling factor to adjust spiral fit in image size
  -r, --range RANGE     Boundary of complex plane will be +/- range
  -t, --tile TILE       The image used as a tile for spiraling

```

### As a Library
```python
import spiralize as sp
import matplotlib.pyplot as plt

tile = plt.imread("tile.png")
img = sp.spiral_tiling(tile, a=4, b=7, scale=3)
plt.imshow(img)
plt.show()
```

## Parameters

- `a`, `b`: Control the spiral shape
- `scale`: Texture scale factor

## Examples

![Example 1](examples/example1.png)

## License

MIT License
```