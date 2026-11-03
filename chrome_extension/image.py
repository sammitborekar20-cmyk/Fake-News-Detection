from PIL import Image, ImageDraw

#  Create a 128x128 image with a blue background
img = Image.new('RGB', (128, 128), color=(0, 0, 255))

#  Add a white circle in the center
draw = ImageDraw.Draw(img)
draw.ellipse((32, 32, 96, 96), fill=(255, 255, 255))

#  Save the image in the chrome_extension folder
img.save("chrome_extension/icon.png")

print(" icon.png has been created in the chrome_extension folder!")
