# spam_detector_ai/formatting/legal_templates.py
"""
Legal compliance templates and disclaimers for spam detection services.
Provides templates for terms of service, privacy notices, and data processing disclaimers.
"""

from typing import Dict


class LegalTemplates:
    """Provides legal compliance templates in multiple languages."""

    def __init__(self, language: str = 'en'):
        """
        Initialize legal templates.

        Args:
            language: Language code (en, es, fr, de)
        """
        self.language = language
        self._load_templates()

    def _load_templates(self):
        """Load legal templates for the specified language."""
        self.templates = {
            'en': {
                'disclaimer': (
                    "DISCLAIMER: This spam detection service is provided as-is without "
                    "any warranty. While we strive for accuracy, no automated system is "
                    "perfect. False positives and false negatives may occur. Users are "
                    "responsible for reviewing flagged content and making final decisions."
                ),
                'data_processing': (
                    "DATA PROCESSING NOTICE: This service analyzes email content including "
                    "URLs, sender information, and message text to determine spam likelihood. "
                    "No personal data is permanently stored. Analysis is performed in real-time "
                    "and results are provided immediately."
                ),
                'terms_of_service': (
                    "TERMS OF SERVICE: By using this spam detection service, you agree to: "
                    "(1) Use the service lawfully and ethically, "
                    "(2) Not attempt to reverse engineer or compromise the system, "
                    "(3) Accept that the service is provided without guarantees of accuracy, "
                    "(4) Understand that final decisions about content are your responsibility."
                ),
                'privacy_notice': (
                    "PRIVACY NOTICE: We respect your privacy. Email content is analyzed "
                    "transiently and not stored permanently. We do not share, sell, or "
                    "distribute your data to third parties. Analysis is performed using "
                    "machine learning models and heuristic rules locally."
                ),
                'legal_compliance': (
                    "LEGAL COMPLIANCE: This service complies with applicable data protection "
                    "regulations. Users are responsible for ensuring their use of this service "
                    "complies with relevant laws in their jurisdiction, including CAN-SPAM Act, "
                    "GDPR, and other anti-spam legislation."
                )
            },
            'es': {
                'disclaimer': (
                    "DESCARGO DE RESPONSABILIDAD: Este servicio de detección de spam se "
                    "proporciona tal cual, sin ninguna garantía. Aunque nos esforzamos por la "
                    "precisión, ningún sistema automatizado es perfecto. Pueden ocurrir falsos "
                    "positivos y falsos negativos. Los usuarios son responsables de revisar el "
                    "contenido marcado y tomar decisiones finales."
                ),
                'data_processing': (
                    "AVISO DE PROCESAMIENTO DE DATOS: Este servicio analiza el contenido del "
                    "correo electrónico, incluidas las URL, la información del remitente y el "
                    "texto del mensaje para determinar la probabilidad de spam. No se almacenan "
                    "datos personales de forma permanente. El análisis se realiza en tiempo real "
                    "y los resultados se proporcionan de inmediato."
                ),
                'terms_of_service': (
                    "TÉRMINOS DE SERVICIO: Al usar este servicio de detección de spam, usted "
                    "acepta: (1) Usar el servicio de manera legal y ética, "
                    "(2) No intentar aplicar ingeniería inversa o comprometer el sistema, "
                    "(3) Aceptar que el servicio se proporciona sin garantías de precisión, "
                    "(4) Entender que las decisiones finales sobre el contenido son su "
                    "responsabilidad."
                ),
                'privacy_notice': (
                    "AVISO DE PRIVACIDAD: Respetamos su privacidad. El contenido del correo "
                    "electrónico se analiza de forma transitoria y no se almacena permanentemente. "
                    "No compartimos, vendemos ni distribuimos sus datos a terceros. El análisis se "
                    "realiza mediante modelos de aprendizaje automático y reglas heurísticas "
                    "localmente."
                ),
                'legal_compliance': (
                    "CUMPLIMIENTO LEGAL: Este servicio cumple con las regulaciones aplicables de "
                    "protección de datos. Los usuarios son responsables de garantizar que su uso "
                    "de este servicio cumpla con las leyes pertinentes en su jurisdicción, "
                    "incluida la Ley CAN-SPAM, GDPR y otra legislación anti-spam."
                )
            },
            'fr': {
                'disclaimer': (
                    "AVERTISSEMENT : Ce service de détection de spam est fourni tel quel, sans "
                    "aucune garantie. Bien que nous nous efforcions d'être précis, aucun système "
                    "automatisé n'est parfait. Des faux positifs et des faux négatifs peuvent "
                    "survenir. Les utilisateurs sont responsables de l'examen du contenu signalé "
                    "et de la prise de décisions finales."
                ),
                'data_processing': (
                    "AVIS DE TRAITEMENT DES DONNÉES : Ce service analyse le contenu des e-mails, "
                    "y compris les URL, les informations sur l'expéditeur et le texte du message "
                    "pour déterminer la probabilité de spam. Aucune donnée personnelle n'est "
                    "stockée de manière permanente. L'analyse est effectuée en temps réel et les "
                    "résultats sont fournis immédiatement."
                ),
                'terms_of_service': (
                    "CONDITIONS D'UTILISATION : En utilisant ce service de détection de spam, "
                    "vous acceptez de : (1) Utiliser le service de manière légale et éthique, "
                    "(2) Ne pas tenter de procéder à une ingénierie inverse ou de compromettre "
                    "le système, (3) Accepter que le service soit fourni sans garantie de précision, "
                    "(4) Comprendre que les décisions finales concernant le contenu sont de votre "
                    "responsabilité."
                ),
                'privacy_notice': (
                    "AVIS DE CONFIDENTIALITÉ : Nous respectons votre vie privée. Le contenu des "
                    "e-mails est analysé de manière transitoire et n'est pas stocké de manière "
                    "permanente. Nous ne partageons, ne vendons ni ne distribuons vos données à "
                    "des tiers. L'analyse est effectuée à l'aide de modèles d'apprentissage "
                    "automatique et de règles heuristiques localement."
                ),
                'legal_compliance': (
                    "CONFORMITÉ LÉGALE : Ce service est conforme aux réglementations applicables "
                    "en matière de protection des données. Les utilisateurs sont responsables de "
                    "s'assurer que leur utilisation de ce service est conforme aux lois pertinentes "
                    "dans leur juridiction, y compris la loi CAN-SPAM, le RGPD et d'autres "
                    "législations anti-spam."
                )
            },
            'de': {
                'disclaimer': (
                    "HAFTUNGSAUSSCHLUSS: Dieser Spam-Erkennungsdienst wird wie besehen ohne "
                    "jegliche Gewährleistung bereitgestellt. Obwohl wir uns um Genauigkeit "
                    "bemühen, ist kein automatisiertes System perfekt. Falsch-positive und "
                    "falsch-negative Ergebnisse können auftreten. Benutzer sind dafür "
                    "verantwortlich, gekennzeichnete Inhalte zu überprüfen und endgültige "
                    "Entscheidungen zu treffen."
                ),
                'data_processing': (
                    "DATENVERARBEITUNGSHINWEIS: Dieser Dienst analysiert E-Mail-Inhalte "
                    "einschließlich URLs, Absenderinformationen und Nachrichtentext, um die "
                    "Spam-Wahrscheinlichkeit zu bestimmen. Es werden keine personenbezogenen "
                    "Daten dauerhaft gespeichert. Die Analyse erfolgt in Echtzeit und die "
                    "Ergebnisse werden sofort bereitgestellt."
                ),
                'terms_of_service': (
                    "NUTZUNGSBEDINGUNGEN: Durch die Nutzung dieses Spam-Erkennungsdienstes "
                    "stimmen Sie zu: (1) Den Dienst rechtmäßig und ethisch zu nutzen, "
                    "(2) Nicht zu versuchen, das System zurückzuentwickeln oder zu kompromittieren, "
                    "(3) Zu akzeptieren, dass der Dienst ohne Genauigkeitsgarantien bereitgestellt "
                    "wird, (4) Zu verstehen, dass endgültige Entscheidungen über Inhalte in Ihrer "
                    "Verantwortung liegen."
                ),
                'privacy_notice': (
                    "DATENSCHUTZHINWEIS: Wir respektieren Ihre Privatsphäre. E-Mail-Inhalte "
                    "werden vorübergehend analysiert und nicht dauerhaft gespeichert. Wir teilen, "
                    "verkaufen oder verteilen Ihre Daten nicht an Dritte. Die Analyse erfolgt "
                    "lokal unter Verwendung von maschinellen Lernmodellen und heuristischen Regeln."
                ),
                'legal_compliance': (
                    "RECHTLICHE KONFORMITÄT: Dieser Dienst entspricht den geltenden "
                    "Datenschutzbestimmungen. Benutzer sind dafür verantwortlich sicherzustellen, "
                    "dass ihre Nutzung dieses Dienstes den relevanten Gesetzen in ihrer "
                    "Gerichtsbarkeit entspricht, einschließlich CAN-SPAM Act, DSGVO und anderer "
                    "Anti-Spam-Gesetzgebung."
                )
            }
        }

    def get_disclaimer(self) -> str:
        """Get the disclaimer text in the current language."""
        return self.templates.get(self.language, self.templates['en'])['disclaimer']

    def get_data_processing_notice(self) -> str:
        """Get the data processing notice in the current language."""
        return self.templates.get(self.language, self.templates['en'])['data_processing']

    def get_terms_of_service(self) -> str:
        """Get the terms of service in the current language."""
        return self.templates.get(self.language, self.templates['en'])['terms_of_service']

    def get_privacy_notice(self) -> str:
        """Get the privacy notice in the current language."""
        return self.templates.get(self.language, self.templates['en'])['privacy_notice']

    def get_legal_compliance(self) -> str:
        """Get the legal compliance notice in the current language."""
        return self.templates.get(self.language, self.templates['en'])['legal_compliance']

    def get_all_notices(self) -> Dict[str, str]:
        """Get all legal notices as a dictionary."""
        return self.templates.get(self.language, self.templates['en'])

    def format_footer(self) -> str:
        """Format a complete legal footer with all notices."""
        t = self.templates.get(self.language, self.templates['en'])
        footer_lines = [
            '=' * 70,
            '',
            t['disclaimer'],
            '',
            '-' * 70,
            '',
            t['privacy_notice'],
            '',
            '-' * 70,
            '',
            t['legal_compliance'],
            '',
            '=' * 70
        ]
        return '\n'.join(footer_lines)
