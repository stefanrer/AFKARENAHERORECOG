import cv2
from pathlib import Path

directory = 'Result/Success'
images = Path(directory).glob('*')

for image in images:
    fraction = cv2.imread(str(image), 1)
    cropped_fraction = fraction[8:18, 10:20]
    image_name = str(image).split("\\")[-1]
    cv2.imwrite(f'FractionCrops/{image_name}', cropped_fraction)