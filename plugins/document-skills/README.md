# document-skills Plugin

Document processing skills for PDF, DOCX, XLSX, and PPTX file manipulation with AI-powered analysis and extraction capabilities.

## Installation

```bash
claude /plugin install ./plugins/document-skills
```

## Contents

### Skills

#### PDF Processing (`pdf/`)
- Read and extract text from PDF files
- Analyze PDF structure and metadata
- Extract tables and images
- Handle multi-page documents

#### Word Documents (`docx/`)
- Read and modify DOCX files
- Extract text, tables, and images
- Preserve formatting during edits
- Track changes support

#### Excel Spreadsheets (`xlsx/`)
- Read and write Excel files
- Process formulas and cell references
- Handle multiple worksheets
- Data extraction and analysis

#### PowerPoint Presentations (`pptx/`)
- Read and modify presentations
- Extract slide content and notes
- Work with shapes and images
- Analyze presentation structure

## Skill Activation

Each skill activates when working with its respective file type:

```bash
# PDF analysis
claude "Analyze the contents of report.pdf"

# Excel processing
claude "Extract data from sales.xlsx into a summary"

# Word editing
claude "Update the contract template.docx"

# PowerPoint review
claude "Summarize the key points from presentation.pptx"
```

## Features

### PDF Skill
- Page-by-page text extraction
- Table detection and extraction
- Image extraction with OCR support
- Metadata analysis (author, dates, keywords)
- Form field extraction

### DOCX Skill
- Full document text extraction
- Style and formatting preservation
- Header/footer handling
- Comments and revision tracking
- Table manipulation

### XLSX Skill
- Cell value and formula reading
- Named range support
- Chart data extraction
- Conditional formatting analysis
- Data validation rules

### PPTX Skill
- Slide content extraction
- Speaker notes access
- Shape and image handling
- Animation and transition info
- Master slide analysis

## Integration

These skills complement:
- `ai-multimodal` for visual document analysis
- `media-processing` for document conversion
- Data analysis workflows for spreadsheet processing

## Dependencies

Skills may require Python packages:
```bash
pip install pypdf2 python-docx openpyxl python-pptx
```
