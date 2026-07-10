import os
import subprocess
import logging
import re
from pathlib import Path

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_docx_to_md(input_path: str, output_path: str) -> bool:
    """
    Extracts raw text/Markdown from a .docx file using pandoc.
    """
    input_file = Path(input_path)
    output_file = Path(output_path)
    
    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        return False
        
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Extracting: {input_file.name} -> {output_file.name}")
    
    try:
        cmd = [
            "pandoc", 
            "--track-changes=all",
            "-t", "gfm",
            str(input_file), 
            "-o", 
            str(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(f"Successfully extracted {input_file.name}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Pandoc extraction failed for {input_file.name}")
        logger.error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error processing {input_file.name}: {e}")
        return False

if __name__ == "__main__":
    source_dir = Path(r"R:\B2\04 - EUROMOD JRC\01 - Repository\02 - Country reports\J2.0+ (2022-2025)\01 - Word")
    output_dir = Path("./country-reports/Y16")
    
    processed_count = 0
    
    logger.info("Starting batch extraction for all remaining countries in Y16.")
    
    # Iterate through all Y16_CR_*.docx files
    for input_docx in sorted(source_dir.glob("Y16_CR_*.docx")):
        # Extract country code using regex
        match = re.search(r"Y16_CR_([A-Z]{2})\.docx", input_docx.name)
        if not match:
            continue
            
        country_code = match.group(1)
        output_md = output_dir / f"{country_code}_Y16.md"
        
        # Skip if file already exists
        if output_md.exists():
            logger.info(f"Skipping {country_code}, output already exists.")
            continue
            
        success = extract_docx_to_md(str(input_docx), str(output_md))
        if success:
            processed_count += 1
            
    logger.info(f"Finished. Extracted {processed_count} new files.")
