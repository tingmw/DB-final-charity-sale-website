from PIL import Image, ImageDraw

def create_placeholder_image(width, height, color, output_path):
    img = Image.new('RGB', (width, height), color=color)
    d = ImageDraw.Draw(img)
    d.text((width/2, height/2), f"{width}x{height}", fill=(255,255,255))
    img.save(output_path)

# Create banner image
create_placeholder_image(1200, 400, 'grey', 'static/images/banner.jpg')

# Create product images
create_placeholder_image(400, 400, 'blue', 'static/images/product1.jpg')
create_placeholder_image(400, 400, 'green', 'static/images/product2.jpg')
create_placeholder_image(400, 400, 'red', 'static/images/product3.jpg')
