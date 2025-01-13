#!/usr/bin/env python3

import argparse
from PIL import Image, ImageDraw

def add_grid(image, grid_size, grid_color=(0, 0, 0),
            central_line_color=(255, 0, 0),
            central_line_width=10):
    """
    Add grid overlay to the image.

    :param image: image object
    :param grid_size: size of each grid cell
    :param grid_color: color of the grid lines
    :param central_line_color: color of the separation line which splits image and its empty grid counterpart (default is red)
    :param central_line_width: width of the separation line (default is 10px_
    :return: image with the grid overlay
    """
    width, height = image.size
    draw = ImageDraw.Draw(image)

    # vertical grid lines
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=grid_color, width = 3)

    # horizontal grid lines
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=grid_color, width = 3)

    # bold red separating vertical line
    central_line_x = width
    draw.line([(central_line_x, 0), (central_line_x, height)], fill=central_line_color, width=central_line_width)

    return image

def create_image_with_grid(input_image_path, output_image_path, grid_size):
    original_image = Image.open(input_image_path).convert('RGB')
    original_width, original_height = original_image.size

    new_height = original_height
    new_width = original_width * 2
    new_image = Image.new('RGB', (new_width, new_height), (255, 255, 255))  # White background

    # original image on the left side
    new_image.paste(original_image, (0, 0))

    # add the grid overlay
    left_image = original_image.copy()
    left_image = add_grid(left_image, grid_size)

    right_image = Image.new('RGB', (original_width, original_height), (255, 255, 255))
    right_image = add_grid(right_image, grid_size)

    # paste both image to get the final image
    new_image.paste(left_image, (0, 0))
    new_image.paste(right_image, (original_width, 0))

    new_image.save(output_image_path)

    print(f"Image saved to {output_image_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert image to grid-copy-able image")
    parser.add_argument("input_image", help="Path to the input image")
    parser.add_argument("grid_size", type=int, nargs='?', default=100, help="Size of the grid cells; default: 100")
    parser.add_argument("output_image", nargs='?', default='out.png',
                       help="Path to save the output image; default: out.png")

    args = parser.parse_args()

    create_image_with_grid(args.input_image, args.output_image, args.grid_size)


if __name__ == "__main__":
    main()

