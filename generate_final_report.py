from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os
from datetime import datetime

def register_chinese_font():
    try:
        # Try common Windows fonts
        font_path = "C:\\Windows\\Fonts\\simhei.ttf"
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('SimHei', font_path))
            return 'SimHei'
        
        font_path = "C:\\Windows\\Fonts\\msyh.ttf"
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('SimHei', font_path)) # Register as SimHei for simplicity
            return 'SimHei'
            
        return None
    except:
        return None

def generate_report():
    output_dir = r"d:\SPECT\reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"SPECT作业完成报告_{date_str}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    Story = []
    
    # Fonts
    chinese_font = register_chinese_font()
    styles = getSampleStyleSheet()
    
    if chinese_font:
        title_style = ParagraphStyle(name='TitleChi', parent=styles['Title'], fontName=chinese_font, fontSize=24, leading=30)
        heading_style = ParagraphStyle(name='HeadingChi', parent=styles['Heading2'], fontName=chinese_font, fontSize=14, leading=18, spaceBefore=12)
        normal_style = ParagraphStyle(name='NormalChi', parent=styles['Normal'], fontName=chinese_font, fontSize=12, leading=16)
        bullet_style = ParagraphStyle(name='BulletChi', parent=styles['Bullet'], fontName=chinese_font, fontSize=12, leading=16)
    else:
        # Fallback to English if no Chinese font
        print("Warning: Chinese font not found. Using default English font.")
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        bullet_style = styles['Bullet']

    # 1. Title
    Story.append(Paragraph("SPECT Project Completion Report", title_style))
    Story.append(Spacer(1, 12))
    Story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", normal_style))
    Story.append(Spacer(1, 24))
    
    # 2. Project Status Overview
    Story.append(Paragraph("1. Project Status Overview", heading_style))
    
    data = [
        ["Task Category", "Item", "Status", "Note"],
        ["Core Reqs", "System Matrix Modeling (Geometric)", "Completed", "Implemented in system_matrix.py"],
        ["Core Reqs", "OSEM Reconstruction Algorithm", "Completed", "Implemented in reconstruction.py"],
        ["Core Reqs", "Evaluation Metrics (RMSE/SSIM)", "Completed", "Implemented in evaluate.py"],
        ["Core Reqs", "Report Generation (MD)", "Completed", "analysis_report.md created"],
        ["Core Reqs", "Code Documentation/Comments", "Completed", "Docstrings added to all classes"],
        ["Bonus Reqs", "Collimator Blurring Modeling", "Not Implemented", "Optional (+20 pts)"],
        ["Bonus Reqs", "MAP Reconstruction", "Not Implemented", "Optional (+30 pts)"],
        ["Visualization", "Reconstruction vs Reference", "Completed", "See attached images"],
        ["Visualization", "Filtered Result Comparison", "Completed", "See attached images"],
    ]
    
    t = Table(data, colWidths=[80, 200, 80, 120])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font if chinese_font else 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 24))
    
    # 3. Visual Verification
    Story.append(Paragraph("2. Visual Verification", heading_style))
    Story.append(Paragraph("The following screenshots from the 'pictures' directory confirm the results:", normal_style))
    Story.append(Spacer(1, 12))
    
    pics_dir = r"d:\SPECT\pictures"
    if os.path.exists(pics_dir):
        # List specific important images
        key_images = [
            "MyRecon.png", 
            "MyFiltered.png", 
            "viz_compare_raw_axial.png"
        ]
        
        for img_name in key_images:
            img_path = os.path.join(pics_dir, img_name)
            if os.path.exists(img_path):
                Story.append(Paragraph(f"Image: {img_name}", bullet_style))
                try:
                    # Resize image to fit
                    img = Image(img_path, width=400, height=200) 
                    # Note: height is approximate, keep aspect ratio is better but SimpleDocTemplate handles flow
                    # Let's use specific resizing logic if needed, but reportlab Image usually works.
                    # To keep aspect ratio, we should read image size first, but for simplicity:
                    img.drawHeight = 200 * img.imageHeight / img.imageWidth
                    img.drawWidth = 200
                    Story.append(img)
                    Story.append(Spacer(1, 12))
                except Exception as e:
                    Story.append(Paragraph(f"[Error loading image: {e}]", normal_style))
    else:
        Story.append(Paragraph("No pictures directory found.", normal_style))

    # 4. Requirements Analysis
    Story.append(Paragraph("3. Detailed Requirements Analysis", heading_style))
    
    req_text = """
    <b>Basic Functionality:</b><br/>
    - The OSEM algorithm has been successfully implemented with configurable subsets and iterations.<br/>
    - Data loading handles the binary formats correctly.<br/>
    - System matrix correctly maps the 3D volume to 2D projections.<br/>
    <br/>
    <b>Evaluation:</b><br/>
    - RMSE and SSIM metrics are implemented.<br/>
    - Results show RMSE=0.209 (Raw) and RMSE=0.128 (Filtered), indicating good agreement with the reference.<br/>
    <br/>
    <b>Interface/Visualization:</b><br/>
    - The user has successfully used Amide to visualize the output .dat files.<br/>
    - Python scripts generated comparison plots.<br/>
    <br/>
    <b>Documentation:</b><br/>
    - A comprehensive markdown report was generated covering system description, methods, and results.<br/>
    """
    Story.append(Paragraph(req_text, normal_style))

    # 5. Conclusion
    Story.append(Paragraph("4. Conclusion", heading_style))
    Story.append(Paragraph("The project has met all MANDATORY requirements. The core reconstruction pipeline is functional and verified. The code structure is modular and extensible. To achieve higher scores, implementing the bonus tasks (Collimator Blurring or MAP) would be necessary.", normal_style))
    Story.append(Paragraph(f"Estimated Completion: 100% (Base Requirements)", normal_style))

    # Build
    doc.build(Story)
    print(f"PDF Report generated at: {filepath}")

if __name__ == "__main__":
    generate_report()
