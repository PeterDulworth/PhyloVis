import os
from PIL import Image

def image_combination(input_directory, plot):
  """
  Combines images from the inout directory horizontally and adds a plot vertically
  Inputs:
  input_directory --- name of directory containing tree images
  plot --- the plot to be included at the top of the image
  """

  bottom_images = []

  # Iterate over each folder in the given directory
  for filename in os.listdir(input_directory):

    input_file = os.path.join(input_directory, filename)

    # If file is a Tree image
    if os.path.splitext(os.path.splitext(filename)[0])[0] == "Tree":

      bottom_images.append(input_file)

  # Open the bottom images
  bottom_images = map(Image.open, bottom_images)
  top_image = Image.open(plot)

  widths, heights = zip(*(i.size for i in bottom_images))

  #Total width is either the total of the bottom widths or the width of the top
  total_width = max(sum(widths),top_image.size[0])
  #Total height is sum of the top image and max of the bottom
  total_height = max(heights)+top_image.size[1]

  new_im = Image.new('RGB', (total_width, total_height))

  new_im.paste(top_image, (0,0))

  x_offset = 0
  y_offset = top_image.size[1]

  #Combine bottom images horizontally with no vertical offset
  for im in bottom_images:
    new_im.paste(im, (x_offset,y_offset))
    x_offset += im.size[0]

  new_im.save('Final.jpg')
