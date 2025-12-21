#!/usr/bin/env python

# Rudimentary graphical user interface to let you create spiralized tiled images
# Uses nicegui for the front end
# © 2025 Andrew Werth

import spiralize as sp
import matplotlib.pyplot as plt
import numpy as np
import base64
from PIL import Image
from nicegui import ui, events
from io import BytesIO

#tile = plt.imread("tile9.png")

BASE64_PREFIX = 'data:image/png;base64,'
IMAGE_SIZE = (2400,2400)

FUNCS = {"Log": np.log,
         "Sqrt": np.sqrt,
         "Squared": np.square,
         "Absolute": np.absolute,
         "Inverse": lambda z:  1/ (z + (z == 0)),
         "Mobius": lambda z: np.log((0.5 * z + 3) / (0.3 * z - 3)),
         "Exponential": np.exp}

# Convert to base64 PNG
def numpy_to_base64(img_array):
    # Save to bytes buffer as PNG
    buf = BytesIO()
    plt.imsave(buf, img_array, cmap='gray', format='png')
    buf.seek(0)
    
    # Encode to base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f'{BASE64_PREFIX}{img_base64}'

# Handles the callback from the Save button to save the image
# by causing it to be downloaded in the browser-based interface
def save_image():
    img_data = spiral_img.source
    
    # Remove the data URL prefix to get just the base64 string
    if img_data.startswith(BASE64_PREFIX):
        img_data = img_data.replace(BASE64_PREFIX, '')
    
    # Trigger browser download
    filename = f'spiral_scale{scale_slider.value}_a{a_slider.value}_b{b_slider.value}.png'

    ui.download(base64.b64decode(img_data), filename)
    ui.notify(f"Image downloaded locally: '{filename}'")

# Grabs the values from the UI elements, generates the spiral, and displays the result
def generate_spiral():
    a = a_slider.value
    b = b_slider.value
    scale = scale_slider.value
    xr = (xrange_slider.value["min"], xrange_slider.value["max"])
    yr = (yrange_slider.value["min"], yrange_slider.value["max"])
    func = FUNCS[function_select.value]

    img = sp.spiral_tiling(tile, a, b, xrange=xr, yrange=yr, 
                        size=IMAGE_SIZE, scale=scale, func=func)
    spiral_img.set_source(numpy_to_base64(img))

# Handler for when user uploads a new tile image
async def handle_upload_tile(e: events.UploadEventArguments):
    global tile
    content = await e.file.read()    
    buf = BytesIO(content)
    tile = np.asarray(Image.open(buf))
    ui.notify(f'Loaded: {e.file.name}')
    generate_spiral()

# Build up the user interface with UI elements

with ui.row().classes('w-full'):
    with ui.column().classes('items-center').style('width: 800px;'):
        initial_img = np.zeros((600,600,3), dtype=float)
        spiral_img = ui.image(numpy_to_base64(initial_img)).style('max-width: 800px; max-height: 800px;')
    with ui.column().classes('gap-6 p-4').style('min-width: 400px;'):
        ui.button("Spiralize", on_click=lambda: generate_spiral())
        with ui.row().classes('items-center gap-2 mb-2 w-full'):
            ui.label("Scale").classes('w-16')
            scale_slider = ui.slider(min=1, max=10, value=3).props('label-always').classes('flex-1')
        with ui.row().classes('items-center gap-2 mb-2 w-full'):
            ui.label("a").classes('w-16')
            a_slider = ui.slider(min=0, max=40, value=5).props('label-always').classes('flex-1')
        with ui.row().classes('items-center gap-2 mb-2 w-full'):
            ui.label("b").classes('w-16')
            b_slider = ui.slider(min=0, max=40, value=7).props('label-always').classes('flex-1')
        with ui.row().classes('items-center gap-2 mb-2 w-full'):
            ui.label("x-range").classes('w-16')
            xrange_slider = ui.range(min=-100, max=100, value={"min": -30, "max": 30}).props('label-always').classes('flex-1')
        with ui.row().classes('items-center gap-2 mb-2 w-full'):
            ui.label("y-range").classes('w-16')
            yrange_slider = ui.range(min=-100, max=100, value={"min": -30, "max": 30}).props('label-always').classes('flex-1')
        with ui.row().classes('items-center gap-2 mb-2 w-full'):
            ui.label("Function").classes('w-16')
            function_select = ui.select(list(FUNCS.keys()), value="Log")

        ui.upload(on_upload=handle_upload_tile, auto_upload=True, label="Load Tile").props('flat accept="image/*"').classes('flex-1')
        ui.button("Save", on_click=save_image)

ui.run(
    title="Spiralized Tilings",
)
