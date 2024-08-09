import os
import re
import shutil

path = os.path.join(os.path.dirname( __file__ ),'..', 'data', 'images', 'train')
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

    file_to_copy = items[i]
    source_directory = os.path.join(path, file_to_copy)

    if regex_PET.match(items[i]):
        PET_num += 1
        destination_directory = os.path.join(os.path.dirname( __file__ ),'..', 'data', 'images', 'PET', file_to_copy)
        shutil.copy(source_directory, destination_directory)


    elif regex_HDPE.match(items[i]):
        HDPE_num += 1
        destination_directory = os.path.join(os.path.dirname( __file__ ),'..', 'data', 'images', 'HDPE', file_to_copy)
        shutil.copy(source_directory, destination_directory)

    elif regex_PP.match(items[i]):
        PP_num += 1
        destination_directory = os.path.join(os.path.dirname( __file__ ),'..', 'data', 'images', 'PP', file_to_copy)
        shutil.copy(source_directory, destination_directory)

    elif regex_PS.match(items[i]):
        PS_num += 1
        destination_directory = os.path.join(os.path.dirname( __file__ ),'..', 'data', 'images', 'PS', file_to_copy)
        shutil.copy(source_directory, destination_directory)


    # print(len(items))

print(f' PET: {PET_num} \n HDPE: {HDPE_num} \n PP: {PP_num} \n PS: {PS_num}')