import os, sys
from PIL import Image

wf = 1000

infile = "Plot.png"
inim = Image.open(infile)
w,h  = inim.size[0], inim.size[1]
ratio = float(h)/w

outfile = os.path.splitext(infile)[0] + "Big"


# size = (inim.size[0]+200,inim.size[1]+200)
im = Image.open(infile)
im = im.resize((wf, int(wf * ratio)))
size = im.size
print im.size
print inim.size
im.save(outfile+".png")

new_im = Image.new('RGB', (size[0], size[1]+inim.size[1]))

new_im.paste(inim, (0,0))

x_offset = 0
y_offset = inim.size[1]


new_im.paste(im, (x_offset,y_offset))


new_im.save('Plottest.jpg')

