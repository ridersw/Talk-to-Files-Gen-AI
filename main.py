from concurrent.futures.process import _process_chunk
import PyPDF2
import os
import hashlib
import json
from tqdm import tqdm
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed


class TalkToPDF():
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def process_pdf(self, chunk_size = 100):
        # check if we have cache of the pdf
        cache = PDFCache()
        cached_text = cache.get_cached_text(self.pdf_path)
        if cached_text:
            print(f'Using Cached Text for {self.pdf_path}')
            return cached_text
        
        print(f'Processing PDF File')

        # get total number of pages
        with open(self.pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

        # create a progress bar for UI
        with tqdm(total=num_pages, desc ="Processing PDF", unit = "Page") as pbar:
            extracted_text = self.extract_data_from_pdf_chunked(self.pdf_path, chunk_size, pbar)

        # caching text for future usage
        cache.cache_text(self.pdf_path, extracted_text)

        return extracted_text
    
    def process_chunk(self, pdf_path, start_page, end_page):
        """Process a chunk of pages from the PDF."""
        chunk_text = ""
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for i in range(start_page, min(end_page, len(reader.pages))):
                chunk_text += reader.pages[i].extract_text() + " "
        return chunk_text
    
    def extract_data_from_pdf_chunked(self, pdf_path, chunk_size, pbar=None):
        with open(self.pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

        # dividing the pdf into chunks
        chunks = [(self.pdf_path, i, min(i + chunk_size, num_pages)) 
          for i in range(0, num_pages, chunk_size)]
        
        extracted_text = []

        with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = [executor.submit(self.process_chunk, *chunk) for chunk in chunks]
            
            for future in as_completed(futures):
                extracted_text.append(future.result())
                if pbar:
                    pbar.update(chunk_size)  # Update progress bar by chunk size

        return ' '.join(extracted_text)

class PDFCache():
    def __init__(self, cache_dir = "pdf_cache"):
        # initializing cache directory
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def get_cached_text(self, pdf_path):
        # to get the cached text of the pdf file if exists
        cache_path = self._get_cached_path(pdf_path)
        if os.path.exists(cache_path):
            with open(cache_path, "rb") as f:
                cache_data = json.load(f)

            # if the pdf file is not updated after last caching
            if os.path.getmtime(pdf_path) <= cache_data['last_modified']:
                return cache_data['text']
        
        return None
    
    def cache_text(self, pdf_path, extracted_text):
        cache_path = self._get_cached_path(pdf_path)
        cached_data = {
            'pdf_path' : pdf_path,
            'text' : extracted_text,
            'last_modified' : os.path.getmtime(pdf_path),
            'cache_date' : datetime.now().isoformat()
        }

        with open(cache_path, "w") as f:
            json.dump(cached_data, f)

    def _get_cached_path(self, pdf_path):
        pdf_hash = hashlib.md5(pdf_path.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{pdf_hash}.json")


if __name__ == "__main__":

    pdf_path = "harrypotter.pdf"
    TTP = TalkToPDF(pdf_path)
    TTP.process_pdf()

