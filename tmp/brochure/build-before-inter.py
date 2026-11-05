from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader,PdfWriter,PageObject,Transformation
from PIL import Image,ImageDraw
import subprocess,json,copy
ROOT=Path('/Users/nateliang/Downloads/ilic-master');D=ROOT/'tmp/brochure';A=D/'assets';O=ROOT/'output/pdf'
for n,f,i in [('Futura','/System/Library/Fonts/Supplemental/Futura.ttc',0),('FuturaBold','/System/Library/Fonts/Supplemental/Futura.ttc',2),('Serif',str(A/'font-1.ttf'),0),('SerifItalic',str(A/'font-0.ttf'),0)]:pdfmetrics.registerFont(TTFont(n,f,subfontIndex=i))
INK='#232823';GRAY='#60665F'
W,H=396,612;G='#1C4C37';C='#F5F3EB';M='#58715F';RULE='#CED6CA';reading=O/'IIC-judges-brochure-draft-reading.pdf';c=canvas.Canvas(str(reading),pagesize=(W,H));c.setTitle('IIC | Judges & Sponsors | November 5-6, 2026 | Draft');c.setAuthor('Ivy Investment Competition')
page=0
bounds=[]
def txt(x,y,s,size=10,font='Futura',color=INK):
 c.setFillColor(HexColor(color));c.setFont('Futura' if font=='FuturaBold' else font,size);c.drawString(x,y,s)
def center(y,s,size=10,font='Futura',color=INK):
 c.setFillColor(HexColor(color));c.setFont(font,size);c.drawCentredString(W/2,y,s)
def line(y,x=36,x2=360,color=RULE,w=.5):c.setStrokeColor(HexColor(color));c.setLineWidth(w);c.line(x,y,x2,y)
def para(s,x,y,width=324,size=10,leading=14,color=INK,font='Futura'):
 st=ParagraphStyle('p',fontName='Futura' if font=='FuturaBold' else font,fontSize=size,leading=leading,textColor=HexColor(color));p=Paragraph(s,st);aw,ah=p.wrap(width,700);p.drawOn(c,x,y-ah);bounds.append((page,y-ah,s[:35]));return y-ah

def img(index,x,y,w,h):
 path=A/f'image-{index}.png';im=Image.open(path);iw,ih=im.size;scale=min(w/iw,h/ih);ww,hh=iw*scale,ih*scale;c.drawImage(ImageReader(im),x+(w-ww)/2,y+(h-hh)/2,width=ww,height=hh,mask='auto')
def start(label=None,title=None,subtitle=None,dark=False):
 global page
 page+=1;c.setFillColor(HexColor(G if dark else C));c.rect(0,0,W,H,fill=1,stroke=0)
 if not dark:
  txt(36,576,'IIC  |  '+(label or '').upper(),8,color=M);line(563)
  if title:txt(36,521,title,34,'Serif',G)
  if subtitle:txt(36,499,subtitle,9,color=M)
def end(dark=False):
 line(31,color='#66836E' if dark else RULE);txt(36,18,'THE IVY INVESTMENT COMPETITION',6.3,color='#C6D4C5' if dark else M)
 txt(346,18,f'{page:02d}',7,color=C if dark else M);c.showPage()
# 1 cover
start(dark=True)
# Website orbit geometry: full-width ellipse at -25 degrees and 88% ellipse at 45 degrees.
c.setStrokeColor(HexColor('#496D53'));c.setLineWidth(.5)
for angle,radius in [(-25,127),(45,111.76)]:
 c.saveState();c.translate(198,447);c.rotate(angle);c.scale(1,.83);c.circle(0,0,radius);c.restoreState()
c.drawImage(str(ROOT/'email/round1-results/iic-logo.png'),86.24,373.36,width=223.52,height=147.28,mask='auto')
center(290,'The Ivy',33,color=C);center(244,'Investment',46,'SerifItalic',C);center(201,'Competition',33,color=C)
center(157,'NOVEMBER 5 - 6, 2026',11,color=C)
center(136,'Brown University | Providence, RI',10,color='#D2DDCC')
center(115,'Judges and Sponsors Brochure',11,color=C)
center(60,'Hosted by the Brown Investment Group',9,color='#D2DDCC');end(True)
#2 Welcome and practical guidance, before itinerary and panels.
start('Welcome','Welcome to IIC')
y=para('Dear Judges & Sponsors,',36,473,size=10)-17
for text in ["Thank you for joining us for the inaugural Ivy Investment Competition and for taking the time to engage with the students' work. We're grateful to have you here at Brown.","We created IIC so students from across the Ivy League could test their investment ideas through thoughtful discussion with experienced investors. Your questions and feedback make that possible.","Thank you for being part of this first competition and helping us build something worth continuing."]:
 y=para(text,36,y,size=10,leading=15)-14
para('Best,<br/>The IIC Organizing Team<br/>Brown Investment Group',36,y,size=10,leading=15)
end()
# Itineraries share a full-width rhythm. Times never wrap.
GOLD='#806226'
def event(y,time,title,description,venue,address,note=None,separator=True):
 txt(36,y,time,9,color=G)
 y=para(title,36,y-8,size=14,leading=17,font='Futura')-5
 if description:y=para(description,36,y,size=9.3,leading=13)-5
 if venue:y=para(venue+'<br/>'+address,36,y,size=9.2,leading=13,color=GOLD)-3
 if note:
  st=ParagraphStyle('note',fontName='Futura',fontSize=9,leading=12,textColor=HexColor(G))
  pp=Paragraph(note,st);_,hh=pp.wrap(304,200)
  c.setFillColor(HexColor('#E6EBDF'));c.rect(36,y-hh-10,324,hh+14,fill=1,stroke=0)
  pp.drawOn(c,46,y-hh-3);y-=hh+17
 if separator:line(y-3,color=RULE,w=.6)
 return y-17
start('Itinerary','Thursday','NOVEMBER 5, 2026  |  ALL TIMES EST')
y=483
y=event(y,'1:30 - 2:30 PM','Welcome Lunch','Recruiter tables present.','Petteruti Lounge, Campus Center','75 Waterman Street, Providence')
y=event(y,'2:30 PM','Fireside Chat','Joanna Albright, COO of Coatue Management.<br/>Moderated by Joshua Kennedy, Deputy CIO of Brown University.','Petteruti Lounge, Campus Center','75 Waterman Street, Providence')
y=event(y,'4:00 - 6:00 PM','Round II: Preliminary Pitches','','Friedman Hall, Rooms 101 & 201','90 George Street, Providence','Judges: Please see Room Allocations and Pitching Order on page 5.')
y=event(y,'6:00 - 7:30 PM','Private Judges & Sponsor Dinner','','Brown Faculty Club','1 Bannister Street, Providence')
y=event(y,'7:30 - 9:30 PM','Cocktail Reception & Recruiter Event','','Brown Faculty Club','1 Bannister Street, Providence',separator=False)
end()
start('Itinerary','Friday','NOVEMBER 6, 2026  |  ALL TIMES EST')
y=483
y=event(y,'9:30 AM','Coffee & Bagels','','Brown Investment Office','1 Citizens Plaza, 4th Floor, Suite 410')
y=event(y,'10:00 AM - 12:00 PM','Round III: Final Pitches','','Brown Investment Office','1 Citizens Plaza, 4th Floor, Suite 410',"Finalists and pitch order will be announced after Thursday's results.")
y=event(y,'12:00 PM','Final Lunch','','Café Nuovo','1 Citizens Plaza, Providence','All participating teams join for lunch.')
y=event(y,'APPROX. 12:30 PM','Winner Announcement','','Café Nuovo','1 Citizens Plaza, Providence','Awards and presentation of the winning checks.')
y=event(y,'BY 2:00 PM','Farewell & Departures','','','',separator=False)
end()
# Page 5: each room is one complete roster and pitching sequence.
start('Round II','Rooms & Pitch Order','THURSDAY  |  FRIEDMAN HALL  |  4:00 - 6:00 PM')
def room(y,num,judges,teams):
 c.setFillColor(HexColor(G));c.rect(36,y-7,324,23,fill=1,stroke=0)
 txt(46,y,'FRIEDMAN '+num,12,color=C)
 c.setFillColor(HexColor('#E6EBDF'));c.rect(36,y-29-16*len(judges),324,11+16*len(judges),fill=1,stroke=0)
 yy=y-31
 for name,firm in judges:
  txt(43,yy,name,11.5,color=INK)
  c.setFillColor(HexColor(GRAY));c.setFont('Futura',8.5);c.drawRightString(353,yy,firm)
  yy-=16
 yy-=11
 for time,group,school in teams:
  txt(43,yy,time,8.2,color=GRAY);txt(144,yy,group,8.5,color=INK)
  txt(144,yy-12,school,7.7,color=GRAY);yy-=30
room(473,'101',[('Benjamin Pass','TCIM'),('James Lu','Viking Global Investors'),('Charles Kalvaria','Third Point')],[('4:00 - 4:30 PM','DIPP','Dartmouth College'),('4:30 - 5:00 PM','Black Diamond Capital Investors','Harvard University'),('5:00 - 5:30 PM','Cornell Financial Analysts','Cornell University'),('5:30 - 6:00 PM','Lion Fund','Columbia University')])
room(254,'201',[('Zac Pollinger','Balyasny Asset Management'),('Craig Fountain','J.P. Morgan Asset Management'),('Rajeev Patel','Millennium'),('Spencer Washburn','Citadel')],[('4:00 - 4:30 PM','Yale Student Investment Group','Yale University'),('4:30 - 5:00 PM','Brown Investment Group','Brown University'),('5:00 - 5:30 PM','Tiger Capital Management','Princeton University'),('5:30 - 6:00 PM','Wharton Investment & Trading Group','University of Pennsylvania')])
end()
#6-8 bios
thu101=[('Benjamin Pass','TOMS Capital Investment Management','Benjamin Pass is the co-founder and Chief Investment Officer of TOMS Capital Investment Management LP (TCIM), a New York-based event-driven and long/short equity hedge fund.'),('James Lu','Viking Global Investors',"James Lu is a Portfolio Manager covering industrials on Viking Global Investors' public equity team. Before joining Viking in 2017, he worked at Bain Capital and Bain & Company. He holds a bachelor's degree in ethics, politics, and economics from Yale."),('Charles Kalvaria','Third Point','Charles Kalvaria is a Principal at Third Point. He previously worked at Coatue Management and Oak Hill Advisors and graduated from Princeton with a degree in Civil Engineering.')]
thu201=[('Zac Pollinger','Balyasny Asset Management','Zac Pollinger is a Director of Associate and Analyst Development at Balyasny Asset Management (BAM). He has previously held development roles at Citadel and Point72, and worked as an investment analyst at Cobia Capital Management and Force Capital Management. He graduated from Harvard with an Economics degree.'),('Craig Fountain','J.P. Morgan Asset Management','Craig Fountain is an Executive Director at J.P. Morgan Asset Management. He previously worked at Axar Capital Management and is a Brown University graduate.'),('Rajeev Patel','Millennium','Rajeev Patel is a senior member of Equities Management with more than two decades of experience investing in financial services. He previously held analyst and portfolio manager roles at Soros Fund Management and Citadel and earned his degree in Quantitative Economics from Tufts.'),('Spencer Washburn','Citadel','Spencer Washburn is a Portfolio Manager in Global Equities focused on industrials. He previously worked at Millennium and Precision Path Capital, began his career at Credit Suisse and graduated from Brown with a degree in Applied Mathematics.')]
fri=[('Previn Mankodi','Viking Global Investors','Previn Mankodi is Deputy Chief Investment Officer, assisting in managing the public equity team and identifying and researching investment ideas in the technology, media and telecommunications sectors. Previously a Partner at Hoplite Capital Management, he holds degrees from Stanford, Cambridge and the University of Chicago.'),('Steve Gambuzza','Millennium','Steve Gambuzza works in Equities Management, focusing on analyst training and development after 15 years at Millennium as an Analyst and Senior Portfolio Manager covering energy and utilities. He previously worked at Longbow Capital Partners and Goldman Sachs and attended Georgetown.'),('Anand Krishnamurthy','SurgoCap Partners',"Anand Krishnamurthy is a Co-Founding Partner and Investor focused on technology's application across financial services and real estate. Previously a Senior Managing Director at Maverick Capital, he holds a bachelor's degree from Columbia and an MBA from Stanford."),('Max Cook','Coatue Management','Max Cook is a New York-based Sector Head leading AI, cloud and software investing, with experience across AI infrastructure, energy and industrials. He previously worked at Advent International and Bain & Company and graduated from Yale, where he played varsity soccer.')]
for title,sub,bios in [('Thursday Panel','ROUND II  |  FRIEDMAN 101',thu101),('Thursday Panel','ROUND II  |  FRIEDMAN 201',thu201),('Friday Panel','ROUND III  |  BROWN INVESTMENT OFFICE',fri)]:
 start('Our judges',title,sub);y=473
 for bi,(name,company,bio) in enumerate(bios):
  txt(36,y,name,15,'Futura');txt(36,y-17,company.upper(),7.8,color=M)
  y=para(bio,36,y-26,size=9.2,leading=13.1)-14
  if bi<len(bios)-1:line(y)
  y-=18

 end()
#9 organizations
start('Across the Ivy League','Participating Groups','OUR COMPETITION COMMUNITY')
groups=[('Brown Investment Group','Brown University',2),('Lion Fund','Columbia University',3),('Morningside Investments','Columbia University',4),('Cornell Financial Analysts','Cornell University',5),('Cornell Hedge Fund','Cornell University',6),('Dartmouth Investment and Philanthropy Program','Dartmouth College',7),('Black Diamond Capital Investors','Harvard University',8),('Harvard Financial Analysts Club','Harvard University',9),('Wharton Investment and Trading Group','University of Pennsylvania',10),('Tiger Capital Management','Princeton University',11),('Tiger Investments','Princeton University',12),('Yale Alternative Investments','Yale University',13),('Yale Student Investment Group','Yale University',14)]
for i,(name,school,idx) in enumerate(groups):
 col=i%2;row=i//2;x=36+col*170;y=472-row*59
 img(idx,x,y-32,37,32);b=para(name,x+45,y,width=112,size=8,leading=10);para(school,x+45,b-3,width=112,size=7,leading=9,color=M)
end()
#10 sponsors
start('With gratitude','Sponsors & Partners')
tiers=[('PLATINUM',[15],464,62),('GOLD',[16,17],375,50),('SILVER',[18,19,20],289,47),('BRONZE',[21,22,23],202,44),('PARTNERS',[24,25],115,42)]
for label,ids,y,h in tiers:
 center(y,label,8,color=M);cell=324/len(ids)
 for i,idx in enumerate(ids):
  maxw=160 if len(ids)==1 else cell-20
  img(idx,36+i*cell+(cell-maxw)/2,y-h-13,maxw,min(h,42))
end()
#11 Thank you
start('Thank You','Thank You')
y=para('Thank you for being part of the inaugural Ivy Investment Competition.',36,463,size=12,leading=18,font='Futura')
y=para('To our judges: thank you for the time and care you have put into reviewing the students\' work. Your questions and feedback are what make this competition a valuable learning experience.',36,y-27,size=11,leading=17)
y=para('To our sponsors and partners: thank you for supporting this first competition and helping bring students from across the Ivy League together at Brown.',36,y-22,size=11,leading=17)
y=para('We are also grateful to the Brown Investment Office, our participating student organizations, and everyone who helped welcome our guests to Providence.',36,y-22,size=11,leading=17)
line(141);txt(36,114,'The IIC Organizing Team',13,'Futura',G);txt(36,91,'Brown Investment Group',10,color=GRAY);end()
#12 back
start(dark=True);c.drawImage(str(ROOT/'email/round1-results/iic-logo.png'),36,499,width=97,height=64,mask='auto');txt(36,464,'Stay in Touch',34,'Serif',C)
txt(36,435,'browninvestmentgroup.co/iic',11,color=C);c.linkURL('https://browninvestmentgroup.co/iic',(36,431,300,448),relative=0)
contacts=[('Faizaan Qureshi','Executive Director','faizaan_qureshi@brown.edu'),('Carl Dinshaw','Director','carl_dinshaw@brown.edu'),('Raiaan Feerasta','Director','raiaan_feerasta@brown.edu'),('Trisha Chhalani','Operations Coordinator','trisha_chhalani@brown.edu'),('Layla Xiao','Operations Coordinator','layla_xiao@brown.edu'),('Nathan Liang','Competition Coordinator','nathan_liang@brown.edu'),('Shazain Wasif','Competition Coordinator','shazain_wasif@brown.edu')]
contacts=sorted(contacts,key=lambda z:['Faizaan Qureshi','Carl Dinshaw','Raiaan Feerasta','Nathan Liang','Shazain Wasif','Trisha Chhalani','Layla Xiao'].index(z[0]))
for i,(name,role,email) in enumerate(contacts):
 y=396-i*37;txt(36,y,name+'  |  '+role,8.5,color=C);txt(36,y-13,email,8,color='#CCD9C8');c.linkURL('mailto:'+email,(36,y-16,330,y-3),relative=0)
line(117,color='#66836E');txt(36,96,'BROWN UNIVERSITY PUBLIC SAFETY',8,color='#CCD9C8');txt(36,71,'Emergency: (401) 863-4111',15,color=C);txt(36,50,'Police | Fire | Medical response, 24 hours',8,color='#CCD9C8');end(True)
c.save()
# Saddle-stitch imposition: outer sheet [12|1] / [2|11], then nested inward.
r=PdfReader(str(reading));assert len(r.pages)==12
writer=PdfWriter();pairs=[]
for i in range(3):
 for a,b in [(12-2*i,1+2*i),(2+2*i,11-2*i)]:
  p=PageObject.create_blank_page(width=792,height=612)
  p.merge_transformed_page(r.pages[a-1],Transformation().translate(0,0));p.merge_transformed_page(r.pages[b-1],Transformation().translate(396,0));writer.add_page(p);pairs.append([a,b])
printpdf=O/'IIC-judges-brochure-draft-booklet-print.pdf'
with open(printpdf,'wb') as f:writer.write(f)
(D/'imposition.json').write_text(json.dumps(pairs))
assert all(y>=40 for _,y,_ in bounds),[z for z in bounds if z[1]<40]
alltext='\n'.join(p.extract_text() for p in r.pages)
for name,_,_ in thu101+thu201+fri:assert name in alltext
assert len(PdfReader(str(printpdf)).pages)==6
subprocess.run(['pdftoppm','-scale-to','1000','-png',str(reading),str(D/'page')],check=True)
board=Image.new('RGB',(4*324,3*500),'#ddd')
for i,p in enumerate(sorted(D.glob('page-*.png'))):
 im=Image.open(p);im.thumbnail((324,500));board.paste(im,((i%4)*324,(i//4)*500))
board.save(D/'all-pages.png')
print('Created 12 reading pages and 6 imposed letter sides (3 sheets). Pairs:',pairs)
print('Lowest paragraph edge',min(y for _,y,_ in bounds))
