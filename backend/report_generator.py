from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    HRFlowable
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
from reportlab.lib.units import inch

from datetime import datetime

import os


def generate_report(

    patient_name,
    age,
    gender,
    prediction,
    confidence,
    model_name,
    original_image,
    gradcam_image

):

    reports_folder = "static/reports"

    os.makedirs(
        reports_folder,
        exist_ok=True
    )

    filename = (

        f"TB_Report_"

        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    )

    pdf_path = os.path.join(

        reports_folder,

        filename

    )

    doc = SimpleDocTemplate(

        pdf_path,

        rightMargin=35,

        leftMargin=35,

        topMargin=35,

        bottomMargin=35

    )

    styles = getSampleStyleSheet()

    # =====================================================
    # CUSTOM STYLES
    # =====================================================

    title_style = ParagraphStyle(

        "Title",

        parent=styles["Title"],

        alignment=TA_CENTER,

        fontSize=24,

        textColor=HexColor("#0F4C81"),

        spaceAfter=5

    )

    subtitle_style = ParagraphStyle(

        "Subtitle",

        parent=styles["Heading2"],

        alignment=TA_CENTER,

        fontSize=13,

        textColor=HexColor("#555555"),

        spaceAfter=20

    )

    heading_style = ParagraphStyle(

        "Heading",

        parent=styles["Heading2"],

        fontSize=15,

        textColor=HexColor("#0F4C81"),

        spaceBefore=12,

        spaceAfter=10

    )

    normal_style = ParagraphStyle(

        "Normal",

        parent=styles["BodyText"],

        fontSize=11,

        leading=18,

        spaceAfter=8

    )

    elements = []

    # =====================================================
    # TITLE
    # =====================================================

    elements.append(

        Paragraph(

            "TB-AI DETECTION REPORT",

            title_style

        )

    )

    elements.append(

        Paragraph(

            "Automated Pulmonary Tuberculosis Detection",

            subtitle_style

        )

    )

    elements.append(

        HRFlowable(

            width="100%",

            thickness=1,

            color=HexColor("#0F4C81")

        )

    )

    elements.append(

        Spacer(1,15)

    )

    elements.append(

        Paragraph(

            f"<b>Generated On:</b> "

            f"{datetime.now().strftime('%d %b %Y | %I:%M %p')}",

            normal_style

        )

    )

    elements.append(

        Spacer(1,18)

    )

    # =====================================================
    # PATIENT INFORMATION
    # =====================================================

    elements.append(

        Paragraph(

            "PATIENT INFORMATION",

            heading_style

        )

    )

    patient_table = Table(

        [

            ["Patient Name", patient_name],

            ["Age", f"{age} Years"],

            ["Gender", gender]

        ],

        colWidths=[2*inch,4*inch]

    )

    patient_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#EAF3FB")),

            ("TEXTCOLOR",(0,0),(0,-1),colors.HexColor("#0F4C81")),

            ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BOX",(0,0),(-1,-1),1,colors.black),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8),

            ("BACKGROUND",(1,0),(1,-1),colors.white)

        ])

    )

    elements.append(

        patient_table

    )

    elements.append(

        Spacer(1,20)

    )
        # =====================================================
    # AI PREDICTION
    # =====================================================

    if prediction == "Tuberculosis":

        prediction_color = "#C62828"

        interpretation = (

            "The AI model predicts that the uploaded chest X-ray "
            "contains radiographic features suggestive of pulmonary "
            "tuberculosis."

        )

        recommendation = (

            "Clinical evaluation together with confirmatory "
            "diagnostic tests (such as GeneXpert, sputum smear "
            "microscopy or culture) is recommended before "
            "establishing a final diagnosis."

        )

    else:

        prediction_color = "#2E7D32"

        interpretation = (

            "The AI model did not detect radiographic features "
            "suggestive of pulmonary tuberculosis in the uploaded "
            "chest X-ray."

        )

        recommendation = (

            "If clinical symptoms persist or the patient is at "
            "high risk, further medical evaluation should still "
            "be considered despite the AI prediction."

        )

    elements.append(

        Paragraph(

            "AI PREDICTION",

            heading_style

        )

    )

    prediction_table = Table(

        [

            [

                "Model Used",

                model_name.upper()

            ],

            [

                "Prediction",

                Paragraph(

                    f"<font color='{prediction_color}'><b>{prediction}</b></font>",

                    normal_style

                )

            ],

            [

                "Confidence",

                f"{confidence:.2f}%"

            ]

        ],

        colWidths=[2*inch,4*inch]

    )

    prediction_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#EAF3FB")),

            ("TEXTCOLOR",(0,0),(0,-1),colors.HexColor("#0F4C81")),

            ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BOX",(0,0),(-1,-1),1,colors.black),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8),

            ("BACKGROUND",(1,0),(1,-1),colors.white)

        ])

    )

    elements.append(

        prediction_table

    )

    elements.append(

        Spacer(1,18)

    )

    # =====================================================
    # INTERPRETATION
    # =====================================================

    elements.append(

        Paragraph(

            "INTERPRETATION",

            heading_style

        )

    )

    elements.append(

        Paragraph(

            interpretation,

            normal_style

        )

    )

    elements.append(

        Spacer(1,10)

    )

    # =====================================================
    # RECOMMENDATION
    # =====================================================

    elements.append(

        Paragraph(

            "RECOMMENDATION",

            heading_style

        )

    )

    elements.append(

        Paragraph(

            recommendation,

            normal_style

        )

    )

    elements.append(

        Spacer(1,20)

    )
        # =====================================================
    # IMAGE ANALYSIS
    # =====================================================

    elements.append(

        Paragraph(

            "IMAGE ANALYSIS",

            heading_style

        )

    )

    elements.append(
        Spacer(1,10)
    )

    # ------------------------------------------
    # Load Images
    # ------------------------------------------

    if os.path.exists(original_image):

        original = Image(

            original_image,

            width=2.6*inch,

            height=2.6*inch

        )

    else:

        original = Paragraph(

            "Original Image Not Available",

            normal_style

        )

    if gradcam_image and os.path.exists(gradcam_image):

        gradcam = Image(

            gradcam_image,

            width=2.6*inch,

            height=2.6*inch

        )

    else:

        gradcam = Paragraph(

            "Grad-CAM Not Available",

            normal_style

        )

    # ------------------------------------------
    # Side-by-side Table
    # ------------------------------------------

    image_table = Table(

        [

            [

                Paragraph(

                    "<b>Original Chest X-ray</b>",

                    heading_style

                ),

                Paragraph(

                    "<b>Grad-CAM Heatmap</b>",

                    heading_style

                )

            ],

            [

                original,

                gradcam

            ],

            [

                Paragraph(

                    "<para align='center'><i>Figure 1</i></para>",

                    normal_style

                ),

                Paragraph(

                    "<para align='center'><i>Figure 2</i></para>",

                    normal_style

                )

            ]

        ],

        colWidths=[3.0*inch,3.0*inch]

    )

    image_table.setStyle(

        TableStyle([

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

            ("GRID",(0,1),(-1,1),0.5,colors.grey),

            ("BOX",(0,1),(-1,1),1,colors.black),

            ("BOTTOMPADDING",(0,0),(-1,-1),10),

            ("TOPPADDING",(0,0),(-1,-1),10),

            ("LINEBELOW",(0,0),(-1,0),1,colors.HexColor("#0F4C81"))

        ])

    )

    elements.append(

        image_table

    )

    elements.append(
        Spacer(1,18)
    )

    # =====================================================
    # GRAD-CAM EXPLANATION
    # =====================================================

    elements.append(

        Paragraph(

            "GRAD-CAM EXPLANATION",

            heading_style

        )

    )

    elements.append(

        Paragraph(

            "The Grad-CAM heatmap highlights the regions of the chest "
            "X-ray that contributed most to the AI model's prediction. "
            "These highlighted regions improve the transparency and "
            "interpretability of the deep learning model by showing "
            "where the network focused during classification.",

            normal_style

        )

    )

    elements.append(
        Spacer(1,20)
    )

    # =====================================================
    # DISCLAIMER
    # =====================================================

    elements.append(

        Paragraph(

            "DISCLAIMER",

            heading_style

        )

    )

    elements.append(

        Paragraph(

            "This report has been generated automatically by an Artificial "
            "Intelligence (AI) system and is intended for educational "
            "and research purposes only.",

            normal_style

        )

    )

    elements.append(

        Paragraph(

            "The prediction should be considered as decision-support "
            "information and must not replace professional medical "
            "diagnosis by a qualified radiologist or physician.",

            normal_style

        )

    )

    elements.append(

        Paragraph(

            "Clinical examination, patient history and laboratory "
            "investigations should always be considered before "
            "making any medical decision.",

            normal_style

        )

    )

    elements.append(
        Spacer(1,20)
    )

    # =====================================================
    # FOOTER
    # =====================================================

    elements.append(

        HRFlowable(

            width="100%",

            thickness=1,

            color=HexColor("#0F4C81")

        )

    )

    elements.append(
        Spacer(1,10)
    )

    footer = Paragraph(

        "<para align='center'>"

        "<font size='10' color='#666666'>"

        "Generated Automatically by TB-AI Detection System"

        "</font>"

        "</para>",

        normal_style

    )

    elements.append(

        footer

    )

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(

        elements

    )

    return "/" + pdf_path.replace(

        "\\",

        "/"

    )