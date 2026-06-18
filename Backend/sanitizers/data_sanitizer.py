import re
import html


class DataSanitizer:
    @staticmethod
    def sanitize_string(value: str, max_length: int = 255) -> str:
        """Remove XSS-risky chars, trim whitespace, enforce length"""
        if not value:
            return value
        value = value.strip()
        value = html.escape(value)
        value = value.replace('\x00', '')
        if len(value) > max_length:
            value = value[:max_length]
        return value

    @staticmethod
    def sanitize_email(value: str) -> str:
        """Sanitize email address"""
        value = value.strip().lower()
        value = re.sub(r'\.+', '.', value)
        return value

    @staticmethod
    def sanitize_phone(value: str) -> str:
        """Keep only digits and +"""
        return re.sub(r'[^\d+\-()]', '', value)

    @staticmethod
    def sanitize_dni(value: str) -> str:
        """Keep only alphanumeric"""
        return re.sub(r'[^a-zA-Z0-9]', '', value).upper()
