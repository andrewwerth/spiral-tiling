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
    img = sp.spiral_tiling(tile, a, b, xrange=(-30,30), yrange=(-30,30), 
                        size=IMAGE_SIZE, scale=scale)
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
    
with ui.row().classes('w-full gap-4 p-4'):
    ui.button("Spiralize", on_click=lambda: generate_spiral())

    ui.label("Scale")
    scale_slider = ui.slider(min=1, max=10, value=3).props('label-always').classes('flex-1')
    ui.label("a")    
    a_slider = ui.slider(min=0, max=40, value=5).props('label-always').classes('flex-1')
    ui.label("b")
    b_slider = ui.slider(min=0, max=40, value=7).props('label-always').classes('flex-1')

with ui.row().classes('w-full items-center'):
    initial_img = np.zeros((200,200,3), dtype=float)
    spiral_img = ui.image(numpy_to_base64(initial_img)).style('max-width: 600px; max-height: 600px;')
    # with ui.upload(on_upload=handle_upload_tile, auto_upload=True, label="Load Tile").props('flat accept="image/*"').classes('flex-1') as upload:
    #     ui.button('Load Tile', icon='upload', on_click=lambda: upload.run_method('pickFiles'))
    ui.upload(on_upload=handle_upload_tile, auto_upload=True, label="Load Tile").props('flat accept="image/*"').classes('flex-1')

with ui.row().classes('w-full gap-4 p-4'):
    ui.button("Save", on_click=save_image)


ui.run(
    title="Spiralized Tilings",
)
