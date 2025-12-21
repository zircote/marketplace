# document-skills Plugin

Document processing skills for PDF, DOCX, XLSX, and PPTX file manipulation with AI-powered analysis and extraction capabilities.

## Installation

```bash
claude /plugin marketplace add zircote/marketplace
claude /plugin install document-skills
```

## Quick Start

Get started in under 2 minutes with these common tasks:

### PDF Analysis
```bash
claude "Analyze the contents of ./report.pdf"
claude "Extract all tables from ./data.pdf"
claude "What are the form fields in ./application.pdf"
claude "OCR this scanned document: ./scan.pdf"
```

### Excel Processing
```bash
claude "Read the data from ./sales.xlsx"
claude "What formulas are in ./budget.xlsx"
claude "List all sheets in ./workbook.xlsx"
claude "Compare Sheet1 and Sheet2 in ./data.xlsx"
```

### Word Documents
```bash
claude "Extract text from ./document.docx"
claude "What comments are in ./review.docx"
claude "Summarize the tracked changes in ./draft.docx"
claude "Create an outline from ./thesis.docx"
```

### PowerPoint
```bash
claude "Summarize the slides in ./presentation.pptx"
claude "Extract speaker notes from ./talk.pptx"
claude "List all slide titles in ./quarterly.pptx"
```

## Common Use Cases

| Use Case | Example Command |
|----------|-----------------|
| **Extract invoice data** | `claude "Extract vendor, date, and amount from ./invoice.pdf"` |
| **Analyze financial report** | `claude "Summarize key metrics from ./annual-report.pdf"` |
| **Review contract** | `claude "Find all obligations and deadlines in ./contract.docx"` |
| **Prepare meeting summary** | `claude "Create executive summary from ./meeting.pptx"` |
| **Data validation** | `claude "Check for missing values in ./data.xlsx"` |
| **Compare documents** | `claude "What changed between v1.docx and v2.docx"` |
| **Extract images** | `claude "Extract all charts and diagrams from ./report.pdf"` |
| **Batch processing** | `claude "Summarize all PDFs in ./reports/ folder"` |

## Verify Installation

After installing, verify the skills are active:

```bash
claude "What document processing skills are available?"
```

You should see PDF, DOCX, XLSX, and PPTX skills listed.

## Contents

### Skills

#### PDF Processing (`pdf/`)
- Read and extract text from PDF files
- Analyze PDF structure and metadata
- Extract tables and images
- Handle multi-page documents
- OCR support for scanned documents
- Form field extraction and filling

#### Word Documents (`docx/`)
- Read and modify DOCX files
- Extract text, tables, and images
- Preserve formatting during edits
- Track changes support
- Header/footer handling
- Comments and revision tracking

#### Excel Spreadsheets (`xlsx/`)
- Read and write Excel files
- Process formulas and cell references
- Handle multiple worksheets
- Data extraction and analysis
- Named range support
- Chart data extraction
- Conditional formatting analysis

#### PowerPoint Presentations (`pptx/`)
- Read and modify presentations
- Extract slide content and notes
- Work with shapes and images
- Analyze presentation structure
- Animation and transition info
- Master slide analysis

## Skill Activation

Each skill activates automatically when working with its respective file type:

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

## Features by Format

### PDF Skill

| Feature | Description |
|---------|-------------|
| Text Extraction | Page-by-page text extraction with layout preservation |
| Table Detection | Identify and extract tabular data |
| Image Extraction | Extract embedded images with OCR support |
| Metadata | Author, dates, keywords, document properties |
| Form Fields | Extract and analyze form field values |
| Bookmarks | Navigate document structure |
| Merge/Split | Combine or separate PDF documents |
| Watermarks | Add text or image watermarks |

### DOCX Skill

| Feature | Description |
|---------|-------------|
| Full Text | Complete document text extraction |
| Styles | Formatting and style preservation |
| Headers/Footers | Access header and footer content |
| Comments | Read and process document comments |
| Revisions | Track changes and revision history |
| Tables | Table manipulation and extraction |
| Images | Extract and insert images |

### XLSX Skill

| Feature | Description |
|---------|-------------|
| Cell Values | Read values and formulas |
| Named Ranges | Access defined names |
| Charts | Extract chart data |
| Conditional Formatting | Analyze formatting rules |
| Data Validation | Read validation rules |
| Multiple Sheets | Handle workbook structure |
| Pivot Tables | Access pivot table data |

### PPTX Skill

| Feature | Description |
|---------|-------------|
| Slide Content | Text and media extraction |
| Speaker Notes | Access presenter notes |
| Shapes | Work with shapes and SmartArt |
| Images | Extract embedded media |
| Animations | View animation settings |
| Masters | Access master slide templates |
| Transitions | Slide transition information |

## Usage Examples

### Extract Data from PDF

```bash
# Basic text extraction
claude "Extract all text from financial-report.pdf"

# Table extraction with analysis
claude "Extract all tables from financial-report.pdf and summarize the key metrics"

# Form field extraction
claude "List all form fields in application.pdf with their values"
```

### Analyze Excel Data

```bash
# Data summary
claude "Read sales.xlsx and identify trends in the Q4 data"

# Multi-sheet analysis
claude "Compare the data in Sheet1 and Sheet2 of workbook.xlsx"

# Formula analysis
claude "Explain the formulas in the budget spreadsheet"
```

### Review Word Document

```bash
# Content analysis
claude "Review contract.docx for legal terms and summarize key obligations"

# Extract structure
claude "Create an outline of the chapters in thesis.docx"

# Track changes review
claude "Summarize all tracked changes in proposal.docx"
```

### Summarize Presentation

```bash
# Content summary
claude "Create an executive summary from quarterly-review.pptx"

# Speaker notes extraction
claude "Extract all speaker notes from training.pptx"

# Slide count and structure
claude "Describe the structure of presentation.pptx including slide titles"
```

## Dependencies

Skills may require Python packages for full functionality:

```bash
# PDF processing
pip install pypdf pdfplumber

# Office documents
pip install python-docx openpyxl python-pptx

# Optional: OCR support for scanned PDFs
pip install pytesseract pdf2image

# Optional: Advanced PDF creation
pip install reportlab
```

## Tool Selection Guide

| Task | Recommended Tool |
|------|------------------|
| Extract text from PDF | pdfplumber |
| Extract tables from PDF | pdfplumber |
| Merge/split PDFs | pypdf |
| Create PDFs from scratch | reportlab |
| Fill PDF forms | pypdf or pdf-lib (JS) |
| OCR scanned PDFs | pytesseract + pdf2image |
| Read DOCX | python-docx |
| Read XLSX | openpyxl |
| Read PPTX | python-pptx |

## Best Practices

### PDF Processing
- Use `pdfplumber` for text/table extraction (better layout preservation)
- Use `pypdf` for document manipulation (merge, split, rotate)
- For scanned documents, convert to images first then OCR

### Excel Processing
- Specify sheet names when working with multi-sheet workbooks
- Handle formulas vs. calculated values explicitly
- Consider data types when extracting (dates, currencies)

### Word Processing
- Track changes are preserved when reading
- Styles provide structure hints for content organization
- Comments can contain important review feedback

### PowerPoint Processing
- Speaker notes often contain more detail than slides
- Master slides define consistent styling
- Check for hidden slides

## Integration with Other Plugins

- **z plugin**: Use `data-analyst` for spreadsheet analysis workflows
- **z plugin**: Use `technical-writer` for document review and improvement
- **git plugin**: Commit extracted data with `/git:cm`
- **nsip plugin**: Export breeding data to XLSX format

## Troubleshooting

### PDF Text Extraction Returns Empty

**Possible causes:**
- Scanned PDF (image-based, not text)
- Encrypted or protected PDF
- Corrupt file

**Solutions:**
```bash
# Check if PDF is image-based
pdftotext input.pdf - | head -20

# If empty, use OCR
pip install pytesseract pdf2image
```

### Excel Formula Values Not Showing

**Cause:** Reading formulas instead of calculated values

**Solution:** Use `data_only=True` when opening:
```python
from openpyxl import load_workbook
wb = load_workbook('file.xlsx', data_only=True)
```

### DOCX Formatting Lost

**Cause:** Reading plain text instead of preserving styles

**Solution:** Access paragraph styles explicitly:
```python
from docx import Document
doc = Document('file.docx')
for para in doc.paragraphs:
    print(f"Style: {para.style.name}, Text: {para.text}")
```

## Version

**Plugin:** 1.0.0
