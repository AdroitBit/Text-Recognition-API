print("setting up...")
from TextRecognizer.TextRecognizer import * #just import this module.and It worked!

def format(s):
	return s.format(char_to_find)
print("Ready\n")

print('Please pick the images to find "E"')
imgs_toFind_E=Images.fromAddress(pickFiles('pick the images to find "E"',"Image to find E/"))
imgs_toFind_E.add(Image.fromScreen().renameTo("Screenshot.jpg"))#will save as "ScreenShot.jpg"
imgs_E=Images.inFolder("E image");

address_toWrite_E=imgs_toFind_E[0].foldername+"/E Result/";
if(createPath(address_toWrite_E)==-1):
	print('Can\'t create folder "%s"' % address_toWrite_E)
	input();
	exit();
else:
	print('Link to folder "%s" completed!' % address_toWrite_E)


	
print()

print("Highlight E? [Y/N]:",end="")
highlight_E=input();
highlight_E=True if highlight_E=="Y" else False
print()


char_to_find="E"
imgs_left=imgs_toFind_E.len()
for img in imgs_toFind_E.imgs:
	print('"%s"' % img.name)
	alphabets=img.readAlphabets()
	oimg=img;
	[basename,extension]=img.filename.split(".")
	
	#hightlight E
	if(highlight_E==True):
		print(format("- Finding and Highlighing {0}"))
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
		print(format("- Saving image with Highlighted {0}"))
		img.saveAs(format(address_toWrite_E+basename+"_highlight_{0}."+extension));
	
	#place_E image
	print(format("- Replacing {0}"))
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
	print(format("- Saving the images with replaced {0}"))
	img.saveAs(format(address_toWrite_E+basename+"_place_{0}"+"."+extension));
	
	imgs_left-=1
	print("...%s images left\n" % imgs_left)
	
print('Finished! Images are saved to "%s"' % address_toWrite_E)
print('You can close the program now :D')
input();

