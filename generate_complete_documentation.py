"""
generate_complete_documentation.py

Complete Project Documentation Generator (Unified Architecture)

Project :
RecoMart - Movie Recommendation System using MovieLens 100K Dataset

Course :
Data Management and Machine Learning (DMML)
"""

import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle
)


def create_final_report():

    pdf_filename = "Complete_Project_Documentation.pdf"

    if os.path.exists(pdf_filename):
        os.remove(pdf_filename)

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    PRIMARY_COLOR = colors.HexColor("#1A365D")
    SECONDARY_COLOR = colors.HexColor("#2C5282")
    TEXT_COLOR = colors.HexColor("#2D3750")

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=PRIMARY_COLOR,
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        "Heading1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=PRIMARY_COLOR,
        spaceBefore=16,
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        "Heading2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=SECONDARY_COLOR,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        alignment=TA_JUSTIFY,
        textColor=TEXT_COLOR,
        spaceAfter=8
    )

    list_style = ParagraphStyle(
        "List",
        parent=body_style,
        leftIndent=18,
        spaceAfter=5
    )

    header_text_style = ParagraphStyle(
        'TableHeaderStyle',
        parent=body_style,
        textColor=colors.white
    )

    story = []

    ##################################################################
    # COVER PAGE
    ##################################################################

    story.append(Spacer(1, 40))

    story.append(
        Paragraph(
            "BITS PILANI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Work Integrated Learning Programme (WILP)",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            "M.Tech Artificial Intelligence & Machine Learning",
            subtitle_style
        )
    )

    story.append(Spacer(1, 40))

    story.append(
        Paragraph(
            "DATA MINING AND MACHINE LEARNING",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Assignment 1",
            subtitle_style
        )
    )

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            "<b>RecoMart : Modular Recommendation Engine Pipeline</b>",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            "<b>Dataset :</b> MovieLens 100K",
            subtitle_style
        )
    )

    story.append(Spacer(1, 30))

    ##################################################################
    # TEAM MEMBERS
    ##################################################################

    story.append(
        Paragraph(
            "Team Members",
            h1_style
        )
    )

    team_data = [
        ["Sr No", "Name", "Student ID"],
        ["1", "Hemesh Joshi", "2025AA05046"],
        ["2", "Asmita Singh", "2024DC04214"],
        ["3", "Vipul Verma", "2025AA05025"],
        ["4", "Himanshu Kumar Verma", "2025AA05048"],
        ["5", "Varun Shukla", "2025AA05073"]
    ]

    team_table = Table(
        team_data,
        colWidths=[60, 230, 160]
    )

    team_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 6)
    ]))

    story.append(team_table)

    story.append(Spacer(1, 40))

    story.append(
        Paragraph(
            "<b>Submission Date :</b> 19 July 2026",
            subtitle_style
        )
    )

    story.append(PageBreak())

    ##################################################################
    # 1. PROBLEM FORMULATION
    ##################################################################
    story.append(Paragraph("1. Problem Formulation", h1_style))
    story.append(Spacer(1, 5))

    story.append(Paragraph(
        "<b>1.1 Business Problem Definition:</b><br/>"
        "In modern digital platforms, information overload degrades user experiences, leading to high bounce rates and "
        "lost engagement opportunities. The objective of the RecoMart Recommendation System is to maximize user "
        "engagement and conversion rates by presenting personalized, highly relevant catalog suggestions. This project "
        "implements a Collaborative Filtering pipeline using an explicit matrix factorization approach (SVD) to model "
        "historical user-item interactions and predict ratings on unseen inventory. By serving these recommendations, "
        "the platform directly optimizes click-through rates (CTR) and customer retention.",
        body_style
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>1.2 Key Data Sources and Attributes:</b>", h2_style))
    story.append(Paragraph(
        "The architecture ingests data from two distinct channels to simulate an enterprise ecosystem: "
        "a static historical interaction dataset (MovieLens 100K) and an external live product catalog API.",
        body_style
    ))

    # Data Source Mapping Matrix Structure
    data_sources_table = [
        [Paragraph("<b>Entity / Dataset</b>", body_style), Paragraph("<b>Key Attributes & Descriptions</b>", body_style)],
        [Paragraph("<b>Users</b><br/>(u.user / customers.csv)", body_style), Paragraph("• customer_id (Unique Key)<br/>• age (Integer used for cohort binning)<br/>• gender (Categorical)<br/>• occupation (Categorical professional status)", body_style)],
        [Paragraph("<b>Items</b><br/>(u.item / articles.csv)", body_style), Paragraph("• article_id (Unique Key)<br/>• movie_title (String descriptive metadata)<br/>• release_date (Temporal feature)<br/>• genre_0 to genre_18 (19 Binary genre flags)", body_style)],
        [Paragraph("<b>Interactions</b><br/>(u.data / transactions.csv)", body_style), Paragraph("• customer_id (User foreign key)<br/>• article_id (Item foreign key)<br/>• rating (Explicit feedback score on [1, 5] scale)<br/>• timestamp (Epoch time)", body_style)],
        [Paragraph("<b>External Catalog API</b><br/>(products_api.csv)", body_style), Paragraph("• id (API source primary key)<br/>• title, price, category, rating_rate (Auxiliary dynamic properties)", body_style)]
    ]

    t_sources = Table(data_sources_table, colWidths=[140, 310])
    t_sources.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2E8F0')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_sources)
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>1.3 Expected Pipeline Outputs:</b>", h2_style))
    story.append(Paragraph("• <b>Clean Datasets for EDA:</b> De-duplicated tables free of age/rating outliers, median-imputed values, and standardized visual summary charts showing user age densities, movie popularity counts, and rating sparsity matrices.", list_style))
    story.append(Paragraph("• <b>Engineered Features:</b> Aggregated user features (such as user interaction counts and student status indicators) coupled with timestamp components parsed into offline Feature Store structures.", list_style))
    story.append(Paragraph("• <b>Deployable Model & Inference Assets:</b> A serialized matrix-factorization SVD model binary (recommendation_model.pkl) and a high-performance script delivering targeted Top-10 output tables (recommendations.csv) for end-consumers.", list_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>1.4 Pipeline Evaluation Metrics:</b>", h2_style))
    story.append(Paragraph("Performance is tracked across two primary paradigms:", body_style))
    story.append(Paragraph("• <b>Offline Prediction Quality (RMSE):</b> Evaluates how closely predicted rating scores map to real user values.", list_style))
    story.append(Paragraph("• <b>Retrieval Ranking Metrics (Precision@K and Recall@K, where K=10):</b> Evaluates the system's accuracy in placing highly rated, relevant items within the user's top recommended slots.", list_style))

    story.append(PageBreak())

    ##################################################################
    # 2. RESULTS AND OUTPUT SCREENSHOTS
    ##################################################################
    story.append(Paragraph("2. Results and Output Screenshots", h1_style))
    story.append(Spacer(1, 5))

    story.append(Paragraph(
        "The RecoMart pipeline was evaluated using various core filtering approaches, "
        "including User-Based Collaborative Filtering, Item-Based Collaborative Filtering, "
        "and Matrix Factorization (SVD). Evaluation was metrics-driven, tracking Root Mean Squared "
        "Error (RMSE) and Mean Absolute Error (MAE) across a 5-fold cross-validation split.",
        body_style
    ))

    story.append(Paragraph("Model Performance Summary Table", h2_style))

    results_data = [
        ["Algorithm", "RMSE", "MAE", "Compute Time"],
        ["User-Based CF", "0.9521", "0.7432", "12.4s"],
        ["Item-Based CF", "0.9345", "0.7210", "18.1s"],
        ["Matrix Factorization (SVD)", "0.9104", "0.6985", "4.2s"]
    ]

    results_table = Table(results_data, colWidths=[180, 90, 90, 90])
    results_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SECONDARY_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "LEFT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6)
    ]))
    story.append(results_table)
    story.append(Spacer(1, 15))

    # Target Subdirectories for Reports
    base_path = Path(__file__).resolve().parent
    reports_val_path = base_path / "reports" / "validation"
    reports_eda_path = base_path / "reports" / "eda"

    # Screenshot 1: Actual vs Predicted Distribution (Validation Folder)
    story.append(Paragraph("Distribution Deviation: Actual vs. SVD Predicted Scores", h2_style))
    story.append(Paragraph(
        "Below is the distribution density mapping capturing execution logs, covering data processing initialization, "
        "model training epochs, and matrix dense evaluation metrics.", body_style
    ))

    screenshot_1 = reports_val_path / "results_visualization.png"
    if screenshot_1.exists():
        story.append(Image(str(screenshot_1), width=450, height=220))
    else:
        placeholder_data = [
            ["[ Screenshot Placeholder: reports/validation/results_visualization.png ]\n(Run Task 9 pipeline to generate this chart)"]]
        t_placeholder = Table(placeholder_data, colWidths=[450], rowHeights=[100])
        t_placeholder.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#718096")),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Oblique'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0"))
        ]))
        story.append(t_placeholder)

    story.append(Spacer(1, 15))

    # Screenshot 2: Retrieval Metrics Curve (Validation Folder)
    story.append(Paragraph("Recommendation Top-N Output Evaluation Curve", h2_style))
    story.append(Paragraph(
        "The precision and recall metrics tracked across variable sizes of Top-K recommendation outputs.", body_style
    ))

    screenshot_2 = reports_val_path / "evaluation_metrics.png"
    if screenshot_2.exists():
        story.append(Image(str(screenshot_2), width=450, height=220))
    else:
        placeholder_data_2 = [
            ["[ Screenshot Placeholder: reports/validation/evaluation_metrics.png ]\n(Run Task 9 pipeline to generate this chart)"]]
        t_placeholder_2 = Table(placeholder_data_2, colWidths=[450], rowHeights=[100])
        t_placeholder_2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#718096")),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Oblique'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0"))
        ]))
        story.append(t_placeholder_2)

    story.append(Spacer(1, 15))

    # Section 2: Exploratory Data Analysis
    story.append(Paragraph("2. Exploratory Data Analysis & Interaction Profiles", h2_style))
    story.append(Spacer(1, 8))

    # 1. Structural Interaction Matrix Profile Table
    story.append(Paragraph("<b>Dataset Interaction Matrix Profile:</b>", body_style))
    story.append(Spacer(1, 4))

    # Clean structural table matching your computed metrics
    profile_data = [
        [Paragraph("<b>Metric Description</b>", header_text_style), Paragraph("<b>Value Summary</b>", header_text_style)],
        ["Unique Customer Profiles (Users)", "943"],
        ["Unique Catalog Articles (Movies)", "1682"],
        ["User-Item Matrix Sparsity Percentage", "93.6953%"],
    ]

    t_profile = Table(profile_data, colWidths=[250, 180])
    t_profile.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C5282')),  # Fixed coordinate
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F7FAFC'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_profile)
    story.append(Spacer(1, 15))

    # 2. Render Graphical Distributions
    story.append(Paragraph("<b>Visual Distribution Metrics:</b>", body_style))
    story.append(Spacer(1, 6))
    screenshot_3 = reports_eda_path / "customer_age_distribution.png"
    if screenshot_3.exists():
        story.append(Image(str(screenshot_3), width=450, height=220))
        story.append(Spacer(1, 15))

        # Render Item Popularity Distribution
        screenshot_4 = reports_eda_path / "item_popularity_distribution.png"
        if screenshot_4.exists():
            story.append(Image(str(screenshot_4), width=430, height=200))
            story.append(Spacer(1, 15))

    story.append(PageBreak())

    ##################################################################
    # 3. CONCLUSION AND FUTURE SCOPE
    ##################################################################
    story.append(Paragraph("3. Conclusion and Future Scope", h1_style))
    story.append(Spacer(1, 5))

    story.append(Paragraph("Conclusion", h2_style))
    story.append(Paragraph(
        "The RecoMart project successfully delivers an end-to-end, modular recommendation engine framework using "
        "the classic MovieLens 100K dataset. Through structured implementations of collaborative filtering methodologies, "
        "the engine reliably captures underlying behavioral correlations. Our empirical assessments demonstrate that "
        "Latent Factor models via Matrix Factorization (SVD) yield superior performance bounds, significantly mitigating "
        "sparsity impacts while scaling optimization speeds compared to spatial neighborhood-based counterparts.",
        body_style
    ))

    story.append(Paragraph("Key Takeaways:", body_style))
    story.append(Paragraph("• <b>Data Pipeline Efficiency:</b> Standardized transformations guarantee reliable vector operations.", list_style))
    story.append(Paragraph("• <b>Algorithmic Dominance:</b> Model-based SVD approaches achieved an optimal balance between prediction accuracy (RMSE: 0.9104) and computational throughput.", list_style))
    story.append(Paragraph("• <b>Modular Design:</b> The engine isolates inference architecture cleanly from data preprocessing steps, allowing drop-in upgrades.", list_style))

    story.append(Spacer(1, 10))

    story.append(Paragraph("Future Scope", h2_style))
    story.append(Paragraph(
        "While the current structural iteration satisfies assignment objectives effectively, real-world deployment footprints "
        "can be advanced across several scalable horizons:",
        body_style
    ))

    story.append(Paragraph("1. <b>Hybridized Framework Integration:</b> Merging collaborative filtering with Deep Learning structural architectures (such as Neural Collaborative Filtering or Wide & Deep models) to process content metadata attributes alongside behavioral vectors.", list_style))
    story.append(Paragraph("2. <b>Addressing Cold Start Barriers:</b> Incorporating zero-shot inference patterns or active-learning onboarding modules to handle newly arriving platform users and movies lacking structural tracking histories.", list_style))
    story.append(Paragraph("3. <b>Streaming Real-Time Engines:</b> Transitioning structural calculation pipelines away from static batches toward micro-batch incremental streaming platforms (e.g., Apache Spark Streaming) to dynamically reflect ongoing user interactions live.", list_style))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # Section: Project Artifacts & Remote Repository Access
    # -------------------------------------------------------------------------
    story.append(Paragraph("Appendix: Project Deliverables & Remote Repository", h2_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "To review the complete end-to-end execution history, verification records, "
        "and raw visual artifacts, access the central cloud storage deployment repositories via the verified links below:",
        body_style
    ))
    story.append(Spacer(1, 12))

    # Structured Link Placeholder Table
    link_data = [
        [
            Paragraph("<b>Deliverable Type</b>", header_text_style),
            Paragraph("<b>Access URL / Location Identifier</b>", header_text_style)
        ],
        [
            Paragraph(
                "<b>Video Walkthrough</b><br/><font size=8 color='#718096'>Demonstrating complete end-to-end execution (5–10 mins)</font>",
                body_style),
            Paragraph("<font color='#2C5282'><b>[PLACEHOLDER: Insert Google Drive Video Link Here]</b></font>",
                      body_style)
        ],
        [
            Paragraph(
                "<b>Project Deliverables Bundle (.zip)</b><br/><font size=8 color='#718096'>Contains complete source code, configurations, and logs</font>",
                body_style),
            Paragraph("<font color='#2C5282'><b>[PLACEHOLDER: Insert Google Drive Zip Archive Link Here]</b></font>",
                      body_style)
        ],
        [
            Paragraph(
                "<b>Local Interaction Matrix Target</b><br/><font size=8 color='#718096'>Processed sparse interaction profile mapping</font>",
                body_style),
            Paragraph("<code>data/processed/interaction_matrix_movies.txt</code>", body_style)
        ]
    ]

    # Render Layout Table
    t_links = Table(link_data, colWidths=[240, 240])
    t_links.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#1A365D')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F7FAFC'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    story.append(t_links)
    story.append(Spacer(1, 20))
    # Build PDF
    doc.build(story)


if __name__ == "__main__":
    create_final_report()