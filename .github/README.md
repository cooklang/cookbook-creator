# 📚 Cooklang Cookbook Generator

Transform your Cooklang recipes into beautiful PDF cookbooks with this comprehensive toolkit.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Cooklang](https://img.shields.io/badge/cooklang-compatible-green.svg)](https://cooklang.org)
[![LaTeX](https://img.shields.io/badge/LaTeX-required-orange.svg)](https://www.latex-project.org/)

Download sample cookbook [here](../examples/my_cookbook.pdf).

## ✨ Features

- 🎨 **Professional formatting** with color-coded ingredients, cookware, and timers
- 📑 **Automatic organization** into chapters based on your folder structure
- 📇 **Table of contents and index** generated automatically
- 🛠️ **Multiple generation methods**: Python, Shell, Make, or manual
- 📖 **Customizable templates** from minimal to feature-rich
- 🖨️ **Print-ready output** or digital ebook format

## 🚀 Quick Start

### Prerequisites

1. [CookCLI](https://github.com/cooklang/CookCLI) installed
2. LaTeX distribution ([TeX Live](https://www.tug.org/texlive/), [MiKTeX](https://miktex.org/), or [MacTeX](https://www.tug.org/mactex/))
3. Python 3 (for automated generation)

### Generate Your First Cookbook

```bash
# Clone this repository
git clone https://github.com/cooklang/cookbook-sample.git
cd cookbook-sample

# Generate cookbook from your recipes
python3 scripts/create_cookbook.py ~/my-recipes my-cookbook.tex \
  --title "Family Recipes" --author "Your Name"

# Compile to PDF
pdflatex my-cookbook.tex
pdflatex my-cookbook.tex  # Run twice for TOC

# View your cookbook
open my-cookbook.pdf  # macOS
xdg-open my-cookbook.pdf  # Linux
```

## 📁 Repository Structure

```
cookbook-creator/
├── README.md                    # This file
├── scripts/
│   ├── create_cookbook.py       # Automated cookbook generator
├── examples/
│   └── my_cookbook.pdf          # Example output
│   └── recipes/                 # Example recipes
```

## 🎯 Usage Example

```bash
python3 scripts/create_cookbook.py recipes/ cookbook.tex \
  --title "My Cookbook" \
  --author "Jane Doe" \
  --no-index  # Optional: skip index generation
```
## 🎨 Customization

### Colors

Edit the color definitions in your LaTeX file:

```latex
\definecolor{ingredientcolor}{RGB}{204, 85, 0}    % Orange
\definecolor{cookwarecolor}{RGB}{34, 139, 34}     % Green
\definecolor{timercolor}{RGB}{220, 20, 60}        % Red
```

### Layout

Modify page geometry:

```latex
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=3cm,bindingoffset=0.5cm}
```

### Sections

Add custom sections to templates:
- Introduction/Preface
- Conversion tables
- Kitchen tips
- Wine pairings
- Nutritional information

## 🔧 Advanced Features

### Recipe Scaling

Generate recipes for different serving sizes:

```bash
cook recipe -f latex "Pasta:2" -o pasta_2.tex   # 2 servings
cook recipe -f latex "Pasta:8" -o pasta_8.tex   # 8 servings
```

### Including Images

```latex
\usepackage{graphicx}
\section{Chocolate Cake}
\includegraphics[width=0.5\textwidth]{images/cake.jpg}
```

### Multiple Languages

```latex
\usepackage[english,spanish]{babel}
\selectlanguage{spanish}
\chapter{Recetas Españolas}
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| LaTeX not found | Install TeX distribution for your OS |
| Missing packages | Run `tlmgr install [package]` |
| Recipes not found | Ensure files have `.cook` extension |
| Index not generated | Run `makeindex` between compilations |
| Compilation errors | Check `cookbook.log` for details |

## 📚 Documentation

- [Full tutorial on cooklang.org](https://cooklang.org/guides/cookbook-creation/)
- [CookCLI documentation](https://cooklang.org/cli/)
- [Cooklang specification](https://cooklang.org/docs/spec/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Cooklang](https://cooklang.org) for the recipe markup language
- [LaTeX Project](https://www.latex-project.org/) for typesetting
- Community contributors and testers

## 💬 Support

- [GitHub Issues](https://github.com/cooklang/cookbook-creator/issues)
- [Cooklang Discussions](https://github.com/cooklang/cooklang/discussions)

---

Created with ❤️ by the Cooklang community
