import os
import re

Images_path = os.path.join(os.path.dirname( __file__ ),'..', 'data', 'images', 'val')


items = os.listdir(Images_path)
items = [i.split(".")[0] for i in items]
# print(items)


Labels_path = os.path.join(os.path.dirname( __file__ ),'..', 'data', 'labels', 'val')

labels = os.listdir(Labels_path)
labels = [i.split(".")[0] for i in labels]
# print('Labels: \n', labels)


for i in range(len(labels)):

    if labels[i] not in items:
        # print(labels[i])
        FileForRemoval = labels[i] + '.txt'
        # print(FileForRemoval)
        UnwantedFile_path = os.path.join(Labels_path, FileForRemoval)
        if os.path.exists(UnwantedFile_path): 
            os.remove(UnwantedFile_path)
            print(f"File '{labels[i]}' deleted successfully.")
        else: 
            print(f"File '{labels[i]}' not found.")
