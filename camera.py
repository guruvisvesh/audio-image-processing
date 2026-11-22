import cv2
import os
import matplotlib.pyplot as plt

def show_image(image, title="Image"):
    """Display an image using Matplotlib."""
    plt.figure()
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()

def process_image(image_path):
    try:
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            print(f"Error: Unable to load image from {image_path}")
            return

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        show_image(image, "Original Image")
        show_image(gray, "Grayscale Image")
        show_image(edges, "Edge Detection")

        # Save processed images
        output_dir = "processed_images"
        os.makedirs(output_dir, exist_ok=True)
        cv2.imwrite(os.path.join(output_dir, "grayscale.png"), gray)
        cv2.imwrite(os.path.join(output_dir, "edges.png"), edges)

        print("Processed images saved in 'processed_images' directory.")

        '''# Open the processed images using system viewer
        if os.name == "posix":  # Linux/macOS
            os.system(f"xdg-open {os.path.join(output_dir, 'edges.png')}")
        elif os.name == "nt":  # Windows
            os.startfile(os.path.join(output_dir, "edges.png"))'''

    except Exception as e:
        print(f"Error processing image: {e}")

def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not accessible. Please provide an existing image.")
        return input("Enter path to an existing image: ")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Error capturing image. Please provide an existing image.")
        return input("Enter path to an existing image: ")

    image_path = "captured_image.jpg"
    cv2.imwrite(image_path, frame)
    print(f"Image captured and saved as {image_path}")
    return image_path


image_file = capture_image()
if os.path.exists(image_file):
   process_image(image_file)
else:
   print("Invalid image path. Exiting.")