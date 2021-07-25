import cv2
from pathlib import Path

DefaultHeight = 960
DefaultWidth = 432
directory = 'HeroFacesForTemplateMatching'
DefaultHeroList = cv2.imread('Template/MgaLXVU2-MI (1).jpg', 1)
Size = DefaultWidth / DefaultHeroList.shape[1]  # Default the Size of Herolist
img = cv2.resize(DefaultHeroList, (0, 0), fx=Size, fy=Size)
img2 = img.copy()
Faces = Path(directory).glob('*')


def increase_box_size_left_upper_corner(corner):
    if (corner[0] - 22) < 0:
        corner[0] = 0
    else:
        corner[0] = corner[0] - 22
    if (corner[1] - 18) < 0:
        corner[1] = 0
    else:
        corner[1] = corner[1] - 18
    return tuple(corner)


def template_match(heroicon):
    template = cv2.imread(str(heroicon), 1)
    h, w = template.shape[0:2]
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)  # Template Match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    location = increase_box_size_left_upper_corner(list(max_loc))  # Left upper corner of Rectangle
    print(max_val, str(heroicon).split("\\")[-1])
    bottom_right = (location[0] + w + 42, location[1] + h + 36)  # Bottom right corner of Rectangle + Increase
    return max_val, location, bottom_right


def fraction_check(zone):
    fractions_directory = 'Fraction'
    fractions = Path(fractions_directory).glob('*')
    fdict = {}
    for frac in fractions:
        # print(frac)
        fracimag = cv2.imread(str(frac))
        fresult = cv2.matchTemplate(zone, fracimag, cv2.TM_CCOEFF_NORMED)
        fmin_val, fmax_val, fmin_loc, fmax_loc = cv2.minMaxLoc(fresult)
        fimage_name = str(frac).split("\\")[-1]
        fdict[fimage_name[0:-4]] = str(fmax_val)[0:4]
    print(fdict)


for Face in Faces:
    val, LeftCorner, RightCorner = template_match(Face)
    crop = img[LeftCorner[1]:RightCorner[1], LeftCorner[0]:RightCorner[0]]
    image_name = str(Face).split("\\")[-1]
    # cv2.putText(crop2, str(val)[0:4], (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0, 0), 3)  # Match value
    if val > 0.85:  # If matched successful
        cv2.imwrite(f'Result/Success/{image_name}', crop)
        cv2.rectangle(img2, LeftCorner, RightCorner, 255, 1)
        # Put Character Name On Result Sheet
        TextLoc = (LeftCorner[0], RightCorner[1])
        if image_name[0:-4].isalpha():
            cv2.putText(img2, image_name[0:-4], TextLoc, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0, 0), 2)
        else:
            cv2.putText(img2, image_name[0:-5], TextLoc, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0, 0), 2)
        mod_check_crop = crop[0:int((crop.shape[0]) / 1.8), 0:int((crop.shape[1]) / 2.3)]  # Zone for mod check
        fraction_check(mod_check_crop)
    else:
        cv2.imwrite(f'Result/Failure/{image_name}', crop)
cv2.imwrite(f'Result/result.jpg', img2)  # ResultSheet
