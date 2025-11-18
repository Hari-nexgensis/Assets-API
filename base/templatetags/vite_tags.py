import json
import os
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def vite_asset(entry_point, asset_type='js'):
    """
    Load Vite asset from manifest.json
    Usage: 
      {% vite_asset 'src/main.jsx' 'js' %}
      {% vite_asset 'src/main.jsx' 'css' %}
    """
    manifest_path = os.path.join(settings.STATIC_ROOT, 'react', '.vite', 'manifest.json')
    
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        if entry_point in manifest:
            entry = manifest[entry_point]
            
            if asset_type == 'css' and 'css' in entry and entry['css']:
                # Return first CSS file
                return f"/static/react/{entry['css'][0]}"
            elif asset_type == 'js':
                return f"/static/react/{entry['file']}"
        
        return ""
    except FileNotFoundError:
        return ""
    except Exception as e:
        return ""
