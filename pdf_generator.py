from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import HexColor
from datetime import datetime
import io
import logging

def generate_policy_report(policy, prediction):
    """
    Generate a comprehensive PDF report for a policy and its predictions
    """
    buffer = io.BytesIO()
    
    try:
        # Create PDF document
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                              rightMargin=72, leftMargin=72, 
                              topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        # Title Page
        elements.append(Paragraph("Policy Impact Analysis Report", title_style))
        elements.append(Spacer(1, 12))
        
        # Policy Information Section
        elements.append(Paragraph("Policy Overview", heading_style))
        
        policy_data = [
            ['Policy Name', policy.name],
            ['Sector', policy.sector],
            ['Region', policy.region],
            ['Numeric Change', f"{policy.numeric_change:+.1f}%"],
            ['Time Period', f"{policy.time_period} months"],
            ['Analysis Date', datetime.now().strftime("%B %d, %Y")]
        ]
        
        policy_table = Table(policy_data, colWidths=[2*inch, 4*inch])
        policy_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(policy_table)
        elements.append(Spacer(1, 20))
        
        # Policy Description
        if policy.description:
            elements.append(Paragraph("Policy Description", heading_style))
            elements.append(Paragraph(policy.description, styles['Normal']))
            elements.append(Spacer(1, 20))
        
        # Economic Impact Predictions
        elements.append(Paragraph("Economic Impact Predictions", heading_style))
        
        impact_data = [
            ['Economic Indicator', 'Predicted Impact', 'Interpretation'],
            ['GDP Growth', f"{prediction.gdp_impact:+.2f}%", _interpret_gdp(prediction.gdp_impact)],
            ['Inflation', f"{prediction.inflation_impact:+.2f} pp", _interpret_inflation(prediction.inflation_impact)],
            ['Unemployment', f"{prediction.unemployment_impact:+.2f} pp", _interpret_unemployment(prediction.unemployment_impact)],
            ['Environmental Impact', f"{prediction.environmental_impact:+.2f}%", _interpret_environment(prediction.environmental_impact)]
        ]
        
        impact_table = Table(impact_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
        impact_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        elements.append(impact_table)
        elements.append(Spacer(1, 20))
        
        # Confidence and Sentiment
        elements.append(Paragraph("Analysis Confidence", heading_style))
        
        confidence_data = [
            ['Metric', 'Score', 'Level'],
            ['Prediction Confidence', f"{prediction.confidence_score:.2f}", _get_confidence_level(prediction.confidence_score)],
            ['Public Sentiment', f"{prediction.sentiment_score:+.2f}", _get_sentiment_level(prediction.sentiment_score)],
        ]
        
        confidence_table = Table(confidence_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
        confidence_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(confidence_table)
        elements.append(Spacer(1, 30))
        
        # Sector-wise Breakdown
        if prediction.get_sector_breakdown():
            elements.append(Paragraph("Sector-wise Impact Breakdown", heading_style))
            
            sector_breakdown = prediction.get_sector_breakdown()
            sector_data = [['Sector', 'GDP Impact (%)', 'Employment Impact (%)', 'Overall Impact (%)']]
            
            for sector, impacts in sector_breakdown.items():
                sector_data.append([
                    sector,
                    f"{impacts.get('gdp_impact', 0):+.2f}",
                    f"{impacts.get('employment_impact', 0):+.2f}",
                    f"{impacts.get('impact_percentage', 0):.1f}"
                ])
            
            sector_table = Table(sector_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            sector_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            elements.append(sector_table)
            elements.append(Spacer(1, 20))
        
        # Page Break
        elements.append(PageBreak())
        
        # Summary and Recommendations
        elements.append(Paragraph("Executive Summary", heading_style))
        
        summary_text = _generate_executive_summary(policy, prediction)
        elements.append(Paragraph(summary_text, styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Recommendations
        elements.append(Paragraph("Recommendations", heading_style))
        recommendations = _generate_recommendations(policy, prediction)
        for rec in recommendations:
            elements.append(Paragraph(f"• {rec}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Methodology Note
        elements.append(Paragraph("Methodology", heading_style))
        methodology_text = """
        This analysis uses machine learning models trained on historical economic data and policy outcomes. 
        The predictions are based on sector-specific multipliers, regional economic factors, and established 
        economic relationships. Confidence scores reflect the certainty of predictions based on input parameters 
        and historical precedents.
        """
        elements.append(Paragraph(methodology_text, styles['Normal']))
        
        # Footer
        elements.append(Spacer(1, 30))
        footer_text = f"Generated by Policy Impact Simulator | {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=1
        )
        elements.append(Paragraph(footer_text, footer_style))
        
        # Build PDF
        doc.build(elements)
        
        # Get the value of the BytesIO buffer
        pdf_value = buffer.getvalue()
        buffer.close()
        
        return pdf_value
        
    except Exception as e:
        logging.error(f"Error generating PDF: {str(e)}")
        buffer.close()
        raise e

def _interpret_gdp(gdp_impact):
    """Interpret GDP impact value"""
    if gdp_impact > 2:
        return "Significant positive growth"
    elif gdp_impact > 0.5:
        return "Moderate positive growth"
    elif gdp_impact > -0.5:
        return "Minimal impact"
    elif gdp_impact > -2:
        return "Moderate negative impact"
    else:
        return "Significant negative impact"

def _interpret_inflation(inflation_impact):
    """Interpret inflation impact value"""
    if inflation_impact > 1:
        return "Inflationary pressure"
    elif inflation_impact > 0.2:
        return "Mild inflation increase"
    elif inflation_impact > -0.2:
        return "Stable inflation"
    else:
        return "Deflationary pressure"

def _interpret_unemployment(unemployment_impact):
    """Interpret unemployment impact value"""
    if unemployment_impact > 1:
        return "Job losses expected"
    elif unemployment_impact > 0.2:
        return "Slight job market softening"
    elif unemployment_impact > -0.2:
        return "Stable employment"
    elif unemployment_impact > -1:
        return "Job creation expected"
    else:
        return "Significant job creation"

def _interpret_environment(env_impact):
    """Interpret environmental impact value"""
    if env_impact > 5:
        return "Negative environmental impact"
    elif env_impact > 0:
        return "Mild environmental concern"
    elif env_impact > -5:
        return "Environmental benefit"
    else:
        return "Significant environmental benefit"

def _get_confidence_level(confidence):
    """Convert confidence score to descriptive level"""
    if confidence > 0.8:
        return "High Confidence"
    elif confidence > 0.6:
        return "Medium Confidence"
    else:
        return "Low Confidence"

def _get_sentiment_level(sentiment):
    """Convert sentiment score to descriptive level"""
    if sentiment > 0.3:
        return "Positive Public Response"
    elif sentiment > -0.3:
        return "Neutral Public Response"
    else:
        return "Negative Public Response"

def _generate_executive_summary(policy, prediction):
    """Generate executive summary based on policy and predictions"""
    summary = f"""
    The proposed {policy.name} policy in the {policy.sector} sector is projected to have a 
    {_interpret_gdp(prediction.gdp_impact).lower()} on GDP growth with a 
    {prediction.gdp_impact:+.2f}% impact. The policy shows a confidence level of 
    {_get_confidence_level(prediction.confidence_score).lower()} and is expected to generate 
    {_get_sentiment_level(prediction.sentiment_score).lower()} among the public.
    
    Key economic indicators suggest the policy will result in {_interpret_inflation(prediction.inflation_impact).lower()}, 
    with unemployment effects showing {_interpret_unemployment(prediction.unemployment_impact).lower()}. 
    Environmental considerations indicate {_interpret_environment(prediction.environmental_impact).lower()}.
    """
    return summary

def _generate_recommendations(policy, prediction):
    """Generate recommendations based on analysis"""
    recommendations = []
    
    if prediction.gdp_impact < -1:
        recommendations.append("Consider gradual implementation to minimize economic disruption")
    
    if prediction.inflation_impact > 1:
        recommendations.append("Monitor inflation closely and prepare countermeasures")
    
    if prediction.unemployment_impact > 1:
        recommendations.append("Develop job retraining programs for affected workers")
    
    if prediction.confidence_score < 0.6:
        recommendations.append("Conduct additional analysis and stakeholder consultation")
    
    if prediction.environmental_impact > 5:
        recommendations.append("Implement environmental mitigation measures")
    
    if not recommendations:
        recommendations.append("Policy appears well-balanced, proceed with standard implementation")
        recommendations.append("Continue monitoring key indicators during rollout")
    
    return recommendations
