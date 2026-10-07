from PIL import Image, ImageDraw, ImageFont

image_path = r'F:\Annadata Mitra\Annadata_Mitra_Report\images\flowchart2_user_flow.png'
img = Image.open(image_path)
draw = ImageDraw.Draw(img)

# Box dimensions
x, y, w, h = 196, 1200, 161, 56
bg_color = (204, 204, 204)

# Draw filled rectangle to erase old text, leaving a 2px margin for the border
draw.rectangle([x + 2, y + 2, x + w - 2, y + h - 2], fill=bg_color)

# Try to load a font, fallback to default if arial is not found
try:
    font = ImageFont.truetype('arial.ttf', 14)
except IOError:
    font = ImageFont.load_default()

text = "Display Current\nWeather & Risk"

# We use textbbox to center the text
try:
    bbox = draw.textbbox((0, 0), text, font=font, align="center")
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
except AttributeError:
    # Older PIL version fallback
    text_w, text_h = draw.textsize(text, font=font)

text_x = x + (w - text_w) / 2
text_y = y + (h - text_h) / 2 - 2 # slight upward adjustment

draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font, align="center")

img.save(image_path)
print('Image updated successfully.')
