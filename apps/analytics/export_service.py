"""
Export service for generating CSV and PDF reports.
"""

import csv
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from config.mongodb import get_collection


class ExportService:
    """Service for exporting application data."""

    def __init__(self):
        self.applications_collection = get_collection('applications')

    def export_applications_csv(self, user_id, filters=None):
        """Export applications to CSV format."""
        # Build query
        query = {'user_id': user_id}

        if filters:
            if filters.get('status'):
                query['application.status'] = filters['status']
            if filters.get('company'):
                query['company.name'] = {
                    '$regex': filters['company'], '$options': 'i'}

        # Get applications
        applications = list(
            self.applications_collection.find(query).sort('created_at', -1)
        )

        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            'Company',
            'Job Title',
            'Status',
            'Applied Date',
            'Source',
            'Employment Type',
            'Work Mode',
            'Experience Level',
            'Salary Min',
            'Salary Max',
            'Location',
            'Industry',
            'Notes'
        ])

        # Write data
        for app in applications:
            company = app.get('company', {})
            job = app.get('job', {})
            application = app.get('application', {})

            writer.writerow([
                company.get('name', ''),
                job.get('title', ''),
                application.get('status', ''),
                application.get('applied_date', '').strftime(
                    '%Y-%m-%d') if application.get('applied_date') else '',
                application.get('source', ''),
                job.get('employment_type', ''),
                job.get('work_mode', ''),
                job.get('experience_level', ''),
                job.get('salary_min', ''),
                job.get('salary_max', ''),
                company.get('location', ''),
                company.get('industry', ''),
                app.get('notes', '')
            ])

        return output.getvalue()

    def export_applications_pdf(self, user_id, filters=None):
        """Export applications to PDF format."""
        # Build query
        query = {'user_id': user_id}

        if filters:
            if filters.get('status'):
                query['application.status'] = filters['status']

        # Get applications
        applications = list(
            self.applications_collection.find(query).sort('created_at', -1)
        )

        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12
        )

        # Title
        elements.append(Paragraph('Job Application Report', title_style))
        elements.append(Paragraph(
            f'Generated on {datetime.now().strftime("%B %d, %Y")}', styles['Normal']))
        elements.append(Spacer(1, 20))

        # Summary statistics
        status_counts = {}
        for app in applications:
            status = app.get('application', {}).get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1

        elements.append(Paragraph('Summary Statistics', heading_style))

        summary_data = [
            ['Metric', 'Value'],
            ['Total Applications', str(len(applications))],
        ]

        for status, count in sorted(status_counts.items()):
            summary_data.append([status.title(), str(count)])

        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 30))

        # Applications list
        elements.append(Paragraph('Applications List', heading_style))
        elements.append(Spacer(1, 12))

        for i, app in enumerate(applications[:50], 1):  # Limit to 50 for PDF
            company = app.get('company', {})
            job = app.get('job', {})
            application = app.get('application', {})

            app_data = [
                ['Company', company.get('name', 'N/A')],
                ['Position', job.get('title', 'N/A')],
                ['Status', application.get('status', 'N/A').title()],
                ['Applied', application.get('applied_date', '').strftime(
                    '%Y-%m-%d') if application.get('applied_date') else 'N/A'],
                ['Source', application.get('source', 'N/A')],
            ]

            if job.get('salary_min'):
                salary = f"${job.get('salary_min', 0):,} - ${job.get('salary_max', 0):,}"
                app_data.append(['Salary Range', salary])

            app_table = Table(app_data, colWidths=[1.5*inch, 4.5*inch])
            app_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))

            elements.append(app_table)
            elements.append(Spacer(1, 15))

            # Page break every 5 applications
            if i % 5 == 0 and i < len(applications):
                elements.append(PageBreak())

        # Build PDF
        doc.build(elements)

        return buffer.getvalue()

    def export_analytics_csv(self, user_id):
        """Export analytics data to CSV."""
        # Get statistics
        from apps.analytics.services import AnalyticsService
        analytics_service = AnalyticsService()

        dashboard_stats = analytics_service.get_dashboard_stats(user_id)
        apps_over_time = analytics_service.get_applications_over_time(
            user_id, 'month')
        skills_demand = analytics_service.get_skills_demand(user_id)

        output = io.StringIO()
        writer = csv.writer(output)

        # Dashboard stats
        writer.writerow(['DASHBOARD STATISTICS'])
        writer.writerow(['Metric', 'Value'])
        writer.writerow(
            ['Total Applications', dashboard_stats['total_applications']])
        writer.writerow(
            ['Success Rate', f"{dashboard_stats['success_rate']}%"])
        writer.writerow(
            ['Response Rate', f"{dashboard_stats['response_rate']}%"])
        writer.writerow(['Applications Last 30 Days',
                        dashboard_stats['applications_last_30_days']])
        writer.writerow([])

        # Status breakdown
        writer.writerow(['STATUS BREAKDOWN'])
        writer.writerow(['Status', 'Count'])
        for status, count in dashboard_stats['status_breakdown'].items():
            writer.writerow([status, count])
        writer.writerow([])

        # Applications over time
        writer.writerow(['APPLICATIONS OVER TIME'])
        writer.writerow(['Period', 'Count'])
        for item in apps_over_time:
            writer.writerow([item['period'], item['count']])
        writer.writerow([])

        # Skills demand
        writer.writerow(['TOP SKILLS DEMANDED'])
        writer.writerow(['Skill', 'Count'])
        for item in skills_demand[:20]:
            writer.writerow([item['skill'], item['count']])

        return output.getvalue()

    def export_companies_csv(self, user_id):
        """Export companies to CSV."""
        companies_collection = get_collection('companies')

        companies = list(
            companies_collection.find({'user_id': user_id}).sort('name', 1)
        )

        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            'Company Name',
            'Industry',
            'Size',
            'Location',
            'Website',
            'Glassdoor Rating',
            'Is Favorite',
            'Tags',
            'Notes'
        ])

        # Write data
        for company in companies:
            # Count applications
            app_count = self.applications_collection.count_documents({
                'user_id': user_id,
                'company.name': company['name']
            })

            writer.writerow([
                company.get('name', ''),
                company.get('industry', ''),
                company.get('size', ''),
                company.get('location', ''),
                company.get('website', ''),
                company.get('glassdoor_rating', ''),
                company.get('is_favorite', False),
                ', '.join(company.get('tags', [])),
                company.get('notes', '')
            ])

        return output.getvalue()
