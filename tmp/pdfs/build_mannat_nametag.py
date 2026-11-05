import json, math
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from pypdf import PdfReader
import subprocess

ROOT=Path('/Users/nateliang/Downloads/ilic-master')
OUT=ROOT/'output/pdf'; OUT.mkdir(parents=True,exist_ok=True)
WORK=ROOT/'tmp/pdfs'
people=[{'name':'Mannat Shah','year':'2027','school':'Franklin & Marshall College'}]
font='/System/Library/Fonts/Supplemental/Futura.ttc'
pdfmetrics.registerFont(TTFont('Futura',font,subfontIndex=0))
pdfmetrics.registerFont(TTFont('Futura-Bold',font,subfontIndex=2))
pdf=OUT/'IIC-spectator-Mannat-Shah.pdf'
c=canvas.Canvas(str(pdf),pagesize=(612,792))
c.setTitle('IIC Spectator Nametags | 4 x 3 inches | US Letter')
c.setAuthor('Ivy Investment Competition')
green=HexColor('#17432F'); cream=HexColor('#F5F3EB')
def tag(p,x,y):
 c.setFillColor(cream);c.rect(x,y,288,216,stroke=0,fill=1)
 # An open ivory field, a fine inset frame, and a floating brand mark.
 c.setStrokeColor(HexColor('#D6DED4'));c.setLineWidth(.45)
 c.rect(x+9,y+9,270,198,stroke=1,fill=0)
 c.drawImage(str(ROOT/'assets/iic-white-transparent.png'),x+102,y+137,width=84,height=55.35,mask='auto')
 c.setStrokeColor(HexColor('#BCCBBC'));c.setLineWidth(.5)
 c.line(x+112,y+126,x+176,y+126)
 name=p['name'];size=26
 while pdfmetrics.stringWidth(name,'Futura',size)>244:size-=.25
 c.setFillColor(green);c.setFont('Futura',size)
 c.drawCentredString(x+144,y+91,name)
 c.setFillColor(HexColor('#5F7568'));c.setFont('Futura',11)
 c.drawCentredString(x+144,y+65,'CLASS OF '+p['year'])
 c.setFillColor(green)
 school=p['school'].upper();school_size=11.5
 while pdfmetrics.stringWidth(school,'Futura',school_size)>240:school_size-=.25
 c.setFont('Futura',school_size)
 c.drawCentredString(x+144,y+46,school)
 c.setFillColor(HexColor('#5F7568'));c.setFont('Futura',8)
 c.drawCentredString(x+144,y+23,'SPECTATOR')

for page in range(math.ceil(len(people)/6)):
 subset=people[page*6:(page+1)*6]
 for j,p in enumerate(subset):tag(p,18+(j%2)*288,504-(j//2)*216)
 # Hairline trim guides mark exact 4-by-3-inch edges.
 c.setStrokeColor(HexColor('#AAB5AF'));c.setLineWidth(.3)
 for j in range(len(subset)):
  x=18+(j%2)*288;y=504-(j//2)*216;c.rect(x,y,288,216,stroke=1,fill=0)
 c.setFillColor(HexColor('#617167'));c.setFont('Futura',7)
 c.drawString(18,749,'IIC  /  SPECTATOR NAMETAGS')
 c.drawRightString(594,749,f'{page+1:02d} / {math.ceil(len(people)/6):02d}')
 c.drawCentredString(306,43,'Print at 100% / Actual size  |  US Letter  |  Cut on the fine lines  |  Each tag: 4 x 3 in')
 c.showPage()
c.save()
r=PdfReader(str(pdf));assert len(r.pages)==math.ceil(len(people)/6)
text='\n'.join(p.extract_text() for p in r.pages)
for p in people:
 assert p['name'] in text or all(w in text for w in p['name'].split())
 assert p['year'] in text and p['school'].upper() in text
assert text.count('SPECTATOR')==2
assert len(people)==1

for stale in WORK.glob('mannat-*.png'):stale.unlink()
subprocess.run(['pdftoppm','-scale-to','990','-png',str(pdf),str(WORK/'mannat')],check=True)
from PIL import Image,ImageOps,ImageDraw
board=Image.new('RGB',(2*306,396),'#ddd')
for i,render in enumerate(sorted(WORK.glob('mannat-*.png'))):
 im=Image.open(render);im.thumbnail((306,396));board.paste(im,((i%2)*306,(i//2)*396))
board.save(WORK/'mannat-review.png')
print(f'{len(people)} unique participants; {len(r.pages)} letter pages; exact 288 x 216 pt tags; font embedded.')
print(pdf)
