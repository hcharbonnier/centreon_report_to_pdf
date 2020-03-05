from reportlab.lib.units import  mm
from reportlab.platypus import BaseDocTemplate,Frame,Paragraph,PageBreak, PageTemplate,FrameBreak,NextPageTemplate
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import green, lightgreen,  red,  black,  orange,  grey,  blueviolet,  silver, salmon, whitesmoke

from reportlab.graphics.shapes import Drawing
#, String
from reportlab.graphics.charts.piecharts import Pie

#from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from CentreonData import *
import Settings


#from CentreonData import *



pdf_output_file = Settings.pdf_output_file 
#csv_filepath = Settings.csv_filepath

# Variables definitions
DOCMARGIN = 10*mm
PAGE_HEIGHT=297*mm
PAGE_WIDTH=210*mm
height=297*mm
width=210*mm

# Table row color
skyblue = "#bfecff"

# Columns variables definition
# [(start_column, start_row), (end_column, end_row)]
all_cells = [(0, 0), (-1, -1)]
header = [(0, 0), (-1, 0)]

# Columns table resume
column_state=  [(0, 0), (0, -1)]
column_total_time = [(1, 0), (1, -1)]
column_mean_time = [(2, 0), (2, -1)]
column_alerts = [(3, 0), (3, -1)]

# Columns table details
column_hostname =  [(0, 0), (0, -1)]
column_service = [(1, 0), (1, -1)]
column_ok_percent = [(2, 0), (2, -1)]
column_ok_alerts = [(3, 0), (3, -1)]
column_warn_percent = [(4, 0), (4, -1)]
column_warn_alerts = [(5, 0), (5, -1)]
column_critical_percent = [(6, 0), (6, -1)]
column_critical_alerts = [(7, 0), (7, -1)]
column_unknow_percent = [(8, 0), (8, -1)]
column_unknow_alerts = [(9, 0), (9, -1)]
column_scheduled_percent = [(10, 0), (10, -1)]
column_undetermined_alerts = [(11, 0), (11, -1)]



# Output document
# Landscape
#template = PageTemplate('normal',  [Frame(DOCMARGIN, DOCMARGIN, 287*mm,200*mm, id='F1')])
# Letter
doc = BaseDocTemplate(
    pdf_output_file,
    pagesize=A4, 
    topMargin=DOCMARGIN,
    bottomMargin=DOCMARGIN,
    leftMargin=DOCMARGIN, 
    rightMargin=DOCMARGIN,
    showBoundary=1, 
)

########################################
########################################  
# TODO - Try diff fonts 
# Function to define some styles
def stylesheet():
    """Function to define some styles"""
    styles= {
        'default': ParagraphStyle(
            'default',
            fontName='Courier',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Courier',
            bulletFontSize=10,
            bulletIndent=0,
            textColor= red,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 0,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,         
            splitLongWords=1,
        ),
    }
    
    styles['table_default'] = TableStyle([
            ('GRID',(0,0),(-1,-1),0.5,grey),
            ('FONTSIZE', all_cells[0], all_cells[1], 8),
            ('VALIGN', all_cells[0], all_cells[1], 'MIDDLE'),
            ('ALIGN', all_cells[0], all_cells[1], 'CENTER'),
        ]
    )    

    styles['table_details_head'] = TableStyle([
            ('SPAN',  (0, 0),  (0, 1)),
            ('SPAN',  (1, 0),  (1, 1)),
            ('SPAN',  (2, 0),  (3, 0)),
            ('SPAN',  (4, 0),  (5, 0)),
            ('SPAN',  (6, 0),  (7, 0)),
            ('SPAN',  (8, 0),  (9, 0)),
        ]
    )    
    
    styles['table_details'] = TableStyle([
            # Columns names 
            #column_hostname =  [(0, 0), (0, -1)]
            #column_service = [(1, 0), (1, -1)]
            #column_ok_percent = [(2, 0), (2, -1)]
            #column_ok_alerts = [(3, 0), (3, -1)]
            #column_warn_percent = [(4, 0), (4, -1)]
            #column_warn_alerts = [(5, 0), (5, -1)]
            #column_critical_percent = [(6, 0), (6, -1)]
            #column_critical_alerts = [(7, 0), (7, -1)]
            #column_unknow_percent = [(8, 0), (8, -1)]
            #column_unknow_alerts = [(9, 0), (9, -1)]
            #column_scheduled_percent = [(10, 0), (10, -1)]
            #column_undetermined_alerts = [(11, 0), (11, -1)]
            ('GRID',(0,0),(-1,-1),0.5,whitesmoke),
            ('ALIGN', column_hostname[0], column_hostname[1], 'LEFT'),
            ('ALIGN', column_service[0], column_service[1], 'LEFT'),
            ('ALIGN', (0, 0),  (0, 1), 'CENTER'),
            ('ALIGN', (1, 0),  (1, 1), 'CENTER'),
            ('BACKGROUND',  (2, 0),  (3, -1),  lightgreen),
            ('BACKGROUND',  (4, 0),  (5, -1),  orange),
            ('BACKGROUND',  (6, 0),  (7, -1),  red),
            ('BACKGROUND',  (8, 0),  (9, -1),  silver),
            ('BACKGROUND',  column_scheduled_percent[0], column_scheduled_percent[1],  blueviolet),
            ('BACKGROUND',  column_undetermined_alerts[0],  column_undetermined_alerts[1],  salmon),
        ]
    )    
    
    styles['table_resume'] = TableStyle([
            # Columns names 
            #column_state=  [(0, 0), (0, -1)]
            #column_total_time = [(1, 0), (1, -1)]
            #column_mean_time = [(2, 0), (2, -1)]
            #column_alerts = [(3, 0), (3, -1)]
            ('FONTSIZE', all_cells[0], all_cells[1], 10),
            ('GRID',(0,0),(-1,-1),0.5,whitesmoke),
            ('ALIGN', column_state[0], column_state[1], 'LEFT'),
            ('BACKGROUND',  (0, 0), (-1, 1),  "#eaeaee"),
            ('TEXTCOLOR',  (0, 1),  (0, 1),  green),
            ('TEXTCOLOR',  (0, 2),  (0, 2),  orange),
            ('TEXTCOLOR',  (0, 3),  (0, 3),  red),
            ('TEXTCOLOR',  (0, 4),  (0, 4),  black),
            ('TEXTCOLOR',  (0, 5),  (0, 5),  blueviolet),
            ('TEXTCOLOR',  (0, 6),  (0, 6),  salmon),
            ('FONTNAME',  (0, 1),  (0, 1),  'Helvetica-Bold'),
            ('FONTNAME',  (0, 2),  (0, 2),  'Helvetica-Bold'),
            ('FONTNAME',  (0, 3),  (0, 3),  'Helvetica-Bold'),
            ('FONTNAME',  (0, 4),  (0, 4),  'Helvetica-Bold'),
            ('FONTNAME',  (0, 5),  (0, 5),  'Helvetica-Bold'),
            ('FONTNAME',  (0, 6),  (0, 6),  'Helvetica-Bold'),
            ('BACKGROUND',  (0,  -1), (-1, -1),  "#eaeaee"),
        ]
    )
    
    return styles

styles = stylesheet()
styleNormal = styles['default']
styleTable = styles['table_default']
styleTableDetailsHead = styles['table_details_head']
styleTableDetails = styles['table_details']
styleTableResume = styles['table_resume']


########################################
########################################  
# Function to put the page number at the end of page to template 1
def foot1(canvas,doc):
    """Function to put the page number at the end of page"""
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(width-20*mm, 2*mm, "%d template 1" % doc.page)
    canvas.restoreState()

    
# Function to put the page number at the end of page to template 2
def foot2(canvas,doc):
    """Function to put the page number at the end of page"""
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(width-20*mm, 2*mm,"%d template 2 " % doc.page)


########################################
########################################  
# Function to generate the Pie Graph
def pie_chart_with_legend():
    """Function to generate the Pie Graph"""

    # Get the details data from CSV file
    data_df = get_centreon_csv_resume()
    
    # Get the values from Total Time and Status 
    data_list = data_df['Total Time'].astype(float).values.tolist()
    data_labels = data_df['Status'].values.tolist()
    
    # Position of the Pie
    drawing = Drawing(width=10*mm, height=70*mm)

    # Set some Pie parameters
    pie = Pie()
    pie.x = 14*mm
    pie.y = 10*mm
    pie.height = 60*mm
    pie.width = 60*mm
    pie.data = data_list
    pie.labels = data_labels

    pie.sideLabels = True
    pie.slices.strokeWidth = 0.5
    pie.slices.popout = 7
    pie.startAngle = 90
    pie.sameRadii = 1
    pie.direction = 'clockwise'
    
    # define colors of Pie
    piecolors = [ green,  orange,  red,  silver,  blueviolet,  salmon ]
    for i, color in enumerate(piecolors): 
        pie.slices[i].fillColor =  color

    # Create the pie
    drawing.add(pie)

    return drawing
    
    
########################################
########################################  
# Function to get RESUME data from CSV, format and create a table
def build_table_resume():
    """Function to get RESUME data from CSV, format and create a table"""
    # Get the details data from CSV file
    data_df=get_centreon_csv_resume()

    # Get the total of Alerts
    total_alerts=0
    total_alerts=int(data_df["Alerts"].sum(skipna = True))

    # Create a extra line with "Total" at the end
    extra_table_foot=[['Total', '', '', total_alerts ]]
    # Conact the header + data to list + t
    data_list=[data_df.columns.values.tolist()] + data_df.values.tolist() + list(extra_table_foot)

    # Generate the table using the list and repeat the headers if necesary
    table=Table(data=data_list,  repeatRows=0, rowHeights=15 )

    # Apply some styles to table and cells
    table.setStyle(styleTable)
    table.setStyle(styleTableResume)
    
    # Get the number of rows (+1 for two lines headers)
    data_len = len(data_df)  + 1
    
    # exchage rows background color
    for each in range(data_len):
        if each == 0:
            continue
        if each % 2 == 0:
            bg_color = whitesmoke
        else:
            bg_color = skyblue

        table.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

    return table


########################################
########################################  
# Function to get DETAILS data from CSV, format and create a table
def build_table_details():
    """Function to get DETAILS data from CSV, format and create a table"""
    # Get the details data from CSV file
    data_df=get_centreon_csv_details ()

    # Create a second subhead to table
    head1=[['', '', '%', 'Alert', '%', 'Alert', '%', 'Alert', '%', 'Alert', 'Downtimes', '%']]

    # Conact the header + sub_header and data to list
    data_list=[data_df.columns.values.tolist()] + list(head1) + data_df.values.tolist()
    
    # Generate the table using the list and repeat the headers if necesary
    table=Table(data=data_list,  repeatRows=2)

    # Apply some styles to table and cells
    table.setStyle(styleTable)
    table.setStyle(styleTableDetailsHead)
    table.setStyle(styleTableDetails)
    
    # Get the number of rows (+2 for two lines headers)
    data_len = len(data_df) + 2
    # exchage rows background color
    for each in range(data_len):
        if each == 0 or each ==1:
            continue
        if each % 2 == 0:
            bg_color = whitesmoke
        else:
            bg_color = skyblue

        table.setStyle(TableStyle([('BACKGROUND', (0, each), (1, each), bg_color)]))

    return table


########################################
########################################  
#  Function to build the PDF report with graph and tables
def build_report():
    """Function to build the PDF report with graph and tables"""
    
    # Define the variable contents
    contents =[]
#    styleSheet = getSampleStyleSheet()

    # Define some Frames to Page 02
    Frame_Graphic = Frame(5*mm, height-85*mm, (width-10*mm)/2, 80*mm,showBoundary = 1)
    Frame_Info = Frame((width)/2, height-30*mm, (width-10*mm)/2, 25*mm,showBoundary = 1)
    Frame_Resume = Frame((width)/2, height-85*mm, (width-10*mm)/2, 55*mm,showBoundary = 1)
    Frame_Details = Frame(5*mm, 5*mm, (width-10*mm), height-90*mm,showBoundary = 1,id='col1')

    # Create a list with all frames to be in the second page
    framesSecondPage = []
    framesSecondPage.append(Frame_Graphic)
    framesSecondPage.append(Frame_Info)
    framesSecondPage.append(Frame_Resume)
    framesSecondPage.append(Frame_Details)

    # Define other Frames (all page) if table_details need more than one page
    Frame_Details_Continue = Frame(5*mm, 5*mm, (width-10*mm), (height-10*mm),showBoundary = 1,id='col1later')

    # Create a list with frame to be in the anothers pages
    framesOthersPages = []
    framesOthersPages.append(Frame_Details_Continue)

    # Create a list of templates and associate the frames list to it.
    templates = []
    templates.append(PageTemplate(frames=framesSecondPage, id="secondpage",onPage=foot1))
    templates.append(PageTemplate(frames=framesOthersPages, id="otherspages",onPage=foot2))
    
    # Add this templates to document.
    doc.addPageTemplates(templates)
  
    # Next content will be on Frame_Info at second page 
    contents.append(NextPageTemplate('secondpage'))
    
    # Create the pie graph with the resume information
    chart = pie_chart_with_legend()
    
    # Add the pie to contents on Frame_Graphic
    contents.append(chart)
    
#    logoleft = Image('/tmp/firodo-port-25.png')
#    logoleft._restrictSize(20*mm, 20*mm)
#    logoleft.hAlign = 'LEFT'
#    logoleft.vAlign = 'CENTER'
#    logoright = Image('/tmp/mona-tc.png')
#    logoright._restrictSize(20*mm, 20*mm)
#    logoright.hAlign = 'RIGHT'
#    logoright.vAlign = 'CENTER'
##    contents.append(logoleft)
##    contents.append(FrameBreak())
#    #
#    ##json_file = open("details.txt","r",encoding='utf-8')
#    ##details = json.load(json_file)
#    isctitle = styleSheet['Title']
#    isctitle.fontSize=12
#    isctitle.alignment=TA_CENTER
#    isctitle.leading=10
#    contents.append(Paragraph("INTERNATIONAL KING VHS UNION. Raamstraat 78, Delft",isctitle))
#    theme = styleSheet['Normal']
#    theme.fontSize=10
#    theme.alignment=TA_CENTER
#    theme.leading = 14
#    contents.append(Paragraph("VHS",theme))
#    celebrant=styleSheet['Normal']
#    celebrant.fontSize=10
#    celebrant.alignment=TA_CENTER
#    celebrant.leading = 14
#    contents.append(Paragraph("president",celebrant))
#    date = styleSheet['Normal']
#    date.fontSize=10
#    date.alignment=TA_CENTER
#    date.leading = 14
#    contents.append(Paragraph("date",date))

    # Next content will be the Information on Frame_Info
    contents.append(FrameBreak())
    
    # Next content will be the Resume on Frame_Resume
    contents.append(FrameBreak())
    
    #Create and add table_details on second page
    contents.append(build_table_resume())

    # Next content will be on Frame_Details
    contents.append(FrameBreak())
    
    contents.append(NextPageTemplate('otherspages'))

    # Add table_details on second page
    contents.append(build_table_details())

#    contents.append(NextPageTemplate('otherspages'))
#    contents.append(PageBreak())

    doc.build(contents)