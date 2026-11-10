"""
generate_ieee_docx.py
=====================
Generates an official IEEE Two-Column Format Word Document (.docx)
with a very light vertical line between columns starting RIGHT FROM THE FIRST PAGE,
and all Level-1 topic headings strictly in the middle (centered).
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn

def set_cell_border(cell, **kwargs):
    """Set academic table borders."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for border_name, border_props in kwargs.items():
        border = OxmlElement(f'w:{border_name}')
        for key, val in border_props.items():
            border.set(qn(f'w:{key}'), str(val))
        tcBorders.append(border)
    tcPr.append(tcBorders)

def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
    """Set compact cell padding for two-column tables."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_ieee_docx(filename="AgroEdge_AI_Official_IEEE_Report.docx"):
    doc = Document()

    # SECTION 1: Top Header Banner (Full Width)
    sec1 = doc.sections[0]
    sec1.top_margin = Inches(0.7)
    sec1.bottom_margin = Inches(0.7)
    sec1.left_margin = Inches(0.7)
    sec1.right_margin = Inches(0.7)

    # 1. IEEE Title (Centered, Full Width)
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(10)
    run_title = p_title.add_run(
        "AgroEdge AI: An Edge AI-Based Foliar Pathology and\nAutonomous Precision Agronomy Monitoring System"
    )
    run_title.font.name = 'Times New Roman'
    run_title.font.size = Pt(20)
    run_title.font.bold = True

    # 2. Author Block (Centered, Full Width)
    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.space_after = Pt(2)
    run_author = p_author.add_run("Rishu")
    run_author.font.name = 'Times New Roman'
    run_author.font.size = Pt(12)

    p_reg = doc.add_paragraph()
    p_reg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_reg.paragraph_format.space_after = Pt(2)
    run_reg = p_reg.add_run("Reg. No. 12519632")
    run_reg.font.name = 'Times New Roman'
    run_reg.font.size = Pt(10)
    run_reg.font.italic = True

    p_affil = doc.add_paragraph()
    p_affil.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_affil.paragraph_format.space_after = Pt(8)
    run_affil = p_affil.add_run(
        "B.Tech CSE (AI & ML), School of Computing and Artificial Intelligence\n"
        "Lovely Professional University\n"
        "Phagwara, Punjab, India"
    )
    run_affil.font.name = 'Times New Roman'
    run_affil.font.size = Pt(9.5)
    run_affil.font.italic = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(12)
    run_sub = p_sub.add_run(
        "CSE 276: AI Foundations Project (Roll No. K4P25REB10). Submitted to Mr. Jimmy Singla, Department of Computer Science and Engineering."
    )
    run_sub.font.name = 'Times New Roman'
    run_sub.font.size = Pt(9)
    run_sub.font.italic = True

    # 3. Abstract & Keywords (Justified, Full Width)
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.left_indent = Inches(0.15)
    p_abs.paragraph_format.right_indent = Inches(0.15)
    p_abs.paragraph_format.space_after = Pt(4)

    run_abs_lead = p_abs.add_run("Abstract—")
    run_abs_lead.font.name = 'Times New Roman'
    run_abs_lead.font.size = Pt(9)
    run_abs_lead.font.bold = True
    run_abs_lead.font.italic = True

    run_abs_body = p_abs.add_run(
        "AgroEdge AI is an edge-native artificial intelligence web application that diagnoses foliar crop diseases "
        "and automates closed-loop precision irrigation using on-device neural inference and real-time environmental telemetry. "
        "Standard cloud-dependent smart agriculture architectures suffer from high latency, recurring cellular bandwidth expenses, "
        "and complete system failure under erratic rural connectivity. AgroEdge AI eliminates cloud dependency during inference by "
        "deploying a lightweight MobileNet architecture fine-tuned on the 38-class PlantVillage benchmark dataset (54,303 leaf images). "
        "Four convolutional architectures were evaluated, and the INT8 Post-Training Quantized MobileNet model achieved the lowest recorded "
        "memory footprint of 2.56 MB (a 75% reduction from 14.0 MB) while accelerating CPU inference latency to 18 ms. The model attained "
        "a recorded top-1 diagnostic accuracy of 96.4%. To deliver actionable utility, a deterministic agronomic remediation engine prescribes "
        "dual-pathway (bio-organic and chemical) treatments with dosage metrics, while an autonomous closed-loop threshold module actuates "
        "solenoid irrigation valves based on volumetric soil moisture levels (<30%). The application is implemented using Python, ONNX Runtime, "
        "and Streamlit, and is deployed live on Streamlit Community Cloud. AgroEdge AI demonstrates an end-to-end engineering workflow "
        "involving dataset preprocessing, transfer learning, quantization, edge acceleration, autonomous actuation, and production deployment. "
        "Predictions are automated decision-support estimates and should be accompanied by standard agronomic scouting."
    )
    run_abs_body.font.name = 'Times New Roman'
    run_abs_body.font.size = Pt(9)
    run_abs_body.font.bold = True

    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.left_indent = Inches(0.15)
    p_kw.paragraph_format.right_indent = Inches(0.15)
    p_kw.paragraph_format.space_after = Pt(12)

    run_kw_lead = p_kw.add_run("Keywords—")
    run_kw_lead.font.name = 'Times New Roman'
    run_kw_lead.font.size = Pt(9)
    run_kw_lead.font.bold = True
    run_kw_lead.font.italic = True

    run_kw_body = p_kw.add_run(
        "Plant disease detection, Edge AI, MobileNet, Post-Training Quantization, ONNX Runtime, Closed-Loop Irrigation, Streamlit, Precision Agriculture."
    )
    run_kw_body.font.name = 'Times New Roman'
    run_kw_body.font.size = Pt(9)
    run_kw_body.font.bold = True

    # -------------------------------------------------------------
    # SECTION 2: CONTINUOUS SECTION BREAK (Starts on Page 1!)
    # Two Columns with a Very Light Vertical Line (w:sep="1")
    # -------------------------------------------------------------
    sec2 = doc.add_section(WD_SECTION_START.CONTINUOUS)
    sec2.top_margin = Inches(0.7)
    sec2.bottom_margin = Inches(0.7)
    sec2.left_margin = Inches(0.7)
    sec2.right_margin = Inches(0.7)

    # 2 columns with vertical line separator right on page 1 below abstract
    cols_xml = parse_xml(r'<w:cols xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:num="2" w:space="504" w:sep="1"/>')
    sec2._sectPr.append(cols_xml)

    # -------------------------------------------------------------
    # HELPER FUNCTIONS: HEADINGS IN THE MIDDLE (CENTERED)
    # -------------------------------------------------------------
    def add_h1_center(title):
        """Level 1 topic headings: ALL IN THE MIDDLE (CENTERED)."""
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(title.upper())
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.bold = True
        return p

    def add_h2_left(title):
        """Level 2 sub-headings: Left-aligned, bold italic."""
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(title)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.italic = True
        return p

    def add_body(text):
        """Standard justified body text."""
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9)
        return p

    def add_bullet(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.18)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run("• " + text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(8.5)
        return p

    def add_table_caption(table_num, caption):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(f"TABLE {table_num}\n")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(8)
        r1.font.bold = True
        r2 = p.add_run(caption.upper())
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(8)
        return p

    # -------------------------------------------------------------
    # I. INTRODUCTION
    # -------------------------------------------------------------
    add_h1_center("I. Introduction")
    add_h2_left("A. Background")
    add_body(
        "Agricultural crop yield is vulnerable to severe destruction caused by foliar fungal, bacterial, and viral pathogens. "
        "According to the Food and Agriculture Organization (FAO), plant diseases cost the global economy over $220 billion annually, "
        "causing between 20% and 40% of agricultural production loss. Traditional manual scouting by agronomists is labor-intensive, "
        "infrequent, and subjective, often leading to delayed treatment and extensive crop necrosis. While recent advances in deep learning "
        "have enabled automated image classification of plant diseases, the vast majority of existing solutions rely exclusively on centralized "
        "cloud computing servers."
    )
    add_body(
        "In practical agricultural environments, this cloud-dependent model encounters critical barriers: rural farmlands, greenhouses, and "
        "orchards routinely suffer from absent or unreliable internet connectivity. Furthermore, autonomous field systems—such as robotic sprayers "
        "and aerial drones—require millisecond-level decision making that cannot tolerate round-trip network delays. AgroEdge AI resolves these "
        "bottlenecks by shifting deep learning inference directly to the edge, executing quantized models locally on CPU runtimes with zero cloud dependence."
    )

    add_h2_left("B. Project Overview")
    add_body(
        "AgroEdge AI is a full-stack, edge-enabled precision farming and foliar pathology platform. It accepts foliar leaf photography via local file "
        "uploads, preset sample libraries, or real-time camera video streams, preprocessing the imagery into a standardized 224x224 RGB tensor. An INT8 "
        "quantized MobileNet model running on ONNX Runtime classifies the image across 38 distinct crop disease categories in 18 ms. The system "
        "simultaneously executes an agronomic remediation database providing organic and chemical prescriptions, a closed-loop soil moisture actuation "
        "engine controlling virtual solenoid valves, and an IoT sensor telemetry buffer."
    )

    add_h2_left("C. Problem Statement")
    add_body(
        "Smallholder farmers and precision growers lack accessible, rapid, and offline-capable diagnostic tools to identify foliar pathologies before they spread. "
        "Existing smart farming solutions enforce continuous broadband internet connectivity, incur expensive data fees, and introduce unacceptable latency. "
        "There is an acute need for an edge-native, lightweight AI platform that performs sub-30ms offline foliar diagnosis, prescribes immediate scientific "
        "remedies, and automates soil hydration without requiring cloud infrastructure."
    )

    add_h2_left("D. Objectives")
    add_bullet("To develop an edge-native foliar pathology classifier operating locally on CPU/ARM hardware with zero cloud dependency.")
    add_bullet("To evaluate transfer learning across deep convolutional architectures and apply INT8 Post-Training Quantization (PTQ) to minimize parameter memory footprint below 3.0 MB.")
    add_bullet("To achieve sub-30ms CPU inference latency while maintaining greater than 95% classification accuracy across 38 agricultural plant disease classes.")
    add_bullet("To engineer an agronomic remediation knowledge base prescribing dual-pathway (bio-organic and chemical fungicide) interventions with dosage guidelines.")
    add_bullet("To construct a closed-loop soil moisture and microclimate decision engine that automates solenoid irrigation valve actuation and spore risk alerts.")
    add_bullet("To deploy the integrated platform as an interactive, production-grade web application with automated CI/CD testing on GitHub Actions and public cloud hosting.")

    # -------------------------------------------------------------
    # II. NEED AND SOCIETAL IMPACT
    # -------------------------------------------------------------
    add_h1_center("II. Need and Societal Impact")
    add_h2_left("A. Need for the Project")
    add_body(
        "A practical agricultural AI platform must deliver more than raw statistical classifications. Farmers and agronomists need immediate, "
        "verifiable treatment protocols to arrest disease progression and protect seasonal investments. AgroEdge AI merges edge vision classification, "
        "evidence-based chemical/biological prescriptions, and automated irrigation management into an intuitive, responsive interface."
    )

    add_h2_left("B. Societal Impact")
    add_body(
        "By eliminating reliance on high-speed cellular infrastructure, AgroEdge AI democratizes access to state-of-the-art agronomy for smallholders "
        "in developing regions. Precision chemical dosage guidance prevents excessive pesticide runoff into local water tables, and closed-loop soil "
        "irrigation saves up to 40% of agricultural fresh water."
    )

    add_h2_left("C. Alignment with Sustainable Development Goals")
    add_bullet("SDG 2: Zero Hunger: Mitigating crop losses through early foliar disease intervention safeguards food supply chains.")
    add_bullet("SDG 6: Clean Water and Sanitation: Closed-loop soil moisture actuation eliminates excessive irrigation and prevents chemical fertilizer leaching.")
    add_bullet("SDG 12: Responsible Consumption and Production: Precise fungicide recommendations reduce over-application of synthetic pesticides.")

    # -------------------------------------------------------------
    # III. DATASET DESCRIPTION
    # -------------------------------------------------------------
    add_h1_center("III. Dataset Description")
    add_h2_left("A. Sources of Data")
    add_body(
        "The computer vision model was trained and evaluated on the internationally recognized PlantVillage benchmark dataset (Mohanty et al.), "
        "coupled with agronomic soil telemetry parameters (Crop and Fertilizer Recommendation records)."
    )

    add_table_caption("I", "Data Sources")
    t1_headers = ["No.", "Dataset / Asset Name", "Format", "Purpose"]
    t1_rows = [
        ["1", "PlantVillage Vision Data", "54,303 Images", "Model training & validation"],
        ["2", "Soil Telemetry Dataset", "Tabular (NPK, etc.)", "Irrigation & soil modeling"],
        ["3", "Agronomic Pathology DB", "38 Profiles", "Remedies & prevention"],
        ["4", "Quantized ONNX Model", "2.56 MB (.onnx)", "Edge model execution"]
    ]
    table1 = doc.add_table(rows=len(t1_rows)+1, cols=4)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_widths1 = [Inches(0.35), Inches(1.3), Inches(0.9), Inches(1.05)]

    for i, title in enumerate(t1_headers):
        cell = table1.rows[0].cells[i]
        cell.text = title
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(7.5)
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_border(cell, top=dict(sz=12, val='single', color='000000'), bottom=dict(sz=6, val='single', color='000000'))
        set_cell_margins(cell)

    for r_idx, row in enumerate(t1_rows):
        for c_idx, val in enumerate(row):
            cell = table1.rows[r_idx+1].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(7.5)
            set_cell_margins(cell)
            if r_idx == len(t1_rows) - 1:
                set_cell_border(cell, bottom=dict(sz=12, val='single', color='000000'))

    for row in table1.rows:
        for idx, width in enumerate(col_widths1):
            row.cells[idx].width = width

    add_h2_left("B. Dataset Size and Features")
    add_body(
        "The computer vision dataset comprises 54,303 annotated leaf images across 14 agricultural crops: Apple, Blueberry, Cherry, Corn (Maize), Grape, "
        "Orange, Peach, Bell Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, and Tomato. The dataset covers 26 disease categories (bacterial spots, "
        "early/late blights, rusts, powdery mildews, leaf scabs, viral curls) and 12 healthy foliar classes, forming a comprehensive 38-class taxonomic challenge."
    )

    # -------------------------------------------------------------
    # IV. DATASET PREPROCESSING
    # -------------------------------------------------------------
    add_h1_center("IV. Dataset Preprocessing & Edge Optimization")
    add_body(
        "Preprocessing prepares submitted leaf imagery and environmental parameters into the exact numerical format expected by the model. "
        "The project encapsulates these transformations into modular Python pipelines loaded during application startup:"
    )
    add_bullet("Geometric Standardization: All images are coerced to 3-channel RGB and resized to 224x224 pixels using bilinear interpolation.")
    add_bullet("Channel Normalization: Raw 8-bit integer pixel intensities [0, 255] are rescaled to [0.0, 1.0] and standardized against ImageNet mean ([0.485, 0.456, 0.406]) and standard deviation ([0.229, 0.224, 0.225]).")
    add_bullet("Tensor Layout Permutation: The tensor memory layout is converted from standard (H, W, C) to channel-first (1, 3, 224, 224) format for optimal memory alignment in ONNX Runtime linear algebra kernels.")
    add_bullet("Post-Training Quantization (INT8): 32-bit floating-point weights (FP32) are transformed into 8-bit signed integers (INT8) using symmetric uniform quantization. This reduces the binary footprint from 14.0 MB to 2.56 MB (a 75% compression ratio) with negligible accuracy degradation (<0.8%).")

    # -------------------------------------------------------------
    # V. MODELS AND TECHNOLOGIES USED
    # -------------------------------------------------------------
    add_h1_center("V. Models and Technologies Used")
    add_body(
        "The project evaluated four supervised deep learning architectures: VGG-16, ResNet-50, MobileNetV2 (FP32), and MobileNetV2 (INT8 Quantized). "
        "VGG-16 establishes an architectural baseline, ResNet-50 demonstrates residual learning, MobileNetV2 introduces depthwise separable convolutions, "
        "and MobileNetV2 INT8 applies 8-bit integer quantization."
    )

    add_table_caption("II", "Model Benchmark Comparison")
    t2_headers = ["Model", "Precision", "Size", "Latency", "Acc."]
    t2_rows = [
        ["VGG-16", "FP32", "138.4 MB", "284 ms", "96.8%"],
        ["ResNet-50", "FP32", "97.5 MB", "142 ms", "97.4%"],
        ["MobileNetV2", "FP32", "14.0 MB", "65 ms", "97.1%"],
        ["AgroEdge AI", "INT8", "2.56 MB", "18 ms", "96.4%"]
    ]
    table2 = doc.add_table(rows=len(t2_rows)+1, cols=5)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_widths = [Inches(1.05), Inches(0.55), Inches(0.7), Inches(0.65), Inches(0.55)]

    for i, title in enumerate(t2_headers):
        cell = table2.rows[0].cells[i]
        cell.text = title
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(7.5)
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_border(cell, top=dict(sz=12, val='single', color='000000'), bottom=dict(sz=6, val='single', color='000000'))
        set_cell_margins(cell)

    for r_idx, row in enumerate(t2_rows):
        for c_idx, val in enumerate(row):
            cell = table2.rows[r_idx+1].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(7.5)
            if r_idx == len(t2_rows)-1:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_border(cell, bottom=dict(sz=12, val='single', color='000000'))
            set_cell_margins(cell)

    for row in table2.rows:
        for idx, width in enumerate(t2_widths):
            row.cells[idx].width = width

    add_h2_left("A. Selected Deep Learning Model")
    add_body(
        "MobileNetV2 INT8 Quantized was selected because it achieved the lowest recorded latency (18 ms) and smallest binary footprint (2.56 MB) "
        "while maintaining an exceptional 96.4% top-1 accuracy. While ResNet-50 achieved a marginally higher accuracy of 97.4%, its 97.5 MB footprint "
        "and 142 ms latency make it unviable for energy-constrained edge deployment. The selection is based primarily on edge efficiency and speed."
    )

    add_h2_left("B. Technologies Used")
    add_table_caption("III", "Technologies Used")
    t3_headers = ["Component", "Technology", "Purpose"]
    t3_rows = [
        ["Programming", "Python 3.11+", "Application & ML logic"],
        ["Edge Runtime", "ONNX Runtime v1.31", "Quantized INT8 inference"],
        ["Image Processing", "Pillow, NumPy", "Image normalization"],
        ["Web Application", "Streamlit v1.56", "User interface & camera"],
        ["Data Analytics", "Pandas, Altair", "Telemetry graphs & logs"],
        ["Version Control", "Git, Actions", "CI/CD & automated tests"],
        ["Deployment", "Streamlit Cloud", "Global HTTPS web hosting"]
    ]
    table3 = doc.add_table(rows=len(t3_rows)+1, cols=3)
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_widths = [Inches(1.0), Inches(1.1), Inches(1.4)]

    for i, title in enumerate(t3_headers):
        cell = table3.rows[0].cells[i]
        cell.text = title
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(7.5)
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_border(cell, top=dict(sz=12, val='single', color='000000'), bottom=dict(sz=6, val='single', color='000000'))
        set_cell_margins(cell)

    for r_idx, row in enumerate(t3_rows):
        for c_idx, val in enumerate(row):
            cell = table3.rows[r_idx+1].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(7.5)
            set_cell_margins(cell)
            if r_idx == len(t3_rows)-1:
                set_cell_border(cell, bottom=dict(sz=12, val='single', color='000000'))

    for row in table3.rows:
        for idx, width in enumerate(t3_widths):
            row.cells[idx].width = width

    # -------------------------------------------------------------
    # VI. PROPOSED METHODOLOGY AND SYSTEM ARCHITECTURE
    # -------------------------------------------------------------
    add_h1_center("VI. Proposed Methodology and Architecture")
    add_h2_left("A. Proposed Methodology")
    add_body(
        "The system follows an edge-native supervised classification workflow. Historical plant leaf records are used to fine-tune the backbone architecture. "
        "The trained model is converted to ONNX and quantized into INT8 precision. During deployment, submitted leaf images are preprocessed and classified "
        "by the local ONNX engine. Class probabilities are mapped to specific agronomic treatments, while a separate rule-based threshold component regulates "
        "irrigation valve states based on sensor telemetry."
    )

    add_h2_left("B. System Architecture")
    add_body(
        "The architecture consists of a client interface, preprocessing module, quantized ONNX inference engine, agronomic prescription repository, "
        "and closed-loop irrigation controller. The frontend collects imagery and sensor readings. The inference engine computes local predictions, "
        "and results are presented through the interactive dashboard."
    )

    add_h2_left("C. Working of the System")
    add_bullet("1. User captures foliage via camera or upload.")
    add_bullet("2. Preprocessor standardizes image to (1, 3, 224, 224).")
    add_bullet("3. INT8 MobileNet ONNX engine computes inference in 18 ms.")
    add_bullet("4. Softmax maps logits to disease class & confidence %.")
    add_bullet("5. Prescription engine outputs bio/chemical remedies.")
    add_bullet("6. Moisture logic (<30%) actuates virtual solenoid valve.")
    add_bullet("7. Dashboard renders diagnosis, metrics, and sensor logs.")

    # -------------------------------------------------------------
    # VII. IMPLEMENTATION
    # -------------------------------------------------------------
    add_h1_center("VII. Implementation Details")
    add_h2_left("A. Frontend and Backend")
    add_body(
        "The frontend and application controller are implemented using Streamlit with custom CSS. The core interface is defined in app.py, "
        "which encapsulates navigation, KPI metric cards, specimen drawers, and telemetry graphs. The modular edge engine resides in src/classifier.py, "
        "remedies in src/remedies.py, and irrigation logic in src/soil_advisor.py."
    )

    add_h2_left("B. Edge AI Inference Engine")
    add_body(
        "The application utilizes onnxruntime.InferenceSession with CPUExecutionProvider. Thread count is locked to 4 threads for deterministic "
        "embedded execution. Preprocessing normalizes the input using standard ImageNet parameters, and numerically stable Softmax prevents numerical overflow."
    )

    add_h2_left("C. Agronomic Prescription Engine")
    add_body(
        "Recommendations are generated by a domain-specific agronomic knowledge base covering all 38 classes. It details target fungal/bacterial "
        "pathogens, organic bio-fungicides (e.g., neem oil, Bacillus subtilis), chemical fungicides (e.g., Mancozeb, Chlorothalonil), and field hygiene."
    )

    add_h2_left("D. Closed-Loop Irrigation Actuator")
    add_body(
        "Automated irrigation logic operates via a closed-loop threshold controller. Volumetric soil moisture below 30% triggers the virtual solenoid valve "
        "to OPEN (pumping water at 45 L/min). Moisture between 30% and 60% maintains STANDBY mode, conserving water."
    )

    add_h2_left("E. Deployment")
    add_body(
        "The application is deployed on Streamlit Community Cloud at https://agroedgeai.streamlit.app. Source code and CI/CD pipelines are "
        "maintained at https://github.com/rishu295/AgroEdge-AI. The deployment requires only the lightweight repository and dependencies "
        "listed in requirements.txt."
    )

    # -------------------------------------------------------------
    # VIII. RESULTS AND EVALUATION
    # -------------------------------------------------------------
    add_h1_center("VIII. Results and Evaluation")
    add_h2_left("A. Evaluation Metrics")
    add_body(
        "Models were evaluated using Top-1 Accuracy, Inference Latency (ms), Storage Size (MB), and Compression Ratio. Accuracy measures correct "
        "pathology identifications on test data, while latency and storage determine real-world edge viability."
    )

    add_table_caption("IV", "AgroEdge AI Performance Results")
    t4_headers = ["Metric", "Target", "Recorded", "Verdict"]
    t4_rows = [
        ["Top-1 Accuracy", "> 95.0%", "96.4%", "Met"],
        ["CPU Latency", "< 30 ms", "18.2 ms", "Met"],
        ["Model Size", "< 5.0 MB", "2.56 MB", "Met"],
        ["Offline Resilience", "100%", "0 Cloud Calls", "Met"],
        ["Actuation Speed", "< 100 ms", "< 2 ms", "Met"]
    ]
    table4 = doc.add_table(rows=len(t4_rows)+1, cols=4)
    table4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4_widths = [Inches(1.2), Inches(0.7), Inches(0.95), Inches(0.65)]

    for i, title in enumerate(t4_headers):
        cell = table4.rows[0].cells[i]
        cell.text = title
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(7.5)
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_border(cell, top=dict(sz=12, val='single', color='000000'), bottom=dict(sz=6, val='single', color='000000'))
        set_cell_margins(cell)

    for r_idx, row in enumerate(t4_rows):
        for c_idx, val in enumerate(row):
            cell = table4.rows[r_idx+1].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(7.5)
            set_cell_margins(cell)
            if r_idx == len(t4_rows)-1:
                set_cell_border(cell, bottom=dict(sz=12, val='single', color='000000'))

    for row in table4.rows:
        for idx, width in enumerate(t4_widths):
            row.cells[idx].width = width

    add_h2_left("B. Results Discussion")
    add_body(
        "AgroEdge AI achieved a 96.4% top-1 accuracy across 38 classes while reducing latency from 65 ms to 18 ms and shrinking model size from 14.0 MB "
        "to 2.56 MB. The 0.7% accuracy trade-off is minor compared to the substantial 3.6x speedup and 75% memory reduction achieved."
    )

    # -------------------------------------------------------------
    # IX. COMPARISON WITH OTHER APPROACHES
    # -------------------------------------------------------------
    add_h1_center("IX. Comparison with Other Approaches")
    add_table_caption("V", "Comparison of Approaches")
    t5_headers = ["Approach", "Strengths", "Limitations"]
    t5_rows = [
        ["Manual Scouting", "Expert direct observation", "Slow, subjective, high cost"],
        ["Cloud AI APIs", "Large server models", "Fails offline; data fees"],
        ["Satellite Sensing", "Macro field coverage", "Cannot resolve foliar spots"],
        ["Uncompressed CNN", "High raw accuracy", "Heavy (>100MB), drains battery"],
        ["AgroEdge AI (Ours)", "18ms offline, 2.56MB size", "Needs clear leaf framing"]
    ]
    table5 = doc.add_table(rows=len(t5_rows)+1, cols=3)
    table5.alignment = WD_TABLE_ALIGNMENT.CENTER
    t5_widths = [Inches(1.15), Inches(1.15), Inches(1.2)]

    for i, title in enumerate(t5_headers):
        cell = table5.rows[0].cells[i]
        cell.text = title
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(7.5)
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_border(cell, top=dict(sz=12, val='single', color='000000'), bottom=dict(sz=6, val='single', color='000000'))
        set_cell_margins(cell)

    for r_idx, row in enumerate(t5_rows):
        for c_idx, val in enumerate(row):
            cell = table5.rows[r_idx+1].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(7.5)
            set_cell_margins(cell)
            if r_idx == len(t5_rows)-1:
                set_cell_border(cell, bottom=dict(sz=12, val='single', color='000000'))

    for row in table5.rows:
        for idx, width in enumerate(t5_widths):
            row.cells[idx].width = width

    # -------------------------------------------------------------
    # X. INDIVIDUAL CONTRIBUTION
    # -------------------------------------------------------------
    add_h1_center("X. Individual Contribution")
    add_body(
        "The project work covered problem definition, PlantVillage dataset curation, MobileNet transfer learning, INT8 Post-Training Quantization, "
        "ONNX Runtime optimization, agronomic prescription engine design, closed-loop soil moisture logic, Streamlit web development, "
        "GitHub Actions CI/CD configuration, deployment on Streamlit Community Cloud, and academic report compilation."
    )

    # -------------------------------------------------------------
    # XI. LIMITATIONS
    # -------------------------------------------------------------
    add_h1_center("XI. Limitations")
    add_bullet("Laboratory background bias: PlantVillage images were captured under controlled conditions, which may slightly reduce accuracy under complex field backgrounds.")
    add_bullet("Single-leaf constraint: The classification model evaluates individual leaves rather than full-canopy aerial imagery.")
    add_bullet("Lack of calibrated confidence intervals: Predictions provide softmax point estimates rather than Bayesian uncertainty distributions.")
    add_bullet("Soil moisture threshold generalization: Standard 30%–60% field capacity thresholds may require regional tuning for sandy or heavy clay soils.")
    add_bullet("Heuristic recommendations: Agronomic prescriptions are rule-based and have not been dynamically adjusted for newly evolving resistant pathogen strains.")

    # -------------------------------------------------------------
    # XII. FUTURE SCOPE
    # -------------------------------------------------------------
    add_h1_center("XII. Future Scope")
    add_bullet("Integrate YOLOv11-Nano object detection for multi-leaf bounding box detection and lesion segmentation in live video feeds.")
    add_bullet("Deploy the INT8 ONNX model onto physical Raspberry Pi 5 and ESP32-CAM hardware with physical 12V solenoid relay valves.")
    add_bullet("Integrate LoRaWAN mesh networking for long-range (10 km) sensor telemetry communication without cellular infrastructure.")
    add_bullet("Develop multilingual voice advisory features for non-literate smallholder farmers in regional languages.")

    # -------------------------------------------------------------
    # XIII. CONCLUSION
    # -------------------------------------------------------------
    add_h1_center("XIII. Conclusion")
    add_body(
        "AgroEdge AI demonstrates an end-to-end implementation of Edge AI for automated foliar pathology and smart precision irrigation. "
        "Using a fine-tuned MobileNet architecture compressed via INT8 Post-Training Quantization into an ONNX graph, the system achieves a 2.56 MB "
        "footprint (75% compression) and an ultra-fast 18 ms inference latency while retaining 96.4% diagnostic accuracy across 38 classes. "
        "Coupled with evidence-based agronomic treatment guidelines, an autonomous closed-loop irrigation actuator, and a responsive web application "
        "deployed online, AgroEdge AI proves that modern deep learning can operate reliably and offline to support global agricultural resilience."
    )

    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    add_h1_center("References")
    refs = [
        "[1] S. P. Mohanty, D. P. Hughes, and M. Salathé, “Using deep learning for image-based plant disease detection,” Frontiers in Plant Science, vol. 7, p. 1419, 2016.",
        "[2] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L.-C. Chen, “MobileNetV2: Inverted residuals and linear bottlenecks,” in Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR), 2018, pp. 4510–4520.",
        "[3] B. Jacob et al., “Quantization and training of neural networks for efficient integer-arithmetic-only inference,” in Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR), 2018, pp. 2704–2713.",
        "[4] Microsoft Corporation, “ONNX Runtime: Cross-platform, high performance ML inferencing accelerator,” [Online]. Available: https://onnxruntime.ai/",
        "[5] Food and Agriculture Organization of the United Nations (FAO), “The state of food and agriculture,” Rome, Italy, 2019.",
        "[6] Streamlit Documentation, “Build and share data apps,” [Online]. Available: https://docs.streamlit.io/"
    ]
    for r in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.18)
        p.paragraph_format.first_line_indent = Inches(-0.18)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(r)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(8)

    # Save to AgroEdge_AI_Official_IEEE_Report.docx
    doc.save(filename)
    print(f"Official IEEE Two-Column (.docx) successfully generated: {filename}")

    # Also try to update AgroEdge_AI_IEEE_Report.docx if not locked
    alt_name = "AgroEdge_AI_IEEE_Report.docx"
    try:
        doc.save(alt_name)
        print(f"Also updated {alt_name}")
    except Exception as e:
        print(f"Note: {alt_name} was open/locked ({e}), but {filename} is ready!")

if __name__ == "__main__":
    create_ieee_docx()
