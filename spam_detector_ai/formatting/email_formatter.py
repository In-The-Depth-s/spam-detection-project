# spam_detector_ai/formatting/email_formatter.py
"""
Email formatting and layout utilities for spam detection results.
Provides structured templates for displaying spam analysis results.
"""

from typing import Dict, Optional
from datetime import datetime


class EmailFormatter:
    """Formats spam detection results into structured email layouts."""

    def __init__(self, language: str = 'en'):
        """
        Initialize the email formatter.

        Args:
            language: Language code (en, es, fr, de)
        """
        self.language = language
        self._load_templates()

    def _load_templates(self):
        """Load email templates for the specified language."""
        self.templates = {
            'en': {
                'subject': 'Spam Detection Report',
                'header': 'Spam Analysis Report',
                'spam_detected': 'SPAM DETECTED',
                'not_spam': 'NOT SPAM',
                'summary': 'Summary',
                'details': 'Detailed Analysis',
                'timestamp': 'Analysis Time',
                'message': 'Message',
                'sender': 'Sender',
                'subject_line': 'Subject',
                'verdict': 'Verdict',
                'confidence': 'Confidence Score',
                'url_analysis': 'URL Analysis',
                'email_analysis': 'Email Analysis',
                'content_analysis': 'Content Analysis'
            },
            'es': {
                'subject': 'Informe de Detección de Spam',
                'header': 'Informe de Análisis de Spam',
                'spam_detected': 'SPAM DETECTADO',
                'not_spam': 'NO ES SPAM',
                'summary': 'Resumen',
                'details': 'Análisis Detallado',
                'timestamp': 'Hora del Análisis',
                'message': 'Mensaje',
                'sender': 'Remitente',
                'subject_line': 'Asunto',
                'verdict': 'Veredicto',
                'confidence': 'Puntuación de Confianza',
                'url_analysis': 'Análisis de URL',
                'email_analysis': 'Análisis de Email',
                'content_analysis': 'Análisis de Contenido'
            },
            'fr': {
                'subject': 'Rapport de Détection de Spam',
                'header': "Rapport d'Analyse de Spam",
                'spam_detected': 'SPAM DÉTECTÉ',
                'not_spam': 'PAS DE SPAM',
                'summary': 'Résumé',
                'details': 'Analyse Détaillée',
                'timestamp': "Heure d'Analyse",
                'message': 'Message',
                'sender': 'Expéditeur',
                'subject_line': 'Sujet',
                'verdict': 'Verdict',
                'confidence': 'Score de Confiance',
                'url_analysis': "Analyse d'URL",
                'email_analysis': "Analyse d'Email",
                'content_analysis': 'Analyse de Contenu'
            },
            'de': {
                'subject': 'Spam-Erkennungsbericht',
                'header': 'Spam-Analysebericht',
                'spam_detected': 'SPAM ERKANNT',
                'not_spam': 'KEIN SPAM',
                'summary': 'Zusammenfassung',
                'details': 'Detaillierte Analyse',
                'timestamp': 'Analysezeit',
                'message': 'Nachricht',
                'sender': 'Absender',
                'subject_line': 'Betreff',
                'verdict': 'Urteil',
                'confidence': 'Konfidenzwert',
                'url_analysis': 'URL-Analyse',
                'email_analysis': 'E-Mail-Analyse',
                'content_analysis': 'Inhaltsanalyse'
            }
        }

    def format_text_report(self, analysis: Dict, message: str,
                          subject: Optional[str] = None,
                          sender: Optional[str] = None) -> str:
        """
        Format spam analysis as a text report.

        Args:
            analysis: Spam analysis results dictionary
            message: The analyzed message
            subject: Optional email subject
            sender: Optional sender email

        Returns:
            Formatted text report
        """
        t = self.templates.get(self.language, self.templates['en'])

        is_spam = analysis.get('is_spam', False)
        combined_score = analysis.get('combined_score', 0.0)

        report_lines = [
            '=' * 70,
            t['header'].center(70),
            '=' * 70,
            '',
            f"{t['timestamp']}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            '',
            f"{'='*20} {t['summary']} {'='*20}",
            '',
            f"{t['verdict']}: {t['spam_detected'] if is_spam else t['not_spam']}",
            f"{t['confidence']}: {combined_score:.2%}",
            ''
        ]

        if sender:
            report_lines.append(f"{t['sender']}: {sender}")

        if subject:
            report_lines.append(f"{t['subject_line']}: {subject}")

        report_lines.extend([
            '',
            f"{'='*20} {t['details']} {'='*20}",
            ''
        ])

        # Add detailed analysis if available
        if 'details' in analysis:
            details = analysis['details']
            if 'url_analysis' in details:
                report_lines.append(f"{t['url_analysis']}: {details['url_analysis']}")
            if 'email_analysis' in details:
                report_lines.append(f"{t['email_analysis']}: {details['email_analysis']}")
            if 'content_analysis' in details:
                report_lines.append(f"{t['content_analysis']}: {details['content_analysis']}")

        report_lines.extend([
            '',
            f"{t['message']}:",
            '-' * 70,
            message[:200] + ('...' if len(message) > 200 else ''),
            '-' * 70,
            ''
        ])

        return '\n'.join(report_lines)

    def format_html_report(self, analysis: Dict, message: str,
                          subject: Optional[str] = None,
                          sender: Optional[str] = None) -> str:
        """
        Format spam analysis as an HTML report.

        Args:
            analysis: Spam analysis results dictionary
            message: The analyzed message
            subject: Optional email subject
            sender: Optional sender email

        Returns:
            Formatted HTML report
        """
        t = self.templates.get(self.language, self.templates['en'])

        is_spam = analysis.get('is_spam', False)
        combined_score = analysis.get('combined_score', 0.0)

        verdict_color = '#d32f2f' if is_spam else '#388e3c'
        verdict_text = t['spam_detected'] if is_spam else t['not_spam']

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; color: #333; border-bottom: 3px solid #1976d2; padding-bottom: 10px; margin-bottom: 20px; }}
        .verdict {{ text-align: center; font-size: 24px; font-weight: bold; color: {verdict_color}; padding: 15px; background-color: #f9f9f9; border-radius: 5px; margin: 20px 0; }}
        .section {{ margin: 20px 0; }}
        .section-title {{ font-weight: bold; color: #1976d2; margin-bottom: 10px; font-size: 18px; }}
        .info-row {{ display: flex; margin: 8px 0; }}
        .info-label {{ font-weight: bold; min-width: 150px; color: #555; }}
        .info-value {{ color: #333; }}
        .message-box {{ background-color: #f9f9f9; padding: 15px; border-left: 4px solid #1976d2; margin: 15px 0; border-radius: 4px; }}
        .timestamp {{ text-align: right; color: #888; font-size: 12px; }}
        .details-box {{ background-color: #fff3e0; padding: 15px; border-radius: 4px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">{t['header']}</h1>
        <div class="timestamp">{t['timestamp']}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>

        <div class="verdict">{verdict_text}</div>

        <div class="section">
            <div class="section-title">{t['summary']}</div>
            <div class="info-row">
                <div class="info-label">{t['confidence']}:</div>
                <div class="info-value">{combined_score:.2%}</div>
            </div>
"""

        if sender:
            html += f"""
            <div class="info-row">
                <div class="info-label">{t['sender']}:</div>
                <div class="info-value">{sender}</div>
            </div>
"""

        if subject:
            html += f"""
            <div class="info-row">
                <div class="info-label">{t['subject_line']}:</div>
                <div class="info-value">{subject}</div>
            </div>
"""

        html += """
        </div>
"""

        # Add detailed analysis if available
        if 'details' in analysis:
            html += f"""
        <div class="section">
            <div class="section-title">{t['details']}</div>
            <div class="details-box">
"""
            details = analysis['details']
            if 'url_analysis' in details:
                html += f"<div><strong>{t['url_analysis']}:</strong> {details['url_analysis']}</div>"
            if 'email_analysis' in details:
                html += f"<div><strong>{t['email_analysis']}:</strong> {details['email_analysis']}</div>"
            if 'content_analysis' in details:
                html += f"<div><strong>{t['content_analysis']}:</strong> {details['content_analysis']}</div>"

            html += """
            </div>
        </div>
"""

        html += f"""
        <div class="section">
            <div class="section-title">{t['message']}</div>
            <div class="message-box">
                {message[:500] + ('...' if len(message) > 500 else '')}
            </div>
        </div>
    </div>
</body>
</html>
"""

        return html

    def format_json_report(self, analysis: Dict, message: str,
                          subject: Optional[str] = None,
                          sender: Optional[str] = None) -> Dict:
        """
        Format spam analysis as a JSON-serializable dictionary.

        Args:
            analysis: Spam analysis results dictionary
            message: The analyzed message
            subject: Optional email subject
            sender: Optional sender email

        Returns:
            Dictionary ready for JSON serialization
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'language': self.language,
            'verdict': 'spam' if analysis.get('is_spam', False) else 'ham',
            'confidence_score': analysis.get('combined_score', 0.0),
            'sender': sender,
            'subject': subject,
            'message_preview': message[:200],
            'analysis': analysis.get('details', {}),
            'features': {
                'ml_score': analysis.get('ml_score', 0.0),
                'feature_score': analysis.get('feature_score', 0.0)
            }
        }
