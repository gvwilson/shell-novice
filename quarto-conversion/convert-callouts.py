import re
import sys

CALLOUT_MAP = {
    'objectives': ('callout-tip', 'Objectives'),
    'questions': ('callout-note', 'Questions'),
    'keypoints': ('callout-tip', 'Key Points'),
    'callout': ('callout-note', None),       # title extracted from content
    'challenge': ('callout-important', 'Challenge'),
    'solution': ('callout-tip', 'Solution', True),   # collapsed
    'instructor': ('callout-warning', 'Instructor Note'),
    'spoiler': ('callout-note', 'Spoiler', True),    # collapsed
    'prereq': ('callout-caution', 'Prerequisites'),
}

def convert_file(input_path, output_path):
    with open(input_path) as f:
        lines = f.readlines()

    result = []
    stack = []  # (keyword, indent_level)
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(:+)\s+(\w+)\s*$', line)
        if m:
            # Opening fence
            keyword = m.group(2)
            stack.append(keyword)
            entry = CALLOUT_MAP.get(keyword, ('callout-note', keyword))
            callout_type = entry[0]
            title = entry[1]
            collapsed = len(entry) > 2 and entry[2]

            # Peek at next line for inline title
            content_start = i + 1
            inline_title = None
            if content_start < len(lines):
                title_match = re.match(r'^##\s+(.+)$', lines[content_start].strip())
                if title_match:
                    inline_title = title_match.group(1)
                    content_start += 1

            final_title = inline_title or title
            attrs = f'.{callout_type}'
            if final_title:
                attrs += f' title="{final_title}"'
            if collapsed:
                attrs += ' collapse="true"'

            result.append(f'::: {{{attrs}}}\n')
            i = content_start
            continue

        m_close = re.match(r'^:+$', line.strip())
        if m_close and stack:
            stack.pop()
            result.append(':::\n')
            i += 1
            continue

        result.append(line)
        i += 1

    with open(output_path, 'w') as f:
        f.writelines(result)

if __name__ == '__main__':
    convert_file(sys.argv[1], sys.argv[2])
