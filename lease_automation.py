
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)





def load_json_data(json_file_path: str) -> Dict[str, Any]:
    """
    Load JSON data from a file.
    
    Args:
        json_file_path (str): Path to the JSON file
        
    Returns:
        Dict[str, Any]: Loaded JSON data
        
    Raises:
        FileNotFoundError: If JSON file doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f"Successfully loaded JSON data from {json_file_path}")
            return data
    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {json_file_path}: {e}")
        raise


def load_docx_template(docx_file_path: str) -> Document:
    """
    Load a Word document template.
    
    Args:
        docx_file_path (str): Path to the .docx template file
        
    Returns:
        Document: Loaded Word document
        
    Raises:
        FileNotFoundError: If .docx file doesn't exist
    """
    try:
        doc = Document(docx_file_path)
        logger.info(f"Successfully loaded Word template from {docx_file_path}")
        return doc
    except FileNotFoundError:
        logger.error(f"Word template file not found: {docx_file_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading Word template {docx_file_path}: {e}")
        raise


def replace_placeholders_in_document(doc: Document, data: Dict[str, Any]) -> Document:
    """
    Replace placeholders in the document with JSON data.
    
    Args:
        doc (Document): Word document to process
        data (Dict[str, Any]): Data to insert
        
    Returns:
        Document: Processed document with replaced placeholders
    """
    # Process paragraphs
    for paragraph in doc.paragraphs:
        for key, value in data.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, str(value))
                logger.debug(f"Replaced placeholder {placeholder} with {value}")
    
    # Process tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for key, value in data.items():
                        placeholder = f"{{{{{key}}}}}"
                        if placeholder in paragraph.text:
                            paragraph.text = paragraph.text.replace(placeholder, str(value))
                            logger.debug(f"Replaced placeholder {placeholder} in table with {value}")
    
    # Process headers and footers
    for section in doc.sections:
        for header in section.header.paragraphs:
            for key, value in data.items():
                placeholder = f"{{{{{key}}}}}"
                if placeholder in header.text:
                    header.text = header.text.replace(placeholder, str(value))
                    logger.debug(f"Replaced placeholder {placeholder} in header with {value}")
        
        for footer in section.footer.paragraphs:
            for key, value in data.items():
                placeholder = f"{{{{{key}}}}}"
                if placeholder in footer.text:
                    footer.text = footer.text.replace(placeholder, str(value))
                    logger.debug(f"Replaced placeholder {placeholder} in footer with {value}")
    
    logger.info("Completed placeholder replacement in document")
    return doc


def save_document(doc: Document, output_path: str) -> None:
    """
    Save the processed document to a file.
    
    Args:
        doc (Document): Document to save
        output_path (str): Path where to save the document
        
    Raises:
        Exception: If saving fails
    """
    try:
        doc.save(output_path)
        logger.info(f"Successfully saved processed document to {output_path}")
    except Exception as e:
        logger.error(f"Error saving document to {output_path}: {e}")
        raise


def process_lease_document(json_file_path: str, docx_template_path: str, output_path: Optional[str] = None) -> str:
    """
    Main function to process JSON data and merge it into a Word document template.
    
    Args:
        json_file_path (str): Path to the JSON file containing data
        docx_template_path (str): Path to the .docx template file
        output_path (Optional[str]): Path for the output file. If None, generates one automatically
        
    Returns:
        str: Path to the generated .docx file
        
    Raises:
        FileNotFoundError: If input files don't exist
        json.JSONDecodeError: If JSON is invalid
        Exception: For other processing errors
    """
    logger.info("Starting lease document processing")
    
    # Validate input files
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")
    
    if not os.path.exists(docx_template_path):
        raise FileNotFoundError(f"Word template not found: {docx_template_path}")
    
    # Generate output path if not provided
    if output_path is None:
        input_dir = os.path.dirname(docx_template_path)
        input_name = Path(docx_template_path).stem
        output_path = os.path.join(input_dir, f"{input_name}_processed.docx")
    
    try:
        # Load JSON data
        data = load_json_data(json_file_path)
        logger.info(f"Loaded {len(data)} data fields from JSON")
        
        # Load Word template
        doc = load_docx_template(docx_template_path)
        
        # Process document (replace placeholders)
        processed_doc = replace_placeholders_in_document(doc, data)
        
        # Save processed document
        save_document(processed_doc, output_path)
        
        logger.info("Lease document processing completed successfully")
        return output_path
        
    except Exception as e:
        logger.error(f"Error processing lease document: {e}")
        raise


def main():
    """
    Main function that can be called from command line or imported.
    """
    if len(sys.argv) < 3:
        print("Usage: python3 lease_automation.py <json_file> <docx_template> [output_file]")
        print("Example: python3 lease_automation.py lease_data.json template.docx output.docx")
        sys.exit(1)
    
    json_file = sys.argv[1]
    docx_template = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        result_path = process_lease_document(json_file, docx_template, output_file)
        print(f"✅ Successfully processed document: {result_path}")
    except Exception as e:
        print(f"❌ Error processing document: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
