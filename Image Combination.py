#import sys
from PIL import Image

bottom_images = map(Image.open, ['Test1.jpg', 'Test2.jpg', 'Test3.jpg'])
top_image = Image.open("top.png")
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
  b = im.size
  new_im.paste(im, (x_offset,y_offset))
  x_offset += im.size[0]

new_im.save('test.jpg')