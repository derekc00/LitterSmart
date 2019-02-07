import io
import os

from google.cloud import vision
from google.cloud.vision import *

import webcamTest

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/derekchang/Downloads/recycle-sort-527b27b21dda.json'

# Instantiates a client
client = vision.ImageAnnotatorClient()

badWords = ['Hand', 'Finger', 'Thumb', 'Gesture', 'Smile', 'Selfie', 'Forehead', 'Jaw', 'Arm']


recycleWords = ['Can', 'Aluminum can', 'Plastic bottle', 'Bottled water',
                'Bottle', 'Drink', 'Silver', 'Metal', 'Aluminium foil', 'Diamond', 'Beverage can']


trashWords = ['Snack', 'Junk food', 'Plastic', 'Fork', 'Cutlery', 'Tableware',
              'Spoon', 'Kitchen utensil', 'Plastic bag']


compostWords = ['Food', 'Cuisine', 'Side dish']

minimum_confidence = 0.5

interestingWords  = ['Junk food', 'Paper']

trashDict = {}
results = []



# The name of the image file to annotate
def check_imgs() -> str:
    count = 0





    for filename in sorted(os.listdir("shots"), key=(lambda x: int(x[:-4]))):

        if len(os.listdir("shots")) - 5 < count < len(os.listdir("shots")):
            break

        count += 1
        if count % 8 == 0:
            # print(filename)
            file_name = os.path.join(os.path.dirname(__file__), 'shots/%s'%(filename))

            # Loads the image into memory
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            # Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations

            """Create dictionary  ->  key: word  |  value: score"""
            trashDict.clear()

            #POPULATE 'trashdict'
            for label in labels:
                trashDict[label.description] = label.score

            # print('Labels:')
            # for label, score in trashDict.items():
            #     print(label, "  score: ", score)


            answer = getAnswer()
            if answer != "?????":
                results.append(getAnswer())

            print("\n")

    print(results)

    def most_common(lst):
        if len(lst) > 0:

            return max(set(lst), key=lst.count)
        return 'None'
    print("RESULT: ", most_common(results))
    return most_common(results)

def getAnswer() -> str:

    """Take out BAD WORDS"""
    print("\n")
    for word in badWords:
        if word in trashDict:
            del trashDict[word]
            print("Deleted: ", word)

    print('New Labels:')
    for label, score in trashDict.items():
        print(label, "  score: ", score)
    print("\n")


    """Checks each word in trashdict. Starts at the most confident. ends when confidence is below minimum value"""
    for word in sorted(list(trashDict.keys()), key=(lambda x: trashDict[x]), reverse=True):

       if trashDict[word] > minimum_confidence:
            #Check recycle
            if word in recycleWords:
                return 'RECYCLE'
            if word in trashWords:
                return 'TRASH'
            if word in compostWords:
                return 'COMPOST'



    #If 'paper' or 'paper product' shows up in the first two guesses, determine if it is clean
    if 'Paper' in sorted(list(trashDict.keys()), key=(lambda x: trashDict[x])) or 'Paper product' in sorted(list(trashDict.keys()), key=(lambda x: trashDict[x])):
        return "RECYCLE"
    return "NONE"