from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from pypdf import PdfReader
import subprocess
ROOT=Path('/Users/nateliang/Downloads/ilic-master');OUT=ROOT/'output/pdf';WORK=ROOT/'tmp/pdfs'
for key,file in [('TNR','Times New Roman.ttf'),('TNR-Bold','Times New Roman Bold.ttf'),('TNR-Italic','Times New Roman Italic.ttf')]:
 pdfmetrics.registerFont(TTFont(key,'/System/Library/Fonts/Supplemental/'+file))
pdf=OUT/'IIC-judge-pitch-rubric.pdf';c=canvas.Canvas(str(pdf),pagesize=(792,612));c.setTitle('IIC | Pitch Evaluation Rubric');c.setAuthor('Ivy Investment Competition')
green=HexColor('#1C4C37');ink=HexColor('#192D23');muted=HexColor('#526459');rule=HexColor('#A8B5AC');pale=HexColor('#F2F5F0')
def text(x,y,s,font='TNR',size=11,color=ink):
 c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,s)
def line(x,y,x2,y2,width=.5,color=rule):
 c.setStrokeColor(color);c.setLineWidth(width);c.line(x,y,x2,y2)
# Custom masthead, with a restrained competition-green rule.
c.drawImage(str(ROOT/'assets/iic-white-transparent.png'),36,513,width=104,height=68.5,mask='auto')
text(164,559,'THE IVY INVESTMENT COMPETITION','TNR-Bold',10,green)
text(164,530,'Pitch Evaluation Rubric','TNR-Bold',27,green)

line(36,497,756,497,1.3,green)
text(36,475,'University Name:','TNR-Bold',11);line(124,473,325,473)
text(350,475,'Company / Ticker:','TNR-Bold',11);line(440,473,756,473)
text(36,450,'SCORING','TNR-Bold',10,green)
text(101,450,'Circle one score per category: 1 = lowest, 5 = best.','TNR',11)
# 4 generous rows allow handwritten comments on each criterion.
x0,x1,x2,x3=36,184,336,756;top=432;head=27;rh=77;bottom=top-head-4*rh
c.setFillColor(green);c.rect(x0,top-head,x3-x0,head,fill=1,stroke=0)
text(x0+11,top-18,'CATEGORY','TNR-Bold',10,HexColor('#FFFFFF'))
text(x1+13,top-18,'SCORE (1-5)','TNR-Bold',10,HexColor('#FFFFFF'))
text(x2+12,top-18,'FEEDBACK','TNR-Bold',10,HexColor('#FFFFFF'))
for i,label in enumerate(['Valuation','Idea Quality','Research','Presentation Material']):
 yt=top-head-i*rh;yb=yt-rh
 c.setFillColor(pale);c.rect(x0,yb,x1-x0,rh,fill=1,stroke=0)
 text(x0+11,yt-42,label,'TNR-Bold',12)
 for j in range(5):
  c.setFillColor(ink);c.setFont('TNR',14);c.drawCentredString(x1+22+j*27,yt-42,str(j+1))
 for offset in [25,47,66]:line(x2+12,yt-offset,x3-12,yt-offset,.35,HexColor('#CCD4CD'))
 line(x0,yb,x3,yb)
for x in [x0,x1,x2,x3]:line(x,top-head,x,bottom)
line(x0,top-head,x3,top-head)
text(36,66,'TOTAL SCORE','TNR-Bold',11,green)
line(127,63,185,63,.75,green);text(192,66,'/ 20','TNR-Bold',14,green)
text(263,66,'Judge initials:','TNR-Bold',11);line(333,63,435,63,.75)

line(36,43,756,43,.5,rule)
text(36,27,'IIC  /  JUDGING & EVALUATION','TNR',8,muted)
c.setFillColor(muted);c.setFont('TNR',8);c.drawRightString(756,27,'Brown Investment Group')
c.showPage();c.save()
r=PdfReader(str(pdf));assert len(r.pages)==1;assert list(r.pages[0].mediabox)==[0,0,792,612]
s=r.pages[0].extract_text()
for label in ['Valuation','Idea Quality','Research','Presentation Material','5 = best','/ 20','Judge initials:']:assert label in s
subprocess.run(['pdftoppm','-scale-to','1500','-png',str(pdf),str(WORK/'rubric')],check=True)
print(pdf)
