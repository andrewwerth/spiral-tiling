""" Spiral Tiling Function and Command Line utility

This file provides the function spiral_tiling() which allows you to create
spiralized tilings from an initial tile image. It was inspired by a paper
and talk by Craig S. Kaplan:

    Escher-Like Spirla Tilings
    https://isohedral.ca/escher-like-spiral-tilings/

You can also run the program from the command line to generate tilings

Author: Andrew Werth
"""

import matplotlib.pyplot as plt
import numpy as np
import argparse

def spiral_tiling(tile, a=3, b=5, xrange=(-30,30), yrange=(-30,30), size=(3000,3000), scale=1):
    """ Create a spiral tiling from an initial tile image

    Args:
        tile: An image stored in a numpy array
        a (int): The 'a' parameter, an integer used to determine part of the spiral
        b (int): The 'b' parameter, an integer used to determine part of the spiral
        xrange (int,int): A tuple specifying the range of the real (x) axis
        yrange (int,int): A tuple specifyingn the range of the imaginary (y) axis
        size (int,int): A tuple specifying the height and width of the final spiral image
        sclae (int): Used to scale the spiral
        file_loc (str): The file location of the spreadsheet

    Returns:
        ndarray: The spiralized image
    """

    two_pi = 2 * np.pi

    # Build up z to hold complex plane between xrange & yrange
    x = np.linspace(xrange[0], xrange[1], size[0])
    y = np.linspace(yrange[0], yrange[1], size[1])
    zm = np.meshgrid(x, y)
    z = zm[0] + zm[1] * 1j

    # Take the inverse of the exponential function
    zinv = np.log(z)

    # Rotate to align vector a+bi so it lines up with imaginary axis
    # by multiplying by b+ai and scaling by the length
    zinv = zinv * (b + a * 1j) 

    # Scale so that the imaginary axis lines up with tile size
    zinv = zinv * (tile.shape[0] * scale / two_pi)

    # Get the real and imaginary components & wrap into the tile 
    xi = np.uint32(np.real(zinv) % tile.shape[1])
    yi = np.uint32(np.imag(zinv) % tile.shape[0])

    # Build the final image by indexing into the tile
    img = tile[yi, xi]
    return img

def main():
    parser = argparse.ArgumentParser(prog='spiralize.py',
                                 description='Generate Escher-like spiral tiles')
    parser.add_argument('-o', '--outfile', default="", type=str, 
                        help="File to save image to; show image on screen if not specified")
    parser.add_argument('-a', default=3, type=int,
                        help="Parameter 'a' for scaling/rotating spiral")
    parser.add_argument('-b', default=5, type=int,
                        help="Parameter 'b' for scaling/rotating spiral")
    parser.add_argument('-s', '--size', default=(3000,3000), nargs=2, type=int,
                        help="Size in pixels of final image, width height")
    parser.add_argument('--scale', default=20, type=int,
                        help="Scaling factor to adjust spiral fit in image size")
    parser.add_argument('-r', '--range', default=30, type=int,
                        help="Boundary of complex plane will be +/- range")
    parser.add_argument('-t', '--tile', default='tile.png', type=str,
                        help="The image used as a tile for spiraling")
    args = parser.parse_args()
    outfile = args.outfile
    a = args.a
    b = args.b
    size = args.size
    scale = args.scale
    zrange = args.range
    tilefile = args.tile
    
    tile = plt.imread(tilefile)
    img = spiral_tiling(tile, a, b, xrange=(-zrange,zrange), yrange=(-zrange,zrange), size=size, scale=scale)

    if outfile:
        plt.imsave(outfile, img, cmap='gray')
    else:
        plt.figure(figsize=(8, 8))
        plt.imshow(img, cmap='gray')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()
