"""
Generated from the exported Magicline studio list.

ALL_STUDIOS contains every entry from the export.
STUDIOS contains only entries with a usable public studio URL and is used by the tracker.
"""

ALL_STUDIOS = [
 {'id': 1377860620,
  'slug': 'ai-fitness-friedrichshafen',
  'name': 'Ai Fitness Friedrichshafen',
  'city': 'Friedrichshafen',
  'url': 'https://www.ai-fitness.de/studios/friedrichshafen-bodenseecenter'}]

STUDIOS = [studio for studio in ALL_STUDIOS if studio["url"]]

