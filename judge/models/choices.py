from collections import defaultdict
from operator import itemgetter

import pytz
from django.utils.translation import gettext_lazy as _


def make_timezones():
    data = defaultdict(list)
    for tz in pytz.all_timezones:
        if '/' in tz:
            area, loc = tz.split('/', 1)
        else:
            area, loc = 'Other', tz
        if not loc.startswith('GMT'):
            data[area].append((tz, loc))
    return sorted(data.items(), key=itemgetter(0))


TIMEZONE = make_timezones()
del make_timezones

ACE_THEMES = (
    ('auto', _('Follow site theme')),
    ('ambiance', 'Ambiance'),
    ('chaos', 'Chaos'),
    ('chrome', 'Chrome'),
    ('clouds', 'Clouds'),
    ('clouds_midnight', 'Clouds Midnight'),
    ('cobalt', 'Cobalt'),
    ('crimson_editor', 'Crimson Editor'),
    ('dawn', 'Dawn'),
    ('dreamweaver', 'Dreamweaver'),
    ('eclipse', 'Eclipse'),
    ('github', 'Github'),
    ('idle_fingers', 'Idle Fingers'),
    ('katzenmilch', 'Katzenmilch'),
    ('kr_theme', 'KR Theme'),
    ('kuroir', 'Kuroir'),
    ('merbivore', 'Merbivore'),
    ('merbivore_soft', 'Merbivore Soft'),
    ('mono_industrial', 'Mono Industrial'),
    ('monokai', 'Monokai'),
    ('pastel_on_dark', 'Pastel on Dark'),
    ('solarized_dark', 'Solarized Dark'),
    ('solarized_light', 'Solarized Light'),
    ('terminal', 'Terminal'),
    ('textmate', 'Textmate'),
    ('tomorrow', 'Tomorrow'),
    ('tomorrow_night', 'Tomorrow Night'),
    ('tomorrow_night_blue', 'Tomorrow Night Blue'),
    ('tomorrow_night_bright', 'Tomorrow Night Bright'),
    ('tomorrow_night_eighties', 'Tomorrow Night Eighties'),
    ('twilight', 'Twilight'),
    ('vibrant_ink', 'Vibrant Ink'),
    ('xcode', 'XCode'),
)

MATH_ENGINES_CHOICES = (
    ('tex', _('Leave as LaTeX')),
    ('svg', _('SVG only')),
    ('mml', _('MathML only')),
    ('jax', _('MathJax with SVG fallback')),
    ('auto', _('Detect best quality')),
)

EFFECTIVE_MATH_ENGINES = ('svg', 'mml', 'tex', 'jax')

SITE_THEMES = (
    ('auto', _('Follow system default')),
    ('light', _('Light')),
    ('dark', _('Dark')),
)

LANGUAGE_CHOICES = [
    (1, 'Python'),
    (2, 'JavaScript'),
    (3, 'Java'),
    (4, 'C++'),
    (5, 'Khác'),
]

EXPERIENCE_CHOICES = [
    (6, 'Dưới 1 năm'),
    (7, '1-3 năm'),
    (8, 'Trên 3 năm'),
]

PURPOSE_CHOICES = [
    (9, 'Làm quen ngôn ngữ mới'),
    (10, 'Luyện tập kỹ năng'),
]

LEVEL_CHOICES = [
    (11, 'Mới bắt đầu (Hiểu cơ bản các khái niệm)'),
    (12, 'Trung bình (Giải quyết được các bài toán cơ bản và trung cấp)'),
    (13, 'Nâng cao (Xây dựng được các dự án lớn, hiểu thuật toán phức tạp)'),
]

ALGORITHM_CHOICES = [
    (14, 'Chưa từng học'),
    (15, 'Đã học cơ bản (sắp xếp, tìm kiếm, stack, queue)'),
    (16, 'Thành thạo (ứng dụng giải bài toán thực tế)'),
]

CONTEST_CHOICES = [
    (17, 'Chưa bao giờ'),
    (18, 'Thỉnh thoảng'),
    (19, 'Thường xuyên'),
]

HOBBY_CHOICES = [
    (20, 'Tốc độ giải bài'),
    (21, 'Độ chính xác và tối ưu'),
    (22, 'Học được kiến thức mới'),
    (23, 'Tận hưởng quá trình thử nghiệm'),
]