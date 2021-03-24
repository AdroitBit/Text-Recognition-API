from Importer import *
from TextReader_Module import *


screensize=pyautogui.size();

img=capture_screen(0,0,screensize.width/2,screensize.height);
#img=get_image('Test_image\\'+input());
img=make_img_2bit(img);
alphabets=obtain_alphabets(img);
"""i=0;
for i in range(len(alphabets)):
	if alphabets[i].char=="f":
		break;
alphabets=[alphabets[i]]"""
#texts=obtain_texts(img);




"""for i in range(len(texts)):
	#if(texts[i].text=="find"):
	dt=0.2
	mouse.moveTo(texts[i].x,texts[i].y,duration=dt)
	time.sleep(dt);
	#print(texts[i].text);"""
for i in range(len(alphabets)):
	#if(texts[i].text=="find"):
	if(alphabets[i].char.upper()=="E"):
		dt=0.5
		mouse.moveTo(alphabets[i].x,screensize.height-alphabets[i].y,duration=dt)
		time.sleep(dt);
		print(alphabets[i].char,end="");


#gc.collect()