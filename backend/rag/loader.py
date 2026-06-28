from pathlib import Path 
from langchain_community.document_loaders import PyMuPDFLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

SCANNED_PDFS = {
    "ASHA Update Jan 2019.pdf",
    "asha_roles_responsibilities.pdf",
    "AX7tgv1oe2Nd-IAP-Recommended-Immunization-Schedule-2020-2021.pdf",
    "e7HEGgDSU8MZ-ACVIP-TABLE-2020-2021.pdf",
    "Notes_for_ASHA_Trainers_Part-2_English.pdf",
    "Reaching_The_Unreached_Brochure_for_ASHA.pdf",
}

def load_all_documents(pdf_dir : str = "data/pdfs", ocr_dir : str = "data/ocr_text"):
    all_docs = []
    pdf_path = Path(pdf_dir)
    ocr_path = Path(ocr_dir)

    pdf_files = list(pdf_path.glob("**/*.pdf"))
    print(f"Found {len(pdf_files)} PDFs, skipping {len(SCANNED_PDFS)} scanned ones")

    for pdf_file in pdf_files:
        if pdf_file.name in SCANNED_PDFS:
            print(f"⏭️ Skipping (scanned) : {pdf_file.name}")
            continue
        try:
            loader = PyMuPDFLoader(str(pdf_file))
            docs = loader.load()
            for doc in docs : 
                doc.metadata["source_file"] = pdf_file.name 
                doc.metadata["source_type"] = "pdf"
            all_docs.extend(docs)
            print(f"✅ Loaded : {pdf_file.name} ({len(docs)} pages)")
        except Exception as e : 
            print(f"❌ Error loading {pdf_file.name} : {e}")
    
    txt_files = list(ocr_path.glob("**/*.txt"))
    print(f"\nFound {len(txt_files)} OCR text files")

    for txt_file in txt_files:
        try:
            loader = TextLoader(str(txt_file), encoding="utf-8")
            docs = loader.load()
            for doc in docs:
                doc.metadata["source_file"] = txt_file.stem + ".pdf"
                doc.metadata["source_type"] = "ocr"
            all_docs.extend(docs)
            print(f"✅ Loaded: {txt_file.name}")
        except Exception as e:
            print(f"❌ Error loading {txt_file.name}: {e}")

    print(f"\nTotal documents loaded: {len(all_docs)}")
    return all_docs

def split_documents(documents, chunk_size=600, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n","\n","."," "]
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks