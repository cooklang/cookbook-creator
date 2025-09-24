# CookCLI Cookbook Generator

This directory contains scripts and templates for creating beautiful PDF cookbooks from your Cooklang recipes using CookCLI's LaTeX export feature.

Download sample cookbook [here](./examples/my_cookbook.pdf).

## Features

- 📚 Generate professional PDF cookbooks from `.cook` files
- 🎨 Customizable LaTeX templates with color-coded ingredients, cookware, and timers
- 📑 Automatic table of contents and recipe index
- 🗂️ Organize recipes by chapters/categories
- 🖼️ Automatic inclusion of recipe images (PNG, JPG, JPEG)
- 🔧 Both automated scripts and manual templates

## Quick Start

### Prerequisites

1. **CookCLI** installed and working
2. **LaTeX distribution** (TeX Live, MiKTeX, or MacTeX)
3. **Python 3** (for automated script)

### Prepare Your Recipes
Ensure you have `.cook` files in a directory:
```
my_recipes/
├── breakfast/
│   └── pancakes.cook
├── lunch/
│   └── sandwich.cook
└── dinner/
    └── pasta.cook
```

### Generate a Cookbook

```bash
# Generate cookbook Latex file from your recipes directory
python scripts/create_cookbook.py path/to/recipes my_cookbook.tex

# Compile to PDF
pdflatex my_cookbook.tex
makeindex my_cookbook.idx
pdflatex my_cookbook.tex
pdflatex my_cookbook.tex
```

## Directory Structure

```
cookbook-creator/
├── README.md                    # This file
├── scripts/
│   ├── create_cookbook.py       # Automated cookbook generator
├── examples/
│   └── my_cookbook.pdf          # Example output
│   └── recipes/                 # Example recipes
```

## Customization

You can change generated cookbook .tex file to your needs.

### Template Variables

All templates support these customization options:

- **Title**: Cookbook title
- **Author**: Your name
- **Colors**: Customize ingredient, cookware, timer colors
- **Layout**: Page margins, binding offset
- **Fonts**: Typography options

### Adding Custom Sections

Edit templates to add:
- Introduction/preface
- Kitchen tips
- Conversion tables
- Glossary
- Wine pairing suggestions

## Output Formats

The generated LaTeX can be compiled to:
- **PDF** - For printing or digital distribution
- **EPUB** - Convert PDF to EPUB for e-readers
- **HTML** - Use htlatex for web version

## Tips

1. **Recipe Organization**: Organize `.cook` files in folders by category
2. **Metadata**: Use frontmatter in recipes for better indexing
3. **Scaling**: Generate scaled versions for different serving sizes
4. **Images**: Place image files (PNG, JPG, JPEG) with same name as recipe (e.g., `pasta.cook` → `pasta.jpg`)

## Troubleshooting

### Common Issues

1. **LaTeX errors**: Ensure all packages are installed
   ```bash
   tlmgr install enumitem multicol xcolor titlesec geometry hyperref makeidx imakeidx fancyhdr
   ```

2. **Missing recipes**: Check file paths and `.cook` extensions

3. **Index not generated**: Run makeindex between pdflatex compilations

## Examples

See `examples/` directory for:
- Sample cookbook PDF
- Recipe organization structure
- Custom styling examples

## License

These scripts and templates are provided as part of CookCLI.

## Credits

Created with CookCLI - The command-line companion for Cooklang
