"""
The following script was created to remove the background from multiple images and then apply a desired background.

PREREQUISITES:
-A folder named ToBe_Modified within data/images folder containing all the images you want the background to be modified.
-A folder named Background_modification containing 2 folders: -Extracted_object
                                                              -Final_result
Input image can be either .jpg or .png
Output image has to be .png

"""


import os
from rembg import remove 
from PIL import Image

import Image_Modification

images_path = os.path.join(os.path.dirname( __file__ ), '..', 'data', 'images', 'ToBe_Modified')


items = os.listdir(images_path)
items_splitted = [i.split(".")[0] for i in items]

for i in range(len(items)):

    #Remove background
    # Store path of the image in the variable input_path 
    input_path =  os.path.join(images_path, items[i])
    
    # Store path of the output image in the variable output_path
    File_name = items_splitted[i] + '.png' 
    output_path = os.path.join(os.path.dirname( __file__ ), '..', 'Background_modification', 'Extracted_object', File_name)
    
    # Processing the image 
    input = Image.open(input_path) 
    
    # Removing the background from the given Image 
    output = remove(input) 
    
    #Saving the image in the given path 
    output.save(output_path)

    
    #Add new background
    new_background_path = os.path.join(os.path.dirname( __file__ ), '..', 'Background_modification', 'Black_background.jpg')
    extracted_image_path = output_path #The result from the remove_background() is the extracted object image

    final_image = Image_Modification.place_on_new_background(extracted_image_path, new_background_path)
    final_image_path = os.path.join(os.path.dirname( __file__ ), '..', 'Background_modification', 'Final_result', File_name)
    final_image.save(final_image_path)




#TESTING ON A SINGLE PHOTO
'''

#Remove background
# Store path of the image in the variable input_path 
input_path =  os.path.join(os.path.dirname( __file__ ), '..', 'Background_modification', 'Background_with_object.png')

# Store path of the output image in the variable output_path
output_path = os.path.join(os.path.dirname( __file__ ), '..', 'Background_modification', 'Background_with_object_extracted.png')

# Processing the image 
input = Image.open(input_path) 

# Removing the background from the given Image 
output = remove(input) 

#Saving the image in the given path 
output.save(output_path)

'''