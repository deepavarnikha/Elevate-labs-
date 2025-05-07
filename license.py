import cv2
import pytesseract

# Configure Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Read the image file
image = cv2.imread(r"C:\Users\sangi\Downloads\car1 (1).JPG")
cv2.imshow("Original", image)

# Convert to Grayscale Image
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray Image", gray_image)

# Apply Canny Edge Detection
canny_edge = cv2.Canny(gray_image, 170, 200)
cv2.imshow("Canny Edge Detection", canny_edge)

# Find contours based on edges
contours, _ = cv2.findContours(canny_edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

# Initialize variables for license plate contour and coordinates
contour_with_license_plate = None
license_plate = None
x = y = w = h = None

# Create a blank canvas to draw contours
contour_image = image.copy()
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
cv2.imshow("Contours", contour_image)

# Loop through contours to find one with 4 corners (rectangular shape)
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
    print("Number of corners:", len(approx))
    if len(approx) == 4:  # Check for rectangular shape
        contour_with_license_plate = approx
        x, y, w, h = cv2.boundingRect(contour)
        license_plate = gray_image[y:y + h, x:x + w]
        cv2.imshow("Detected License Plate", license_plate)
        break

# Apply threshold to the license plate image
if license_plate is not None:
    _, license_plate = cv2.threshold(license_plate, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow("Thresholded License Plate", license_plate)

    # Remove noise using Bilateral Filtering
    license_plate = cv2.bilateralFilter(license_plate, 11, 17, 17)

    # Perform OCR to recognize text
    text = pytesseract.image_to_string(license_plate)
    print("License Plate Text:", text)

    # Draw rectangle and display the recognized text on the original image
    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3)
    image = cv2.putText(image, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("Final Result", image)
else:
    print("License plate not found.")

# Ensure all windows stay open until a key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()