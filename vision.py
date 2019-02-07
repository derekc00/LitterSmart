import io
import os
import cv2
from google.cloud import vision
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/derekchang/Downloads/recycle-sort-527b27b21dda.json'



badWords = ['Hand', 'Finger', 'Thumb', 'Gesture', 'Smile', 'Selfie']


recycleWords = ['Can', 'Aluminum can', 'Plastic bottle', 'Water', 'Bottled water',
                'Bottle', 'Drink', 'Silver', 'Metal', 'Aluminium foil', 'Diamond', 'Beverage can']


trashWords = ['Snack', 'Junk food', 'Plastic', 'Fork', 'Cutlery', 'Tableware',
              'Spoon', 'Kitchen utensil', 'Plastic bag']


compostWords = ['Food', 'Cuisine', 'Side dish']

minimum_confidence = 0.5

interestingWords  = ['Junk food', 'Paper']




cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    cv2.imshow('frame', rgb)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        out = cv2.imwrite('capture.jpg', frame)
        break

cap.release()
cv2.destroyAllWindows()




# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'capture.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations




"""Create dictionary  ->  key: word  |  value: score"""
trashDict = {}
for label in labels:
    trashDict[label.description] = label.score


print('Labels:')
for label, score in trashDict.items():
    print(label , "  score: ", score)







"""TESTING RECYCLING WORDS"""
print("\n")

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



    for word in recycleWords:
        if word in trashDict and trashDict[word] > minimum_confidence:
            return 'RECYCLE'
    for word in trashWords:
        if word in trashDict and trashDict[word] > minimum_confidence:
            return "TRASH"
    for word in compostWords:
        if word in trashDict and trashDict[word] > minimum_confidence / 2:
            return "COMPOST"

    objects = list(trashDict.keys())
    objects.sort(key=(lambda x: trashDict[x]))
    # print(objects)

    #If 'paper' or 'paper product' shows up in the first two guesses, determine if it is clean
    if 'Paper' in objects[:3] or 'Paper product' in objects[:3]:
        return "Recycle if clean, otherwise, TRASH"
    return "lol waht  is this"
print(getAnswer())
