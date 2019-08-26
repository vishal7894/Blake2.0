
"""
importing required libraries and modules
"""

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,BaseDocTemplate,Table,TableStyle
from reportlab.platypus import Frame,NextPageTemplate,PageTemplate,Image,ParagraphAndImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch,cm
from reportlab.platypus import PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.pdfgen import canvas
from  reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate


"""
initiating a new class 
"""

class PDF(SimpleDocTemplate):
    
    # collecting page properties
    PAGE_HEIGHT=defaultPageSize[1]
    PAGE_WIDTH=defaultPageSize[0]

    # styles to be used in the PDF document
    styles = getSampleStyleSheet()
    styles.add(PS(name='centered-italic',fontName='Times-Italic',fontSize=20,leading=12,alignment=1,spaceAfter=20))
    styles.add(PS(name='centered-italic1',fontName='Times-Italic',fontSize=18,leading=12,alignment=1,spaceAfter=20))
    styles.add(PS(name='centered-bold',fontName='Times-Bold',fontSize=20,leading=12,alignment=1,spaceAfter=20))
    styles.add(PS(name='body1',fontName='Times', fontSize=10, leading=12,firstLineIndent=20, spaceAfter=20))
    styles.add(PS(name='BodyText1',fontName='Times', fontSize=10, leading=12, spaceAfter=3))
    styles.add(PS(name='bullet',fontName='Times', fontSize=10, leading=12, leftIndent=40,rightIndent=40,spaceAfter=3))


    def __init__(self, file_name,**kw):
        self.allowSplitting = 0
        # self.page_info = page_info
        # self.image=image
        super().__init__(file_name)
        self.flowables=[]
        self.initial_document = SimpleDocTemplate(file_name,showBoundary=1)
    
    
    def myFirstPage(self,canvas,doc):
        canvas.saveState()
        canvas.setFont('Times-Roman',9)
        canvas.setStrokeColor('grey')
        canvas.rect(0.5*inch,0.5*inch, 7.27*inch, 10.6*inch,stroke=1 ,fill=0)
        canvas.restoreState()


    def myLaterPages(self,canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman',9)
        canvas.setStrokeColor('grey')
        canvas.rect(0.5*inch,0.5*inch, 7.27*inch, 10.6*inch,stroke=1, fill=0)
        canvas.drawString(PDF.PAGE_WIDTH*0.47, 0.8* inch, "Page %d " % (doc.page-1))
        canvas.restoreState()

    def cover_page(self,first_line,second_line,third_line=None):

        """  ____________
            |            |
            |            |
            |  1st line  |
            |  2nd line  |
            |  3rd line  |
            |            |
            |____________|"""


        self.add_spacer(x=0, y=3.6)
        self.add_heading(first_line, htmltag='centered-bold')
        self.add_heading(second_line, htmltag='centered-italic')
        self.add_heading(third_line,htmltag='centered-italic1')
        self.add_page_break()

    def add_spacer(self,x=0,y=1):
         '''
         adds space between flowables
         by default unit is inch and y = 1
         '''
        gap=Spacer(x*inch,y*inch)
        self.flowables.append(gap)

    def add_image(self,image,width=None,height=None,kind='direct',mask='auto',lazy=1,hAlign='CENTER'):
        """
        adds image,
        adjust width, height, alignment and masking
        """
        im = Image(image,
                    width=width,
                    height=height,
                    hAlign=hAlign,
                    mask=mask,
                    lazy=lazy,
                    )
        self.flowables.append(im)

    def add_heading(self,input_text,htmltag= 'h1'):
        '''

        tag ==> 'h1','h2','h3','h4','h5','h6'
        other = 'Title'
        # Italic, Normal
        # OrderedList
        # Title
        # UnorderedList

        '''
        self.flowables.append(
        Paragraph(input_text,self.styles[htmltag])
        )

    def add_paragraph(self,paragraph,htmltag='BodyText'):
        """

        :param self:
        :param paragraph:
        :param htmltag:
        :return adds a paragraph as flowable
:
        """
        self.flowables.append(Paragraph(paragraph,self.styles[htmltag]))

    def add_bullet_points(self, paragraph,htmltag='bullet'):
        """

        :param self:
        :param paragraph:
        :param htmltag:
        :return  bullet points in paragraph flowables
:
        """
        style = self.styles[htmltag]
        p = Paragraph(paragraph, style, bulletText='◘')
        self.flowables.append(p)

    def add_page_break(self):
        """

        :param self:
        :return page breaks and the remaing flowables are added in the next page:
        """
        self.flowables.append(PageBreak())

    def add_text(self, text, style, tag):
        """

        :param self:
        :param text:
        :param style:
        :param tag:
        :return a flowable with tags:
        """
        x = '<%s>%s</%s>' % (tag, text, tag)
        self.flowables.append(Paragraph(x, PS(style)))

    def add_colored_text(self, text, fontname='times', color='black', style='body'):
        """
        :param self:
        :param text:
        :param fontname:
        :param color:
        :param style:
        :return a flowable :
        """
        x = "<font fontname = '%s' color='%s'>%s</font>" % (fontname, color, text)
        self.flowables.append(Paragraph(x, PS(style)))

    def font_tags(self, text, style, fontname='times', fontsize=12, color='black'):
        """

        :param self:
        :param text:
        :param style:
        :param fontname:
        :param fontsize:
        :param color:
        :return a flowable with tags:
        """
        x = "<font fontname = '%s' size = %d color='%s'>%s</font>" % (fontname, fontsize, color, text)
        self.flowables.append(Paragraph(x, PS(style)))

    def add(self, text, style):
        """

        :param self:
        :param text:
        :param style:
        :return:
        """
        self.flowables.append(Paragraph(text, PS(style)))

    def add_table(
            self, data,
            colWidths=1.33 * inch,
            rowHeights=None,
            style=None,
            splitByRow=1,
            repeatRows=0,
            repeatCols=0,
            rowSplitRange=None,
            spaceBefore=None,
            spaceAfter=None):
        """

        :param self:
        :param data:
        :param colWidths:
        :param rowHeights:
        :param style:
        :param splitByRow:
        :param repeatRows:
        :param repeatCols:
        :param rowSplitRange:
        :param spaceBefore:
        :param spaceAfter:
        :return add a table to flowable:
        """
        styles1 = getSampleStyleSheet()

        data1 = [[word if len(str(word)) < 18 else Paragraph(str(word), styles1['Normal']) for word in line] for line in
                 data]

        t = Table(
            data1,
            colWidths=colWidths,
            rowHeights=rowHeights,
            style=style,
            splitByRow=splitByRow,
            repeatRows=repeatRows,
            repeatCols=repeatCols,
            rowSplitRange=rowSplitRange,
            spaceBefore=spaceBefore,
            spaceAfter=spaceAfter
        )
        t.setStyle(TableStyle([
            # ('FONTNAME',(0,0),(-1,-1),'Vera'),
            # ('SIZE',(0,0),(-1,-1),1),
            ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.grey),
            ('BOX', (0, 0), (-1, -1), 0.2, colors.blue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lavender),
        ])
        )
        self.flowables.append(t)

    def afterFlowable(self, flowable):
        """

        :param self:
        :param flowable:
        :return registers entries into the TOC:
        (automatically runs when add_table_of_contents is called)
        """
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry',(0,text,self.page-1))
            if style == 'Heading2':
                self.notify('TOCEntry',(1,text,self.page-1))
            if style == 'Heading3':
                self.notify('TOCEntry',(2,text,self.page-1))
            if style == 'Heading4':
                self.notify('TOCEntry',(3,text,self.page-1))
            if style == 'Heading5':
                self.notify('TOCEntry',(4,text,self.page-1))
            if style == 'Heading6':
                self.notify('TOCEntry',(6,text,self.page-1))
                
    def add_table_of_contents(self):
        """

        :param self:
        :return TOC :
        """
        self.add_heading('Table of Contents', htmltag='centered-bold')
        toc = TableOfContents()
        toc.levelStyles = [
            PS(fontName='Times-Bold', fontSize=18, name='TOCHeading1', leftIndent=10, firstLineIndent=-15, spaceBefore=10, leading=16),
            PS(fontName='Times-Italic',fontSize=16, name='TOCHeading2', leftIndent=22, firstLineIndent=-15, spaceBefore=5, leading=12),
            PS(fontName='Times-Italic',fontSize=14, name='TOCHeading3', leftIndent=34, firstLineIndent=-15, spaceBefore=5, leading=12),
            PS(fontName='Times-Italic',fontSize=12, name='TOCHeading4', leftIndent=46, firstLineIndent=-15, spaceBefore=5, leading=12)
        ]
        self.flowables.append(toc)
        
    def buildPDF(self):
        """

        :param self:
        :return builds the entire document:
        """
        self.multiBuild(self.flowables, onFirstPage = self.myFirstPage
                        ,onLaterPages = self.myLaterPages
                        )
