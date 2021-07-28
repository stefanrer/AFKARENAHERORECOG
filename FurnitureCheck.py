import cv2
from pathlib import Path

directory = 'FurnData'
files = Path(directory).glob('*.jpg')
for file in files:
    img = cv2.imread(str(file), 1)
    croppedimage = img[150:224, 45:160]
    with open(f'{str(file)[0:-4]}.txt', 'r') as infile:
        for line in infile:
            numbers = line.split()
            if numbers[0] == '0':
                name = 'furn3'
            else:
                name = 'furn9'
            break
    cv2.imwrite(f'FurnData/FurnTemplate/{name}_{str(file)[12:16]}.jpg', croppedimage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()