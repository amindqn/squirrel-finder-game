from PIL import Image, ImageDraw, ImageFont


def create_koala_image():
    img = Image.new("RGBA", (40, 40), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw koala face
    draw.ellipse((5, 5, 35, 35), fill=(160, 160, 160))  # Head
    draw.ellipse((2, 2, 15, 15), fill=(120, 120, 120))  # Left ear
    draw.ellipse((25, 2, 38, 15), fill=(120, 120, 120))  # Right ear
    draw.ellipse((15, 15, 25, 25), fill=(80, 80, 80))  # Nose
    draw.ellipse((12, 20, 15, 23), fill=(0, 0, 0))  # Left eye
    draw.ellipse((25, 20, 28, 23), fill=(0, 0, 0))  # Right eye

    img.save("koala.png")


def create_strawberry_image():
    img = Image.new("RGBA", (40, 40), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw strawberry body
    draw.polygon([(20, 5), (35, 30), (5, 30)], fill=(220, 20, 60))
    # Draw seeds
    for x in range(10, 31, 5):
        for y in range(15, 26, 5):
            draw.ellipse((x, y, x + 2, y + 2), fill=(255, 255, 0))
    # Draw leaves
    draw.polygon([(17, 5), (23, 5), (20, 0)], fill=(34, 139, 34))

    img.save("strawberry.png")


def create_squirrel_image():
    img = Image.new("RGBA", (40, 40), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw body
    draw.ellipse((10, 15, 30, 35), fill=(139, 69, 19))  # Body
    # Draw head
    draw.ellipse((5, 10, 15, 20), fill=(139, 69, 19))  # Head
    # Draw tail
    draw.ellipse((25, 5, 40, 35), fill=(160, 82, 45))  # Tail
    # Draw eyes
    draw.ellipse((8, 13, 10, 15), fill=(0, 0, 0))  # Eye
    # Draw ear
    draw.polygon([(7, 10), (10, 5), (12, 10)], fill=(139, 69, 19))

    img.save("squirrel.png")


def create_rock_image():
    img = Image.new("RGBA", (40, 40), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rock with irregular shape
    draw.polygon(
        [(5, 30), (10, 10), (20, 5), (30, 10), (35, 30), (20, 35)], fill=(112, 128, 144)
    )
    # Add texture
    for _ in range(10):
        x = random.randint(10, 30)
        y = random.randint(10, 30)
        draw.ellipse((x, y, x + 2, y + 2), fill=(105, 105, 105))

    img.save("rock.png")


def create_background_image():
    img = Image.new("RGBA", (800, 600), color=(25, 25, 112))  # Midnight blue background
    draw = ImageDraw.Draw(img)

    # Add stars to the background
    for _ in range(100):
        x = random.randint(0, 799)
        y = random.randint(0, 599)
        draw.point((x, y), fill=(255, 255, 255))

    img.save("background.png")


if __name__ == "__main__":
    import random

    create_koala_image()
    create_strawberry_image()
    create_squirrel_image()
    create_rock_image()
    create_background_image()
    print("Images have been created and saved.")
