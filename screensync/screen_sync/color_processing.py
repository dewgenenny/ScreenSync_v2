import mss
import numpy as np
from PIL import ImageStat, Image, ImageEnhance, ImageColor
import colorsys
from screensync.screen_sync.stats import runtime_stats

# Global variable to cache screen size
screen_width, screen_height = None, None
# Global variables to cache screen size and zone bounding boxes
screen_size = None
zone_bboxes = {}
# Global variable to store the current mode
current_mode = 'normal'

def set_mode(mode):
    global current_mode
    current_mode = mode
    # Adjust behavior based on mode

def get_screen_size():
    """Returns the current screen size as a tuple (width, height)."""
    global screen_size
    if screen_size is None:
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Get the first monitor
            screen_size = (monitor['width'], monitor['height'])
    return screen_size


def get_zone_bbox(zone):
    """Get the bounding box for a given screen zone."""
    if not zone_bboxes:
        calculate_zone_bbox()
    return zone_bboxes.get(zone, (0, 0, screen_size[0], screen_size[1]))  # Default to full screen


def calculate_zone_bbox(zone_height=100, zone_width=100):
    """Calculate the bounding boxes for all screen zones."""
    global zone_bboxes, screen_size
    screen_width, screen_height = get_screen_size()
    third_width, third_height = screen_width // 3, screen_height // 3

    zone_bboxes = {
        'top-left': (0, 0, third_width, zone_height),
        'top-center': (third_width, 0, 2 * third_width, zone_height),
        'top-right': (2 * third_width, 0, screen_width, zone_height),
        'center-left': (0, third_height, zone_width, 2 * third_height),
        'center': (third_width, third_height, 2 * third_width, 2 * third_height),
        'center-right': (screen_width - zone_width, third_height, screen_width, 2 * third_height),
        'bottom-left': (0, screen_height - zone_height, third_width, screen_height),
        'bottom-center': (third_width, screen_height - zone_height, 2 * third_width, screen_height),
        'bottom-right': (2 * third_width, screen_height - zone_height, screen_width, screen_height)

    }

def process_screen_zone(zone, saturation_factor=2.0, mode='normal'):
    """Capture and process a specific screen zone."""
    # Handle the shooter mode
    if mode == 'Shooter':
        # In shooter mode, always capture the center
        zone = 'center'
        size = (50, 50)  # You can adjust the size as necessary
        bbox = get_screen_center(size)
    else:
        # For normal mode, use the provided zone
        bbox = get_zone_bbox(zone)
    # Capture and process the screen zone
    screenshot = capture_screen(bbox)
    avg_color = get_average_color(screenshot)
    adjusted_color = adjust_color(*avg_color, saturation_factor=saturation_factor)
    return adjusted_color



def capture_screen(bbox):
    """Capture the screen using python-mss."""
    with mss.mss() as sct:
        sct_img = sct.grab(bbox)
        # Convert to PIL Image for compatibility with existing processing
        return Image.frombytes("RGB", sct_img.size, sct_img.rgb)


def get_screen_center(size=(100, 100)):
    global screen_width, screen_height
    if not screen_width or not screen_height:
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Get the first monitor
            screen_width, screen_height = monitor['width'], monitor['height']
    center_x, center_y = screen_width // 2, screen_height // 2
    half_width, half_height = size[0] // 2, size[1] // 2

    return (center_x - half_width, center_y - half_height,
            center_x + half_width, center_y + half_height)

def capture_screen_center():
    """Capture a 100x100 pixel box at the center of the screen."""
    bbox = get_screen_center()

    # Convert the bbox to a format suitable for mss
    #mss_bbox = {"top": bbox[1], "left": bbox[0], "width": bbox[2] - bbox[0], "height": bbox[3] - bbox[1]}
    return capture_screen(bbox)

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
    """Capture the screen color and process it, returning RGB values."""
    bbox = get_screen_center(size)
    screenshot = ImageGrab.grab(bbox=bbox)
    r, g, b = get_average_color(screenshot)
    adjusted_r, adjusted_g, adjusted_b = adjust_color(r, g, b, saturation_factor=3)
    return adjusted_r, adjusted_g, adjusted_b
