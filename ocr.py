import cv2
import pytesseract
import numpy as np
import math
import json
import re
from difflib import SequenceMatcher
import os
from pytesseract import Output

def lDist(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class OCR:
    resultPath = './temp/result.jpeg'

    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        super().__init__()

    def cropImage(self, path):
        image = cv2.imread(path, -1)
        if image is None:
            print('no image found')
            return
        org = image.copy()
        image = cv2.resize(image, (300, 300))
        HEIGHT, WIDTH, _ = org.shape

        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(image, (5, 5), 0)
        edged = cv2.Canny(image, 75, 200)
        kernel = np.ones((30, 30), np.uint8)
        closing = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        edges = cv2.Canny(closing, 100, 200)

        (contours, _) = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        topLeftX = 299
        topLeftY = 299

        topRightX = 0
        topRightY = 299

        bottomLeftX = 299
        bottomLeftY = 0

        bottomRightX = 0
        bottomRightY = 0

        for contour in contours:
            for c in contour:
                list_of_c = list(c)
                x = list_of_c[0][0]
                y = list_of_c[0][1]
                if lDist(x, y, 0, 0) < lDist(topLeftX, topLeftY, 0, 0):
                    topLeftX = x
                    topLeftY = y
                if lDist(x, y, 299, 0) < lDist(topRightX, topRightY, 299, 0):
                    topRightX = x
                    topRightY = y
                if lDist(x, y, 0, 299) < lDist(bottomLeftX, bottomLeftY, 0, 299):
                    bottomLeftX = x
                    bottomLeftY = y
                if lDist(x, y, 299, 299) < lDist(bottomRightX, bottomRightY, 299, 299):
                    bottomRightX = x
                    bottomRightY = y

        cv2.line(edges, (topLeftX, topLeftY),
                 (topLeftX, topLeftY), (255, 0, 0), 5)
        cv2.line(edges, (topRightX, topRightY),
                 (topRightX, topRightY), (255, 0, 0), 5)
        cv2.line(edges, (bottomLeftX, bottomLeftY),
                 (bottomLeftX, bottomLeftY), (255, 0, 0), 5)
        cv2.line(edges, (bottomRightX, bottomRightY),
                 (bottomRightX, bottomRightY), (255, 0, 0), 5)

        topLeftX = int((topLeftX / 300) * WIDTH)
        topRightX = int((topRightX / 300) * WIDTH)
        bottomLeftX = int((bottomLeftX / 300) * WIDTH)
        bottomRightX = int((bottomRightX / 300) * WIDTH)

        topLeftY = int((topLeftY / 300) * HEIGHT)
        topRightY = int((topRightY / 300) * HEIGHT)
        bottomLeftY = int((bottomLeftY / 300) * HEIGHT)
        bottomRightY = int((bottomRightY / 300) * HEIGHT)

        sPoints = np.array(
            [[topLeftX, topLeftY], [topRightX, topRightY], [
                bottomRightX, bottomRightY], [bottomLeftX, bottomLeftY]],
            np.float32)

        tPoints = np.array(
            [[0, 0], [WIDTH - 1, 0], [WIDTH - 1, HEIGHT - 1], [0, HEIGHT - 1]], np.float32)

        M = cv2.getPerspectiveTransform(sPoints, tPoints)
        newImage = cv2.warpPerspective(org, M, (WIDTH, HEIGHT))

        # blur = cv2.blur(newImage, (5, 5))
        # print(pytesseract.image_to_string(newImage))
        # cv2.imshow("Test", edges)
        # k = cv2.waitKey(0)
        try:
            os.remove(OCR.resultPath)
        except OSError:
            pass
        print('image removed')
        cv2.imwrite(OCR.resultPath, newImage)
        print('crop done')

    def detect(self, json_path, path=None):
        if path is None:
            path = OCR.resultPath
        img = cv2.imread(path)
        h, w, _ = img.shape

        detectJSON = json.load(open(json_path))

        for doc in detectJSON['doc']:
            mulH = float(h) / doc['mh']
            mulW = float(w) / doc['mw']

            cx = int(doc['y'] * mulH)
            cy = int(doc['x'] * mulW)
            cw = int(doc['h'] * mulH)
            ch = int(doc['w'] * mulW)

            cropImg = img[cx:cx + cw:, cy:cy + ch]
            data = pytesseract.image_to_string(cropImg, lang='eng+guj')
            # print(data)
            # cv2.imshow("Test", cropImg)
            # k = cv2.waitKey(0)
            # frame = cv2.GaussianBlur(cropImg, (0, 0), 3)

            print(data)
            if doc['char'] == 'alpha':
                refineData = re.sub('[^a-zA-Z ]+', '', data)
                per = similar(refineData.lower(), doc['f'].lower())
                if per > 0.8:
                    print('Document type is : ', doc['name'])
                    print(refineData)
                    return doc['name']
            elif doc['char'] == 'guj':
                per = similar(data, doc['f'].lower())
                if per > 0.8:
                    print('Document type is : ', doc['name'])
                    print(data)
                    return doc['name']

    def dataFind(self, json_path, image_path=None):
        if image_path is None:
            image_path = OCR.resultPath

        doc = json.load(open(json_path))
        img = cv2.imread(image_path)

        ocrImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, _ = img.shape
        mulH = float(h) / doc['h']
        mulW = float(w) / doc['w']

        dictData = {
            'type': doc['type'],
            'doc': []
        }

        for data in doc['data']:
            cx = int(data['y'] * mulH)
            cy = int(data['x'] * mulW)
            cw = int(data['h'] * mulH)
            ch = int(data['w'] * mulW)

            cropImg = ocrImg[cx:cx + cw:, cy:cy + ch]
            dataOCR = pytesseract.image_to_string(cropImg)
            refineData = re.sub(data['char'], '', dataOCR)
            if len(refineData) < 4:
                frame = cv2.GaussianBlur(cropImg, (0, 0), 3)
                grayCrop = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                ret, thresh1 = cv2.threshold(
                    grayCrop, data['thresh'], 255, cv2.THRESH_BINARY)
                dataOCR = pytesseract.image_to_string(thresh1)
                refineData = re.sub(data['char'], '', dataOCR)
                # cv2.imshow('Test', thresh1)
                # cv2.waitKey(0)
            print('dataData: ', data['name'], ': ', refineData)
            # cv2.imshow('Test', cropImg)
            # cv2.waitKey(0)
            dictData['doc'].append({
                'field': data['name'],
                'data': refineData
            })

        return dictData

    def aadhar(self, path=None):
        if path is None:
            path = OCR.resultPath
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, thresh1 = cv2.threshold(img, 115, 255, cv2.THRESH_BINARY)

        # print(pytesseract.image_to_string(thresh1))
        res = pytesseract.image_to_data(
            thresh1, lang="eng+guj", output_type=Output.DICT)
        # print(res['text'])

        checkPos = 0
        nameCount = 0
        numCount = 0
        nameEngCount = 0

        name = ''
        nameEng = ''
        gender = ''
        aadharNum = ''
        dob = ''
        flag = False

        for word in res['text']:
            # print(word, '<----')
            if checkPos == 0:
                if word == 'ભારત':
                    # print(word)
                    checkPos += 1
            elif checkPos == 1:
                if word == 'સરકાર':
                    # print(word)
                    checkPos += 1
            elif checkPos == 2:
                if word == 'India':
                    # print(word)
                    checkPos += 1
            elif checkPos == 3:
                if len(word) > 3:
                    if nameCount < 2:
                        nameCount += 1
                        print(word)
                        name = name + ' ' + word
                    else:
                        print(word)
                        name = name + ' ' + word
                        checkPos += 1
            elif checkPos == 4:
                if len(word) > 3:
                    if nameEngCount < 2:
                        nameEngCount += 1
                        print(word)
                        nameEng = nameEng + ' ' + word
                    else:
                        print(word)
                        nameEng = nameEng + ' ' + word
                        checkPos += 1
            elif checkPos == 5:
                if word == 'DOB':
                    checkPos += 1
            elif checkPos == 6:
                if len(word) > 5:
                    print(word)
                    dob = word
                    checkPos += 1
            elif checkPos == 7:
                if word == 'Male' or word == 'Female':
                    checkPos += 1
                    print(word)
                    gender = word
            elif checkPos == 8:
                if len(word) == 4:
                    if numCount < 2:
                        numCount += 1
                        print(word)
                        aadharNum = aadharNum + ' ' + word
                    else:
                        print(word)
                        aadharNum = aadharNum + ' ' + word
                        checkPos += 1
            elif checkPos == 9:
                if word.strip() == 'આધાર':
                    print(word)
                    flag = True
                    break

        print(name.strip(), nameEng.strip(),
              gender, dob, aadharNum.strip(), flag)

        dictData = None
        if flag:
            dictData = {
                'type': 'Aadhar',
                'doc': [
                    {
                        'field': 'Name-english',
                        'data': nameEng.strip()
                    },
                    {
                        'field': 'Name-gujarati',
                        'data': name.strip()
                    },
                    {
                        'field': 'gender',
                        'data': gender
                    },
                    {
                        'field': 'Date Of Birth',
                        'data': dob
                    },
                    {
                        'field': 'Aadhar Number',
                        'data': aadharNum.strip()
                    }
                ]
            }

        return dictData


ocr = OCR()