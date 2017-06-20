# -*- coding:utf-8 -*-

import input_data
import gzip
import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
from IPython.display import display
from matplotlib import pyplot as pt

def read_image(filename):
    with gzip.open(filename) as bytestream:
        magic = input_data._read32(bytestream)
        num_images = input_data._read32(bytestream)
        rows = input_data._read32(bytestream)
        cols = input_data._read32(bytestream)
        buf = bytestream.read(rows * cols * num_images)
        data = np.frombuffer(buf, dtype=np.uint8)
        # print filename, "rows=" + str(rows) , "cols=" + str(cols) , "nums=" + str(num_images), "len=" + str(len(data))
        data = data.reshape(num_images, rows, cols)
        return data

def print_ndarray(narr):
    print "ndim=" + str(narr.ndim), "size=" + str(narr.size), "shape=" + str(narr.shape)

def to_image(imageBuffer2D):
    return Image.frombuffer('L', imageBuffer2D.shape, imageBuffer2D,'raw', 'L', 0, 1)

def render_images(image_data):
    nums = image_data.shape[0]
    image_full_color = np.full((28,28), 255,dtype=np.uint8)
    for i in range(0, nums):
        display(to_image(image_full_color - image_data[i]))
        
def to_full_image(image_data, draw_grid=True, columns = 25):
    nums = image_data.shape[0]
    width = image_data.shape[1]
    height = image_data.shape[2]
    rows = nums / columns
    if nums % columns > 0:
        rows += 1
    full_width = columns * width
    full_height = rows * height
    full_image = Image.new('RGB', (full_width, full_height), (255,255,255))
    image_full_color = np.full((28,28), 255,dtype=np.uint8)
    for i in range(0, nums) :
        image = to_image(image_full_color - image_data[i])
        x1, x2 = i % columns * width, (i % columns + 1)* width
        y1, y2 = i / columns * height, (i / columns + 1) * height
        box = (x1, y1, x2, y2)
        # 将每个小图片粘贴到大图上
        full_image.paste(image, box)
        
    # 绘制网格线
    if draw_grid: 
        draw = ImageDraw.Draw(full_image)
        grid_color = 'black'
        # 绘制水平网格线
        for i in range(0, rows - 1):
            line = (0, (i + 1) * height, full_width, (i + 1) * height)
            draw.line(line, grid_color, 1)
        # 绘制垂直网格线
        for i in range(0, columns - 1):
            line = ((i + 1) * width, 0, (i + 1) * width, full_height)     
            draw.line(line, grid_color, 1)
        # 绘制边框
        draw.line((0,0, full_width, 0), grid_color, 1)
        draw.line((0,full_height - 1, full_width, full_height - 1), grid_color, 1)
        draw.line((0,0, 0, full_height), grid_color, 1)
        draw.line((full_width -1,0, full_width - 1, full_height), grid_color, 1)
    return full_image

def render_full_images(image_data, draw_grid=True, columns = 25):
    display(to_full_image(image_data, draw_grid, columns))