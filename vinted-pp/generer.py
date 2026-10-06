import math, sys
from PIL import Image, ImageDraw, ImageFont
S=2160; OUT=sys.argv[1]; NAME="MA BOUTIQUE"; MONO="MB"
F="/usr/share/fonts/opentype/inter/"
def font(n,s): return ImageFont.truetype(n,s)
def ctext(d,y,t,f,fill,spacing=0):
    w=sum(d.textlength(c,font=f) for c in t)+spacing*(len(t)-1); x=(S-w)/2
    for c in t: d.text((x,y),c,font=f,fill=fill,anchor="ls"); x+=d.textlength(c,font=f)+spacing
def ring(img,t,r,f,fill,start=-90):
    total=sum(ImageDraw.Draw(img).textlength(c,font=f) for c in t)
    ang=start-math.degrees(total/r)/2
    for c in t:
        w=ImageDraw.Draw(img).textlength(c,font=f); a=ang+math.degrees(w/2/r)
        tile=Image.new("RGBA",(400,400),(0,0,0,0)); ImageDraw.Draw(tile).text((200,200),c,font=f,fill=fill,anchor="mm")
        tile=tile.rotate(-(a+90),resample=Image.BICUBIC)
        x=S/2+r*math.cos(math.radians(a)); y=S/2+r*math.sin(math.radians(a))
        img.alpha_composite(tile,(int(x-200),int(y-200))); ang+=math.degrees(w/r)
def ring_bottom(img,t,r,f,fill):
    dr=ImageDraw.Draw(img); total=sum(dr.textlength(c,font=f) for c in t)
    ang=90+math.degrees(total/r)/2
    for c in t:
        w=dr.textlength(c,font=f); a=ang-math.degrees(w/2/r)
        tile=Image.new("RGBA",(400,400),(0,0,0,0)); ImageDraw.Draw(tile).text((200,200),c,font=f,fill=fill,anchor="mm")
        tile=tile.rotate(-(a-90),resample=Image.BICUBIC)
        x=S/2+r*math.cos(math.radians(a)); y=S/2+r*math.sin(math.radians(a))
        img.alpha_composite(tile,(int(x-200),int(y-200))); ang-=math.degrees(w/r)
def hanger(d,cx,cy,w,col,lw):
    d.arc((cx-45,cy-150,cx+45,cy-60),180,90,fill=col,width=lw)
    d.line((cx,cy-60,cx,cy-30),fill=col,width=lw)
    d.line((cx,cy-30,cx-w/2,cy+60),fill=col,width=lw); d.line((cx,cy-30,cx+w/2,cy+60),fill=col,width=lw)
    d.line((cx-w/2,cy+60,cx+w/2,cy+60),fill=col,width=lw)
    for x in (cx-w/2,cx+w/2): d.ellipse((x-lw/2,cy+60-lw/2,x+lw/2,cy+60+lw/2),fill=col)

# 1 — vert sapin + crème
img=Image.new("RGBA",(S,S),"#1F3D36"); d=ImageDraw.Draw(img)
hanger(d,S/2,640,520,"#EADFC8",34)
ctext(d,1330,MONO,font(F+"InterDisplay-Bold.otf",560),"#EADFC8",-10)
ctext(d,1520,NAME,font(F+"Inter-SemiBold.otf",110),"#C9A86A",28)
img.convert("RGB").resize((1080,1080),Image.LANCZOS).save(f"{OUT}/pp-vinted-1-vert.png")

# 2 — crème + terracotta, texte circulaire
img=Image.new("RGBA",(S,S),"#F4EDE1"); d=ImageDraw.Draw(img)
d.ellipse((S/2-930,S/2-930,S/2+930,S/2+930),outline="#B8573A",width=14)
d.ellipse((S/2-650,S/2-650,S/2+650,S/2+650),outline="#B8573A",width=6)
for a in (180,0):
    x=S/2+790*math.cos(math.radians(a)); d.ellipse((x-16,S/2-16,x+16,S/2+16),fill="#B8573A")
ring(img,NAME,790,font(F+"Inter-Bold.otf",120),"#B8573A",start=-90)
ring_bottom(img,"SECONDE MAIN · ENVOI RAPIDE",790,font(F+"Inter-SemiBold.otf",88),"#B8573A")
d=ImageDraw.Draw(img)
ctext(d,1250,MONO,font("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",420),"#2B2420",-6)
img.convert("RGB").resize((1080,1080),Image.LANCZOS).save(f"{OUT}/pp-vinted-2-creme.png")

# 3 — noir minimal + accent
img=Image.new("RGBA",(S,S),"#111111"); d=ImageDraw.Draw(img)
ctext(d,1180,MONO,font(F+"InterDisplay-ExtraBold.otf",700),"#FFFFFF",-30)
d.rounded_rectangle((S/2-380,1300,S/2+380,1320),10,fill="#FF6B4A")
ctext(d,1500,NAME,font(F+"Inter-Bold.otf",112),"#FFFFFF",24)
ctext(d,1640,"VENDEUR PRO",font(F+"Inter-Medium.otf",72),"#FF6B4A",30)
img.convert("RGB").resize((1080,1080),Image.LANCZOS).save(f"{OUT}/pp-vinted-3-noir.png")

# aperçu recadré en cercle comme sur Vinted
prev=Image.new("RGB",(1080*3+160,1160),"#FFFFFF")
for i,n in enumerate(["1-vert","2-creme","3-noir"]):
    im=Image.open(f"{OUT}/pp-vinted-{n}.png"); m=Image.new("L",(1080,1080),0); ImageDraw.Draw(m).ellipse((0,0,1079,1079),fill=255)
    prev.paste(im,(40+i*1120,40),m)
prev.resize((prev.width//2,prev.height//2),Image.LANCZOS).save(f"{OUT}/apercu-cercle.png")
