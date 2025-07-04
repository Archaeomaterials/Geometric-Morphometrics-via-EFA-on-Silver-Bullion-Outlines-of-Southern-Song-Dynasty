import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.fft import ifft

# ====== CONFIGURATION ======
IMAGE_DIR = "OpenCV--get_coordinates/data"
OUTPUT_DIR = "OpenCV--get_coordinates/coordinates"
USE_FOURIER = True
NUM_HARMONICS = 1000
# ===========================

def reconstruct_contour(fourier_descriptors, num_harmonics):
    filtered = np.zeros_like(fourier_descriptors)
    filtered[0] = fourier_descriptors[0]
    filtered[1:num_harmonics + 1] = fourier_descriptors[1:num_harmonics + 1]
    filtered[-num_harmonics:] = fourier_descriptors[-num_harmonics:]
    contour = ifft(filtered)
    return contour.real, contour.imag


def extract_contour_from_alpha(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None or image.shape[2] < 4:
        print(f"[SKIPPED] Image {image_path} missing alpha channel.")
        return None

    alpha = image[:, :, 3]
    _, mask = cv2.threshold(alpha, 128, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print(f"[SKIPPED] No contour found in {image_path}")
        return None

    largest = sorted(contours, key=lambda x: len(x), reverse=True)[0].squeeze()
    return largest


def save_contour_plot(x, y, save_path):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x, y, color='black')
    ax.axis('equal')
    ax.axis('off')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()


def save_contour_coordinates(contour, save_path):
    with open(save_path, 'w') as f:
        for pt in contour:
            f.write(f"{pt[0]}\t{pt[1]}\n")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    coordinates_dir = os.path.join(OUTPUT_DIR, "coordinates_txt")
    os.makedirs(coordinates_dir, exist_ok=True)

    for fname in os.listdir(IMAGE_DIR):
        if not fname.lower().endswith(".png"):
            continue

        image_path = os.path.join(IMAGE_DIR, fname)
        base_name = os.path.splitext(fname)[0]
        print(f"[INFO] Processing: {fname}")

        contour = extract_contour_from_alpha(image_path)
        if contour is None or contour.ndim != 2 or contour.shape[1] != 2:
            print(f"[ERROR] Invalid contour in {fname}, skipping.")
            continue

        # Save coordinates
        txt_path = os.path.join(coordinates_dir, f"{base_name}.txt")
        save_contour_coordinates(contour, txt_path)
        if USE_FOURIER:
            fd = np.fft.fft(contour[:, 0] + 1j * contour[:, 1])
            x_re, y_re = reconstruct_contour(fd, NUM_HARMONICS)
            x_re, y_re = np.append(x_re, x_re[0]), np.append(y_re, y_re[0])
            img_out_path = os.path.join(OUTPUT_DIR, f"{base_name}.png")
            save_contour_plot(x_re, y_re, img_out_path)

    print("All contours processed successfully.")


if __name__ == "__main__":
    main()
