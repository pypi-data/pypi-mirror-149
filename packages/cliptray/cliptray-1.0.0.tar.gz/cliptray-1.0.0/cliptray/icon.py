#!/usr/bin/env python3

from PIL import Image, ImageDraw


def create_icon():
    """
    Creates a clipboard-ish icon.
    :returns: A 64x64 image with a clipboard in a circle.
    """
    icon_size = 64
    bottom_rectangle_width = 0.4 * icon_size
    bottom_rectangle_height = 0.5 * icon_size
    bottom_rectangle_position = (0.5 * icon_size, 0.55 * icon_size)
    bottom_rectangle_shape = [(bottom_rectangle_position[0] - (bottom_rectangle_width / 2), bottom_rectangle_position[1] - (bottom_rectangle_height / 2)),
             (bottom_rectangle_position[0] + (bottom_rectangle_width / 2), bottom_rectangle_position[1] + (bottom_rectangle_height / 2))]

    top_rectangle_width = 0.6 * bottom_rectangle_width
    top_rectangle_height = 0.2 * bottom_rectangle_height
    top_rectangle_position = (bottom_rectangle_position[0], bottom_rectangle_position[1] - bottom_rectangle_height / 2 - top_rectangle_height / 2)
    top_rectangle_shape = [(top_rectangle_position[0] - (top_rectangle_width / 2), top_rectangle_position[1] - (top_rectangle_height / 2)),
             (top_rectangle_position[0] + (top_rectangle_width / 2), top_rectangle_position[1] + (top_rectangle_height / 2))]        

    line_width = 0.5 * bottom_rectangle_width
    
    line_shapes = []
    line_shapes.append([(bottom_rectangle_position[0] - line_width / 2, bottom_rectangle_position[1] + bottom_rectangle_height / 6),
                    (bottom_rectangle_position[0] + line_width / 2, bottom_rectangle_position[1] + bottom_rectangle_height / 6)])
    line_shapes.append([(bottom_rectangle_position[0] - line_width / 2, bottom_rectangle_position[1]),
                    (bottom_rectangle_position[0] + line_width / 2, bottom_rectangle_position[1])])   
    line_shapes.append([(bottom_rectangle_position[0] - line_width / 2, bottom_rectangle_position[1] - bottom_rectangle_height / 6),
                    (bottom_rectangle_position[0] + line_width / 2, bottom_rectangle_position[1] - bottom_rectangle_height / 6)])

    background_color = "#00000000"
    foreground_color = "#FFFFFFFF"
    image = Image.new('LA', (icon_size, icon_size), background_color)

    draw = ImageDraw.Draw(image)
    draw.ellipse([(0, 0), (icon_size, icon_size)], fill=foreground_color)
    draw.rectangle(bottom_rectangle_shape, outline=background_color, width=4)
    draw.rectangle(top_rectangle_shape, outline=background_color, width=2)

    for line_shape in line_shapes:
        draw.line(line_shape, fill=background_color, width=2)

    return image
