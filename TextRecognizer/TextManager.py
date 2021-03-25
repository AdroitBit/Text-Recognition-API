class AlphaBet:
	def __init__(self,char,x1,y1,x2,y2):
		self.char=char;
		(x1,y1)=(int(x1),int(y1))
		(x2,y2)=(int(x2),int(y2))
		if x1>x2:
			(x1,x2)=(x2,x1)
		if y1>y2:
			(y1,y2)=(y2,y1)
		
		(self.x1,self.y1)=(x1,y1)
		(self.x2,self.y2)=(x2,y2)
		(self.pos1,self.pos2)=((x1,y1),(x2,y2))
		(self.x,self.y)=((x1+x2)/2,(y1+y2)/2)
		(self.w,self.h)=(x2-x1,y2-y1)
class AlphaBets:
	def __init__(self,data):#data is dict
		self.alphabets=[];
class Text:
	def __init__(self,text,x,y,w,h):
		self.text=text;
		self.x1=x;self.y1=y;
		self.x2=x+w;self.y2=y+h;
		(self.x,self.y)=(x+w/2,y+h/2);