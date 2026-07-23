# Quarto Conversion Plan: shell-novice

## Objective

Convert the Software Carpentry `shell-novice` lesson from Sandpaper to
[Quarto](https://quarto.org), producing both HTML and PDF output while retaining
the visual identity and pedagogical structure of the existing lesson.

## 1. Current State Inventory

### 1.1 Source files

FIXME: rewrite this as a tree structure like the one in section 2.2 below

| Path | Purpose |
|------|---------|
| `index.md` | Home page / lesson introduction |
| `episodes/01-intro.md` – `07-find.md` | Seven core lesson episodes |
| `learners/setup.md` | Setup instructions for learners |
| `learners/reference.md` | Command summary and glossary |
| `learners/discuss.md` | Discussion and supplementary notes |
| `instructors/instructor-notes.md` | Teaching notes for instructors |
| `profiles/learner-profiles.md` | Example learner personas |
| `config.yaml` | Project-level metadata and episode order |
| `shell-lesson-data/` | Exercise data files |
| `filesystem/` | Simulated filesystem for exercises |
| `episodes/fig/` | SVG and ODG figures |

### 1.2 Sandpaper-specific syntax that must be mapped

**YAML frontmatter** (per-episode):

```yaml
---
title: Introducing the Shell
teaching: 5
exercises: 0
---
```

**Colon-fenced callout divs** (9 distinct box types):

| Sandpaper box | Purpose | Frequency |
|---------------|---------|-----------|
| `objectives` | Learning objectives (top of episode) | Every episode |
| `questions` | Framing questions (top of episode) | Every episode |
| `keypoints` | Takeaway summary (bottom of episode) | Every episode |
| `callout` | Sidebar note with optional title | ~3–8 per episode |
| `challenge` | Exercise/prompt for learners | ~3–5 per episode |
| `solution` | Expandable answer to a challenge | Nested inside challenges |
| `instructor` | Instructor-only notes | ~2 per episode |
| `spoiler` | Expandable detail/hint | Occasional |
| `prereq` | Prerequisite callout | `index.md` only |

Syntax:
```markdown
::::::::::::::::::::::::::::::::::::::: objectives

- Explain how the shell relates to...

::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::  callout

## Command not found

If the shell can't find a program...

::::::::::::::::::::::::::::::::::::::::::::::::::
```

**Code blocks**: Standard fenced blocks with language tags (`bash`, `output`, `source`).

**Images**:

```markdown
![](fig/filesystem.svg){alt='The file system is made up of...'}
```

**Inline**: `<kbd>Enter</kbd>` for key caps, `**bold**` for emphasis.

**Links**: Standard Markdown `[text](url)` plus reference-style links.

### 1.3 Build artifacts produced by Sandpaper

- HTML website with sidebar navigation, carpentry-themed header/footer
- Episode pages with objectives/questions at top, keypoints at bottom
- Styled callout boxes with icons
- Expandable solutions

## 2. Target State: Quarto Project

### 2.1 Project type

Use a Quarto Book project. Books support sequential chapters (episodes), a
sidebar with table of contents, and both HTML and PDF output from a single
source. A Book provides better chapter ordering, cross-references, and PDF
generation than a Quarto website.

### 2.2 Proposed file layout

```
shell-novice/
├── _quarto.yml                  # Project configuration (replaces config.yaml)
├── index.qmd                    # Home page (converted from index.md)
├── 01-intro.qmd                 # Episodes renamed .qmd
├── 02-filedir.qmd
├── 03-create.qmd
├── 04-pipefilter.qmd
├── 05-loop.qmd
├── 06-script.qmd
├── 07-find.qmd
├── setup.qmd                    # From learners/setup.md
├── reference.qmd                # From learners/reference.md
├── discuss.qmd                  # From learners/discuss.md
├── instructor-notes.qmd         # From instructors/instructor-notes.md
├── learner-profiles.qmd         # From profiles/learner-profiles.md
├── styles/
│   └── carpentries.scss         # Custom SCSS to replicate Carpentries look
├── _extensions/
│   └── carpentries/             # (Optional) Quarto extension for reuse
├── episodes/fig/                # Figures (unchanged)
├── shell-lesson-data/           # Exercise data (unchanged)
├── filesystem/                  # Filesystem simulation (unchanged)
└── .github/workflows/           # Updated CI (quarto render instead of sandpaper)
```

Rationale: Quarto Books work best with `.qmd` files at the project root. Episode
files are promoted from `episodes/` to root and renamed `.qmd`. The
`episodes/fig/` directory stays where it is and image paths are updated to
`episodes/fig/...` to match.

## 3. Metadata Mapping

### 3.1 `config.yaml` to `_quarto.yml`

Before:

```yaml
carpentry: 'swc'
title: 'The Unix Shell'
created: '2014-10-22'
keywords: 'software, data, lesson, The Carpentries'
life_cycle: 'stable'
license: 'CC-BY 4.0'
source: 'https://github.com/swcarpentry/shell-novice'
branch: 'main'
contact: 'team@carpentries.org'
lang: en
episodes:
- 01-intro.md
- 02-filedir.md
- 03-create.md
- 04-pipefilter.md
- 05-loop.md
- 06-script.md
- 07-find.md
```

After:

```yaml
project:
  type: book
  output-dir: _site

book:
  title: "The Unix Shell"
  subtitle: "Software Carpentry"
  author: "The Carpentries"
  date: "2025-10-22"
  license: "CC-BY 4.0"
  repo-url: "https://github.com/swcarpentry/shell-novice"
  repo-branch: "main"
  language: en
  chapters:
    - index.qmd
    - 01-intro.qmd
    - 02-filedir.qmd
    - 03-create.qmd
    - 04-pipefilter.qmd
    - 05-loop.qmd
    - 06-script.qmd
    - 07-find.qmd
    - setup.qmd
    - reference.qmd
    - discuss.qmd
    - instructor-notes.qmd
    - learner-profiles.qmd

format:
  html:
    theme:
      - default
      - styles/carpentries.scss
    toc: true
    toc-depth: 3
    number-sections: false
    code-copy: true
  pdf:
    documentclass: scrbook
    toc: true
    number-sections: true
    include-in-header:
      - text: |
          \usepackage{fontspec}
          \setmonofont{Source Code Pro}
    keep-tex: true
```

### 3.2 Episode frontmatter mapping

Before:

```yaml
---
title: Introducing the Shell
teaching: 5
exercises: 0
---
```

After:

```yaml
---
title: "Introducing the Shell"
teaching: 5
exercises: 0
subtitle: "Episode 1"
---
```

The `teaching` and `exercises` fields are retained for potential use in
shortcodes or Lua filters that render time estimates. If no automated rendering
is desired, they can be dropped.

## 4. Callout Syntax Mapping

This is the largest mechanical transformation. Sandpaper uses colon-fenced divs
with a trailing keyword; Quarto uses Pandoc's fenced-div syntax with curly-brace
classes and attributes. Every episode must be transformed.  We don't need AI to
do conversion: a Python or shell script should do the job.

1. Detect lines matching `^:+ +(\w+)$` (opening fence) and `^:+$` (closing fence).
2. Map the keyword (objectives, questions, etc.) to the Quarto callout type.
3. Read the content between opening and closing fences.
4. If the first line of content is `## Title`:
   1. Extract the title, strip it, and pass it as the `title` attribute.
   2. Otherwise, use the default title from the mapping.
5. Emit `::: {.callout-X ...}` ... `:::`.

### Objectives

Before:

```
::::::::::::::::::::::::::::::::::::::: objectives

- Explain how the shell relates to the keyboard...
- Explain when and why command-line interfaces...

::::::::::::::::::::::::::::::::::::::::::::::::::
```

After:

```markdown
::: {.callout-tip title="Objectives"}

- Explain how the shell relates to the keyboard...
- Explain when and why command-line interfaces...

:::
```

### Callout with title

Before:

```
:::::::::::::::::::::::::::::::::::::::::  callout

## Command not found

If the shell can't find a program whose name is the command you typed...

::::::::::::::::::::::::::::::::::::::::::::::::::
```

After:

```markdown
::: {.callout-note}

### Command not found

If the shell can't find a program whose name is the command you typed...

:::
```

### Challenge + Solution

Before:

```
:::::::::::::::::::::::::::::::::::::::  challenge

## What Does `sort -n` Do?

...prompt text...

::::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::  solution

...solution text...

::::::::::::::::::::::::::::::::::
```

After:

```markdown
::: {.callout-important title="Challenge"}

### What Does `sort -n` Do?

...prompt text...

:::

::: {.callout-tip title="Solution" collapse="true"}

...solution text...

:::
```

### Keypoints

These become a dedicated `{.callout-tip}` at the end of each episode.

## 5. Other Markdown Transformations

### 5.1 Image paths

Images in episode files currently use relative paths like `fig/filesystem.svg`
(relative to the episode file's location in `episodes/`). After moving `.qmd`
files to root, these become `episodes/fig/filesystem.svg`.

We fix this by prepending `episodes/` to all `![](fig/...)` references.

### 5.2 Image alt text

Before: `![](fig/filesystem.svg){alt='The file system...'}`

After: `![](episodes/fig/filesystem.svg "The file system...")`

Quarto/Pandoc uses the title attribute (text in double quotes) as the alt text
when the `alt=` attribute is absent. The `{alt='...'}` syntax is a Pandoc
attribute that also works, but the quoted title form is more portable.

### 5.3 `<kbd>` elements

`<kbd>Enter</kbd>` works as-is in Quarto HTML output. For PDF via LaTeX, add the
following to the LaTeX preamble in `_quarto.yml`:

```yaml
include-in-header:
  - text: |
      \usepackage{fontawesome5}
```

Alternatively, we can define a custom macro for key rendering. Another option is
to use a Lua filter that converts `<kbd>X</kbd>` to `\fbox{\texttt{X}}` in LaTeX
output.

### 5.4 Reference-style links

Sandpaper uses reference-style links defined at the bottom of files:

```markdown
[zip-file]: data/shell-lesson-data.zip
```

Quarto supports this syntax natively. No change is needed, but we should look at
consolidating all external links in a single file that is automatically appended
to each `.qmd` file during build (which will probably require a custom
extension).

### 5.5 Glossary definitions (reference.md)

Lessons currently use this:

```markdown
[absolute path]{#absolute-path}
:   A [path](#path) that refers to a particular location...
```

Quarto supports Pandoc definition lists natively for HTML output. For PDF, this
also works, so no change is needed.

### 5.6 Tables

The `reference.md` file contains a Markdown table:

```markdown
| Action       | Files | Folders      |
| ------------ | ----- | ------------ |
| Inspect      | ls    | ls           |
```

Quarto supports this. No change needed.

## 6. Styling: Replicating the Carpentries Look

### 6.1 HTML output

The Carpentries lesson style features:

- Blue top banner with "Software Carpentry" branding
- "Schedule" sidebar with episode list and estimated times
- Left sidebar with site navigation
- Colored callout boxes with icons (key icon for keypoints, graduation cap for objectives, etc.)
- Episode header showing teaching/exercise times
- "Prerequisites" box on the index page
- Footer with license, source link, contact

A possible implementation is shown in `carpentries.scss`.

### 6.2 Navigation sidebar

Quarto Books automatically generate a sidebar table of contents from the chapter
list in `_quarto.yml`. To add estimated times to the sidebar, create a
`_brand.yml` or override the sidebar title. For per-episode timing, a Lua filter
can inject time metadata from the `teaching`/`exercises` YAML fields into the
sidebar entries.

### 6.3 PDF output

For PDF, LaTeX is the primary engine. The key requirements are:

- **Font**: Specify Fira Sans for body, Source Code Pro for code in `_quarto.yml`:

```yaml
format:
  pdf:
    pdf-engine: lualatex
    mainfont: Fira Sans
    monofont: Source Code Pro
```

- **Callout boxes**: Quarto's built-in callout support renders to `tcolorbox`
  environments in LaTeX. The SCSS color variables do not apply to PDF; instead,
  add LaTeX color definitions in the preamble:

```yaml
include-in-header:
  - text: |
      \definecolor{carpentries-blue}{HTML}{2b3990}
      \definecolor{carpentries-green}{HTML}{6ab187}
      \definecolor{carpentries-orange}{HTML}{f0ad4e}
      \definecolor{carpentries-red}{HTML}{d9534f}
```

- **Cover page**: The PDF title page is generated from `book.title` and
  `book.author` in `_quarto.yml`. Add the Carpentries logo as a `cover-image`.

- **Page size**: US letter or A4 with reasonable margins.

- **Line wrapping in code**: LaTeX handles this; set `code-block-bg: true` and
  `code-block-border-left: "#2b3990"` for visual distinction.

### 6.4 Branding and headers

For the Carpentries header banner in HTML, add a `before-body` include or use
the `_brand.yml` approach:

```yaml
website:
  navbar:
    title: "The Unix Shell"
    logo: https://carpentries.org/assets/img/TheCarpentries.svg
    left:
      - text: "Home"
        href: index.html
    right:
      - icon: github
        href: https://github.com/swcarpentry/shell-novice
```

## 7. HTML Output Configuration

### 7.1 `_quarto.yml` HTML section

```yaml
format:
  html:
    theme:
      - cosmo
      - styles/carpentries.scss
    toc: true
    toc-depth: 3
    toc-title: "On this page"
    number-sections: false
    code-copy: true
    code-link: true
    code-line-numbers: true
    code-block-bg: "#f8f8f8"
    code-block-border-left: "#2b3990"
    highlight-style: arrow
    citations-hover: true
    footnotes-hover: true
```

### 7.2 Sidebar configuration

```yaml
book:
  sidebar:
    title: "The Unix Shell"
    logo: episodes/fig/carpentries-logo.svg
    style: docked
    background: light
    search: true
    tools:
      - icon: github
        href: https://github.com/swcarpentry/shell-novice
```

### 7.3 Episode metadata rendering

To show teaching/exercise times at the top of each episode, create a Lua filter
`_extensions/carpentries/episode-meta.lua`:

```lua
function Pandoc(doc)
  local meta = doc.meta
  if meta.teaching or meta.exercises then
    local blocks = {}
    local total = (meta.teaching or 0) + (meta.exercises or 0)
    local text = ''
    if meta.teaching then
      text = text .. 'Teaching: ' .. tostring(meta.teaching) .. ' min'
    end
    if meta.exercises then
      text = text .. '  |  Exercises: ' .. tostring(meta.exercises) .. ' min'
    end
    table.insert(blocks, pandoc.Div({
      pandoc.Para({pandoc.Str(text)})
    }, {class = 'episode-meta'}))
    -- Prepend to document
    for i, block in ipairs(doc.blocks) do
      table.insert(blocks, block)
    end
    doc.blocks = blocks
  end
  return doc
end
```

Register this in `_quarto.yml`:

```yaml
filters:
  - _extensions/carpentries/episode-meta.lua
```

## 8. PDF Output Configuration

### 8.1 `_quarto.yml` PDF section

```yaml
format:
  pdf:
    documentclass: scrbook
    classoption:
      - oneside
      - 11pt
    papersize: letter
    toc: true
    toc-depth: 2
    number-sections: true
    colorlinks: true
    linkcolor: "2b3990"
    urlcolor: "2b3990"
    citecolor: "6ab187"
    include-before-body:
      - text: |
          \frontmatter
    include-in-header:
      - text: |
          \usepackage{fontspec}
          \setmainfont{Fira Sans}
          \setmonofont{Source Code Pro}[Scale=MatchLowercase]
          \usepackage{geometry}
          \geometry{margin=1in}
          \usepackage{fancyhdr}
          \pagestyle{fancy}
          \fancyhf{}
          \fancyhead[LE,RO]{\leftmark}
          \fancyfoot[LE,RO]{\thepage}
          \renewcommand{\headrulewidth}{0.4pt}
    keep-tex: true
```

### 8.2 PDF-specific considerations

- **Callout boxes**: Quarto renders callouts as `tcolorbox` environments in
  LaTeX. The default colors may need adjustment. Add to the preamble:

```latex
\usepackage{tcolorbox}
\tcbset{
  colback=white,
  colframe=carpentries-blue,
  arc=3mm,
  boxrule=0.5pt
}
```

- **Code blocks**: Ensure `minted` or `listings` is available for syntax
  highlighting. Quarto defaults to `minted` with `pygments`; set
  `highlight-style: arrow` for consistent coloring between HTML and PDF.

- **Images**: SVG figures must be converted for LaTeX. Either:
  - Pre-convert SVGs to PDFs (add a `Makefile` step using `rsvg-convert`)
  - Add `\usepackage{svg}` to the preamble
  - Use the `quarto` default which handles SVG via `rsvg-convert`

- **Page breaks**: Insert `\newpage` between major sections. Add to the Lua
  filter to inject page breaks after keypoints sections.

## 9. Build Process and Automation

Replace `make lesson-*` / `sandpaper::build_lesson()` with:

```bash
# Install Quarto (once)
# macOS:  brew install --cask quarto
# Linux:  download from https://quarto.org/docs/download/

# Render both HTML and PDF
quarto render

# Render HTML only
quarto render --to html

# Render PDF only
quarto render --to pdf

# Preview with live reload
quarto preview
```

We can put this in a Makefile:

```makefile
.PHONY: html pdf clean

html:
	quarto render --to html

pdf:
	quarto render --to pdf

all: html pdf

clean:
	rm -rf _site _book
```

See `quarto-render.yml` for a GitHub Actions configuration.

## 10. Migration Steps

### Phase 1: Project scaffold (no content changes)

1. Create `_quarto.yml` at project root with complete book configuration.
2. Create `styles/carpentries.scss` with initial SCSS rules.
3. Create `_extensions/carpentries/` directory with `episode-meta.lua`.
4. Install Quarto CLI locally and run `quarto create-project . --type book`.
5. Verify `quarto render --to html` produces a skeleton site.

### Phase 2: Content migration (one episode at a time)

6. Start with `episodes/01-intro.md`:
   - Copy to `01-intro.qmd` at project root.
   - Update image paths (`fig/` -> `episodes/fig/`).
   - Convert all callout divs from colon-fenced to `:::` syntax.
   - Update YAML frontmatter.
   - Render and visually inspect.
   - Fix styling issues.
7. Repeat for episodes 02–07.
8. Migrate `index.md` -> `index.qmd`.
9. Migrate `learners/setup.md` -> `setup.qmd`.
10. Migrate `learners/reference.md` -> `reference.qmd`.
11. Migrate `learners/discuss.md` -> `discuss.qmd`.
12. Migrate `instructors/instructor-notes.md` -> `instructor-notes.qmd`.
13. Migrate `profiles/learner-profiles.md` -> `learner-profiles.qmd`.

### Phase 3: Styling refinement

14. Iterate on `carpentries.scss` until HTML output visually matches the
    existing lesson rendering at `https://swcarpentry.github.io/shell-novice/`.
15. Add Carpentries logo and header banner.
16. Fix callout box colors, spacing, and icons.
17. Style the sidebar to show episode list with times.

### Phase 4: PDF output

18. Enable PDF rendering in `_quarto.yml`.
19. Install LaTeX (`quarto install tinytex` or system TeX Live).
20. Render PDF, fix font issues, adjust margins.
21. Convert SVGs to PDF-compatible format (add a pre-render step if needed).
22. Add page breaks, toc, and cover page.

### Phase 5: CI/CD

23. Remove old `.github/workflows/*.yaml` files (or archive them).
24. Add `.github/workflows/quarto-render.yaml`.
25. Configure GitHub Pages deployment.
26. Merge a PR and verify deployment.

### Phase 6: Cleanup

27. Remove Sandpaper-specific files: `config.yaml`, `site/`, R-related files.
28. Update `README.md` with new build instructions.
29. Update `CONTRIBUTING.md` with new workflow.
30. Remove `episodes/` directory (content now at root as `.qmd` files).
    Keep `episodes/fig/` in place since images are referenced from there.

## 11. Risks and Mitigations

- High:
  - Callout conversion errors (misnested divs): Per-episode review; build a Python script with test cases.
- Medium:
  - Image path breakage: Grep for `![](fig/` and update in one pass.
  - PDF rendering fails on SVGs: Add `rsvg-convert` to CI; pre-convert SVGs to PDF as a Makefile step.
  - SCSS doesn't perfectly match Carpentries look: Accept 95% fidelity; document remaining differences.
- Low:
  - Lua filter bugs: Test with episodes that have `teaching: 0` and missing fields.
  - GitHub Pages deployment path mismatch: Test deployment on a fork before merging to main.
  - Contributor confusion during transition: Keep old files in `./legacy` for one release cycle.

## 12. Automation Scripts

- `convert-callouts.py`: a Python script that reads a `.md` file, detects
  colon-fenced divs, and emits a `.qmd` file with Quarto `:::` callouts.
- `image-paths.sh`: a one-liner to fix image paths after moving files to root.

## 13. Verification Checklist

- [ ] All episodes render to HTML without errors
- [ ] All callout boxes appear with correct colors and icons
- [ ] Objectives, questions, and keypoints appear on every episode
- [ ] Challenge solutions are collapsed by default
- [ ] Code blocks are syntax-highlighted (bash, output, source)
- [ ] Inline `<kbd>` elements render as styled key caps
- [ ] Images display correctly
- [ ] Internal links (e.g., `#exploring-other-directories`) resolve
- [ ] External links open correctly
- [ ] Reference-style links work (`[zip-file]: data/...`)
- [ ] Glossary definitions render correctly in `reference.qmd`
- [ ] Teaching/exercise times appear in episode headers
- [ ] Sidebar shows correct chapter order
- [ ] Home page (`index.qmd`) renders with prerequisites box
- [ ] PDF output contains all content with correct formatting
- [ ] PDF code blocks do not overflow page margins
- [ ] PDF table of contents is generated
- [ ] GitHub Actions CI passes on push
- [ ] Deployed site matches local rendering

## 14. Notes

- Estimated effort: 3–5 days for a single developer.
- Hardest part: Callout block conversion (50+ callouts across 7 episodes + supporting files). The automated script might handle 90%; manual review catches nested blocks and edge cases.
- Highest-risk item: PDF rendering of code blocks with long lines. Test early with `07-find.qmd` (has the longest grep commands).
- Stakeholder check-in: Share the rendered HTML of the first converted episode with Carpentries maintainers before converting the remaining six, to confirm the styling approach is acceptable.
- Rollback strategy: Keep the original Sandpaper files in a `legacy` branch until the switch is validated.
