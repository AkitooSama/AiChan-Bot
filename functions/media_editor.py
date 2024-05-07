#Importing buil-in module.
from io import BytesIO
#Importing requests module.
import requests
#Importing PIL module
from PIL import Image, ImageSequence

def crop_gif_to_square_ratio(gif_link: str) -> None:
    """
    Crop a GIF to a 1:1 square aspect ratio.

    Parameters:
    - gif_link (str): The URL link to the GIF image to be processed.

    Returns:
    - bytes or None: A cropped GIF image in bytes format, or None if the operation fails.
    """
    
    # Download the GIF file
    response = requests.get(gif_link)
    if response.status_code != 200:
        return None

    # Load the downloaded GIF into a PIL Image
    gif_bytes = BytesIO(response.content)
    gif = Image.open(gif_bytes)

    # Ensure it's a GIF
    if gif.format != "GIF":
        return None

    # Get the dimensions of the GIF
    width, height = gif.size

    # Calculate dimensions for a square crop
    min_dimension = min(width, height)
    x1 = (width - min_dimension) / 2
    y1 = (height - min_dimension) / 2
    x2 = x1 + min_dimension
    y2 = y1 + min_dimension

    # Crop each frame of the GIF to a 1:1 aspect ratio
    frames = []
    for frame in ImageSequence.Iterator(gif):
        cropped_frame = frame.crop((x1, y1, x2, y2))
        frames.append(cropped_frame.copy())

    # Create a new GIF from cropped frames
    output = BytesIO()
    frames[0].save(output, format='GIF', save_all=True, append_images=frames[1:], loop=0)

    return output.getvalue()

if __name__ == "__main__":
    pass