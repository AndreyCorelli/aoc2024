import os
import imageio.v3 as iio
from PIL import Image

SRC_FOLDER = "/Users/andreisitaev/sources/sennder/aoc2024/day14/images/x"


def create_animation(output_path, frame_indices, interval=0.2, folder=None, render_function=None):
    frames = []
    duration = interval  # Duration of each frame in seconds

    if render_function:
        # Render frames using the provided render_function
        for idx in frame_indices:
            # Render bitmap, convert to an Image, and append
            bitmap = render_function(idx)
            image = Image.fromarray(bitmap)  # Assumes `render_function` returns a NumPy array
            frames.append(image)
    elif folder:
        # Load frames from the folder
        for idx in frame_indices:
            file_name = f"img_{idx:05d}.png"  # Example: "image00001.png"
            file_path = os.path.join(folder, file_name)
            if os.path.exists(file_path):
                frames.append(iio.imread(file_path))
            else:
                print(f"Warning: {file_path} not found, skipping.")
    else:
        raise ValueError("Either `folder` or `render_function` must be provided.")

    # Save frames as an animation
    if not frames:
        raise ValueError("No frames were collected for the animation.")

    iio.imwrite(output_path + "/result.gif", frames, duration=duration, plugin="pillow")
    print(f"Animation saved to {output_path}")


if __name__ == "__main__":
# Example Usage
# Folder-based example
    folder_path = SRC_FOLDER
    frame_indices = list(range(331, 404))  # Frames to include
    create_animation(SRC_FOLDER, frame_indices, interval=0.2, folder=folder_path)
