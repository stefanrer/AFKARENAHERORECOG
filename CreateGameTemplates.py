import cv2
from pathlib import Path

directory = 'HeroFacesDirectory/CroppedTemplates'
DefaultHeight = 960
DefaultWidth = 432

Images = Path(directory).glob('*')
DefaultHeroList = cv2.imread('Herolist/Screenshot_2021-08-01-17-12-51.jpg', 1)
Size = DefaultWidth / DefaultHeroList.shape[1]  # Default the Size of Herolist
img = cv2.resize(DefaultHeroList, (0, 0), fx=Size, fy=Size)
for Image in Images:
    Template = cv2.imread(str(Image), 1)
    h, w = Template.shape[0:2]
    TestRect = cv2.matchTemplate(img, Template, cv2.TM_CCOEFF_NORMED)   # Herolist Match
    Tmin_val, Tmax_val, Tmin_loc, Tmax_loc = cv2.minMaxLoc(TestRect)
    changemax_loc = list(Tmax_loc)
    location = tuple(changemax_loc)  # Left upper corner of Rectangle
    print(Tmax_val, str(Image).split("\\")[-1])
    bottom_right = (location[0] + w, location[1] + h)
    crop = img[location[1]:bottom_right[1], location[0]:bottom_right[0]]
    image_name = str(Image).split("\\")
    cv2.imwrite(f'HeroFacesDirectory/NewcroppedTemplates/{image_name[-1]}', crop)
