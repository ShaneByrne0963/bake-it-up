from django import template
import webcolors


register = template.Library()

@register.simple_tag
def shade_color(color, value_scale):
    """
    Returns a shaded version of a hex color, where
    value_scale=1 returns the same color
    """
    color_rgb = webcolors.hex_to_rgb(color)

    r = int(color_rgb[0] * value_scale)
    g = int(color_rgb[1] * value_scale)
    b = int(color_rgb[2] * value_scale)

    return webcolors.rgb_to_hex((r, g, b))
