"""Builds the signage + ads texture atlases for World of Somnath.
Kannada-first boards (Karnataka signage rule: Kannada on top, larger). All brands are original/fictional."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json, os, random
HERE=os.path.dirname(os.path.abspath(__file__)); FONTS=os.path.join(HERE,'..','..','fonts')
KN=os.path.join(FONTS,'NotoSansKannada.ttf'); DISP=os.path.join(FONTS,'AnybodyCond.ttf'); FUN=os.path.join(FONTS,'FunnelDisplay.ttf')
def font(path,size,wght=800,wdth=None):
    f=ImageFont.truetype(path,size,layout_engine=ImageFont.Layout.RAQM)
    try:
        axes=f.get_variation_axes(); vals=[]
        for a in axes:
            n=a.get('name',b'')
            n=n.decode() if isinstance(n,bytes) else n
            if 'eight' in n or n.lower().startswith('w') and 'idth' not in n: vals.append(wght)
            elif 'idth' in n: vals.append(wdth if wdth else a['default'])
            else: vals.append(a['default'])
        f.set_variation_by_axes(vals)
    except Exception as e: pass
    return f
def fit(draw,text,path,maxw,start,wght=800,wdth=None):
    s=start
    while s>10:
        f=font(path,s,wght,wdth); w=draw.textlength(text,font=f)
        if w<=maxw: return f
        s-=2
    return font(path,10,wght,wdth)
def grime(im,amount=0.18,seed=0):
    rnd=random.Random(seed); W,H=im.size; ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for i in range(int(W*H/900)):
        x,y=rnd.randrange(W),rnd.randrange(H); r=rnd.randint(1,3); a=int(255*amount*rnd.random())
        d.ellipse([x,y,x+r,y+r],fill=(40,30,20,a))
    for i in range(18):
        x=rnd.randrange(W); h=rnd.randint(H//6,H); ov2=Image.new('RGBA',(rnd.randint(3,14),h),(60,45,30,int(255*amount*0.6)))
        ov.alpha_composite(ov2,(x,0))
    im.alpha_composite(ov.filter(ImageFilter.GaussianBlur(0.6)))
    return im
def board(w,h,kn,en,bg,fg,sub=None,seed=0,border=True,accent=None):
    # English leads (large); Kannada is a smaller secondary line, always beside the English.
    im=Image.new('RGBA',(w,h),bg); d=ImageDraw.Draw(im)
    if accent: d.rectangle([0,h-int(h*0.1),w,h],fill=accent)
    if border: d.rectangle([8,8,w-9,h-9],outline=fg,width=6)
    fe=fit(d,en,DISP,w-80,int(h*0.44),wght=880,wdth=72); d.text((w/2,h*0.38),en,font=fe,fill=fg,anchor='mm')
    fk=fit(d,kn,KN,w*0.62,int(h*0.2)); d.text((w/2,h*0.72),kn,font=fk,fill=fg,anchor='mm')
    if sub:
        fs=fit(d,sub,FUN,w*0.4,int(h*0.085),wght=600); d.text((w-26,h-22),sub,font=fs,fill=fg,anchor='rs')
    return grime(im,0.12,seed)

ATLAS={}
def pack(name,items,cell,grid,size=2048):
    at=Image.new('RGBA',(size,size),(0,0,0,255)); meta={}
    cw,ch=cell
    for i,(key,img) in enumerate(items):
        col,row=i%grid[0],i//grid[0]; x,y=col*cw,row*ch
        at.paste(img.resize((cw,ch),Image.LANCZOS),(x,y))
        # uv rect (u0,v0,u1,v1) with v up (glTF/three flips handled in blender via image flip)
        meta[key]=[x/size,1-(y+ch)/size,(x+cw)/size,1-y/size]
    at.convert('RGB').save(os.path.join(HERE,'atlas',name+'.png'),optimize=True)
    ATLAS[name]=meta
# ---------------- shop boards (1024x256) ----------------
SHOPS=[
 ('bakery','ಶ್ರೀ ಗಣೇಶ ಅಯ್ಯಂಗಾರ್ ಬೇಕರಿ','SRI GANESHA IYENGAR BAKERY','#c3122d','#fff1cf','Honey cake · Khara bun · Puffs'),
 ('darshini','ಉಡುಪಿ ದರ್ಶಿನಿ','UDUPI DARSHINI','#0d5c3a','#ffe7a0','Pure Veg · Self Service · Since 1994'),
 ('medicals','ಮಂಜುನಾಥ ಮೆಡಿಕಲ್ಸ್','MANJUNATHA MEDICALS','#f7f7f2','#0b7a44','24 Hrs · Home delivery'),
 ('xerox','ಗಣೇಶ ಜೆರಾಕ್ಸ್ & ಸ್ಟೇಷನರಿ','GANESHA XEROX & STATIONERY','#1b3d9e','#ffffff','Print · Lamination · Spiral binding'),
 ('fancy','ಲಕ್ಷ್ಮಿ ಫ್ಯಾನ್ಸಿ ಸ್ಟೋರ್','LAKSHMI FANCY STORE','#ffd21a','#a3001c','Bangles · Gifts · Toys'),
 ('mobile','ನ್ಯೂ ಮೊಬೈಲ್ ವರ್ಲ್ಡ್','NEW MOBILE WORLD','#121214','#3fe1ff','Repair · Recharge · Accessories'),
 ('condiments','ಶ್ರೀ ರಾಮ ಕಾಂಡಿಮೆಂಟ್ಸ್','SRI RAMA CONDIMENTS','#f06b1a','#ffffff','Provisions · Fruits · Vegetables'),
 ('tailors','ಬೆಂಗಳೂರು ಟೈಲರ್ಸ್','BENGALURU TAILORS','#5a2a86','#ffffff','Gents & Ladies · Alterations'),
 ('juice','ಎಸ್.ಎಲ್.ವಿ ಕೂಲ್ ಡ್ರಿಂಕ್ಸ್','SLV COOL DRINKS & JUICE','#df0d0d','#fff6e8','Fresh Juice · Milkshakes · Soda'),
 ('salon','ನಮ್ಮ ಸಲೂನ್','NAMMA SALON','#0f0f10','#ff63a5','Hair · Beard · Facial'),
 ('hardware','ವಿನಾಯಕ ಹಾರ್ಡ್‌ವೇರ್ಸ್','VINAYAKA HARDWARES','#26262a','#ffcc00','Paints · Pipes · Electricals'),
 ('darkstore','ಬೇಗ ಡಾರ್ಕ್ ಸ್ಟೋರ್','BEEGA · DARK STORE','#2b1a5e','#c8ff3d','Riders only · 9-minute delivery'),
 ('milk','ಹಾಲು · ಮೊಸರು · ಬೆಣ್ಣೆ','MILK BOOTH','#e9f3ff','#1856a8','Morning 5:30 · Evening 4:30'),
 ('chai','ಟೀ · ಕಾಫಿ · ಬಿಸ್ಕತ್','TEA · FILTER COFFEE','#fff0c2','#8e1010','Since forever'),
 ('roadMain','೮ನೇ ಮುಖ್ಯರಸ್ತೆ','8th MAIN ROAD','#1d5fb0','#ffffff',None),
 ('roadCross','೪ನೇ ಅಡ್ಡರಸ್ತೆ','4th CROSS ROAD','#1d5fb0','#ffffff',None),
]
items=[(k,board(1024,256,kn,en,bg,fg,sub,seed=i)) for i,(k,kn,en,bg,fg,sub) in enumerate(SHOPS)]
pack('signs',items,(1024,256),(2,8))
# ---------------- ads: billboards 1024x512 (4) + posters 512x512 (8) ----------------
def billboard(kn,brand,line1,line2,bg,fg,acc,seed):
    W,H=1024,512; im=Image.new('RGBA',(W,H),bg); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,int(H*0.18)],fill=acc)
    fb=fit(d,brand,DISP,W*0.62,90,wght=900,wdth=60); d.text((40,int(H*0.09)),brand,font=fb,fill=bg,anchor='lm')
    fk=fit(d,kn,KN,W*0.26,46); d.text((W-40,int(H*0.09)),kn,font=fk,fill=bg,anchor='rm')
    f1=fit(d,line1,FUN,W-80,96,wght=800); d.text((40,int(H*0.45)),line1,font=f1,fill=fg,anchor='lm')
    f2=fit(d,line2,FUN,W-80,60,wght=500); d.text((40,int(H*0.72)),line2,font=f2,fill=fg,anchor='lm')
    return grime(im,0.1,seed)
def poster(title,kn,body,bg,fg,seed):
    W=H=512; im=Image.new('RGBA',(W,H),bg); d=ImageDraw.Draw(im)
    ft=fit(d,title,DISP,W-50,92,wght=900,wdth=55); d.text((W/2,90),title,font=ft,fill=fg,anchor='mm')
    fk=fit(d,kn,KN,W-160,36); d.text((W/2,170),kn,font=fk,fill=fg,anchor='mm')
    fb=font(FUN,34,600); y=270
    for line in body: d.text((W/2,y),line,font=fit(d,line,FUN,W-50,34,wght=600),fill=fg,anchor='mm'); y+=50
    return grime(im,0.2,seed)
ads=[
 ('bbBeega',billboard('ಬೇಗ','BEEGA','Groceries in 9 minutes.','Traffic in 90. We checked.','#f4f0ff','#2b1a5e','#2b1a5e',1)),
 ('bbHogona',billboard('ಹೋಗೋಣ','HOGONA bike taxi','Silk Board to anywhere.','Probably. Helmets included, patience not.','#fff8e1','#1d1d1d','#ffb300',2)),
 ('bbOota',billboard('ಊಟ','OOTA food','Your biryani is closer','than your cab. Again.','#fff0ea','#7a1200','#ff4d1f',3)),
 ('bbCowork',billboard('ಸ್ವಲ್ಪ ಅಡ್ಜಸ್ಟ್','ADJUST MAADI cowork','Hot desks. Hotter chai.','Series A sold separately.','#eafff3','#0f3b2a','#13a36b',4)),
 ('pRent',poster('TO-LET','ಬಾಡಿಗೆಗೆ ಇದೆ',['2BHK · 4 months deposit','LinkedIn profile mandatory','Owner will judge your startup'],'#fff7c7','#b00000',5)),
 ('pWater',poster('NEERU EXPRESS','ನೀರು ಎಕ್ಸ್‌ಪ್ರೆಸ್',['Water tanker 24x7','Faster than BEEGA','(not really)'],'#dff3ff','#0b4f8a',6)),
 ('pKannada',poster('KANNADA CLASS','ಸ್ವಲ್ಪ ಕನ್ನಡ ಕಲಿಯಿರಿ',['Evening batch · 7 PM','Start with "swalpa"','and a smile'],'#ffe9d6','#8a2b00',7)),
 ('pYoga',poster('PARK YOGA','ಬೆಳಗಿನ ಯೋಗ',['6 AM · BBMP park','Uncles walking backwards','welcome'],'#ecffe2','#2c6b17',8)),
 ('pLostDog',poster('LOST DOG','ನಾಯಿ ಕಾಣೆಯಾಗಿದೆ',['Brown, very friendly','answers to "Guru"','Reward: one masala dosa'],'#ffffff','#222222',9)),
 ('pHackathon',poster('HACK NIGHT','ಹ್ಯಾಕಥಾನ್',['Build an app that finds','an auto that goes by meter','Prize: Rs 1 lakh'],'#141414','#c8ff3d',10)),
 ('pCoffee',poster('FILTER COFFEE','ಫಿಲ್ಟರ್ ಕಾಫಿ',['Strong. Hot. Tiny glass.','Life advice free','with every second cup'],'#3b2112','#ffdca8',11)),
 ('pRain',poster('MONSOON SALE','ಮಳೆಗಾಲದ ಸೇಲ್',['Umbrellas · Raincoats','Boats on request','(Koramangala only)'],'#e3ecff','#1b2f7a',12)),
]
at=Image.new('RGBA',(2048,2048),(0,0,0,255)); meta={}
for i,(k,img) in enumerate(ads[:4]):
    x,y=(i%2)*1024,(i//2)*512; at.paste(img,(x,y)); meta[k]=[x/2048,1-(y+512)/2048,(x+1024)/2048,1-y/2048]
for i,(k,img) in enumerate(ads[4:]):
    x,y=(i%4)*512,1024+(i//4)*512; at.paste(img,(x,y)); meta[k]=[x/2048,1-(y+512)/2048,(x+512)/2048,1-y/2048]
at.convert('RGB').save(os.path.join(HERE,'atlas','ads.png'),optimize=True); ATLAS['ads']=meta
json.dump(ATLAS,open(os.path.join(HERE,'atlas','atlas.json'),'w'),indent=1)
print('ok',{k:len(v) for k,v in ATLAS.items()})
