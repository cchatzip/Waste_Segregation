import os
import re

path = os.path.join('.', 'data', 'images', 'train')
regex_PET = re.compile('(.*a01.*jpg$)')
regex_HDPE = re.compile('(.*a02.*jpg$)')
regex_PP = re.compile('(.*a05.*jpg$)')
regex_PS = re.compile('(.*a06.*jpg$)')

items = os.listdir(path)

PET_num = 0
HDPE_num = 0
PS_num = 0
PP_num = 0

for i in range(len(items)):
    if regex_PET.match(items[i]):
        PET_num += 1

    elif regex_HDPE.match(items[i]):
        HDPE_num += 1

    elif regex_PP.match(items[i]):
        PP_num += 1

    elif regex_PS.match(items[i]):
        PS_num += 1


    # print(len(items))

print(f' PET: {PET_num} \n HDPE: {HDPE_num} \n PP: {PP_num} \n PS: {PS_num}')