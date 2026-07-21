from PIL import Image

RAMP = " .`:-=+*cs#%@"
WIDTH = 80


class AsciiGenerator:

    def __init__(self, image_path):
        self.image = Image.open(image_path).convert("L")

    def resize(self):
        w, h = self.image.size
        ratio = h / w
        new_height = int(WIDTH * ratio * 0.46)
        self.image = self.image.resize((WIDTH, new_height))

    def pixels_to_ascii(self):
        pixels = self.image.getdata()
        chars = ""
        for p in pixels:
            # 255 (bright background) -> index 0 (space)
            # 0 (dark subject) -> index len-1 (@)
            chars += RAMP[(255 - p) * (len(RAMP) - 1) // 255]
        return chars

    def generate(self):
        self.resize()
        chars = self.pixels_to_ascii()
        width = self.image.width
        rows = []
        for i in range(0, len(chars), width):
            rows.append(chars[i:i+width])
        return rows


if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    generator = AsciiGenerator(os.path.join(current_dir, "source-prepped.png"))
    rows = generator.generate()
    with open(os.path.join(current_dir, "ascii.txt"), "w", encoding="utf8") as f:
        for r in rows:
            f.write(r + "\n")
    print("ASCII generated.")