# `pl_style_mixin`

**Class:** `PlStyleMixin`

## Public Methods

### `setStyleSheet(style)`
**Returns:** `None`

_No docstring_

### `convert_stylesheet(cls, source, output_file)`
**Returns:** `str`

Convert a standard stylesheet (with pseudo states and regular properties)
into a qproperty-compatible stylesheet for use with custom QWidget-based widgets.

Args:
    source (str or PathLike): Path to a CSS file or a raw CSS string.
    output_file (str, optional): If set, writes the converted QSS to this file.

Returns:
    str: Converted stylesheet string.

### `getColor(prop, fallback)`
**Returns:** `QtGui.QColor`

_No docstring_

### `getInt(prop, fallback)`
**Returns:** `int`

_No docstring_