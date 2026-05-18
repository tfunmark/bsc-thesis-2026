# RNU BSc Thesis LaTeX Template (XeLaTeX)

This template implements the key layout and styling rules from the provided RNU guidelines (A4, 12pt, Times New Roman/Calibri, 1.5 line spacing, mirrored margins, outer page numbers, table/figure caption placement, chapter-based numbering, and an alphabetized bibliography).

Detailed LaTeX documentation can be found at [latex-project.org](https://www.latex-project.org/help/documentation/)

---

## 🎯 Workflow Overview for Students

When your **BSc thesis topic** is approved by your supervisor and officially submitted, you are required to:

1. **Create a GitHub account** (if you do not already have one).  
   - [Sign up here](https://github.com/join).  

2. **Clone this repository** (the official RNU thesis template) to your own private GitHub repository.  
   - This will ensure your thesis work is version-controlled and progress is visible.  

3. **Set up LaTeX** on your computer (see installation instructions below).  

4. **Work with the template**:  
   - Edit the `.tex` files to reflect your own thesis contents.  
   - Keep the structure, formatting, and guidelines intact unless your supervisor specifies changes.  

5. **Commit and push changes at least every two weeks**.  
   - This is **mandatory**. Failure to do so will mean your thesis may be **discarded**.  
   - A “last-day full thesis commit” is not acceptable, as supervisors need to verify that you have been consistently working.  

---

## 🚨 Mandatory Git Commit Policy

- **Bi-weekly commits are required.**  
- Each commit should represent meaningful progress (e.g., introduction draft, updated figures, conclusions refined).  
- Supervisors will monitor your GitHub repository for activity.  
- **No visible commit history = thesis work cannot be verified = thesis not accepted.**

---

## 🛠️ Git & GitHub Setup

### 1. Install Git

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install git
```

#### Fedora/RHEL
```bash
sudo dnf install git
```

#### Arch Linux
```bash
sudo pacman -S git
```

#### Windows

Download and install from [git-scm.com](git-scm.com).

During installation, choose “Git from the command line” option.

#### macOS
```bash
# With Homebrew
brew install git
```
Or install from [git-scm.com](git-scm.com).

### 2. Configure Git (once)

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### 3. Clone the Template

```bash
git clone https://github.com/RNU-university/bsc-thesis-template.git
cd bsc-thesis-template
```

### 4. Create Your Own GitHub Repository

- On [GitHub](https://github.com/), create a new private repository named e.g. bsc-thesis-2025-YourName.
- Link your local project to your private repository:

```bash
git remote remove origin
git remote add origin https://github.com/YourUsername/bsc-thesis-2025_YourName.git
git branch -M main
git push -u origin main
```

### 5. Basic Git Commands You Will Use

It is assumed that last year BSC students should know how to use de-facto world standart 
code Version Control System (VCS). If not, no worries - it is rather simple, below are the main commands
you will be using (in any full documentation describing all use cases can be found at [https://git-scm.com/doc](https://git-scm.com/doc)):

```bash
# Check file status
git status

# Stage all changes
git add .

# Commit with a descriptive message
git commit -m "Draft of introduction section"

# Push to GitHub
git push
```

Make local commits regularly, ideally each focused result, make pushes of local work progress every 1–2 weeks minimum, preferably more often.

## 📦 Installation of LaTeX Environment

You must set up XeLaTeX and dependencies on your system. Instructions per platform:

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install texlive-xetex texlive-latex-extra texlive-science
sudo apt-get install python3-pygments texlive-bibtex-extra biber
```

### Fedora/RHEL
```bash
sudo dnf install texlive-xetex texlive-latexextra texlive-science
sudo dnf install python3-pygments texlive-biblatex biber
```

### Arch Linux
```bash
sudo pacman -S texlive-core texlive-latexextra texlive-science
sudo pacman -S python-pygments texlive-bibtexextra biber
```

### Windows

- Install [MiKTeX](https://miktex.org/).
- During installation, allow “Install missing packages on the fly.”
- Use **MiKTeX Console** to install:
    - `latex-extra`, `science` and `biber` dependencies.
- Install Python from [python.org](python.org) and then:

```bash
pip install pygments
```

### macOS

#### Option 1: BasicTeX (lightweight)

```bash
brew install basictex
sudo tlmgr update --self
sudo tlmgr install collection-latexextra collection-science biber minted xetex
brew install python
pip3 install pygments
```

#### Option 2: Full MacTeX (recommended if you have space)
- Download from [tug.org/mactex](tug.org/mactex)

## 📖 Compilation Instructions

To compile your thesis to PDF:
```bash
xelatex main
biber main
xelatex main
xelatex main
```

You might wonder why multiple 'xelatex' runs are needed - thats for references and cross-links.


## 📝 Notes for Students

- Always start your thesis work by pulling the latest template updates (if any).
- Keep a clean commit history (avoid uploading temporary files).
- Use `.gitignore` (already included) to avoid committing unnecessary build files.
- If you face issues with LaTeX compilation, consult your supervisor or the provided troubleshooting section.
- Use English or Latvian consistently for your thesis, unless instructed otherwise.

## 💡 Editor Suggestions

- VS Code with LaTeX Workshop plugin (recommended).
- TeXStudio (free, user-friendly).
- Overleaf (online, if local setup fails).

In regards to feedback - you can:
- give direct feedback, plain text in email;
- Issue tracking - you can create issues in the repository (but student have to give you writing permissions), still your will have to refer to the places in text;
- PullRequests - most advanced but allow to review each commits series and comment on a specic places of edited files.

## 📊 Highlights (Template Features)

- A4, mirrored margins.
- Times New Roman 12pt font (default).
- 1.5 line spacing.
- Figures below, tables above captions.
- Chapter-based numbering (e.g., Table 2.3).
- BibLaTeX + Biber for bibliography.
- Multilingual support (EN/LV/RU).
- Appendices & examples included.

## 🚀 Final Checklist Before Submission

1. Thesis structure complete (Introduction → Chapters → Conclusions → References → Appendices).
2. Commit history visible, with at least bi-weekly progress updates.
3. PDF compiles without errors.
4. Supervisor has approved your contents and structure.
5. Keywords, abstract, and title page filled correctly in both English and Latvian.

---

Happy writing, and remember: commit often, commit meaningfully (mind commit messages!), and push to GitHub regularly!