import os
import re
from typing import Union


class PlStyleMixin:
    """
    Utility class for converting standard Qt stylesheets to qproperty-compatible
    stylesheets for use in custom widgets.

    Example usage:
        qss = PlWidgetsStyleUtils.convert_stylesheet("style.css")
        widget.setStyleSheet(qss)
    """

    # Known pseudo-states to convert
    _state_map = {
        ":checked": '[checked="true"]',
        ":unchecked": '[checked="false"]',
        ":hover": '[hover="true"]',
        ":pressed": '[pressed="true"]',
        ":disabled": '[enabled="false"]',
        ":enabled": '[enabled="true"]',
        ":focus": '[focus="true"]'
    }

    def setStyleSheet(self, style: str) -> None:
        converted = self.convert_stylesheet(style)
        super().setStyleSheet(converted)

    @classmethod
    def convert_stylesheet(
        cls,
        source: Union[str, os.PathLike],
        output_file: str = None
    ) -> str:
        """
        Convert a standard stylesheet (with pseudo states and regular properties)
        into a qproperty-compatible stylesheet for use with custom QWidget-based widgets.

        Args:
            source (str or PathLike): Path to a CSS file or a raw CSS string.
            output_file (str, optional): If set, writes the converted QSS to this file.

        Returns:
            str: Converted stylesheet string.
        """
        # Load stylesheet content
        if isinstance(source, (str, os.PathLike)) and os.path.isfile(source):
            with open(source, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = str(source)

        # Replace states like :checked -> [checked="true"]
        for pseudo, replacement in cls._state_map.items():
            content = content.replace(pseudo, replacement)

        # Regex to replace standard properties with qproperty equivalents
        content = re.sub(
            r'(\s*)([a-zA-Z_][\w\-]*)\s*:\s*([^;]+);',
            lambda m: f'{m.group(1)}qproperty-{cls._camel_case(m.group(2))}: {m.group(3).strip()};',
            content
        )

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)

        return content

    @staticmethod
    def _camel_case(name: str) -> str:
        """
        Convert kebab-case or snake_case to camelCase (for Qt property compatibility).

        Args:
            name (str): The input property name.

        Returns:
            str: Converted camelCase name.
        """
        parts = re.split(r"[-_]", name)
        return parts[0] + ''.join(p.title() for p in parts[1:])
