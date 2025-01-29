# My Tools Repository

## Overview

This repository contains a collection of useful tools developed to streamline various tasks. Each tool is carefully crafted to provide specific functionalities, enhancing productivity and efficiency.

## Tools

### 1. convert_docx.py

A Python script that converts Markdown files to DOCX format using Pandoc. It supports advanced formatting options, including:

- Math equations
- Custom styling through reference templates
- Embedded images and assets
- Table of contents generation

#### Usage

```bash
./convert_docx.py input.md output.docx [--reference-doc template.docx] [--resource-dir assets/]
```

#### Features

- Maintains brand-consistent styling with reference templates
- Ensures proper handling of special elements like math equations
- Embeds all images and assets correctly
- Generates table of contents automatically

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/raphaelmansuy/mytools.git
   ```
2. Install Pandoc from [https://pandoc.org/installing.html](https://pandoc.org/installing.html)

## Contribution

Contributions are welcome! Please submit a pull request with your changes.

