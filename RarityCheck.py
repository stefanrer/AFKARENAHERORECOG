import cv2
from pathlib import Path

directory = 'Result/Success'
files = Path(directory).glob('*.jpg')
for file in files:
    img = cv2.imread(str(file), 1)
    cv2.imshow('ss', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()