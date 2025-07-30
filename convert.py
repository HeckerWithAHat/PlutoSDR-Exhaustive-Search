import cv2

# Load the image
image = cv2.imread('./files/image.jpg')

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Resize to 32x32
resized_image = cv2.resize(gray_image, (32, 32))

# Save the processed image
cv2.imwrite('./files/small_image.jpg', resized_image)