from Importer import *
import enum
def capture_screen(x1,y1,x2,y2):
	#screensize=pyautogui.size();
	return nm.array(ImageGrab.grab(bbox=(x1,y1,x2,y2)))
def get_image(adr):
	return cv2.imread(adr);
def white_img(img=None):
	img=nm.zeros(img.shape,nm.uint8);#bgr but wil be same as rgb
	for y in range(img.shape[0]):
		for x in range(img.shape[1]):
			for i in range(3):
				img[y][x][i]=255;
	return img
def black_img(img=None):
	img=nm.zeros(img.shape,nm.uint8);#bgr but wil be same as rgb
	for y in range(img.shape[0]):
		for x in range(img.shape[1]):
			for i in range(3):
				img[y][x][i]=0;
	return img
	
def make_img_2bit(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.GaussianBlur(img, (1,1), 0)#3,3
	img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1];
	return img
def make_img_invert(img):
	return cv2.bitwise_not(img)
def mixColor(img1,img2,value):
	if(img1.shape!=img2.shape):
		return None;
	img1=img1.copy();
	for y in range(img1.shape[0]):
		for x in range(img1.shape[1]):
			for i in range(3):
				img1[y][x][i]+=int((img2[y][x][i]-img1[y][x][i])*value)
	return img1
def mulColor(img1,img2):
	img1=img1.copy();
	for y in range(img1.shape[0]):
		for x in range(img1.shape[1]):
			for i in range(3):
				img1[y][x][i]=(img1[y][x][i]*img2[y][x][i])/0xffff*0xff
	return img1
			
def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = nm.zeros(image.shape,nm.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output
def noise_img(shape=None):
	if(shape is None):return None;
	img=nm.zeros(shape.shape,nm.uint8);
	img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV);
	for y in range(len(img)):
		for x in range(len(img[y])):
			img[y][x][0]=255*random.random()
			img[y][x][1]=255 if 255*random.random()>50 else 0
			img[y][x][2]=255 if 255*random.random()>50 else 0
	img=cv2.cvtColor(img,cv2.COLOR_HSV2RGB);
	return img
def color_noise(img,value):
	#img=cv2.cvtColor(img, cv2.COLOR_RGB2HSV);
	img=img.copy();
	noise=noise_img(img);
	#img=cv2.merge([r,g,b]);
	#img=cv2.cvtColor(img, cv2.COLOR_HSV2RGB);
	
	return mixColor(img,noise,value);
	
def obtain_texts(img):
	_texts_=[];
	_d_=pytesseract.image_to_data(img, output_type=Output.DICT);
	for i in range(len(_d_['level'])):
		if _d_['text'][i]=="":
			continue;
		_texts_.append(Text(
			_d_['text'][i],
			_d_['left'][i],_d_['top'][i],
			_d_['width'][i],_d_['height'][i]
		));
	return _texts_;
def obtain_alphabets(img):
	_alphabets_=[]
	_b_=pytesseract.image_to_boxes(img);
	_s_=_char_=_x1_=_y1_=_x2_=_y2_="";
	_i2_=0;	
	for i in range(0,len(_b_)):
		if _b_[i]!=' ' and _b_[i]!='\n':
			_s_+=_b_[i];
		else:
			_i3_=_i2_%6
			if _i3_==0:
				_char_=_s_
			else:
				_s_=int(_s_)
				if _i3_==1:
					_x1_=_s_
				elif _i3_==2:
					_y1_=_s_
				elif _i3_==3:
					_x2_=_s_
				elif _i3_==4:
					_y2_=_s_
				else:
					_alphabets_.append(AlphaBet(
						_char_,
						_x1_,img.shape[0]-_y1_,
						_x2_,img.shape[0]-_y2_
					))
			_s_="";
			_i2_+=1
	return _alphabets_;
pytesseract.pytesseract.tesseract_cmd=r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe";




#graphical stuff
def line(img,start,end,color,thick):
	return cv2.line(img,start,end,color,thick);
def rect(
	img,
	pos1=None,pos2=None,
	color=(0,255,0),thick=10,margin=(0,0,0,0),#left,up,right,bottom
	placeImg=None
	):
	if not forallNone(pos1,pos2):
		if isinstance(margin,int):
			margin=(margin,margin,margin,margin)
		_pos1_=(pos1[0]-margin[0],pos1[1]-margin[1])
		_pos2_=(pos2[0]+margin[3],pos2[1]+margin[3])
		return cv2.rectangle(img,_pos1_,_pos2_,color,thick);
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
		return cv2.resize(img,(int(width),int(height)),interpolation=interpolation);
	elif isreal(width):
		return resize(
			img,
			width,
			img.shape[0]/img.shape[1]*width if constrain_aspect_ratio==True else img.shape[0],
			interpolation=interpolation
		)
	elif isreal(height):
		return resize(
			img,
			img.shape[1]/img.shape[0]*height if constrain_aspect_ratio==True else img.shape[1],
			height,
			interpolation=interpolation
		)
	elif not forallNone(pos1,pos2):
		return resize(
			img,
			pos2[0]-pos1[0],
			pos2[1]-pos1[1],
			interpolation=interpolation
		)
def placeImg(img,img_to_put,x,y,w=nan,h=nan):
	#img_to_put.shape[0]
	if isnan(w):
		w=img_to_put.shape[0];
	if isnan(h):
		h=img_to_put.shape[1];
	_img_=img.copy()
	_img_[x:x+w,y:y+h]=img_to_put;
	return _img_
def placeImgVert(img,img_to_place,x,y,alignX=0,alignY=0,interpolation=None):
	_img_=img.copy();
	_xi_=_yi_=0;
	_placeWidth_=img_to_place.shape[1];
	_placeHeight_=img_to_place.shape[0];
	_limitWidth_=img.shape[1];
	_limitHeight_=img.shape[0];
	while _yi_<img_to_place.shape[0]:
		_xi_=0;
		_yreal_=int(y-_placeHeight_/2*(alignY+1))+_yi_
		if _yreal_>0 and _yreal_<_limitHeight_:
			while _xi_<img_to_place.shape[1]:
				_xreal_=int(x-_placeWidth_/2*(alignX+1))+_xi_
				if _xreal_>0 and _xreal_<_limitWidth_:
					_img_[_yreal_][_xreal_]=img_to_place[_yi_][_xi_]
				_xi_+=1
		_yi_+=1
		
	return _img_

