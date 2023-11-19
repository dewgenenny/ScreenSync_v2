from PIL import ImageGrab, ImageStat, Image, ImageEnhance, ImageColor


def get_screen_center(size=(100, 100)):
    """Calculate the coordinates for a central region of the screen."""
    screen = ImageGrab.grab()
    screen_width, screen_height = screen.size
    center_x, center_y = screen_width // 2, screen_height // 2
    half_width, half_height = size[0] // 2, size[1] // 2
    return center_x - half_width, center_y - half_height, center_x + half_width, center_y + half_height

def capture_screen_center():
    """Capture a 100x100 pixel box at the center of the screen."""
    bbox = get_screen_center()
    return ImageGrab.grab(bbox=bbox)

def get_average_color(image):
    """Calculate the average color of the given image."""
    stats = ImageStat.Stat(image)
    avg = stats.mean
    return int(avg[0]), int(avg[1]), int(avg[2])  # RGB values

def adjust_color(r, g, b, saturation_factor=1.5):
    """Increase the saturation of the given RGB color."""
    # Convert RGB to a Pillow Image
    image = Image.new("RGB", (1, 1), (r, g, b))

    # Convert to HSV, increase saturation, and convert back to RGB
    converter = ImageEnhance.Color(image)
    image_enhanced = converter.enhance(saturation_factor)

    # Extract the RGB value of the enhanced image
    enhanced_color = image_enhanced.getpixel((0, 0))

    return enhanced_color

def process_screen_color():
    """Capture the screen color and process it."""
    screenshot = capture_screen_center()
    r, g, b = get_average_color(screenshot)
    adjusted_r, adjusted_g, adjusted_b = adjust_color(r, g, b, saturation_factor=3.0)
    return adjusted_r, adjusted_g, adjusted_b
