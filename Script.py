import cv2
import random
from pathlib import Path

DefaultHeight = 960
DefaultWidth = 432
directory = 'HeroFacesDirectory/HeroFacesForTemplateMatching'
filename = 'com.lilithgame.hgame.gp_Screenshot_2021.05.13_20.52.26.jpeg'  # Input HeroList
DefaultHeroList = cv2.imread(f'Herolist/{filename}', 1)
Size = DefaultWidth / DefaultHeroList.shape[1]  # Default the Size of Herolist
img = cv2.resize(DefaultHeroList, (0, 0), fx=Size, fy=Size)
img2 = img.copy()
faces = Path(directory).glob('*')

success_dict = {}  # Dictionary of heroes successfully matched/ Key:hero name Value: Fraction, SI, Furn
failure_list = []  # List of failed matching


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
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)  # Herolist Match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    location = increase_box_size_left_upper_corner(list(max_loc))  # Left upper corner of Rectangle
    bottom_right = (location[0] + w + 42, location[1] + h + 36)  # Bottom right corner of Rectangle + Increase
    return max_val, location, bottom_right


def fraction_check(zone):
    fractions_directory = 'Fraction'
    fractions = Path(fractions_directory).glob('*.jpg')
    fdict = {}
    for frac in fractions:
        # print(frac)
        fracimag = cv2.imread(str(frac), 1)
        fresult = cv2.matchTemplate(zone, fracimag, cv2.TM_CCOEFF_NORMED)
        f_min_val, f_max_val, f_min_loc, f_max_loc = cv2.minMaxLoc(fresult)
        fdict[str(frac).split('\\')[-1][0:-4]] = str(f_max_val)[0:4]
    fdictlist = sorted(fdict.items(), key=lambda x: x[1], reverse=True)
    print(fdict, file=log)
    print(fdict)
    return fdictlist[0][0]


def signature_check(zone):
    signatures_directory = 'Si'
    signatures = Path(signatures_directory).glob('*')
    sidict = {}
    for sign in signatures:
        # print(signature)
        signimag = cv2.imread(str(sign), 1)
        signresult = cv2.matchTemplate(zone, signimag, cv2.TM_CCOEFF_NORMED)
        sign_min_val, sign_max_val, sign_min_loc, sign_max_loc = cv2.minMaxLoc(signresult)
        sidict[str(sign).split('\\')[1][0:-4]] = str(sign_max_val)[0:4]
    sidictlist = sorted(sidict.items(), key=lambda x: x[1], reverse=True)
    print(sidict, file=log)
    print(sidict)
    return sidictlist[0][0]


def furniture_check(zone):
    furniture_directory = 'FurnData/FurnTemplate'
    furnzone = cv2.resize(zone, (224, 224))
    furnitures = Path(furniture_directory).glob('*.jpg')
    max_value = 0
    furndict = {}
    for furn in furnitures:
        furnimag = cv2.imread(str(furn), 1)
        furnresult = cv2.matchTemplate(furnzone, furnimag, cv2.TM_CCOEFF_NORMED)
        furn_min_val, furn_max_val, furn_min_loc, furn_max_loc = cv2.minMaxLoc(furnresult)
        furndict[str(furn).split('\\')[-1]] = float(str(furn_max_val)[0:4])
        if furn_max_val > max_value:
            max_value = furn_max_val
            furn_name = str(furn).split('\\')[-1][0:5]
            # full_furnname = str(furn).split('\\')[-1]  # Get file name
    sort_furn_list = sorted(furndict.items(), key=lambda x: x[1], reverse=True)
    sort_furn_dict = dict(sort_furn_list)
    print(sort_furn_dict)
    print(sort_furn_dict, file=log)
    if max_value < 0.92:
        furn_name = 'furn0'
    return furn_name


with open('Result/Log.txt', 'w') as log:
    for face in faces:
        val, LeftCorner, RightCorner = template_match(face)
        crop = img[LeftCorner[1]:RightCorner[1], LeftCorner[0]:RightCorner[0]]
        image_name = str(face).split("\\")[-1]
        # cv2.putText(crop2, str(val)[0:4], (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)  # Match value
        if val > 0.85:  # If matched successful
            print(str(val)[0:4], str(face).split("\\")[-1])
            print(str(val)[0:4], str(face).split("\\")[-1], file=log)
            # Text locations
            text_loc = (LeftCorner[0], RightCorner[1])  # Hero name location
            frac_text_loc = (LeftCorner[0], RightCorner[1] - 15)  # Hero fraction text location
            sign_text_loc = (LeftCorner[0] + 25, RightCorner[1] - 30)  # Hero signature text location
            furn_text_loc = (LeftCorner[0] + 25, RightCorner[1] - 45)  # Hero furniture text location
            # Crop for template
            mod_check_crop = crop[0:int((crop.shape[0]) / 1.8), 0:int((crop.shape[1]) / 2.3)]  # Zone for mod check
            # hero mods check
            fraction = fraction_check(mod_check_crop)  # Check for fraction
            signature = signature_check(mod_check_crop)  # Check for signature
            furniture = furniture_check(mod_check_crop)  # Check for furniture

            # print(fraction[0])
            if image_name[0:-4].isalpha():
                image_true_name = image_name[0:-4]
            else:
                image_true_name = image_name[0:-5]
            # put Hero name on result jpg
            if image_true_name not in success_dict:
                cv2.putText(img2, image_true_name, text_loc, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.imwrite(f'Result/Success/{image_name}', crop)
                cv2.rectangle(img2, LeftCorner, RightCorner, 255, 1)
                success_dict[image_true_name] = [fraction, signature, furniture]  # Add hero to dict
                # Put Fraction on herolist
                cv2.putText(img2, fraction, frac_text_loc, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # Put Si on herolist
                cv2.putText(img2, signature, sign_text_loc, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(img2, furniture, furn_text_loc, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        else:
            cv2.imwrite(f'Result/Failure/{image_name}', crop)
            failure_list.append(image_name[0:-4])

    cv2.imwrite(f'Result/result.jpg', img2)  # ResultSheet
    print(f'\nFailure list\n{failure_list}')
    print(f'\nFailure list\n{failure_list}', file=log)
    print(f'\nSuccess dict\n{success_dict}')
    print(f'\nSuccess dict\n{success_dict}', file=log)
