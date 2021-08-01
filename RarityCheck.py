import cv2
from pathlib import Path

directory = 'Result/Success'
files = Path(directory).glob('*.jpg')
for file in files:
    img = cv2.imread(str(file), 1)
    crop = img[20:50, 0:10]
    # cv2.imshow('as', crop)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    rarity_directory = 'Rarity'
    images = Path(rarity_directory).glob('*.jpg')
    rar_dict = {}
    for image in images:
        rar_template = cv2.imread(str(image), 1)
        rar_result = cv2.matchTemplate(img, rar_template, cv2.TM_CCOEFF_NORMED)
        rar_min_val, rar_max_val, rar_min_loc, rar_max_loc = cv2.minMaxLoc(rar_result)
        rar_dict[str(image).split('\\')[1][0:-4]] = float(str(rar_max_val)[0:4])
    rar_dict_list = sorted(rar_dict.items(), key=lambda x: x[1], reverse=True)
    print(str(file))
    print(rar_dict)
    rarity = rar_dict_list[0][0]
    rarity_match = rar_dict_list[0][1]
    if rarity != 'Ascended':
        plus_crop = img[int(img.shape[0]*2/3):img.shape[0], 0:int(img.shape[1]/3)]
        # cv2.imshow('ss', plus_crop)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        if rarity == 'Mythic':
            plus_path = 'Rarity/PlusRarity/Mythic+.jpg'
        elif rarity == 'Legendary':
            plus_path = 'Rarity/PlusRarity/Legendary+.jpg'
        elif rarity == 'Elite':
            plus_path = 'Rarity/PlusRarity/Elite+.jpg'
        plus_img = cv2.imread(plus_path, 1)
        plus_result = cv2.matchTemplate(plus_crop, plus_img, cv2.TM_CCOEFF_NORMED)
        plus_min_val, plus_max_val, plus_min_loc, plus_max_loc = cv2.minMaxLoc(plus_result)
        print(plus_max_val)
        if plus_max_val > 0.9:
            rarity += '+'
    print(rarity, rarity_match)





# # Create crops for Rarity Templates
# img = cv2.imread('Rarity/Mythic+.jpg', 1)
# print(img.shape[0:2])
# crop = img[59:68, 4:12]
# cv2.imshow('ad', img)
# cv2.imshow('ss', crop)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite('Rarity/Mythic+.jpg', crop)
