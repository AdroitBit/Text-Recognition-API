"""
I compile to exe with
pyinstaller --onefile --console E-finder.py
"""
print("setting up...")
def format(s):
	return s.format(char_to_find)
from TextReader_Module import *
from Additional_Function import *

print("Ready\n")

print('Please pick the images to find "E"')
imgs_toFind_E=Images.fromAddress(pickFiles('pick files to find "E"',"Image to find E/"))
imgs_toFind_E.add(Image.fromScreen().renameTo("ScreenShot.jpg"))
imgs_E=Images.inFolder("E image");
address_toWrite_E="E Result/";


char_to_find="E"
imgs_left=imgs_toFind_E.len()
for img in imgs_toFind_E.imgs:
	alphabets=img.readAlphabets()
	oimg=img;
	filename=img.name.split("\\")[-1].split("/")[-1].split(".")
	[basename,extension]=filename
	
	#hightlight E
	print(format("Finding and Highlighing {0}...."))
	img=oimg.copy()
	for i in range(len(alphabets)):
		if(alphabets[i].char.upper()==char_to_find):
			img=img.rect(
				pos1=alphabets[i].pos1,
				pos2=alphabets[i].pos2,
				color=(0,255,0),
				thick=2,
				margin=4
			)
	print(format("Saving image with Highlighted {0}...."))
	img.saveAs(format(address_toWrite_E+basename+"_highlight_{0}."+extension));
	
	#place_E image
	img=oimg.copy()
	for i in range(len(alphabets)):
		if(alphabets[i].char.upper()==char_to_find):
			newE=imgs_E[random.randint(0,imgs_E.len()-1)].copy().resize(
				width=alphabets[i].w+10,
				constrain_aspect_ratio=True
			)
			img.placeImg(
				newE,
				alphabets[i].x,
				alphabets[i].y
			)
	img.saveAs(format(address_toWrite_E+basename+"_place_{0}"+"."+extension));
	
	imgs_left-=1
	mprint("- ",imgs_left," images left\n")
	
mprint('Finished! Images are saved to "',address_toWrite_E,'"');
print('You can close the program now :D')
while True:
	input()

