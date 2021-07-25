import cv2
from pathlib import Path

directory = 'HeroTemplates'
folders = Path(directory).glob('*')

for folder in folders:
    images = Path(folder).glob('*')
    for image in images:
        template = cv2.imread(str(image), 1)
        cropped_image = template[22:78, 25:75]
        sizeimag = cv2.resize(cropped_image, (0, 0), fx=0.65, fy=0.65)
        image_name = str(image).split("\\")
        cv2.imwrite(f'CroppedTemplates/{image_name[-1]}', sizeimag)
