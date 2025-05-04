from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
import os
import json
import faiss
import numpy as np
from pathlib import Path
import requests
from markitdown import MarkItDown
import time
from models import AddInput, AddOutput, SqrtInput, SqrtOutput, StringsToIntsInput, StringsToIntsOutput, ExpSumInput, ExpSumOutput
from PIL import Image as PILImage
from tqdm import tqdm
import hashlib
from typing import List
import re
from bs4 import BeautifulSoup
import re

mcp = FastMCP("Search and Indexing Engine", "1.0.0")

EMBED_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
CHUNK_SIZE = 256
CHUNK_OVERLAP = 40
ROOT = Path(__file__).parent.resolve()

def get_embedding(text: str) -> np.ndarray:
    response = requests.post(EMBED_URL, json={"model": EMBED_MODEL, "prompt": text})
    response.raise_for_status()
    return np.array(response.json()["embedding"], dtype=np.float32)

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    for i in range(0, len(words), size - overlap):
        yield " ".join(words[i:i+size])

def mcp_log(level: str, message: str) -> None:
    """Log a message to stderr to avoid interfering with JSON communication"""
    sys.stderr.write(f"{level}: {message}\n")
    sys.stderr.flush()

# @mcp.tool()
# def search_documents(query: str) -> list[str]:
#     """Search for relevant content from uploaded documents."""
#     ensure_faiss_ready()
#     mcp_log("SEARCH", f"Query: {query}")
#     try:
#         index = faiss.read_index(str(ROOT / "faiss_index" / "index.bin"))
#         metadata = json.loads((ROOT / "faiss_index" / "metadata.json").read_text())
#         query_vec = get_embedding(query).reshape(1, -1)
#         D, I = index.search(query_vec, k=5)
#         results = []
#         for idx in I[0]:
#             data = metadata[idx]
#             results.append(f"{data['chunk']}\n[Source: {data['doc']}, ID: {data['chunk_id']}]")
#         return results
#     except Exception as e:
#         return [f"ERROR: Failed to search: {str(e)}"]
    
@mcp.tool()
def search_documents(query: str) -> list[str]:
    """Search for relevant content from uploaded documents."""
    ensure_faiss_ready()
    mcp_log("SEARCH", f"Query: {query}")
    try:
        index = faiss.read_index(str(ROOT / "faiss_index" / "index.bin"))
        metadata = json.loads((ROOT / "faiss_index" / "metadata.json").read_text())
        query_vec = get_embedding(query).reshape(1, -1)
        D, I = index.search(query_vec, k=5)
        results = []
        for idx in I[0]:
            data = metadata[idx]
            results.append(f"{data['chunk']}\n[Source: {data['doc']}, URL: {data.get('url','')} , ID: {data['chunk_id']}]")
        return results
    except Exception as e:
        return [f"ERROR: Failed to search: {str(e)}"]

@mcp.tool()
def add(input: AddInput) -> AddOutput:
    print("CALLED: add(AddInput) -> AddOutput")
    return AddOutput(result=input.a + input.b)

@mcp.tool()
def sqrt(input: SqrtInput) -> SqrtOutput:
    """Square root of a number"""
    print("CALLED: sqrt(SqrtInput) -> SqrtOutput")
    return SqrtOutput(result=input.a ** 0.5)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)


# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(input: StringsToIntsInput) -> StringsToIntsOutput:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(StringsToIntsInput) -> StringsToIntsOutput")
    ascii_values = [ord(char) for char in input.string]
    return StringsToIntsOutput(ascii_values=ascii_values)

@mcp.tool()
def int_list_to_exponential_sum(input: ExpSumInput) -> ExpSumOutput:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(ExpSumInput) -> ExpSumOutput")
    result = sum(math.exp(i) for i in input.int_list)
    return ExpSumOutput(result=result)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"

# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")

@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

@mcp.tool()

@mcp.tool()
def process_html(url: str, title: str, text: str = ""):
    """Process the content from a URL and text and create FAISS index"""
    mcp_log("INFO", "Indexing document content...")

    # Define paths
    ROOT = Path(__file__).parent.resolve()
    INDEX_CACHE = ROOT / "faiss_index"
    INDEX_CACHE.mkdir(exist_ok=True)
    INDEX_FILE = INDEX_CACHE / "index.bin"
    METADATA_FILE = INDEX_CACHE / "metadata.json"
    CACHE_FILE = INDEX_CACHE / "doc_index_cache.json"

    # Sanitize title for filename (remove special characters)
    def sanitize_filename(name):
        # Replaces characters that are not allowed in filenames with underscores
        sanitized_name = re.sub(r'[\\/*?:"<>|]', "_", name)
        mcp_log("DEBUG", f"Sanitized filename: {sanitized_name}")
        return sanitized_name

    # Sanitize the title
    safe_title = sanitize_filename(title)

    # Debugging: Check sanitized title
    mcp_log("DEBUG", f"Sanitized title for file: {safe_title}")

    # Save and read from documents_html
    DOCUMENTS_FOLDER = ROOT / "documents_html"
    DOCUMENTS_FOLDER.mkdir(exist_ok=True)
    text_file_path = DOCUMENTS_FOLDER / f"{safe_title}.html"

    # ✅ Write input text to file (ensures file exists)
    try:
        text_file_path.write_text(text, encoding='utf-8')
        mcp_log("INFO", f"Text written to: {text_file_path}")
    except Exception as e:
        mcp_log("ERROR", f"Failed to write file {text_file_path}: {e}")
        return {"status": "error", "message": f"Failed to write file: {e}"}

    # ✅ Read it back
    try:
        text = text_file_path.read_text(encoding='utf-8')
        mcp_log("INFO", "Text successfully read back from file.")
    except Exception as e:
        mcp_log("ERROR", f"Could not read file {text_file_path}: {e}")
        return {"status": "error", "message": f"Could not read file: {e}"}

    # Compute content hash
    def file_hash(content):
        return hashlib.md5(content.encode("utf-8")).hexdigest()

    CACHE_META = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}
    metadata = json.loads(METADATA_FILE.read_text()) if METADATA_FILE.exists() else []
    index = faiss.read_index(str(INDEX_FILE)) if INDEX_FILE.exists() else None

    fhash = file_hash(text)
    if title in CACHE_META and CACHE_META[title] == fhash:
        mcp_log("SKIP", f"Skipping unchanged content for title: {title}")
        return {"status": "skipped", "message": "Content has not changed"}

    mcp_log("PROC", f"Processing content: {title}")
    try:
        # Convert HTML to Markdown (or plain text)
        converter = MarkItDown()  # You need to ensure this is defined
        result = converter.convert(text_file_path)
        markdown = result.text_content

        # Chunk and embed
        chunks = list(chunk_text(markdown))  # Ensure chunk_text is defined
        embeddings_for_file = []
        new_metadata = []

        for i, chunk in enumerate(tqdm(chunks, desc=f"Embedding {title}")):
            embedding = get_embedding(chunk)  # Ensure get_embedding is defined
            embeddings_for_file.append(embedding)
            new_metadata.append({"doc": title, "url": url, "chunk": chunk, "chunk_id": f"{title}_{i}"})

        if embeddings_for_file:
            if index is None:
                dim = len(embeddings_for_file[0])
                index = faiss.IndexFlatL2(dim)
            index.add(np.stack(embeddings_for_file))
            metadata.extend(new_metadata)

        CACHE_META[title] = fhash

    except Exception as e:
        mcp_log("ERROR", f"Failed to process {title}: {e}")
        return {"status": "error", "message": f"Failed to process content: {str(e)}"}

    # Save updates
    CACHE_FILE.write_text(json.dumps(CACHE_META, indent=2))
    METADATA_FILE.write_text(json.dumps(metadata, indent=2))

    if index and index.ntotal > 0:
        faiss.write_index(index, str(INDEX_FILE))
        mcp_log("SUCCESS", "Saved FAISS index and metadata")
        return {"status": "success", "message": "Saved FAISS index and metadata"}
    else:
        mcp_log("WARN", "No new content or updates to process.")
        return {"status": "warn", "message": "No content to index or process."}

def cleat_text(html_text: str) -> str:
    # Step 1: Parse with BeautifulSoup (even though it's not full HTML, it works)
    soup = BeautifulSoup(html_text, "html.parser")

    # Step 2: Get all visible text
    text = soup.get_text(separator="\n")

    # Step 3: Clean up extra newlines and whitespace
    cleaned_text = re.sub(r'\n+', '\n', text)  # Remove multiple newlines
    cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)  # Normalize spaces
    cleaned_text = cleaned_text.strip()

    # Step 4: Optional — Print or use the cleaned text
    print(cleaned_text)


@mcp.tool()
def process_documents():
    """Process documents and create FAISS index"""
    mcp_log("INFO", "Indexing documents with MarkItDown...")
    ROOT = Path(__file__).parent.resolve()
    DOC_PATH = ROOT / "documents"
    INDEX_CACHE = ROOT / "faiss_index"
    INDEX_CACHE.mkdir(exist_ok=True)
    INDEX_FILE = INDEX_CACHE / "index.bin"
    METADATA_FILE = INDEX_CACHE / "metadata.json"
    CACHE_FILE = INDEX_CACHE / "doc_index_cache.json"

    def file_hash(path):
        return hashlib.md5(Path(path).read_bytes()).hexdigest()

    CACHE_META = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}
    metadata = json.loads(METADATA_FILE.read_text()) if METADATA_FILE.exists() else []
    index = faiss.read_index(str(INDEX_FILE)) if INDEX_FILE.exists() else None
    all_embeddings = []
    converter = MarkItDown()

    for file in DOC_PATH.glob("*.*"):
        fhash = file_hash(file)
        if file.name in CACHE_META and CACHE_META[file.name] == fhash:
            mcp_log("SKIP", f"Skipping unchanged file: {file.name}")
            continue

        mcp_log("PROC", f"Processing: {file.name}")
        try:
            result = converter.convert(str(file))
            markdown = result.text_content
            chunks = list(chunk_text(markdown))
            embeddings_for_file = []
            new_metadata = []
            for i, chunk in enumerate(tqdm(chunks, desc=f"Embedding {file.name}")):
                embedding = get_embedding(chunk)
                embeddings_for_file.append(embedding)
                new_metadata.append({"doc": file.name, "chunk": chunk, "chunk_id": f"{file.stem}_{i}"})
            if embeddings_for_file:
                if index is None:
                    dim = len(embeddings_for_file[0])
                    index = faiss.IndexFlatL2(dim)
                index.add(np.stack(embeddings_for_file))
                metadata.extend(new_metadata)
            CACHE_META[file.name] = fhash
        except Exception as e:
            mcp_log("ERROR", f"Failed to process {file.name}: {e}")

    CACHE_FILE.write_text(json.dumps(CACHE_META, indent=2))
    METADATA_FILE.write_text(json.dumps(metadata, indent=2))
    if index and index.ntotal > 0:
        faiss.write_index(index, str(INDEX_FILE))
        mcp_log("SUCCESS", "Saved FAISS index and metadata")
    else:
        mcp_log("WARN", "No new documents or updates to process.")

def ensure_faiss_ready():
    from pathlib import Path
    index_path = ROOT / "faiss_index" / "index.bin"
    meta_path = ROOT / "faiss_index" / "metadata.json"
    if not (index_path.exists() and meta_path.exists()):
        mcp_log("INFO", "Index not found — running process_documents()...")
        process_documents()
    else:
        mcp_log("INFO", "Index already exists. Skipping regeneration.")


if __name__ == "__main__":
    print("STARTING THE SERVER AT AMAZING LOCATION")

    
    
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run() # Run without transport for dev server
    else:
        # Start the server in a separate thread
        import threading
        server_thread = threading.Thread(target=lambda: mcp.run(transport="stdio"))
        server_thread.daemon = True
        server_thread.start()
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Process documents after server is running
        #process_documents()
        test ={
        "url": "https://ollama.com/library/nomic-embed-text",
        "title": "nomic-embed-text",
        "text": open("documents_html/nomic-embed-text.html").read()
        }
        #process_html(test.get("url"),test.get("title"),test.get("text"))
        #search_documents("What is nomice embeddings?")
        # Keep the main thread alive
        try:
            while True:
                 time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")