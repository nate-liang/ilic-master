import math, subprocess
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from pypdf import PdfReader
from PIL import Image
ROOT=Path('/Users/nateliang/Downloads/ilic-master');WORK=ROOT/'tmp/pdfs';OUT=ROOT/'output/pdf'
people=[('Benjamin Pass','TCIM'),('James Lu','Viking'),('Craig Fountain','J.P. Morgan'),('Rajeev Patel','Millennium'),('Spencer Washburn','Citadel'),('Charles Kalvaria','Third Point'),('Zac Pollinger','Balyasny Asset Management'),('Previn Mankodi','Viking'),('Steve Gambuzza','Millennium'),('Anand Krishnamurthy','SurgoCap Partners'),('Max Cook','Coatue')]
people.sort(key=lambda x:x[0].split()[-1])
pdfmetrics.registerFont(TTFont('Futura','/System/Library/Fonts/Supplemental/Futura.ttc',subfontIndex=0))
pdf=OUT/'IIC-judge-nametags-letter.pdf';c=canvas.Canvas(str(pdf),pagesize=(612,792));c.setTitle('IIC Judge Nametags | 4 x 3 inches | US Letter');c.setAuthor('Ivy Investment Competition')
green=HexColor('#1C4C37');ivory=HexColor('#F5F3EB')
for page in range(math.ceil(len(people)/6)):
 subset=people[page*6:(page+1)*6]
 for j,(name,company) in enumerate(subset):
  x=18+(j%2)*288;y=504-(j//2)*216
  c.setFillColor(green);c.rect(x,y,288,216,fill=1,stroke=0)
  c.setStrokeColor(HexColor('#789382'));c.setLineWidth(.45);c.rect(x+9,y+9,270,198,fill=0,stroke=1)
  c.drawImage(str(ROOT/'email/round1-results/iic-logo.png'),x+102,y+130,width=84,height=55.35,mask='auto')
  c.setStrokeColor(HexColor('#789382'));c.line(x+112,y+118,x+176,y+118)
  size=26
  while pdfmetrics.stringWidth(name,'Futura',size)>244:size-=.25
  c.setFillColor(ivory);c.setFont('Futura',size);c.drawCentredString(x+144,y+82,name)
  subtitle=company.upper();subtitle_size=11.5
  while pdfmetrics.stringWidth(subtitle,'Futura',subtitle_size)>240:subtitle_size-=.25
  c.setFont('Futura',subtitle_size);c.drawCentredString(x+144,y+53,subtitle)
  c.setStrokeColor(HexColor('#AAB5AF'));c.setLineWidth(.3);c.rect(x,y,288,216,fill=0,stroke=1)
 c.setFillColor(HexColor('#617167'));c.setFont('Futura',7)
 c.drawString(18,749,'IIC  /  JUDGE NAMETAGS');c.drawRightString(594,749,f'{page+1:02d} / 02')
 c.drawCentredString(306,43,'Print at 100% / Actual size  |  US Letter  |  Cut on the fine lines  |  Each tag: 4 x 3 in')
 c.showPage()
c.save()
r=PdfReader(str(pdf));assert len(r.pages)==2
text='\n'.join(p.extract_text() for p in r.pages)
for name,company in people:assert name in text and company.upper() in text
assert 'JUDGE' not in text.replace('JUDGE NAMETAGS','')
for page in r.pages:assert list(page.mediabox)==[0,0,612,792]
subprocess.run(['pdftoppm','-scale-to','1200','-png',str(pdf),str(WORK/'judges')],check=True)
board=Image.new('RGB',(928,600),'white')
for i,p in enumerate(sorted(WORK.glob('judges-*.png'))):
 im=Image.open(p);im.thumbnail((464,600));board.paste(im,(i*464,0))
board.save(WORK/'judge-pages-review.png')
print(f'Verified {len(people)} judges on 2 US Letter pages. {pdf}')
