# -*- coding: utf-8 -*-
"""
Created on Mon Aug 01 11:07:50 2016

@author: Kalyan

Ploting of shapefile and attributes to PDF
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import shapefile as shp
import matplotlib.pyplot as plt
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

#header for each page
def header(cvs, logo):
    cvs.setFont('Helvetica', 20)
 
    cvs.roundRect(0, 740, 612, 52, 0,stroke=0, fill=1)
    cvs.drawImage(logo,475,750,mask='auto')

    cvs.setFillColorRGB(255,0,0)
    cvs.roundRect(30, 735, 150, 57, 0,stroke=0, fill=1)

    cvs.setFillColorRGB(255,255, 255)
    cvs.drawString(40,750,"Shapefile Plot")
    
    return

def shapefileplotpdf(in_file, out_dir, out_file, logo):
    
    width, height = letter
    #print width, height
    cvs = canvas.Canvas(out_dir + out_file, pagesize=letter)
    header(cvs, logo)
    #norm = mpl.colors.Normalize(vmin=0, vmax=10000)
    #cmap = plt.cm.RdYlBu_r

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    pointx, pointy, cx, cy = [], [], [], []
    sf = shp.Reader(in_file)
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        pointx.append(x)
        pointy.append(y)
        centerx  = ((max(x)-min(x))/2)+min(x)
        centery = ((max(y)-min(y))/2)+min(y)
        cx.append(centerx)
        cy.append(centery)
        plt.plot(x,y, color = 'Blue')
        #print pointx, pointy
        #print cx, cy

    t_head = [['Plot No', 'Plant Count', 'Y1', 'Y2', 'Y3', 'Y4']]
    t_data, plot_no = [], []
    for i in sf.records():
        plot = int(i[7])
        count = int(i[8])
        y1 = int(i[9])
        y2 = int(i[10])
        y3 = int(i[11])
        y4 = int(i[12])
 
        data = [plot,count,y1,y2,y3,y4]
        plot_no.append(plot)
        t_data.append(data)
    #print plot_no
    plt.axis('off')
    for i, txt in enumerate(plot_no):
        ax.annotate(txt, (cx[i],cy[i]))
        #cax = fig.add_axes([0.05, 0.2, 0.02, 0.6])
        #cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, spacing='proportional')
        #cb.set_label('Plant Count', labelpad=-20, y=1.10, rotation=0)
    fig.savefig(out_dir+'fig.png', fmt='png', dpi=100, bbox_inches='tight')

    cvs.drawImage(out_dir+'fig.png',30,330,520,400,mask='auto')
    t_len = len(t_data)
    pages = int(((t_len-15)/32)+2)
    #print pages 

    if t_len >15:
        table=Table([t_head[0]]+t_data[0:14], colWidths=82, rowHeights=20 )
        table.setStyle(TableStyle([
                                   ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                   ('BOX', (0,0), (-1,-1), 1, colors.black),
                                   ('ALIGN',(0,0), (-1,-1),'CENTRE'),
                                   ]))
        table.wrapOn(cvs, width, height)
        table.drawOn(cvs,50,46)
        cvs.showPage()
        for p in range(pages):    
            if p > 0:
                
                header(cvs, logo)
                
                table=Table([t_head[0]]+t_data[((p-1)*32)+14:(p*32)+14], colWidths=82, rowHeights=20 )
                table.setStyle(TableStyle([
                                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                           ('BOX', (0,0), (-1,-1), 1, colors.black),
                                           ('ALIGN',(0,0), (-1,-1),'CENTRE'),
                                           ]))
            
                if p == (pages-1):
                    table.wrapOn(cvs, width, height)
                    table.drawOn(cvs,50,792-46-40-(t_len-((pages-2)*32)-14+1)*20)
                    cvs.showPage()
                else:
                    table.wrapOn(cvs, width, height)
                    table.drawOn(cvs,50,46)
                    cvs.showPage()
    else:
        table=Table([t_head[0]]+t_data, colWidths=82, rowHeights=20)
        table.setStyle(TableStyle([
                                   ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                   ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                   ('ALIGN',(0,0), (-1,-1),'CENTRE'),
                                   ]))
        table.wrapOn(cvs, width, height)
        table.drawOn(cvs,50,792-456-((t_len+1)*20))
    
    cvs.save()
    
#Output directory
out_dir = "E:/Python_Learning/Exercise/ShpPlotPdf/"
#out file name
out_file = "PDF_report.pdf"
#input shapefile
in_file = "E:/Python_Learning/Exercise/ShpPlotPdf/YOGIK_State_shp.shp"
#location of logo
logo ="E:/Python_Learning/Exercise/ShpPlotPdf/datamapper_logo.png"

shapefileplotpdf(in_file, out_dir, out_file, logo)
