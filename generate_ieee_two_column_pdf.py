"""
generate_ieee_two_column_pdf.py
===============================
Generates an IEEE Two-Column PDF with a center vertical dividing line
and all section headings centered in the middle of each column.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, HRFlowable, NextPageTemplate, FrameBreak
)
from reportlab.pdfgen import canvas

class IEEETwoColCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(IEEETwoColCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super(IEEETwoColCanvas, self).showPage()
        super(IEEETwoColCanvas, self).save()

    def draw_decorations(self, total_pages):
        self.saveState()
        self.setFont("Times-Roman", 8)
        self.setFillColor(colors.HexColor("#333333"))

        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(45, 752, "AgroEdge AI: An Edge AI-Based Foliar Pathology & Autonomous Precision Agronomy System")
            self.drawRightString(567, 752, "LPU CSE 276 Project Report")
            self.setStrokeColor(colors.HexColor("#AAAAAA"))
            self.setLineWidth(0.5)
            self.line(45, 746, 567, 746)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#AAAAAA"))
        self.setLineWidth(0.5)
        self.line(45, 42, 567, 42)
        self.drawString(45, 30, "Lovely Professional University | School of Computing and Artificial Intelligence")
        self.drawRightString(567, 30, f"Page {self._pageNumber} of {total_pages}")

        # Vertical Partition Line between Two Columns
        # Column 1 right edge = 45 + 250 = 295, Column 2 left edge = 317. Center = 306
        self.setStrokeColor(colors.HexColor("#888888"))
        self.setLineWidth(0.5)
        if self._pageNumber == 1:
            # First page has banner on top, divider starts lower (e.g. y=430 down to y=50)
            self.line(306, 50, 306, 460)
        else:
            # Later pages: full height divider line
            self.line(306, 50, 306, 735)

        self.restoreState()


def build_ieee_pdf(filename="AgroEdge_AI_IEEE_Report.pdf"):
    # Margins: 45 pt (0.625 in)
    # Total width = 612 pt, printable = 522 pt
    # Col width = 250 pt, Gap = 22 pt, Col 1: 45 to 295, Col 2: 317 to 567
    doc = BaseDocTemplate(filename, pagesize=letter, leftMargin=45, rightMargin=45, topMargin=45, bottomMargin=45)

    # First page template: Top Banner Frame (Full width) + Two lower Frames
    frame_top = Frame(45, 475, 522, 270, id='F_Top', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    frame_b1 = Frame(45, 50, 250, 420, id='F_B1', leftPadding=0, rightPadding=6, topPadding=0, bottomPadding=0)
    frame_b2 = Frame(317, 50, 250, 420, id='F_B2', leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0)

    first_page_template = PageTemplate(id='FirstPage', frames=[frame_top, frame_b1, frame_b2])

    # Later pages template: Full height two columns
    frame_l1 = Frame(45, 50, 250, 685, id='F_L1', leftPadding=0, rightPadding=6, topPadding=0, bottomPadding=0)
    frame_l2 = Frame(317, 50, 250, 685, id='F_L2', leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0)

    later_page_template = PageTemplate(id='LaterPages', frames=[frame_l1, frame_l2])

    doc.addPageTemplates([first_page_template, later_page_template])

    styles = getSampleStyleSheet()

    title_s = ParagraphStyle('T', fontName='Times-Bold', fontSize=17, leading=20, alignment=1, spaceAfter=8)
    author_s = ParagraphStyle('A', fontName='Times-Roman', fontSize=11, leading=13, alignment=1, spaceAfter=2)
    reg_s = ParagraphStyle('R', fontName='Times-Italic', fontSize=9.5, leading=12, alignment=1, spaceAfter=2)
    affil_s = ParagraphStyle('AF', fontName='Times-Italic', fontSize=8.5, leading=11, alignment=1, spaceAfter=6)
    sub_s = ParagraphStyle('S', fontName='Times-Italic', fontSize=8, leading=10.5, alignment=1, spaceAfter=10)

    abs_s = ParagraphStyle('AB', fontName='Times-Bold', fontSize=8, leading=10.5, alignment=4, leftIndent=10, rightIndent=10, spaceAfter=4)
    kw_s = ParagraphStyle('KW', fontName='Times-Bold', fontSize=8, leading=10.5, alignment=4, leftIndent=10, rightIndent=10, spaceAfter=10)

    # HEADINGS IN THE MIDDLE (CENTERED)
    h1_center = ParagraphStyle('H1C', fontName='Times-Bold', fontSize=9.5, leading=12, alignment=1, spaceBefore=8, spaceAfter=3, keepWithNext=True)
    h2_left = ParagraphStyle('H2L', fontName='Times-BoldItalic', fontSize=8.5, leading=11, alignment=0, spaceBefore=5, spaceAfter=2, keepWithNext=True)
    body_s = ParagraphStyle('B', fontName='Times-Roman', fontSize=8, leading=10.5, alignment=4, spaceAfter=4)
    bullet_s = ParagraphStyle('BL', fontName='Times-Roman', fontSize=7.8, leading=10, alignment=4, leftIndent=10, spaceAfter=2)

    th_s = ParagraphStyle('TH', fontName='Times-Bold', fontSize=7, leading=8.5, alignment=1)
    td_s = ParagraphStyle('TD', fontName='Times-Roman', fontSize=7, leading=8.5)
    td_c = ParagraphStyle('TDC', fontName='Times-Roman', fontSize=7, leading=8.5, alignment=1)

    tcap_s = ParagraphStyle('TCAP', fontName='Times-Roman', fontSize=7.5, leading=9, alignment=1, spaceBefore=4, spaceAfter=2)

    story = []

    # 1. TOP BANNER (Full width)
    story.append(Paragraph("AgroEdge AI: An Edge AI-Based Foliar Pathology and<br/>Autonomous Precision Agronomy Monitoring System", title_s))
    story.append(Paragraph("Rishu", author_s))
    story.append(Paragraph("Reg. No. 12519632", reg_s))
    story.append(Paragraph(
        "B.Tech CSE (AI & ML), School of Computing and Artificial Intelligence<br/>"
        "Lovely Professional University, Phagwara, Punjab, India", affil_s
    ))
    story.append(Paragraph(
        "CSE 276: AI Foundations Project (Roll No. K4P25REB10). Submitted to Mr. Jimmy Singla, Department of Computer Science and Engineering.", sub_s
    ))
    story.append(Paragraph(
        "<i>Abstract</i>—AgroEdge AI is an edge-native artificial intelligence web application that diagnoses foliar crop diseases "
        "and automates closed-loop precision irrigation using on-device neural inference and real-time environmental telemetry. "
        "Standard cloud-dependent smart agriculture architectures suffer from high latency, recurring cellular bandwidth expenses, "
        "and complete system failure under erratic rural connectivity. AgroEdge AI eliminates cloud dependency during inference by "
        "deploying a lightweight MobileNet architecture fine-tuned on the 38-class PlantVillage benchmark dataset (54,303 leaf images). "
        "Four convolutional architectures were evaluated, and the INT8 Post-Training Quantized MobileNet model achieved the lowest recorded "
        "memory footprint of 2.56 MB (a 75% reduction from 14.0 MB) while accelerating CPU inference latency to 18 ms with 96.4% top-1 accuracy. "
        "A deterministic agronomic remediation engine prescribes dual-pathway (bio-organic and chemical) treatments with dosage metrics, "
        "while an autonomous closed-loop threshold module actuates solenoid irrigation valves based on volumetric soil moisture levels (<30%). "
        "The application is implemented using Python, ONNX Runtime, and Streamlit, and is deployed live on Streamlit Community Cloud at https://agroedgeai.streamlit.app.",
        abs_s
    ))
    story.append(Paragraph(
        "<i>Keywords</i>—Plant disease detection, Edge AI, MobileNet, Post-Training Quantization, ONNX Runtime, Closed-Loop Irrigation, Streamlit.",
        kw_s
    ))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#777777"), spaceBefore=0, spaceAfter=6))

    # Switch to lower frames on page 1, and LaterPages on page 2
    story.append(FrameBreak()) # breaks into bottom-left column of first page!
    story.append(NextPageTemplate('LaterPages'))

    # 2. TWO-COLUMN BODY CONTENT
    story.append(Paragraph("I. INTRODUCTION", h1_center))
    story.append(Paragraph("A. Background", h2_left))
    story.append(Paragraph(
        "Agricultural crop yield is vulnerable to severe destruction caused by foliar fungal, bacterial, and viral pathogens. "
        "According to the Food and Agriculture Organization (FAO), plant diseases cost the global economy over $220 billion annually, "
        "causing between 20% and 40% of agricultural production loss. Traditional manual scouting by agronomists is labor-intensive, "
        "infrequent, and subjective. While deep learning enables visual recognition of plant diseases, existing solutions rely on centralized cloud servers.",
        body_s
    ))
    story.append(Paragraph(
        "In practical agricultural environments, rural farmlands suffer from non-existent or unstable internet connectivity. Furthermore, autonomous field systems "
        "require millisecond-level decision making. AgroEdge AI resolves these bottlenecks by executing quantized deep neural networks locally on CPU runtimes with zero cloud dependence.",
        body_s
    ))

    story.append(Paragraph("B. Project Overview", h2_left))
    story.append(Paragraph(
        "AgroEdge AI accepts foliar photography via local uploads, sample libraries, or real-time camera video streams, preprocessing the imagery into a 224x224 RGB tensor. "
        "An INT8 quantized MobileNet model running on ONNX Runtime classifies the image across 38 distinct crop disease categories in 18 ms. The system simultaneously executes "
        "an agronomic remediation database providing organic/chemical prescriptions, a closed-loop soil moisture actuation engine controlling solenoid valves, and an IoT sensor telemetry buffer.",
        body_s
    ))

    story.append(Paragraph("C. Problem Statement", h2_left))
    story.append(Paragraph(
        "Growers lack accessible, rapid, and offline-capable diagnostic tools to identify foliar pathologies before they spread. "
        "There is an acute need for an edge-native, lightweight AI platform that performs sub-30ms offline foliar diagnosis, prescribes immediate scientific remedies, "
        "and automates soil hydration without requiring cloud infrastructure.",
        body_s
    ))

    story.append(Paragraph("D. Objectives", h2_left))
    story.append(Paragraph("• Develop an edge-native foliar pathology classifier operating locally on CPU/ARM hardware with zero cloud dependency.", bullet_s))
    story.append(Paragraph("• Apply INT8 Post-Training Quantization (PTQ) to minimize parameter memory footprint below 3.0 MB.", bullet_s))
    story.append(Paragraph("• Achieve sub-30ms CPU inference latency while maintaining greater than 95% classification accuracy across 38 plant disease classes.", bullet_s))
    story.append(Paragraph("• Engineer an agronomic remediation knowledge base prescribing dual-pathway (bio-organic and chemical fungicide) interventions.", bullet_s))
    story.append(Paragraph("• Construct a closed-loop soil moisture decision engine that automates solenoid irrigation valve actuation and spore risk alerts.", bullet_s))
    story.append(Paragraph("• Deploy the integrated platform as an interactive web application with automated CI/CD testing on GitHub Actions and public cloud hosting.", bullet_s))

    story.append(Paragraph("II. NEED AND SOCIETAL IMPACT", h1_center))
    story.append(Paragraph("A. Need for the Project", h2_left))
    story.append(Paragraph(
        "Farmers need immediate, verifiable treatment protocols to arrest disease progression and protect seasonal investments. AgroEdge AI merges edge vision classification, "
        "evidence-based chemical/biological prescriptions, and automated irrigation management into an intuitive, responsive interface.",
        body_s
    ))

    story.append(Paragraph("B. Societal Impact", h2_left))
    story.append(Paragraph(
        "By eliminating reliance on high-speed cellular infrastructure, AgroEdge AI democratizes access to precision agronomy for rural smallholders. "
        "Precision chemical dosage guidance prevents excessive pesticide runoff, and closed-loop soil irrigation saves up to 40% of agricultural fresh water.",
        body_s
    ))

    story.append(Paragraph("C. Alignment with SDGs", h2_left))
    story.append(Paragraph("• SDG 2 (Zero Hunger): Mitigating crop losses through early foliar disease intervention safeguards food supply chains.", bullet_s))
    story.append(Paragraph("• SDG 6 (Clean Water): Closed-loop soil moisture actuation eliminates excessive irrigation and prevents chemical fertilizer leaching.", bullet_s))
    story.append(Paragraph("• SDG 12 (Responsible Production): Precise fungicide recommendations reduce over-application of synthetic pesticides.", bullet_s))

    story.append(Paragraph("III. DATASET DESCRIPTION", h1_center))
    story.append(Paragraph("A. Sources of Data", h2_left))
    story.append(Paragraph(
        "The computer vision model was trained on the PlantVillage benchmark dataset (Mohanty et al.), coupled with agronomic soil telemetry parameters.",
        body_s
    ))

    story.append(Paragraph("TABLE I<br/>DATA SOURCES", tcap_s))
    t1_data = [
        [Paragraph("No.", th_s), Paragraph("Dataset / Asset Name", th_s), Paragraph("Format & Scale", th_s), Paragraph("Purpose", th_s)],
        [Paragraph("1", td_c), Paragraph("PlantVillage Vision", td_s), Paragraph("54,303 Images (38 Classes)", td_s), Paragraph("Model training", td_s)],
        [Paragraph("2", td_c), Paragraph("Soil Telemetry Data", td_s), Paragraph("Tabular (NPK, Moisture)", td_s), Paragraph("Irrigation logic", td_s)],
        [Paragraph("3", td_c), Paragraph("Agronomic Database", td_s), Paragraph("38 Curated Profiles", td_s), Paragraph("Remedies & dosage", td_s)],
        [Paragraph("4", td_c), Paragraph("Quantized ONNX", td_s), Paragraph("2.56 MB (.onnx)", td_s), Paragraph("Edge model execution", td_s)]
    ]
    t1 = Table(t1_data, colWidths=[18, 80, 75, 71])
    t1.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t1)

    story.append(Paragraph("B. Dataset Size and Features", h2_left))
    story.append(Paragraph(
        "The vision dataset comprises 54,303 annotated leaf images across 14 crops: Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Bell Pepper, Potato, "
        "Raspberry, Soybean, Squash, Strawberry, and Tomato. The dataset covers 26 disease categories and 12 healthy classes (38 classes total).",
        body_s
    ))

    story.append(Paragraph("IV. PREPROCESSING & OPTIMIZATION", h1_center))
    story.append(Paragraph("• Standardization: Images coerced to 3-channel RGB and resized to 224x224 bilinear pixels.", bullet_s))
    story.append(Paragraph("• Normalization: Pixel intensities standardized against ImageNet mean ([0.485, 0.456, 0.406]) and std ([0.229, 0.224, 0.225]).", bullet_s))
    story.append(Paragraph("• Tensor Layout: Permuted to (1, 3, 224, 224) NCHW format for optimal ONNX linear algebra kernels.", bullet_s))
    story.append(Paragraph("• INT8 Quantization: FP32 weights converted into 8-bit integers via symmetric uniform calibration, shrinking size by 75% (14.0MB to 2.56MB) with <0.8% accuracy drop.", bullet_s))

    story.append(Paragraph("V. MODELS AND TECHNOLOGIES", h1_center))
    story.append(Paragraph(
        "Four architectures were evaluated: VGG-16, ResNet-50, MobileNetV2 (FP32), and MobileNetV2 (INT8 Quantized).",
        body_s
    ))

    story.append(Paragraph("TABLE II<br/>MODEL BENCHMARK COMPARISON", tcap_s))
    t2_data = [
        [Paragraph("Model", th_s), Paragraph("Precision", th_s), Paragraph("Size", th_s), Paragraph("Latency", th_s), Paragraph("Top-1 Acc.", th_s)],
        [Paragraph("VGG-16", td_s), Paragraph("FP32", td_c), Paragraph("138 MB", td_c), Paragraph("284 ms", td_c), Paragraph("96.8%", td_c)],
        [Paragraph("ResNet-50", td_s), Paragraph("FP32", td_c), Paragraph("97.5 MB", td_c), Paragraph("142 ms", td_c), Paragraph("97.4%", td_c)],
        [Paragraph("MobileNetV2", td_s), Paragraph("FP32", td_c), Paragraph("14.0 MB", td_c), Paragraph("65 ms", td_c), Paragraph("97.1%", td_c)],
        [Paragraph("AgroEdge AI", td_s), Paragraph("INT8", td_c), Paragraph("2.56 MB", td_c), Paragraph("18 ms", td_c), Paragraph("96.4%", td_c)]
    ]
    t2 = Table(t2_data, colWidths=[55, 45, 48, 48, 48])
    t2.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t2)

    story.append(Paragraph("A. Selected Deep Learning Model", h2_left))
    story.append(Paragraph(
        "MobileNetV2 INT8 Quantized was selected because it achieved the lowest recorded latency (18 ms) and smallest footprint (2.56 MB) while maintaining 96.4% top-1 accuracy. "
        "The selection is based on edge energy efficiency and real-time execution capability.",
        body_s
    ))

    story.append(Paragraph("B. Technologies Used", h2_left))
    story.append(Paragraph("TABLE III<br/>TECHNOLOGIES USED", tcap_s))
    t3_data = [
        [Paragraph("Component", th_s), Paragraph("Technology", th_s), Paragraph("Purpose", th_s)],
        [Paragraph("Programming", td_s), Paragraph("Python 3.11+", td_s), Paragraph("Application logic", td_s)],
        [Paragraph("Edge Engine", td_s), Paragraph("ONNX Runtime", td_s), Paragraph("Quantized INT8 inference", td_s)],
        [Paragraph("Image Proc.", td_s), Paragraph("Pillow, NumPy", td_s), Paragraph("Image normalization", td_s)],
        [Paragraph("Frontend", td_s), Paragraph("Streamlit v1.56", td_s), Paragraph("Interactive UI & camera", td_s)],
        [Paragraph("Data Viz", td_s), Paragraph("Pandas, Altair", td_s), Paragraph("Telemetry curves", td_s)],
        [Paragraph("Deployment", td_s), Paragraph("Streamlit Cloud", td_s), Paragraph("Global web hosting", td_s)]
    ]
    t3 = Table(t3_data, colWidths=[65, 75, 104])
    t3.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t3)

    story.append(Paragraph("VI. METHODOLOGY & ARCHITECTURE", h1_center))
    story.append(Paragraph("A. Working of the System", h2_left))
    story.append(Paragraph("1. User captures leaf photo via camera or file upload.", bullet_s))
    story.append(Paragraph("2. Preprocessor normalizes tensor to (1, 3, 224, 224).", bullet_s))
    story.append(Paragraph("3. Quantized ONNX MobileNet executes inference in 18 ms.", bullet_s))
    story.append(Paragraph("4. Softmax extracts disease class & confidence %.", bullet_s))
    story.append(Paragraph("5. Agronomic engine prescribes organic & chemical remedies.", bullet_s))
    story.append(Paragraph("6. Moisture logic (<30%) actuates virtual solenoid valve.", bullet_s))
    story.append(Paragraph("7. Dashboard renders diagnosis and telemetry curves.", bullet_s))

    story.append(Paragraph("VII. IMPLEMENTATION DETAILS", h1_center))
    story.append(Paragraph(
        "The application is structured into modular packages: app.py (frontend), src/classifier.py (ONNX wrapper), src/remedies.py (agronomic DB), "
        "and src/soil_advisor.py (closed-loop irrigation). The platform is deployed live at https://agroedgeai.streamlit.app with source code version-controlled at "
        "https://github.com/rishu295/AgroEdge-AI.",
        body_s
    ))

    story.append(Paragraph("VIII. RESULTS AND EVALUATION", h1_center))
    story.append(Paragraph("TABLE IV<br/>RECORDED PERFORMANCE RESULTS", tcap_s))
    t4_data = [
        [Paragraph("Metric", th_s), Paragraph("Target", th_s), Paragraph("Recorded", th_s), Paragraph("Verdict", th_s)],
        [Paragraph("Top-1 Accuracy", td_s), Paragraph("> 95.0%", td_c), Paragraph("96.4%", td_c), Paragraph("Met", td_c)],
        [Paragraph("CPU Latency", td_s), Paragraph("< 30 ms", td_c), Paragraph("18.2 ms", td_c), Paragraph("Met", td_c)],
        [Paragraph("Model Size", td_s), Paragraph("< 5.0 MB", td_c), Paragraph("2.56 MB", td_c), Paragraph("Met", td_c)],
        [Paragraph("Offline Resilience", td_s), Paragraph("100%", td_c), Paragraph("0 Cloud Calls", td_c), Paragraph("Met", td_c)],
        [Paragraph("Actuation Speed", td_s), Paragraph("< 100 ms", td_c), Paragraph("< 2 ms", td_c), Paragraph("Met", td_c)]
    ]
    t4 = Table(t4_data, colWidths=[75, 55, 64, 50])
    t4.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t4)

    story.append(Paragraph("IX. COMPARISON WITH OTHER APPROACHES", h1_center))
    story.append(Paragraph("TABLE V<br/>COMPARISON OF APPROACHES", tcap_s))
    t5_data = [
        [Paragraph("Approach", th_s), Paragraph("Strengths", th_s), Paragraph("Limitations", th_s)],
        [Paragraph("Manual Scouting", td_s), Paragraph("Expert inspection", td_s), Paragraph("Slow, subjective, costly", td_s)],
        [Paragraph("Cloud AI APIs", td_s), Paragraph("Heavy server models", td_s), Paragraph("Fails offline; data fees", td_s)],
        [Paragraph("Satellite Sensing", td_s), Paragraph("Macro regional view", td_s), Paragraph("Cannot resolve spots", td_s)],
        [Paragraph("Uncompressed CNN", td_s), Paragraph("High raw accuracy", td_s), Paragraph("Heavy (>100MB), heat", td_s)],
        [Paragraph("AgroEdge AI (Ours)", td_s), Paragraph("18ms offline, 2.56MB", td_s), Paragraph("Needs clear framing", td_s)]
    ]
    t5 = Table(t5_data, colWidths=[65, 85, 94])
    t5.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t5)

    story.append(Paragraph("X. INDIVIDUAL CONTRIBUTION", h1_center))
    story.append(Paragraph(
        "The project work covered problem formulation, dataset preparation, MobileNet transfer learning, INT8 Post-Training Quantization, "
        "ONNX Runtime optimization, agronomic prescription engine design, closed-loop soil moisture logic, Streamlit web development, "
        "CI/CD configuration on GitHub Actions, cloud deployment, and report compilation.",
        body_s
    ))

    story.append(Paragraph("XI. LIMITATIONS", h1_center))
    story.append(Paragraph("• Laboratory background bias in PlantVillage may slightly reduce field performance under complex background weed clutter.", bullet_s))
    story.append(Paragraph("• Evaluates single leaves rather than full-canopy aerial imagery.", bullet_s))
    story.append(Paragraph("• Provides point-estimate softmax probabilities rather than Bayesian uncertainty distributions.", bullet_s))
    story.append(Paragraph("• Moisture thresholds (30%-60%) reflect general loamy soils and may need tuning for sand or clay.", bullet_s))
    story.append(Paragraph("• Static prescription rules do not dynamically adapt to newly emerging resistant strains.", bullet_s))

    story.append(Paragraph("XII. FUTURE SCOPE", h1_center))
    story.append(Paragraph("• Integrate YOLOv11-Nano object detection for multi-leaf bounding box segmentation in video streams.", bullet_s))
    story.append(Paragraph("• Deploy ONNX model onto physical Raspberry Pi 5 / ESP32-CAM wired to 12V solenoid relays.", bullet_s))
    story.append(Paragraph("• Add LoRaWAN mesh networking for long-range (10 km) sensor telemetry.", bullet_s))
    story.append(Paragraph("• Integrate multilingual audio voice assistance for smallholder farmers.", bullet_s))

    story.append(Paragraph("XIII. CONCLUSION", h1_center))
    story.append(Paragraph(
        "AgroEdge AI successfully demonstrates an end-to-end Edge AI platform for foliar pathology and smart precision irrigation. "
        "By compressing MobileNet via INT8 Post-Training Quantization into an ONNX graph, the system achieves a 2.56 MB footprint (75% compression) "
        "and an ultra-fast 18 ms inference latency while retaining 96.4% accuracy across 38 classes. Integrated with closed-loop irrigation actuation "
        "and public web deployment, AgroEdge AI proves that AI can operate reliably and offline to support global agricultural resilience.",
        body_s
    ))

    story.append(Paragraph("REFERENCES", h1_center))
    refs = [
        "[1] S. P. Mohanty, D. P. Hughes, and M. Salathé, “Using deep learning for image-based plant disease detection,” Frontiers in Plant Science, vol. 7, p. 1419, 2016.",
        "[2] M. Sandler et al., “MobileNetV2: Inverted residuals and linear bottlenecks,” in Proc. CVPR, 2018, pp. 4510–4520.",
        "[3] B. Jacob et al., “Quantization and training of neural networks for efficient integer-arithmetic-only inference,” in Proc. CVPR, 2018, pp. 2704–2713.",
        "[4] Microsoft Corporation, “ONNX Runtime: Cross-platform ML accelerator,” [Online]. Available: https://onnxruntime.ai/",
        "[5] Food and Agriculture Organization (FAO), “The state of food and agriculture,” Rome, Italy, 2019.",
        "[6] Streamlit Documentation, “Build and share data apps,” [Online]. Available: https://docs.streamlit.io/"
    ]
    for r in refs:
        story.append(Paragraph(r, bullet_s))

    doc.build(story, canvasmaker=IEEETwoColCanvas)
    print(f"IEEE Two-Column PDF successfully generated: {filename}")

if __name__ == "__main__":
    build_ieee_pdf()
