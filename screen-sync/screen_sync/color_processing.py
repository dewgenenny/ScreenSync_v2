from PIL import ImageGrab, ImageStat, Image, ImageEnhance, ImageColor
import colorsys


# Global variable to cache screen size
screen_width, screen_height = None, None

def get_screen_center(size=(100, 100)):
    global screen_width, screen_height
    if not screen_width or not screen_height:
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

def process_screen_color(size=(100, 100)):
    """Capture the screen color and process it, returning HSV values."""
    bbox = get_screen_center(size)
    screenshot = ImageGrab.grab(bbox=bbox)
    r, g, b = get_average_color(screenshot)
    adjusted_r, adjusted_g, adjusted_b = adjust_color(r, g, b, saturation_factor=3)

    # Convert RGB to HSV
    h, s, v = colorsys.rgb_to_hsv(adjusted_r / 255.0, adjusted_g / 255.0, adjusted_b / 255.0)

    # Scale HSV values to the appropriate range
    h_scaled = int(h * 360)  # Hue: 0-360
    s_scaled = int(s * 1000) # Saturation: 0-1000
    v_scaled = int(v * 1000) # Value: 0-1000

    return h_scaled, s_scaled, v_scaled
