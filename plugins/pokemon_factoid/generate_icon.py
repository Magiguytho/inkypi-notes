from PIL import Image, ImageDraw, ImageFont

SIZE = 64
OUTPUT = "icon.png"


def main():
    img = Image.new("RGB", (SIZE, SIZE), "white")
    draw = ImageDraw.Draw(img)

    # simple monochrome pokeball-like mark for e-ink compatibility
    draw.ellipse((4, 4, SIZE - 4, SIZE - 4), outline="black", width=3)
    draw.line((4, SIZE // 2, SIZE - 4, SIZE // 2), fill="black", width=3)
    draw.ellipse((SIZE // 2 - 8, SIZE // 2 - 8, SIZE // 2 + 8, SIZE // 2 + 8), outline="black", width=3)

    # add a tiny "P" marker for plugin discoverability
    font = ImageFont.load_default()
    draw.text((SIZE // 2 - 3, SIZE // 2 - 3), "P", fill="black", font=font)

    img.save(OUTPUT, format="PNG")
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
