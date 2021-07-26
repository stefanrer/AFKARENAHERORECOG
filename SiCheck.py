import cv2
from pathlib import Path

directory = 'Result/Success'
faces = Path(directory).glob('*')
signatures = ['Si/Si30.jpg', 'Si/Si20.jpg', 'Si/Si10.jpg', 'Si/Si0.jpg']
for face in faces:
    print(str(face).split("\\")[-1])
    dict = {}
    for signature in signatures:
        img = cv2.imread(str(face), 1)
        imgcrop = img[0:int((img.shape[0]) / 1.8), 0:int((img.shape[1]) / 2.3)]
        template = cv2.imread(signature, 1)
        result = cv2.matchTemplate(imgcrop, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        dict[signature.split('/')[1][0:-4]] = str(max_val)[0:4]
    print(dict)
