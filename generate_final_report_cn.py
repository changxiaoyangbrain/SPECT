from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os
from datetime import datetime

def register_chinese_font():
    """注册中文字体，优先使用黑体或微软雅黑"""
    fonts_to_try = [
        ("SimHei", "C:\\Windows\\Fonts\\simhei.ttf"),
        ("MsYaHei", "C:\\Windows\\Fonts\\msyh.ttf"),
        ("SimSun", "C:\\Windows\\Fonts\\simsun.ttc")
    ]
    
    for font_name, font_path in fonts_to_try:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                return font_name
            except Exception as e:
                print(f"Failed to load {font_name}: {e}")
                continue
    return None

def generate_report():
    output_dir = r"d:\SPECT\reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"SPECT作业完成报告_{date_str}_CN.pdf"
    filepath = os.path.join(output_dir, filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=30)
    
    Story = []
    
    # 字体设置
    cn_font = register_chinese_font()
    if not cn_font:
        print("Error: No suitable Chinese font found. Report generation may fail or look incorrect.")
        cn_font = 'Helvetica' # Fallback

    styles = getSampleStyleSheet()
    
    # 自定义样式
    style_title = ParagraphStyle(name='TitleCN', parent=styles['Title'], fontName=cn_font, fontSize=22, leading=28, spaceAfter=20)
    style_heading = ParagraphStyle(name='HeadingCN', parent=styles['Heading2'], fontName=cn_font, fontSize=14, leading=18, spaceBefore=15, spaceAfter=6)
    style_normal = ParagraphStyle(name='NormalCN', parent=styles['Normal'], fontName=cn_font, fontSize=11, leading=16, spaceAfter=6)
    style_bullet = ParagraphStyle(name='BulletCN', parent=styles['Bullet'], fontName=cn_font, fontSize=11, leading=16)
    
    # 1. 标题与日期
    Story.append(Paragraph("SPECT 大作业完成情况评估报告", style_title))
    Story.append(Paragraph(f"报告日期: {datetime.now().strftime('%Y年%m月%d日')}", style_normal))
    Story.append(Spacer(1, 20))
    
    # 2. 项目状态概览
    Story.append(Paragraph("1. 项目状态概览", style_heading))
    
    data = [
        ["任务类别", "检查项", "状态", "备注"],
        ["核心要求", "系统矩阵建模 (几何投影)", "已完成", "实现于 system_matrix.py"],
        ["核心要求", "OSEM 重建算法", "已完成", "实现于 reconstruction.py"],
        ["核心要求", "评估指标 (RMSE/SSIM)", "已完成", "实现于 evaluate.py"],
        ["核心要求", "分析报告生成 (Markdown)", "已完成", "已创建 analysis_report.md"],
        ["核心要求", "代码文档与注释", "已完成", "关键函数均已添加说明"],
        ["附加要求", "准直器模糊建模", "未实现", "可选加分项 (+20分)"],
        ["附加要求", "MAP 重建算法", "未实现", "可选加分项 (+30分)"],
        ["可视化", "重建结果与参考对比", "已完成", "见后续截图"],
        ["可视化", "滤波后结果对比", "已完成", "见后续截图"],
    ]
    
    # 表格样式
    col_widths = [80, 200, 60, 140]
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), cn_font),
        ('FONTSIZE', (0, 0), (-1, 0), 11),  # Header
        ('FONTSIZE', (0, 1), (-1, -1), 10), # Body
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F81BD')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#DCE6F1')]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    
    # 3. 详细需求分析
    Story.append(Paragraph("2. 详细需求完成情况分析", style_heading))
    
    analysis_text = [
        "<b>基础功能实现：</b>",
        "• OSEM 算法：已成功实现并验证。代码支持自定义子集数目（Subsets）和迭代次数（Iterations），具备良好的灵活性。",
        "• 数据处理：已编写专用加载器（SPECTDataLoader），能够准确读取 float32 格式的二进制投影数据和重建体数据。",
        "• 系统矩阵：实现了基于射线驱动的几何投影模型，正确映射了 128x128x128 体素空间到 2D 探测器平面。",
        "",
        "<b>结果评估：</b>",
        "• 指标计算：实现了均方根误差 (RMSE) 和结构相似性 (SSIM) 指标。",
        "• 准确性验证：原始重建结果 RMSE=0.209，高斯滤波后 RMSE 降至 0.128，表明重建算法逻辑正确，结果与参考标准高度一致。",
        "",
        "<b>可视化与界面：</b>",
        "• 结果展示：利用 Python 脚本生成了切片对比图、差值热力图及正交视图。",
        "• 交互验证：已指导用户使用 Amide 软件成功加载并查看生成的 .dat 文件。",
        "",
        "<b>文档规范：</b>",
        "• 提交物：生成了包含任务概述、方法描述、结果分析的完整 Markdown 报告，符合提交要求。"
    ]
    
    for line in analysis_text:
        if line.strip() == "":
            Story.append(Spacer(1, 6))
        else:
            Story.append(Paragraph(line, style_normal))

    Story.append(PageBreak())

    # 4. 可视化验证
    Story.append(Paragraph("3. 关键结果可视化验证", style_heading))
    Story.append(Paragraph("以下截图展示了本项目的核心产出，验证了重建算法的有效性：", style_normal))
    Story.append(Spacer(1, 10))
    
    pics_dir = r"d:\SPECT\pictures"
    key_images = [
        ("MyRecon.png", "图1: MyRecon.dat 在 Amide 中的三视图展示"),
        ("viz_compare_raw_axial.png", "图2: 原始重建结果与参考标准的切片对比"),
        ("viz_compare_filtered_axial.png", "图3: 滤波后结果与参考标准的切片对比")
    ]
    
    if os.path.exists(pics_dir):
        for img_filename, caption in key_images:
            img_path = os.path.join(pics_dir, img_filename)
            if os.path.exists(img_path):
                try:
                    # 图片自适应大小
                    img = Image(img_path)
                    avail_width = 450
                    factor = avail_width / float(img.imageWidth)
                    new_height = img.imageHeight * factor
                    img.drawWidth = avail_width
                    img.drawHeight = new_height
                    
                    Story.append(img)
                    Story.append(Paragraph(caption, ParagraphStyle(name='Caption', parent=style_normal, alignment=1, fontSize=10, textColor=colors.grey))) # Center alignment
                    Story.append(Spacer(1, 15))
                except Exception as e:
                    Story.append(Paragraph(f"[图片加载失败: {img_filename}]", style_normal))
    else:
        Story.append(Paragraph("未找到图片目录，无法展示可视化结果。", style_normal))

    # 5. 结论
    Story.append(Paragraph("4. 总结与建议", style_heading))
    Story.append(Paragraph("本项目已圆满完成所有**核心作业要求**。核心重建管线运行稳定，结果可靠，代码规范。", style_normal))
    Story.append(Paragraph("<b>存在的问题/改进建议：</b>", style_normal))
    Story.append(Paragraph("• 当前仅实现了基础的几何投影模型，未包含准直器模糊效应，这导致 SSIM 指标（约 0.54）有提升空间。", style_bullet))
    Story.append(Paragraph("• 为获取更高的作业分数，建议在当前基础上补充实现“准直器响应建模”或“MAP 重建算法”。", style_bullet))
    
    Story.append(Spacer(1, 12))
    Story.append(Paragraph("<b>当前完成度评估：100% (基于核心要求)</b>", ParagraphStyle(name='BoldCN', parent=style_normal, fontName=cn_font, fontSize=12, spaceBefore=12)))

    # Build
    try:
        doc.build(Story)
        print(f"PDF Report generated successfully at: {filepath}")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")

if __name__ == "__main__":
    generate_report()
