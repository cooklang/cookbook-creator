#!/usr/bin/env python3
"""
CookCLI Cookbook Generator

Creates a professional LaTeX cookbook from a directory of Cooklang recipes.

Usage:
    python3 create_cookbook.py <recipe_directory> <output_file> [options]

Options:
    --title TITLE       Cookbook title (default: "My Cookbook")
    --author AUTHOR     Author name (optional)
    --no-index         Skip index generation
    --no-toc           Skip table of contents

Examples:
    python3 create_cookbook.py recipes cookbook.tex
    python3 create_cookbook.py recipes cookbook.tex --title "Family Recipes" --author "Jane Doe"
"""

import os
import sys
import subprocess
import re
import argparse
from pathlib import Path
from datetime import datetime

class CookbookGenerator:
    def __init__(self, title="My Cookbook", author=None, include_index=True, include_toc=True):
        self.title = title
        self.author = author
        self.include_index = include_index
        self.include_toc = include_toc
        self.chapters = {}

    def get_recipe_latex(self, recipe_path):
        """Extract LaTeX content from a recipe using CookCLI."""
        try:
            # Try using installed 'cook' command
            result = subprocess.run(
                ["cook", "recipe", "-f", "latex", str(recipe_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # If 'cook' not found, try cargo run as fallback
            if result.returncode != 0 and "not found" in result.stderr:
                result = subprocess.run(
                    ["cargo", "run", "--", "recipe", "-f", "latex", str(recipe_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

            if result.returncode != 0:
                return None, {}

            content = result.stdout

            # Extract metadata from comments
            metadata = self.extract_metadata(content)

            # Look for marker comments
            start_marker = r'% BEGIN_RECIPE_CONTENT'
            end_marker = r'% END_RECIPE_CONTENT'

            start_match = re.search(start_marker, content)
            end_match = re.search(end_marker, content)

            if start_match and end_match:
                # Use marker comments if present
                # Include everything after the newline following BEGIN marker
                # up to the line before END marker
                start_pos = content.find('\n', start_match.start()) + 1
                end_pos = content.rfind('\n', 0, end_match.start())
                recipe_content = content[start_pos:end_pos].strip()

                # Remove the title section since we're adding it as a LaTeX section
                # Look for BEGIN_TITLE...END_TITLE block and remove it
                title_start = re.search(r'% BEGIN_TITLE', recipe_content)
                title_end = re.search(r'% END_TITLE', recipe_content)
                if title_start and title_end:
                    # Find the newline after END_TITLE to remove the whole block
                    title_end_pos = recipe_content.find('\n', title_end.end())
                    if title_end_pos == -1:
                        title_end_pos = title_end.end()
                    recipe_content = recipe_content[:title_start.start()] + recipe_content[title_end_pos:].lstrip()
            else:
                return None, metadata

            return recipe_content, metadata

        except Exception as e:
            print(f"Error processing {recipe_path}: {e}", file=sys.stderr)

        return None, {}

    def extract_metadata(self, latex_content):
        """Extract metadata from LaTeX comments."""
        metadata = {}

        patterns = {
            'description': r'% DESCRIPTION: (.+)',
            'tags': r'% TAGS: (.+)',
            'servings': r'% SERVINGS: (.+)',
            'prep_time': r'% PREP_TIME: (.+)',
            'cook_time': r'% COOK_TIME: (.+)',
            'author': r'% AUTHOR: (.+)',
            'source': r'% SOURCE: (.+)',
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, latex_content)
            if match:
                metadata[key] = match.group(1)

        return metadata

    def scan_recipes(self, recipe_dir):
        """Scan directory for .cook files and organize by chapter."""
        recipe_path = Path(recipe_dir)

        for cook_file in recipe_path.rglob("*.cook"):
            rel_path = cook_file.relative_to(recipe_path)

            # Determine chapter based on directory structure
            if len(rel_path.parts) > 1:
                chapter = self.format_chapter_name(rel_path.parts[0])
            else:
                chapter = "Main Dishes"

            if chapter not in self.chapters:
                self.chapters[chapter] = []

            self.chapters[chapter].append(cook_file)

    def format_chapter_name(self, name):
        """Format directory name as chapter name."""
        # Convert underscores/hyphens to spaces and capitalize
        name = name.replace('_', ' ').replace('-', ' ')
        return ' '.join(word.capitalize() for word in name.split())

    def generate_header(self):
        """Generate LaTeX document header."""
        header = r"""\documentclass[11pt,a4paper,twoside]{book}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{textcomp}
\usepackage{microtype}
\usepackage{enumitem}
\usepackage{multicol}
\usepackage[space]{grffile}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{geometry}
\usepackage{hyperref}"""

        if self.include_index:
            header += r"""
\usepackage{makeidx}
\usepackage{imakeidx}"""

        header += r"""
\usepackage{fancyhdr}
\usepackage{tocloft}

% Page geometry
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=3cm,bindingoffset=0.5cm}

% Color definitions
\definecolor{ingredientcolor}{RGB}{204, 85, 0}
\definecolor{cookwarecolor}{RGB}{34, 139, 34}
\definecolor{timercolor}{RGB}{220, 20, 60}

% Custom commands
\newcommand{\ingredient}[1]{\textcolor{ingredientcolor}{\textbf{#1}}}
\newcommand{\cookware}[1]{\textcolor{cookwarecolor}{\textbf{#1}}}
\newcommand{\timer}[1]{\textcolor{timercolor}{\textbf{#1}}}
"""

        if self.include_index:
            header += r"""
% Index setup
\makeindex[columns=2, title=Recipe Index, intoc]"""

        header += r"""

% Page style
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE,RO]{\thepage}
\fancyhead[RE]{\textit{""" + self.escape_latex(self.title) + r"""}}
\fancyhead[LO]{\leftmark}
\renewcommand{\headrulewidth}{0.4pt}

% Section formatting - smaller for TOC entries
\titleformat{\section}[block]
  {\normalfont\large\bfseries}
  {}
  {0pt}
  {}

% Suppress section numbers
\setcounter{secnumdepth}{0}

\begin{document}

% Title page
\begin{titlepage}
\centering
\vspace*{5cm}
{\Huge\bfseries """ + self.escape_latex(self.title) + r"""}\par"""

        if self.author:
            header += r"""
\vspace{2cm}
{\Large """ + self.escape_latex(self.author) + r"""}\par"""

        header += r"""
\vfill
\textit{Created with CookCLI}\par
\vspace{1cm}
{\large \today}
\end{titlepage}
"""

        if self.include_toc:
            header += r"""
% Table of contents
\tableofcontents
\clearpage
"""

        return header

    def generate_footer(self):
        """Generate LaTeX document footer."""
        footer = ""

        if self.include_index:
            footer += r"""
% Index
\printindex
"""

        footer += r"""
\end{document}
"""
        return footer

    def find_recipe_image(self, recipe_file):
        """Find an image file with the same base name as the recipe."""
        image_extensions = ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']
        recipe_dir = recipe_file.parent
        recipe_stem = recipe_file.stem

        for ext in image_extensions:
            image_path = recipe_dir / f"{recipe_stem}{ext}"
            if image_path.exists():
                return image_path

        return None

    def escape_latex(self, text):
        """Escape special LaTeX characters."""
        replacements = {
            '\\': r'\\',
            '{': r'\{',
            '}': r'\}',
            '$': r'\$',
            '&': r'\&',
            '#': r'\#',
            '^': r'\^{}',
            '_': r'\_',
            '~': r'\~{}',
            '%': r'\%',
            '<': r'\textless{}',
            '>': r'\textgreater{}',
            '|': r'\textbar{}',
        }

        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def generate(self, recipe_dir, output_file):
        """Generate the complete cookbook."""
        print(f"Scanning recipes in {recipe_dir}...")
        self.scan_recipes(recipe_dir)

        if not self.chapters:
            print("No recipes found!", file=sys.stderr)
            return False

        print(f"Found {sum(len(recipes) for recipes in self.chapters.values())} recipes in {len(self.chapters)} chapters")

        with open(output_file, 'w') as f:
            # Write header
            f.write(self.generate_header())

            # Process each chapter
            for chapter_name in sorted(self.chapters.keys()):
                print(f"\nProcessing chapter: {chapter_name}")
                f.write(f"\n\\chapter{{{self.escape_latex(chapter_name)}}}\n\n")

                # Process recipes in chapter
                for recipe_file in sorted(self.chapters[chapter_name]):
                    recipe_name = recipe_file.stem.replace('_', ' ').replace('-', ' ')
                    print(f"  Adding recipe: {recipe_name}")

                    # Get recipe content and metadata
                    content, metadata = self.get_recipe_latex(recipe_file)

                    # Add recipe to index with tags if available
                    if self.include_index:
                        f.write(f"\\index{{{self.escape_latex(recipe_name)}}}\n")

                        # Index by tags
                        if 'tags' in metadata:
                            tags = metadata['tags'].split(', ')
                            for tag in tags:
                                f.write(f"\\index{{{self.escape_latex(tag)}!{self.escape_latex(recipe_name)}}}\n")

                        # Index by author if available
                        if 'author' in metadata:
                            f.write(f"\\index{{Authors!{self.escape_latex(metadata['author'])}!{self.escape_latex(recipe_name)}}}\n")

                    # Add metadata as LaTeX comments for reference
                    if metadata:
                        f.write(f"% Recipe: {recipe_name}\n")
                        for key, value in metadata.items():
                            f.write(f"% {key}: {value}\n")
                        f.write("\n")

                    # Add section for TOC but suppress its display with a phantom section
                    f.write(f"\\phantomsection\n")
                    f.write(f"\\addcontentsline{{toc}}{{section}}{{{self.escape_latex(recipe_name)}}}\n")

                    # Add a larger, centered title for visual impact
                    f.write("\\begin{center}\n")
                    f.write(f"{{\\Huge\\bfseries {self.escape_latex(recipe_name)}}}\n")
                    f.write("\\end{center}\n")
                    f.write("\\vspace{1cm}\n\n")

                    # Check for and include recipe image
                    image_path = self.find_recipe_image(recipe_file)
                    if image_path:
                        print(f"    Including image: {image_path.name}")
                        # Use center environment - grffile package handles spaces
                        f.write("\\begin{center}\n")
                        image_path_str = str(image_path.absolute())
                        f.write(f"\\includegraphics[width=0.8\\textwidth]{{{image_path_str}}}\n")
                        f.write("\\end{center}\n")
                        f.write("\\vspace{0.5cm}\n\n")

                    # Write recipe content
                    if content:
                        f.write(content)
                        f.write("\n\n\\clearpage\n\n")
                    else:
                        print(f"    Warning: Could not process {recipe_file}", file=sys.stderr)
                        f.write("\\textit{Recipe content could not be processed.}\n\n\\clearpage\n\n")

            # Write footer
            f.write(self.generate_footer())

        print(f"\n✅ Cookbook created: {output_file}")
        print("\n📖 To compile to PDF:")
        print(f"  pdflatex {output_file}")

        if self.include_index:
            print(f"  makeindex {output_file[:-4]}.idx")
            print(f"  pdflatex {output_file}")

        print(f"  pdflatex {output_file}")
        print("\n💡 Tip: Run pdflatex multiple times to ensure proper cross-references")

        return True

def main():
    parser = argparse.ArgumentParser(description='Generate a LaTeX cookbook from Cooklang recipes')
    parser.add_argument('recipe_dir', help='Directory containing .cook files')
    parser.add_argument('output_file', help='Output LaTeX file')
    parser.add_argument('--title', default='My Cookbook', help='Cookbook title')
    parser.add_argument('--author', help='Author name')
    parser.add_argument('--no-index', action='store_true', help='Skip index generation')
    parser.add_argument('--no-toc', action='store_true', help='Skip table of contents')

    args = parser.parse_args()

    if not os.path.exists(args.recipe_dir):
        print(f"Error: Recipe directory '{args.recipe_dir}' not found", file=sys.stderr)
        sys.exit(1)

    generator = CookbookGenerator(
        title=args.title,
        author=args.author,
        include_index=not args.no_index,
        include_toc=not args.no_toc
    )

    if not generator.generate(args.recipe_dir, args.output_file):
        sys.exit(1)

if __name__ == "__main__":
    main()
