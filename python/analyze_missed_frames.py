import cv2
import os
import glob


# ========================================
# Vyom Assist
# Step 4 - Missed Frames Analysis
# ========================================

FOLDER = "diagnostic_missed_frames"


# ========================================
# Check Folder
# ========================================

if not os.path.exists(FOLDER):

    print()
    print("ERROR: Folder not found!")
    print()
    print("Expected folder:")
    print(FOLDER)
    print()

    input("Press Enter to exit...")
    raise SystemExit


# ========================================
# Get Images
# ========================================

image_files = sorted(
    glob.glob(os.path.join(FOLDER, "*.jpg"))
)


if len(image_files) == 0:

    print()
    print("ERROR: No missed-frame images found.")
    print()

    input("Press Enter to exit...")
    raise SystemExit


# ========================================
# Statistics
# ========================================

total_images = len(image_files)

valid_images = 0

invalid_images = 0

brightness_values = []

dark_images = 0

bright_images = 0

normal_brightness_images = 0

blur_values = []

blurry_images = 0

sharp_images = 0


# ========================================
# Brightness Thresholds
# ========================================

DARK_THRESHOLD = 60

BRIGHT_THRESHOLD = 190

BLUR_THRESHOLD = 80


# ========================================
# Analyze Images
# ========================================

for image_path in image_files:

    image = cv2.imread(image_path)

    if image is None:

        invalid_images += 1

        continue


    valid_images += 1


    # ------------------------------------
    # Grayscale
    # ------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # ------------------------------------
    # Brightness
    # ------------------------------------

    brightness = float(gray.mean())

    brightness_values.append(brightness)


    if brightness < DARK_THRESHOLD:

        dark_images += 1

    elif brightness > BRIGHT_THRESHOLD:

        bright_images += 1

    else:

        normal_brightness_images += 1


    # ------------------------------------
    # Blur / Sharpness
    # ------------------------------------

    blur_score = float(
        cv2.Laplacian(
            gray,
            cv2.CV_64F
        ).var()
    )


    blur_values.append(blur_score)


    if blur_score < BLUR_THRESHOLD:

        blurry_images += 1

    else:

        sharp_images += 1


# ========================================
# Calculate Averages
# ========================================

if valid_images > 0:

    average_brightness = (
        sum(brightness_values)
        / len(brightness_values)
    )

    average_blur = (
        sum(blur_values)
        / len(blur_values)
    )

else:

    average_brightness = 0

    average_blur = 0


# ========================================
# Final Report
# ========================================

print()
print("========================================")
print("       MISSED FRAME ANALYSIS")
print("========================================")
print()

print(f"Total missed images: {total_images}")

print(f"Valid images: {valid_images}")

print(f"Invalid images: {invalid_images}")

print()

print("------------- Brightness ---------------")

print(
    f"Average brightness: "
    f"{average_brightness:.2f}"
)

print(
    f"Dark images (< {DARK_THRESHOLD}): "
    f"{dark_images}"
)

print(
    f"Normal brightness: "
    f"{normal_brightness_images}"
)

print(
    f"Bright images (> {BRIGHT_THRESHOLD}): "
    f"{bright_images}"
)

print()

print("--------------- Sharpness --------------")

print(
    f"Average sharpness score: "
    f"{average_blur:.2f}"
)

print(
    f"Potentially blurry images "
    f"(< {BLUR_THRESHOLD}): "
    f"{blurry_images}"
)

print(
    f"Sharp images: "
    f"{sharp_images}"
)

print()

print("========================================")
print("             ANALYSIS COMPLETE")
print("========================================")
print()