# PDF Processor

This Python script provides functionality to process PDF files, extract text from them, and cache the results for future use. It uses multiprocessing to handle large PDFs efficiently.

## Features

- Extract text from PDF files
- Cache extracted text for faster subsequent access
- Process large PDFs in chunks using multiprocessing
- Progress bar to track PDF processing

## Dependencies

- PyPDF2
- tqdm
- concurrent.futures

## Installation

To install the required dependencies, run:

```bash
pip install PyPDF2 tqdm
```

## Classes

### TalkToPDF

The main class for processing PDF files.

#### Methods:

- `__init__(self, pdf_path)`: Initialize with the path to the PDF file.
- `process_pdf(self, chunk_size=100)`: Process the PDF, either retrieving cached text or extracting it.
- `process_chunk(self, pdf_path, start_page, end_page)`: Process a chunk of pages from the PDF.
- `extract_data_from_pdf_chunked(self, pdf_path, chunk_size, pbar=None)`: Extract text from the PDF in chunks.

### PDFCache

A class to handle caching of processed PDF text.

#### Methods:

- `__init__(self, cache_dir="pdf_cache")`: Initialize the cache directory.
- `get_cached_text(self, pdf_path)`: Retrieve cached text for a PDF if available.
- `cache_text(self, pdf_path, extracted_text)`: Cache the extracted text for a PDF.
- `_get_cached_path(self, pdf_path)`: Get the cache file path for a PDF.

## Usage

```python
from pdf_processor import TalkToPDF

pdf_path = "harrypotter.pdf"
TTP = TalkToPDF(pdf_path)
extracted_text = TTP.process_pdf()
```

This will process the PDF file "harrypotter.pdf", extracting its text and caching the result.

## Note

Make sure you have the necessary permissions to read the PDF files and write to the cache directory.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/ridersw/Talk-to-Files-Gen-AI/issues) if you want to contribute.

## License
