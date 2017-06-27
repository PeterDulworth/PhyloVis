import re
from PIL import Image
import math
import os


def image_combination():
    """
    Combines images from the inout directory horizontally and adds a plot vertically
    Inputs:
    input_directory --- name of directory containing tree images
    plot --- the plot to be included at the top of the image
    """

    pattern = "(Topology)(\d)"

    topology_images = []

    # Iterate over each folder in the given directory
    for filename in os.listdir("."):

        # If file is a Topology image
        if re.match(pattern, (os.path.splitext(filename)[0])):

            topology_images.append(filename)

    # Open the bottom images
    topology_images = map(Image.open, topology_images)

    num_images = len(topology_images)

    widths, heights = zip(*(i.size for i in topology_images))

    # If there are more than two topology images at most two are side by side
    if num_images > 1:
        total_width = (widths[0] *2)

    else:
        total_width = widths[0]

    # Total height is one of the heights times the number of images stacked vertically
    total_height = int(heights[0] * math.ceil(num_images/2.0))

    # Create combined image of plot and trees
    new_im = Image.new('RGB', (total_width, total_height))
    new_im.paste((255,255,255), (0, 0, total_width, total_height))

    x_offset = 0
    y_offset = 0

    odd = num_images % 2

    #Combine images in pairwise vertical stacks
    for i in range(len(topology_images)):

        im = topology_images[i]

        # If there are an odd number of images and the current one is the last one put it in the middle
        if odd and i == (len(topology_images) -1):
            x_offset = total_width/4
            new_im.paste(im, (x_offset, y_offset), mask=im)


        else:
            if i % 2 == 1:
                x_offset = (total_width/2)
                new_im.paste(im, (x_offset,y_offset), mask=im)
                new_im.save("TEst" + str(i) + ".png")
                y_offset += im.size[1]
                x_offset = 0

            else:
                new_im.paste(im, (x_offset, y_offset), mask=im)

    new_im.save("TopTopologies.png")


if __name__ == '__main__':
    image_combination()




