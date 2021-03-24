from TextReader_Module import *
class Images:
	def __init__(self,*imgs):
		self.imgs=[];
		for i in imgs:
			if isiterable(i):
				for i2 in i:
					if isinstance(i2,Image):
						self.imgs.append(i2);
			elif isinstance(i,Image):
				self.imgs.append(i);
		self._index=-1;
	def __getitem__(self,key):
		return self.imgs[key];
	def len(self):
		return len(self.imgs)
	def add(self,*imgs):
		for i in imgs:
			self.imgs.append(i);
		return self
			
	@staticmethod
	def inFolder(folderAdr):
		filesname=[i for i in (glob(folderAdr+"/*.jpg")+glob(folderAdr+"/*.png"))]
		return Images([Image.fromAddress(i) for i in filesname])
	def fromAddress(*adr):
		if(isiterable(adr[0])):
			return Images([Image.fromAddress(i) for i in adr[0] ])
		else:
			return Images.fromAddress(adr)
		


class Image:
	def __init__(self,name,data):
		self.name=name
		self.data=data
	@property
	def width(self):
		return self.data.shape[1];
	@property
	def height(self):
		return self.data.shape[0];
		
	def renameTo(self,name):
		self.name=name
		return self
	def copy(self):
		return Image(self.name,self.data.copy())
	def saveAs(self,adr):
		cv2.imwrite(adr,self.data)
		return self
	def invert(self):
		self.data=cv2.bitwise_not(self.data)
		return self
	def toGray(self):
		self.data=cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)
		return self
	def to2bit(self):
		self.data=cv2.adaptiveThreshold(
			self.to_gray(),
			255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1
		)
		return self
	
	def readTexts(self):
		texts=[];
		d=pytesseract.image_to_data(self.data, output_type=Output.DICT);
		for i in range(len(d['level'])):
			if d['text'][i]=="":
				continue
			texts.append(Text(
				d['text'][i],
				d['left'][i],d['top'][i],
				d['width'][i],d['height'][i]
			));
		return texts
	def readAlphabets(self):
		alphabets=[]
		b=pytesseract.image_to_boxes(self.data)#I have to use this function which have the uncompleted API
		"""
		pytesseract.image_to_boxes will return tuple of string like this
		R 11 12 13 14 0
		S 49 10 20 50 0
		but it's actually ["R","\s","1","1",...,"\n",...,0]
		which also include "\s" and "\n" for some reason
		and 0 just mean nothing
		"""
		b="".join(b).replace("0\n","").split(' ');
		for i in range(0,int(len(b)/5)):
			i2=i*5
			char=b[i2];
			x1=b[i2+1];
			y1=b[i2+2];
			x2=b[i2+3];
			y2=b[i2+4];
			alphabets.append(AlphaBet(
				char,
				int(x1),self.height-int(y1),#self.height to fix open-cv2 bug
				int(x2),self.height-int(y2)
			))
			
		return alphabets
		
	@staticmethod
	def fromAddress(adr):
		return Image(
			adr,
			cv2.imread(adr)
		)
	@staticmethod
	def fromScreen(pos1=None,pos2=None,name="ScreenShot.jpg"):
		if not forsomeNone(pos1,pos2):
			data=cv2.cvtColor(nm.array(ImageGrab.grab(bbox=(pos1[0],pos1[1],pos2[0],pos2[1]))),cv2.COLOR_BGR2RGB)
		else:
			screen=pyautogui.size();
			data=cv2.cvtColor(nm.array(ImageGrab.grab(bbox=(0,0,screen.width,screen.height))),cv2.COLOR_BGR2RGB)
		return Image(
			hex(id(data)),
			data
		)
	
	def rect(
		self,
		pos1=None,pos2=None,
		color=(0,255,0),thick=10,margin=(0,0,0,0)#left,up,right,bottom
	):
		if not forallNone(pos1,pos2):
			if isinstance(margin,int):
				margin=(margin,margin,margin,margin)
			_pos1=(pos1[0]-margin[0],pos1[1]-margin[1])
			_pos2=(pos2[0]+margin[3],pos2[1]+margin[3])
			self.data=cv2.rectangle(self.data,_pos1,_pos2,color,thick);
		return self
	def resize(img,width=nan,height=nan,pos1=None,pos2=None,interpolation=None,constrain_aspect_ratio=False):
		#design
		"""
			resize with width
			resize(img,width,constrain_aspect_ratio=true/false)
			
			
			resize with height
			resize(img,width,constrain_aspect_ratio=true/false)
			
			resize width and height
			resize(img,width,height)
		"""
		if forallReal(width,height):
			img.data=cv2.resize(img.data,(int(width),int(height)),interpolation=interpolation)
			return img
		elif isreal(width):
			return img.resize(
				width,
				img.height/img.width*width if constrain_aspect_ratio==True else img.height,
				interpolation=interpolation
			)
		elif isreal(height):
			return img.resize(
				img.width/img.height*height if constrain_aspect_ratio==True else img.width,
				height,
				interpolation=interpolation
			)
		elif not forallNone(pos1,pos2):
			return img.resize(
				pos2[0]-pos1[0],
				pos2[1]-pos1[1],
				interpolation=interpolation
			)
	def placeImg(img,img_to_place,x,y,alignX=0,alignY=0,interpolation=None):
		xi=yi=0;
		placeWidth=img_to_place.width;
		placeHeight=img_to_place.height;
		limitWidth=img.width;
		limitHeight=img.height;
		while yi<placeHeight:
			xi=0;
			yreal=int(y-placeHeight/2*(alignY+1))+yi
			if yreal>0 and yreal<limitHeight:
				while xi<placeWidth:
					xreal=int(x-placeWidth/2*(alignX+1))+xi
					if xreal>0 and xreal<limitWidth:
						img.data[yreal][xreal]=img_to_place.data[yi][xi]
					xi+=1
			yi+=1
			
		return img
