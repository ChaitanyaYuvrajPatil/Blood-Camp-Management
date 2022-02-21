import os
import cv2
import numpy as np
certificate_template_image = cv2.imread(r'C:\Users\mypc\PycharmProjects\Blood Camp Management\certificate_vol.jpg')
m = cv2.putText(certificate_template_image, "Chaitanya Patil", (1166, 1350), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 250), 13,cv2.LINE_AA)
cv2.imwrite(r"C:\Users\mypc\PycharmProjects\Blood Camp Management\Certificates\new_img.jpg", certificate_template_image)
#cv2.imshow('ram',m)
#cv2.waitKey(0)
print('Executed')

'''
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
df = pd.read_csv('list.csv')
font = ImageFont.truetype('arial.ttf',60)
for index,j in df.iterrows():
    img = Image.open('certificate.jpg')
    draw = ImageDraw.Draw(img)
    draw.text(xy=(725,760),text='{}'.format(j['name']),fill=(0,0,0),font=font)
    img.save('pictures/{}.jpg'.format(j['name'])) 
'''