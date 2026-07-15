import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT


def create_report():
    pdf_filename = "Problem_Formulation_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=54, leftMargin=54,
        topMargin=54, bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1A365D'),
        alignment=TA_CENTER,
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4A5568'),
        alignment=TA_CENTER,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2C5282'),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2D3748'),
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )

    list_style = ParagraphStyle(
        'List_Custom',
        parent=body_style,
        leftIndent=15,
        spaceAfter=4
    )

    story = []

    # Header / Title Block
    story.append(Paragraph("BITS PILANI WILP — M.TECH (AI & ML)", subtitle_style))
    story.append(Paragraph("Course: Data Mining and Machine Learning (DMML)", subtitle_style))
    story.append(Paragraph("RecoMart Recommendation Pipeline", title_style))
    story.append(Paragraph("Phase 1: Problem Formulation Report", subtitle_style))
    story.append(Spacer(1, 15))

    # Section 1
    story.append(Paragraph("1. Problem Formulation", h1_style))
    story.append(Paragraph(
        "<b>1.1 Business Problem Definition:</b><br/>"
        "In modern digital platforms, information overload degrades user experiences, leading to high bounce rates and lost engagement opportunities. "
        "The objective of the RecoMart Recommendation System is to maximize user engagement and conversion rates by presenting personalized, highly relevant catalog suggestions. "
        "This project implements a Collaborative Filtering pipeline using an explicit matrix factorization approach (SVD) to model historical user-item interactions and predict ratings on unseen inventory. "
        "By serving these recommendations, the platform directly optimizes click-through rates (CTR) and customer retention.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # Section 1.2
    story.append(Paragraph("<b>1.2 Key Data Sources and Attributes:</b>", h2_style))
    story.append(Paragraph(
        "The architecture ingests data from two distinct channels to simulate an enterprise ecosystem: "
        "a static historical interaction dataset (MovieLens 100K) and an external live product catalog API.",
        body_style
    ))

    # Data Table
    data = [
        [Paragraph("<b>Entity / Dataset</b>", body_style),
         Paragraph("<b>Key Attributes & Descriptions</b>", body_style)],
        [Paragraph("<b>Users</b><br/>(u.user / customers.csv)", body_style), Paragraph(
            "• customer_id (Unique Key)<br/>• age (Integer used for cohort binning)<br/>• gender (Categorical)<br/>• occupation (Categorical professional status)",
            body_style)],
        [Paragraph("<b>Items</b><br/>(u.item / articles.csv)", body_style), Paragraph(
            "• article_id (Unique Key)<br/>• movie_title (String descriptive metadata)<br/>• release_date (Temporal feature)<br/>• genre_0 to genre_18 (19 Binary genre flags)",
            body_style)],
        [Paragraph("<b>Interactions</b><br/>(u.data / transactions.csv)", body_style), Paragraph(
            "• customer_id (User foreign key)<br/>• article_id (Item foreign key)<br/>• rating (Explicit feedback score on [1, 5] scale)<br/>• timestamp (Epoch time)",
            body_style)],
        [Paragraph("<b>External Catalog API</b><br/>(products_api.csv)", body_style), Paragraph(
            "• id (API source primary key)<br/>• title, price, category, rating_rate (Auxiliary dynamic properties)",
            body_style)]
    ]

    t = Table(data, colWidths=[150, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#E2E8F0')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # Section 1.3
    story.append(Paragraph("<b>1.3 Expected Pipeline Outputs:</b>", h2_style))
    story.append(Paragraph(
        "The modular machine learning pipeline isolates execution steps to deliver clear, versioned output artifacts:",
        body_style))
    story.append(Paragraph(
        "• <b>Clean Datasets for EDA:</b> De-duplicated tables free of age/rating outliers, median-imputed values, and standardized visual summary charts showing user age densities, movie popularity counts, and rating sparsity matrices.",
        list_style))
    story.append(Paragraph(
        "• <b>Engineered Features:</b> Aggregated user features (such as user interaction counts and student status indicators) coupled with timestamp components parsed into offline Feature Store structures.",
        list_style))
    story.append(Paragraph(
        "• <b>Deployable Model & Inference Assets:</b> A serialized matrix-factorization SVD model binary (recommendation_model.pkl) and a high-performance script delivering targeted Top-10 output tables (recommendations.csv) for end-consumers.",
        list_style))

    story.append(Spacer(1, 10))

    # Section 1.4
    story.append(Paragraph("<b>1.4 Pipeline Evaluation Metrics:</b>", h2_style))
    story.append(Paragraph("Performance is tracked across two primary paradigms:", body_style))
    story.append(Paragraph(
        "• <b>Offline Prediction Quality (RMSE):</b> Evaluates how closely predicted rating scores map to real user values.",
        list_style))
    story.append(Paragraph(
        "• <b>Retrieval Ranking Metrics (Precision@K and Recall@K, where K=10):</b> Evaluates the system's accuracy in placing highly rated, relevant items within the user's top recommended slots.",
        list_style))

    doc.build(story)
    print(f"✓ PDF successfully built and saved as: {pdf_filename}")


if __name__ == "__main__":
    create_report()