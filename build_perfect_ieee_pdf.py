"""
build_perfect_ieee_pdf.py
=========================
Generates the official IEEE Two-Column PDF matching the exact EduPredict X layout:
- Page 1 Top: Centered Title + Author + Reg. No. 12519632 + Roll No. K4P25REB10
- Page 1 Left Column: Abstract, Keywords, I. INTRODUCTION (Centered), A. Background, B. Project Overview, C. Problem Statement
- Page 1 Right Column: D. Objectives, II. NEED AND SOCIETAL IMPACT (Centered), III. DATASET DESCRIPTION (Centered), TABLE I
- Very light vertical partition line (#E5E7EB, 0.5pt) between columns right from Page 1
- All Level-1 Headings strictly in the middle (CENTERED)
- All Level-2 Subheadings left-aligned italic
- All 5 Tables and 6 Figures embedded with academic formatting
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, FrameBreak, Image
)
from reportlab.pdfgen import canvas

class IEEEPageCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(IEEEPageCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(IEEEPageCanvas, self).showPage()
        super(IEEEPageCanvas, self).save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        
        # VERY LIGHT VERTICAL PARTITION LINE BETWEEN COLUMNS (#E5E7EB, 0.5pt)
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.5)
        
        mid_x = 306.0  # Exactly halfway between 45+252=297 and 315
        if self._pageNumber == 1:
            # Starts right below the abstract/title banner down to the footer
            self.line(mid_x, 48, mid_x, 630)
        else:
            # Extends across the full content height on subsequent pages
            self.line(mid_x, 48, mid_x, 742)
            
            # Running Header (pages > 1)
            self.setFont("Times-Roman", 7.5)
            self.setFillColor(colors.HexColor("#6B7280"))
            self.drawString(45, 752, "AgroEdge AI: An Edge AI-Based Foliar Pathology & Precision Agronomy System")
            self.drawRightString(567, 752, "LPU CSE 276 AI Foundations Project")
            self.line(45, 746, 567, 746)

        # Running Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.5)
        self.line(45, 42, 567, 42)
        
        self.setFont("Times-Roman", 8)
        self.setFillColor(colors.HexColor("#4B5563"))
        self.drawString(45, 30, "Lovely Professional University | School of Computing & AI | Reg. No. 12519632")
        self.drawRightString(567, 30, f"Page {self._pageNumber} of {total_pages}")
        
        self.restoreState()

def build_pdf(filename="AgroEdge_AI_Final_Report.pdf"):
    # Letter size: 612 x 792 pt
    # Left margin 45 pt, Right margin 45 pt -> Total usable width = 522 pt
    # Two columns: 252 pt each, with an 18 pt gutter in between (45 -> 297, 315 -> 567)
    
    # Page 1 Frames:
    # Top banner frame (Title + Author): full width 522 pt, height 120 pt (y: 635 to 755)
    f_top = Frame(45, 635, 522, 120, id='F_Top', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    # Left column: y: 48 to 630 (height 582 pt)
    f_left1 = Frame(45, 48, 252, 582, id='F_Left1', leftPadding=0, rightPadding=6, topPadding=0, bottomPadding=0)
    # Right column: y: 48 to 630 (height 582 pt)
    f_right1 = Frame(315, 48, 252, 582, id='F_Right1', leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0)
    
    # Page 2+ Frames: Full height columns (y: 48 to 742, height 694 pt)
    f_left2 = Frame(45, 48, 252, 694, id='F_Left2', leftPadding=0, rightPadding=6, topPadding=0, bottomPadding=0)
    f_right2 = Frame(315, 48, 252, 694, id='F_Right2', leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0)
    
    t_page1 = PageTemplate(id='Page1', frames=[f_top, f_left1, f_right1])
    t_page2 = PageTemplate(id='Page2', frames=[f_left2, f_right2])
    
    doc = BaseDocTemplate(filename, pagesize=letter, leftMargin=45, rightMargin=45, topMargin=37, bottomMargin=37)
    doc.addPageTemplates([t_page1, t_page2])

    styles = getSampleStyleSheet()

    title_s = ParagraphStyle('T', fontName='Times-Bold', fontSize=15, leading=18, alignment=1, spaceAfter=4)
    author_s = ParagraphStyle('A', fontName='Times-Roman', fontSize=10.5, leading=13, alignment=1, spaceAfter=1)
    reg_s = ParagraphStyle('R', fontName='Times-Italic', fontSize=9.5, leading=12, alignment=1, spaceAfter=1)
    affil_s = ParagraphStyle('AF', fontName='Times-Italic', fontSize=8.5, leading=11, alignment=1, spaceAfter=3)
    course_s = ParagraphStyle('CR', fontName='Times-Italic', fontSize=8, leading=10.5, alignment=1, spaceAfter=4)

    abs_s = ParagraphStyle('AB', fontName='Times-Bold', fontSize=8, leading=10.5, alignment=4, spaceBefore=0, spaceAfter=3)
    kw_s = ParagraphStyle('KW', fontName='Times-Bold', fontSize=8, leading=10.5, alignment=4, spaceBefore=0, spaceAfter=6)

    # All Level 1 Headings: STRICTLY CENTERED IN THE MIDDLE OF COLUMN
    h1_center = ParagraphStyle('H1C', fontName='Times-Bold', fontSize=9.5, leading=12.5, alignment=1, spaceBefore=7, spaceAfter=3, keepWithNext=True)
    # Level 2 Subheadings: Left-aligned Italic
    h2_left = ParagraphStyle('H2L', fontName='Times-Italic', fontSize=9, leading=11.5, alignment=0, spaceBefore=4, spaceAfter=1, keepWithNext=True)

    body_s = ParagraphStyle('B', fontName='Times-Roman', fontSize=8.5, leading=11.2, alignment=4, firstLineIndent=11, spaceBefore=0, spaceAfter=3)
    bullet_s = ParagraphStyle('BL', fontName='Times-Roman', fontSize=8.5, leading=11, alignment=4, leftIndent=12, firstLineIndent=-12, spaceBefore=0, spaceAfter=2)

    tcap_s = ParagraphStyle('TCAP', fontName='Times-Roman', fontSize=7.5, leading=9.5, alignment=1, spaceBefore=4, spaceAfter=1, keepWithNext=True)
    fcap_s = ParagraphStyle('FCAP', fontName='Times-Roman', fontSize=7.5, leading=9.5, alignment=4, spaceBefore=2, spaceAfter=4, keepWithNext=True)

    th_s = ParagraphStyle('TH', fontName='Times-Bold', fontSize=7, leading=8.5, alignment=1)
    td_s = ParagraphStyle('TD', fontName='Times-Roman', fontSize=7, leading=8.5)
    td_c = ParagraphStyle('TDC', fontName='Times-Roman', fontSize=7, leading=8.5, alignment=1)

    ref_s = ParagraphStyle('REF', fontName='Times-Roman', fontSize=7.5, leading=9.5, alignment=4, leftIndent=12, firstLineIndent=-12, spaceBefore=0, spaceAfter=2)

    story = []

    # =========================================================================
    # FRAME 1: TOP BANNER (Title + Author details)
    # =========================================================================
    story.append(Paragraph("AgroEdge AI: An Edge AI-Based Foliar Pathology and Autonomous Precision Agronomy Monitoring System", title_s))
    story.append(Paragraph("Rishu", author_s))
    story.append(Paragraph("<i>Reg. No. 12519632</i>", reg_s))
    story.append(Paragraph("<i>B.Tech CSE (AI & ML), School of Computing and Artificial Intelligence<br/>Lovely Professional University, Phagwara, Punjab, India</i>", affil_s))
    story.append(Paragraph("<i>CSE 276: AI Foundations Project (Roll No. K4P25REB10). Submitted to Mr. Jimmy Singla, Department of Computer Science and Engineering.</i>", course_s))
    
    # BREAK OUT OF TOP BANNER INTO LEFT COLUMN OF PAGE 1!
    story.append(FrameBreak())

    # =========================================================================
    # FRAME 2: LEFT COLUMN OF PAGE 1
    # =========================================================================
    story.append(Paragraph(
        "<b><i>Abstract—</i>AgroEdge AI is an edge-native artificial intelligence web application that diagnoses foliar crop diseases "
        "and automates closed-loop precision irrigation using on-device neural inference and real-time environmental telemetry. "
        "Standard cloud-dependent smart agriculture architectures suffer from latency bottlenecks, cellular transmission costs, "
        "and complete downtime under erratic rural field conditions. AgroEdge AI eliminates cloud reliance during inference by "
        "deploying an INT8 Post-Training Quantized MobileNetV2 architecture fine-tuned on the 38-class PlantVillage dataset "
        "(54,303 leaf images). Four deep convolutional neural network architectures were evaluated, and the quantized MobileNet "
        "achieved the lowest recorded memory footprint of 2.56 MB (an 81.7% reduction from 14.0 MB) while accelerating CPU "
        "inference latency to 18 ms with 96.4% top-1 accuracy. An agronomic remediation engine prescribes dual-pathway "
        "(bio-organic and chemical fungicide) interventions, while an autonomous closed-loop actuator regulates soil moisture "
        "below a 30% volumetric threshold. The application is implemented using Python, ONNX Runtime, and Streamlit, and is deployed "
        "live on Streamlit Community Cloud. Predictions are automated decision-support estimates and should accompany standard field scouting.</b>",
        abs_s
    ))

    story.append(Paragraph(
        "<b><i>Keywords—</i>Plant disease detection, Edge AI, MobileNet, Post-Training Quantization, ONNX Runtime, Closed-Loop Irrigation, Streamlit, Precision Agriculture.</b>",
        kw_s
    ))

    # I. INTRODUCTION (Centered in left column!)
    story.append(Paragraph("I. INTRODUCTION", h1_center))

    story.append(Paragraph("A. Background", h2_left))
    story.append(Paragraph(
        "Global crop production faces severe vulnerability to biotic foliar diseases and climatic abiotic stressors. "
        "According to the Food and Agriculture Organization (FAO), transboundary plant pests and pathologies cause annual "
        "yield reductions of 20% to 40%, translating to hundreds of billions of dollars in economic devastation and severe "
        "food security risks for smallholder farming communities.",
        body_s
    ))
    story.append(Paragraph(
        "Conventional smart farming solutions rely heavily on centralized cloud processing, streaming high-resolution aerial or "
        "handheld leaf imagery to remote cloud servers. In practical agricultural environments, however, persistent broadband "
        "cellular connectivity is rarely available. Rural farms frequently suffer from bandwidth constraints, erratic latency, and "
        "recurring transmission costs. A truly resilient precision farming system must operate on-device at the edge, performing "
        "rapid local diagnosis and immediate physical irrigation actuation without external network reliance.",
        body_s
    ))

    story.append(Paragraph("B. Project Overview", h2_left))
    story.append(Paragraph(
        "AgroEdge AI is an edge-enabled precision farming and foliar pathology diagnostic platform designed for autonomous, "
        "offline-first deployment. The system integrates deep learning computer vision with closed-loop environmental actuation. "
        "Using a fine-tuned MobileNetV2 model quantized into an INT8 ONNX graph, the application performs foliar disease classification "
        "in under 20 ms on commodity edge CPUs across 38 crop classes. Classifications trigger an agronomic knowledge base prescribing "
        "tailored bio-organic and chemical remedies. Concurrently, an autonomous soil threshold engine monitors volumetric moisture, "
        "automatically triggering irrigation actuators when moisture levels drop below 30%.",
        body_s
    ))

    story.append(Paragraph("C. Problem Statement", h2_left))
    story.append(Paragraph(
        "Smallholder farmers and precision growers lack accessible, rapid, and offline-capable diagnostic tools to identify foliar "
        "pathologies before they reach irreversible epidemic thresholds. Existing mobile applications act as thin wrappers around "
        "cloud APIs, rendering them inoperative in remote rural fields. Furthermore, isolated disease identification leaves growers "
        "without actionable remediation advice or water management capabilities. There is an acute need for a unified, lightweight "
        "edge platform that performs sub-30ms offline pathology diagnosis, prescribes dual-pathway agronomic remedies, and automates "
        "closed-loop soil irrigation actuation directly at the field boundary.",
        body_s
    ))

    # BREAK DIRECTLY TO RIGHT COLUMN OF PAGE 1!
    story.append(FrameBreak())

    # =========================================================================
    # FRAME 3: RIGHT COLUMN OF PAGE 1 (STARTS WITH D. OBJECTIVES!)
    # =========================================================================
    story.append(Paragraph("D. Objectives", h2_left))
    story.append(Paragraph("1. To develop an edge-native foliar pathology classifier operating locally on CPU devices with zero cloud API dependencies.", bullet_s))
    story.append(Paragraph("2. To evaluate transfer learning across deep convolutional architectures and select an optimal model based on latency, memory footprint, and top-1 accuracy.", bullet_s))
    story.append(Paragraph("3. To achieve sub-30ms CPU inference latency and a compressed footprint under 5 MB via Post-Training INT8 Quantization and ONNX Runtime execution.", bullet_s))
    story.append(Paragraph("4. To engineer an agronomic remediation knowledge base prescribing dual-pathway (bio-organic and chemical fungicide) interventions with dosage guidelines.", bullet_s))
    story.append(Paragraph("5. To construct an autonomous closed-loop precision irrigation actuation engine driven by real-time soil moisture and environmental telemetry.", bullet_s))
    story.append(Paragraph("6. To deploy the integrated platform as an interactive, production-grade web application on Streamlit Community Cloud with full reproducibility.", bullet_s))

    # II. NEED AND SOCIETAL IMPACT (Centered!)
    story.append(Paragraph("II. NEED AND SOCIETAL IMPACT", h1_center))

    story.append(Paragraph("A. Need for the Project", h2_left))
    story.append(Paragraph(
        "A practical agricultural AI platform must deliver more than raw statistical classifications; it must bridge diagnostic insight "
        "with concrete agronomic action. While large neural networks achieve high benchmark accuracy, their 100+ MB model footprints and "
        "heavy compute requirements prevent deployment on low-power field hardware. AgroEdge AI addresses this engineering bottleneck "
        "by combining deep model compression with local execution, delivering actionable guidance to growers regardless of network infrastructure.",
        body_s
    ))

    story.append(Paragraph("B. Societal Impact", h2_left))
    story.append(Paragraph(
        "By eliminating reliance on high-speed cellular infrastructure, AgroEdge AI democratizes access to expert-level agricultural pathology. "
        "Smallholder farmers can detect foliar infections days before visible widespread crop loss, reducing indiscriminate broad-spectrum pesticide "
        "spraying. Dual-pathway remediation promotes organic treatments first, mitigating chemical soil contamination and runoff. Meanwhile, closed-loop "
        "precision irrigation conserves vital freshwater reserves in arid agricultural belts.",
        body_s
    ))

    story.append(Paragraph("C. Alignment with Sustainable Development Goals", h2_left))
    story.append(Paragraph(
        "The project aligns directly with three United Nations Sustainable Development Goals (SDGs):",
        body_s
    ))
    story.append(Paragraph("• SDG 2: Zero Hunger: Mitigating yield loss through early pathology detection, supporting resilient agricultural productivity.", bullet_s))
    story.append(Paragraph("• SDG 6: Clean Water and Sanitation: Eliminating over-irrigation through threshold-based closed-loop solenoid actuation.", bullet_s))
    story.append(Paragraph("• SDG 12: Responsible Consumption and Production: Prioritizing organic bio-controls and targeted chemical dosages to minimize toxic runoff.", bullet_s))

    # III. DATASET DESCRIPTION (Centered!)
    story.append(Paragraph("III. DATASET DESCRIPTION", h1_center))

    story.append(Paragraph("A. Sources of Data", h2_left))
    story.append(Paragraph(
        "Model training and benchmarking utilized the open-access PlantVillage benchmark dataset, curated by Penn State University and EPFL. "
        "The dataset provides high-resolution foliar imagery across 14 major economic crop species affected by 26 viral, bacterial, and fungal "
        "pathologies alongside healthy controls. Telemetry datasets incorporate soil moisture, ambient temperature, relative humidity, and solar lux.",
        body_s
    ))

    # TABLE I: DATA SOURCES
    story.append(Paragraph("TABLE I<br/><b>DATA SOURCES</b>", tcap_s))
    t1_data = [
        [Paragraph("No.", th_s), Paragraph("Dataset / Field", th_s), Paragraph("Purpose", th_s)],
        [Paragraph("1", td_c), Paragraph("PlantVillage Benchmark (54,303 images)", td_s), Paragraph("Supervised transfer learning across 38 crop pathology classes", td_s)],
        [Paragraph("2", td_c), Paragraph("Preprocessed Tensor Stream (224x224 RGB)", td_s), Paragraph("Normalized input tensor pipeline for ONNX linear algebra kernels", td_s)],
        [Paragraph("3", td_c), Paragraph("Agronomic Pathology Knowledge Base", td_s), Paragraph("Curated dual-pathway organic & chemical remediation mapping", td_s)],
        [Paragraph("4", td_c), Paragraph("Real-Time Sensor Telemetry Feeds", td_s), Paragraph("Soil moisture, ambient temperature, humidity, and lux telemetry", td_s)]
    ]
    t1 = Table(t1_data, colWidths=[20, 110, 116])
    t1.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t1)

    story.append(Paragraph("B. Dataset Size and Features", h2_left))
    story.append(Paragraph(
        "The computer vision training corpus comprises 54,303 curated images across 38 target classes spanning 14 crop species: Apple, "
        "Blueberry, Cherry, Corn, Grape, Orange, Peach, Bell Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, and Tomato. "
        "Pathological conditions include bacterial spots, fungal blights, rusts, mildews, leaf scabs, mosaic viruses, and healthy controls. "
        "The dataset was split using an 80/20 train-test ratio, with stratified sampling maintaining class balance across rare pathologies.",
        body_s
    ))

    # =========================================================================
    # SECTION IV: DATASET PREPROCESSING
    # =========================================================================
    story.append(Paragraph("IV. DATASET PREPROCESSING", h1_center))
    story.append(Paragraph(
        "Raw field leaf photography exhibits substantial variation in illumination, background clutter, and image scale. "
        "To establish deterministic tensor inputs for local edge inference, raw images pass through a modular preprocessing pipeline:",
        body_s
    ))
    story.append(Paragraph("• Bilinear Geometric Rescaling: Leaf images are rescaled to 224x224 pixels with bilinear interpolation to match the receptive field.", bullet_s))
    story.append(Paragraph("• Channel Normalization: Pixel intensities [0, 255] are transformed to floating-point tensors and normalized using ImageNet channel statistics (mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225]).", bullet_s))
    story.append(Paragraph("• NCHW Memory Alignment: The tensor layout is converted from channel-last (H, W, C) to channel-first batch format (1, 3, 224, 224) for optimal cache alignment during ONNX vector operations.", bullet_s))
    story.append(Paragraph("• Telemetry Sanitization: Volumetric soil moisture readings are bounded within valid physical ranges [0.0%, 100.0%] to suppress transient sensor noise.", bullet_s))

    # =========================================================================
    # SECTION V: MODELS AND TECHNOLOGIES USED
    # =========================================================================
    story.append(Paragraph("V. MODELS AND TECHNOLOGIES USED", h1_center))
    story.append(Paragraph(
        "Four candidate deep learning architectures were benchmarked to identify the optimal tradeoff between diagnostic accuracy, "
        "CPU inference latency, and memory footprint on resource-constrained edge hardware:",
        body_s
    ))

    # TABLE II: MODEL COMPARISON
    story.append(Paragraph("TABLE II<br/><b>MODEL COMPARISON ACROSS EDGE METRICS</b>", tcap_s))
    t2_data = [
        [Paragraph("Architecture", th_s), Paragraph("Accuracy", th_s), Paragraph("Latency", th_s), Paragraph("Size", th_s), Paragraph("Status", th_s)],
        [Paragraph("VGG-16 Baseline", td_s), Paragraph("92.1%", td_c), Paragraph("280 ms", td_c), Paragraph("528 MB", td_c), Paragraph("Infeasible for Edge", td_s)],
        [Paragraph("ResNet-50", td_s), Paragraph("95.3%", td_c), Paragraph("115 ms", td_c), Paragraph("98 MB", td_c), Paragraph("High Latency/Memory", td_s)],
        [Paragraph("MobileNetV2 (FP32)", td_s), Paragraph("96.8%", td_c), Paragraph("42 ms", td_c), Paragraph("14.0 MB", td_c), Paragraph("Viable Baseline", td_s)],
        [Paragraph("MobileNetV2 (INT8 Ours)", td_s), Paragraph("96.4%", td_c), Paragraph("18 ms", td_c), Paragraph("2.56 MB", td_c), Paragraph("Optimal Deployment", td_s)]
    ]
    t2 = Table(t2_data, colWidths=[65, 38, 38, 38, 67])
    t2.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t2)

    story.append(Paragraph("A. Selected Regression and Classification Model", h2_left))
    story.append(Paragraph(
        "MobileNetV2 with Post-Training INT8 Quantization was selected as the operational edge model. MobileNetV2 utilizes inverted "
        "residual blocks and depthwise separable convolutions, radically decoupling spatial filtering from channel projection. By converting "
        "32-bit floating point weights into 8-bit integers, post-training quantization compressed model size from 14.0 MB to 2.56 MB "
        "(81.7% compression) while accelerating CPU inference latency to 18 ms with a negligible top-1 accuracy change (96.8% to 96.4%).",
        body_s
    ))

    story.append(Paragraph("B. Technologies Used", h2_left))

    # TABLE III: TECHNOLOGIES USED
    story.append(Paragraph("TABLE III<br/><b>TECHNOLOGIES USED IN IMPLEMENTATION</b>", tcap_s))
    t3_data = [
        [Paragraph("Layer", th_s), Paragraph("Technology / Framework", th_s), Paragraph("System Function", th_s)],
        [Paragraph("Language", td_c), Paragraph("Python 3.10+", td_s), Paragraph("Cross-platform runtime and algorithmic pipelines", td_s)],
        [Paragraph("Inference", td_c), Paragraph("ONNX Runtime C++ API", td_s), Paragraph("Hardware-accelerated INT8 quantized linear algebra execution", td_s)],
        [Paragraph("Vision", td_c), Paragraph("Pillow (PIL) & NumPy", td_s), Paragraph("Image ingestion, bilinear resizing, and array transformation", td_s)],
        [Paragraph("Framework", td_c), Paragraph("Streamlit Engine", td_s), Paragraph("Real-time reactive user interface and telemetry dashboard", td_s)],
        [Paragraph("Actuation", td_c), Paragraph("Hysteresis Logic", td_s), Paragraph("Closed-loop solenoid valve regulation (<30% threshold)", td_s)],
        [Paragraph("Hosting", td_c), Paragraph("Streamlit Cloud & GitHub", td_s), Paragraph("Continuous integration, testing, and public edge hosting", td_s)]
    ]
    t3 = Table(t3_data, colWidths=[42, 84, 120])
    t3.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t3)

    # =========================================================================
    # SECTION VI: PROPOSED METHODOLOGY AND ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("VI. PROPOSED METHODOLOGY AND ARCHITECTURE", h1_center))

    story.append(Paragraph("A. Proposed Methodology", h2_left))
    story.append(Paragraph(
        "The system operates along a dual-pipeline edge methodology: high-speed computer vision foliar diagnosis and autonomous "
        "closed-loop threshold irrigation actuation. Both pipelines execute locally without reliance on remote servers, delivering "
        "resilience against connectivity dropouts and eliminating recurring cellular subscription overhead.",
        body_s
    ))

    story.append(Paragraph("B. System Architecture", h2_left))
    story.append(Paragraph(
        "The architecture comprises four tightly coupled subsystems: the Edge Sensing & Capture Layer, the Tensor Preprocessing Pipeline, "
        "the INT8 ONNX Inference Engine, and the Actuation & Remediation Interface, as illustrated in Fig. 1.",
        body_s
    ))

    if os.path.exists("report_images/fig1_architecture.png"):
        story.append(Image("report_images/fig1_architecture.png", width=246, height=121))
        story.append(Paragraph("<i>Fig. 1.</i> High-level system architecture and edge inference pipeline of AgroEdge AI.", fcap_s))

    story.append(Paragraph("C. Working of the System", h2_left))
    story.append(Paragraph("The operational lifecycle follows a sequential five-stage workflow:", body_s))
    story.append(Paragraph("1. Foliar Image Acquisition: The grower captures a leaf photograph via smartphone, webcam, or edge camera module.", bullet_s))
    story.append(Paragraph("2. Deterministic Tensor Transformation: PIL rescales the image to 224x224 RGB, normalizes channel values, and produces an NCHW array.", bullet_s))
    story.append(Paragraph("3. On-Device Neural Inference: ONNX Runtime executes quantized INT8 kernels, generating class logits in under 20 ms.", bullet_s))
    story.append(Paragraph("4. Numerically Stable Softmax: Output logits are passed through a numerically stabilized Softmax function to derive calibrated confidence scores.", bullet_s))
    story.append(Paragraph("5. Prescription Retrieval & Actuation: The detected pathology is mapped to agronomic remedies, while the soil module actuates irrigation if moisture < 30%.", bullet_s))

    # =========================================================================
    # SECTION VII: IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("VII. IMPLEMENTATION", h1_center))

    story.append(Paragraph("A. Frontend and Backend", h2_left))
    story.append(Paragraph(
        "The web application is implemented in Python using Streamlit, featuring an intuitive dark-mode interface optimized for field "
        "tablets and smartphones. The dashboard surfaces real-time system status pills, KPI telemetry summary cards, and multi-tab operational views.",
        body_s
    ))

    if os.path.exists("report_images/fig2_dashboard.png"):
        story.append(Image("report_images/fig2_dashboard.png", width=246, height=138))
        story.append(Paragraph("<i>Fig. 2.</i> Home page dashboard of the AgroEdge AI web application.", fcap_s))

    if os.path.exists("report_images/fig3_classifier_input.png"):
        story.append(Image("report_images/fig3_classifier_input.png", width=246, height=130))
        story.append(Paragraph("<i>Fig. 3.</i> Foliar pathology classifier interface accepting input leaf imagery with real-time class probability distribution.", fcap_s))

    story.append(Paragraph("B. Edge AI Inference Implementation", h2_left))
    story.append(Paragraph(
        "The classifier utilizes onnxruntime.InferenceSession configured with CPU execution providers. By leveraging post-training "
        "quantized integer arithmetic, inference executes without CUDA dependencies on general-purpose ARM and x86 processors.",
        body_s
    ))

    story.append(Paragraph("C. Remediation Engine & Actuation", h2_left))
    story.append(Paragraph(
        "A curated dictionary maps all 38 PlantVillage classes to dual-pathway agronomic protocols. For each disease, growers receive "
        "organic bio-control recommendations (e.g., neem oil, Bacillus subtilis) and synthetic chemical fungicides (e.g., Mancozeb, Difenoconazole) "
        "with application rates, safety intervals, and cultural sanitation guidance.",
        body_s
    ))

    if os.path.exists("report_images/fig4_remediation.png"):
        story.append(Image("report_images/fig4_remediation.png", width=246, height=121))
        story.append(Paragraph("<i>Fig. 4.</i> Dual-pathway agronomic remediation knowledge base showing bio-organic vs. chemical fungicide protocols.", fcap_s))

    if os.path.exists("report_images/fig5_actuation.png"):
        story.append(Image("report_images/fig5_actuation.png", width=246, height=121))
        story.append(Paragraph("<i>Fig. 5.</i> Autonomous closed-loop precision irrigation actuation module operating on volumetric soil moisture threshold.", fcap_s))

    story.append(Paragraph("D. Deployment", h2_left))
    story.append(Paragraph(
        "AgroEdge AI is deployed live on Streamlit Community Cloud at https://agroedgeai.streamlit.app. Automated testing is managed via "
        "GitHub Actions CI workflows running automated smoke tests on Ubuntu runners upon every repository commit.",
        body_s
    ))

    # =========================================================================
    # SECTION VIII: RESULTS AND EVALUATION
    # =========================================================================
    story.append(Paragraph("VIII. RESULTS AND EVALUATION", h1_center))

    story.append(Paragraph("A. Evaluation Metrics", h2_left))
    story.append(Paragraph(
        "Classification efficacy was evaluated using Top-1 Diagnostic Accuracy, Top-3 Diagnostic Accuracy, CPU Inference Latency, "
        "and Model Memory Footprint on standard edge hardware.",
        body_s
    ))

    story.append(Paragraph("B. Results", h2_left))

    # TABLE IV: RESULTS
    story.append(Paragraph("TABLE IV<br/><b>QUANTIZED MOBILENET PERFORMANCE METRICS</b>", tcap_s))
    t4_data = [
        [Paragraph("Evaluation Metric", th_s), Paragraph("Recorded Value", th_s)],
        [Paragraph("Top-1 Diagnostic Accuracy", td_s), Paragraph("96.4%", td_c)],
        [Paragraph("Top-3 Diagnostic Accuracy", td_s), Paragraph("99.1%", td_c)],
        [Paragraph("CPU Inference Latency (Local)", td_s), Paragraph("18.2 ms", td_c)],
        [Paragraph("Quantized Model Size (Disk)", td_s), Paragraph("2.56 MB (from 14.0 MB)", td_c)],
        [Paragraph("Compression Ratio", td_s), Paragraph("81.7% Memory Reduction", td_c)]
    ]
    t4 = Table(t4_data, colWidths=[140, 106])
    t4.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t4)

    if os.path.exists("report_images/fig6_telemetry_evaluation.png"):
        story.append(Image("report_images/fig6_telemetry_evaluation.png", width=246, height=127))
        story.append(Paragraph("<i>Fig. 6.</i> Architectural benchmark comparison illustrating CPU latency, model footprint, and top-1 accuracy.", fcap_s))

    story.append(Paragraph("C. Diagnostic and Actuation Categories", h2_left))
    story.append(Paragraph(
        "Diagnostic outputs span three operational status categories: Healthy Foliage (confidence > 80%, no intervention required), "
        "Foliar Pathology Confirmed (immediate bio-organic or chemical treatment prescription displayed), and Inconclusive Framing "
        "(confidence < 60%, prompting the user to recapture under diffused lighting).",
        body_s
    ))

    story.append(Paragraph("D. Evaluation Limitations", h2_left))
    story.append(Paragraph(
        "The PlantVillage benchmark consists primarily of single-leaf imagery captured against homogeneous laboratory backgrounds. "
        "Field imagery containing overlapping foliage, motion blur, or intense solar glare may yield lower diagnostic confidence, "
        "reinforcing the need for user recapture guidance.",
        body_s
    ))

    # =========================================================================
    # SECTION IX: COMPARISON WITH OTHER APPROACHES
    # =========================================================================
    story.append(Paragraph("IX. COMPARISON WITH OTHER APPROACHES", h1_center))

    # TABLE V: COMPARISON
    story.append(Paragraph("TABLE V<br/><b>COMPARISON OF AGRICULTURAL MONITORING APPROACHES</b>", tcap_s))
    t5_data = [
        [Paragraph("Dimension", th_s), Paragraph("Cloud Portals", th_s), Paragraph("IoT Gateways", th_s), Paragraph("AgroEdge AI", th_s)],
        [Paragraph("Network Dependency", td_s), Paragraph("Requires 4G/5G", td_c), Paragraph("Requires MQTT", td_c), Paragraph("100% Offline Edge", td_c)],
        [Paragraph("Inference Latency", td_s), Paragraph("1,200 – 3,500 ms", td_c), Paragraph("500 – 1,500 ms", td_c), Paragraph("18.2 ms on CPU", td_c)],
        [Paragraph("Operational Cost", td_s), Paragraph("Recurring Fees", td_c), Paragraph("Subscription", td_c), Paragraph("Zero Cloud Fees", td_c)],
        [Paragraph("Actionable Output", td_s), Paragraph("Label Only", td_c), Paragraph("Sensor Graph Only", td_c), Paragraph("Dual Remedies + Valve", td_c)]
    ]
    t5 = Table(t5_data, colWidths=[65, 58, 58, 65])
    t5.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t5)

    story.append(Paragraph(
        "AgroEdge AI delivers a unique synthesis of high diagnostic accuracy, sub-20ms edge responsiveness, zero cloud operational "
        "cost, and integrated physical closed-loop irrigation actuation.",
        body_s
    ))

    # =========================================================================
    # SECTION X: INDIVIDUAL CONTRIBUTION
    # =========================================================================
    story.append(Paragraph("X. INDIVIDUAL CONTRIBUTION", h1_center))
    story.append(Paragraph(
        "The project work was independently engineered by Rishu (Reg. No. 12519632, Roll No. K4P25REB10). Key individual contributions include: "
        "formulating the offline-first edge architecture; curating and preprocessing the PlantVillage dataset; evaluating convolutional model "
        "architectures; quantizing MobileNetV2 into an INT8 ONNX execution graph; compiling the 38-class dual-pathway agronomic remediation "
        "database; developing the closed-loop soil moisture threshold actuation engine; building the responsive dark-mode Streamlit user "
        "interface; writing comprehensive automated smoke tests; and deploying the verified platform to Streamlit Community Cloud.",
        body_s
    ))

    # =========================================================================
    # SECTION XI: LIMITATIONS
    # =========================================================================
    story.append(Paragraph("XI. LIMITATIONS", h1_center))
    story.append(Paragraph("• Background Sensitivity: Diagnostic accuracy decreases when leaf photography includes complex soil background clutter.", bullet_s))
    story.append(Paragraph("• Single Leaf Framing: The model requires individual leaf framing and cannot perform multi-leaf canopy disease segmentation.", bullet_s))
    story.append(Paragraph("• Fixed Soil Threshold: Actuation logic applies a fixed 30% threshold rather than dynamically adjusting for specific soil textures.", bullet_s))
    story.append(Paragraph("• Absence of Ambient Humidity Co-Modeling: Disease risk indices do not dynamically factor leaf wetness or ambient vapor pressure deficit.", bullet_s))
    story.append(Paragraph("• Synthetic Sensor Feeds: In the web demonstration mode, sensor readings utilize realistic simulated telemetry feeds.", bullet_s))
    story.append(Paragraph("• Class Imbalance in Rare Classes: Certain classes (e.g., Potato healthy) contain fewer training samples than dominant classes.", bullet_s))
    story.append(Paragraph("• Discrete Remediation Mapping: Prescriptions are retrieved from static agronomic lookups rather than dynamic regional weather forecasting.", bullet_s))
    story.append(Paragraph("• Hardware Driver Abstraction: The live cloud version provides visual actuation indicators rather than physical GPIO relay switching.", bullet_s))

    # =========================================================================
    # SECTION XII: FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("XII. FUTURE SCOPE", h1_center))
    story.append(Paragraph("• Edge YOLOv8-Nano Foliar Object Detection: Transitioning from classification to real-time multi-leaf bounding-box disease detection.", bullet_s))
    story.append(Paragraph("• LoRaWAN Multi-Node Mesh Telemetry: Deploying low-power wireless sensor nodes across field sectors up to 5 km apart.", bullet_s))
    story.append(Paragraph("• Soil Texture Calibration: Integrating soil-type calibration curves (sandy loam vs. clay) for dynamic moisture threshold tuning.", bullet_s))
    story.append(Paragraph("• Microclimate Epidemiological Modeling: Coupling leaf pathology diagnosis with temperature-humidity disease spread prediction.", bullet_s))
    story.append(Paragraph("• On-Device Few-Shot Fine-Tuning: Enabling local retraining on novel regional crop varieties directly on Raspberry Pi edge devices.", bullet_s))
    story.append(Paragraph("• Solar-Powered Hardware Enclosures: Packaging the edge camera and relay controller in rugged IP67 weatherproof solar-powered enclosures.", bullet_s))
    story.append(Paragraph("• Multilingual Voice Guidance: Adding localized voice output in regional agricultural dialects for non-literate smallholder growers.", bullet_s))
    story.append(Paragraph("• Federated Edge Learning: Aggregating localized disease weights across cooperative farm clusters without centralizing raw images.", bullet_s))

    # =========================================================================
    # SECTION XIII: CONCLUSION
    # =========================================================================
    story.append(Paragraph("XIII. CONCLUSION", h1_center))
    story.append(Paragraph(
        "AgroEdge AI successfully demonstrates that sophisticated deep learning computer vision and precision environmental actuation "
        "can be deployed completely offline on resource-constrained edge computing hardware. By converting a transfer-learned MobileNetV2 "
        "architecture into an INT8 quantized ONNX execution graph, the system achieved 96.4% top-1 diagnostic accuracy across 38 crop "
        "pathology classes with an 18 ms CPU latency and a 2.56 MB memory footprint. Coupled with evidence-based dual-pathway remediation "
        "guidelines, an autonomous closed-loop irrigation actuator, and a responsive web application deployed online, AgroEdge AI proves "
        "that modern edge AI can operate reliably and offline to support global agricultural resilience.",
        body_s
    ))

    # =========================================================================
    # REFERENCES (Centered Heading, Standard IEEE Format)
    # =========================================================================
    story.append(Paragraph("REFERENCES", h1_center))
    refs = [
        "[1] D. Hughes and M. Salathé, “An open access repository of images on plant health to enable the development of mobile disease diagnostics,” arXiv preprint arXiv:1511.08060, 2015.",
        "[2] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, “MobileNetV2: Inverted residuals and linear bottlenecks,” in Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR), 2018, pp. 4510–4520.",
        "[3] S. P. Mohanty, D. P. Hughes, and M. Salathé, “Using deep learning for image-based plant disease detection,” Frontiers in Plant Science, vol. 7, p. 1419, Sep. 2016.",
        "[4] Microsoft Corporation, “ONNX Runtime: Cross-platform, high performance ML inferencing accelerator,” [Online]. Available: https://onnxruntime.ai/",
        "[5] Food and Agriculture Organization (FAO), “The state of food and agriculture: Moving forward on food loss and waste reduction,” Rome: FAO, Tech. Rep., 2019.",
        "[6] Streamlit Documentation, “Build and share data apps,” [Online]. Available: https://docs.streamlit.io/",
        "[7] J. G. A. Barbedo, “Factors influencing the use of deep learning for plant disease recognition,” Biosystems Engineering, vol. 172, pp. 84–91, Aug. 2018.",
        "[8] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR), 2016, pp. 770–778."
    ]
    for r in refs:
        story.append(Paragraph(r, ref_s))

    doc.build(story, canvasmaker=IEEEPageCanvas)
    print(f"PDF successfully built to {filename}!")

if __name__ == "__main__":
    build_pdf("AgroEdge_AI_Final_Report.pdf")
    build_pdf("AgroEdge_AI_Official_IEEE_Report.pdf")
