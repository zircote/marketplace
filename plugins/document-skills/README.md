# document-skills Plugin

Document processing skills for PDF, DOCX, XLSX, and PPTX file manipulation with AI-powered analysis and extraction capabilities.

## Installation

```bash
claude /plugin marketplace add zircote/marketplace
claude /plugin install document-skills
```

## Contents

### Skills

#### PDF Processing (`pdf/`)
- Read and extract text from PDF files
- Analyze PDF structure and metadata
- Extract tables and images
- Handle multi-page documents
- OCR support for scanned documents
- Form field extraction

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

### DOCX Skill

| Feature | Description |
|---------|-------------|
| Full Text | Complete document text extraction |
| Styles | Formatting and style preservation |
| Headers/Footers | Access header and footer content |
| Comments | Read and process document comments |
| Revisions | Track changes and revision history |
| Tables | Table manipulation and extraction |

### XLSX Skill

| Feature | Description |
|---------|-------------|
| Cell Values | Read values and formulas |
| Named Ranges | Access defined names |
| Charts | Extract chart data |
| Conditional Formatting | Analyze formatting rules |
| Data Validation | Read validation rules |
| Multiple Sheets | Handle workbook structure |

### PPTX Skill

| Feature | Description |
|---------|-------------|
| Slide Content | Text and media extraction |
| Speaker Notes | Access presenter notes |
| Shapes | Work with shapes and SmartArt |
| Images | Extract embedded media |
| Animations | View animation settings |
| Masters | Access master slide templates |

## Usage Examples

### Extract Data from PDF

```bash
claude "Extract all tables from financial-report.pdf and summarize the key metrics"
```

### Analyze Excel Data

```bash
claude "Read sales.xlsx and identify trends in the Q4 data"
```

### Review Word Document

```bash
claude "Review contract.docx for legal terms and summarize key obligations"
```

### Summarize Presentation

```bash
claude "Create an executive summary from quarterly-review.pptx"
```

## Dependencies

Skills may require Python packages for full functionality:

```bash
# PDF processing
pip install pypdf2 pdfplumber

# Office documents
pip install python-docx openpyxl python-pptx

# Optional: OCR support
pip install pytesseract pdf2image
```

## Integration with Other Plugins

- **z plugin**: Use `data-analyst` for spreadsheet analysis workflows
- **z plugin**: Use `technical-writer` for document review and improvement
- **git plugin**: Commit extracted data with `/git:cm`

## Version

**Plugin:** 1.0.0
