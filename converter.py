# function that takes in a JSON file and converts it to a Key Value mapping pair. It is able to dynamically generate/add signature blocks
# three main steps  
# the JSON file is a list of objects with the following structure:
"""
{
  "document_name": "Foster_SK_Lilac Easement Agreement (WA)",
  "grantor_type": "Individual",
  "grantor_name_1": "Stephen Douglas Foster",
  "grantor_name_2": "Karen Rene Foster",
  "trust_entity_name": "NA",
  "grantor_name": "Stephen Douglas Foster and Karen Rene Foster",
  "owner_type": "a married couple",
  "number_of_grantor_signatures": 2,
  "grantor_address_1": "1706 RIVER TRL SUGAR LAND",
  "grantor_address_2": "SUGAR LAND TX 77479",
  "state": "Washington",
  "county": "Spokane",
  "total_acres": 35.2,
  "apn_list": ["16174.908", "16174.9077", "16174.9078"],
  "parcels": [
    {
      "apn": "16174.908",
      "acres": 15.2,
      "legal_description": "17-26-41(SE1/4): THE NORTH 492.68 FT OF THE SOUTH 1645.84 FT OF THE SE1/4; EXCEPT THE WEST 1329.35 FT THEREOF. (PARCEL D ROS AFN 7390810)",
      "isPortion": False
    },
    {
      "apn": "16174.9077",
      "acres": 10,
      "legal_description": "17-26-41(SE1/4): THE WEST 887.00 FT OF THE NORTH 492.68 FT OF THE SOUTH 1645.84 FT OF THE SE1/4; EXCEPT COUNTY ROADS. (PARCEL A ROS AFN 7390810)",
      "isPortion": False
    },
    {
      "apn": "16174.9078",
      "acres": 10,
      "legal_description": "17-26-41(SE1/4): THE WEST 887.00 FT OF THE SOUTH 1153.16 FT OF THE SE1/4; EXCEPT THE S1/2 OF THE S1/2 OF SAID SE1/4; AND EXCEPT COUNTY ROADS. (PARCEL B ROS AFN 7390810)",
      "isPortion": False
    }
  ],
  "number_of_parcels": 3
}
"""
# after that the signature block with and without the notraries are created

#!/usr/bin/env python3
"""
Comprehensive Signature Block Generator Module
Uses the existing generator() function for dynamic/nested functionality.
Returns both signature blocks in JSON format.
"""
import os
import json
def load_sig_block_template(filename):
    """
    Load a signature block template from the templates/sigBlocks directory.
    
    Args:
        filename (str): Name of the template file
        
    Returns:
        str: Template content
    """  
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Use repository root (this file's directory) for current structure
        project_root = script_dir
        path = os.path.join(project_root, 'templates', 'sigBlocks', filename)
        
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return f"Template file '{filename}' not found at {path}"
    except Exception as e:
        return f"Error reading template: {str(e)}"

def load_notary_template():
    """
    Load the notary template from templates/Notorary/notrary.txt.
    
    Returns:
        str: Notary template content
    """
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Use repository root (this file's directory) for current structure
        project_root = script_dir
        notary_file_path = os.path.join(project_root, 'templates', 'Notorary', 'notrary.txt')
        
        with open(notary_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Notary block template file 'notrary.txt' not found."
    except Exception as e:
        return f"Error reading notary block: {str(e)}"

def get_sig_block(owner_type, num_signatures):
    """
    Get signature block content based on owner type and number of signatures.
    
    Args:
        owner_type (str): Type of owner (individual, corporation, etc.)
        num_signatures (int): Number of signatures needed
        
    Returns:
        list: Array with filename1 and filename2 content
    """
    filename1 = None
    filename2 = None
    filename1Content = None
    filename2Content = None
    
    # Map owner types to template files (using files that actually exist)
    if owner_type == 'his/her sole property' and num_signatures == 1:
        filename1 = 'SI1.txt'
    elif owner_type == 'a married couple' and num_signatures == 2:
        filename1 = 'I1.txt'
        filename2 = 'I1.txt'
    elif owner_type == 'Corporation':
        filename1 = 'E1.txt'
        if num_signatures == 2:
            filename2 = 'E1.txt'
    elif owner_type == 'LLC':
        filename1 = 'E1.txt'
        if num_signatures == 2:
            filename2 = 'E1.txt'
    elif owner_type == 'LP':    
        filename1 = 'E1.txt'
        if num_signatures == 2:
            filename2 = 'E1.txt'
    elif owner_type == 'Trust':
        filename1 = 'E1.txt'
        if num_signatures == 2:
            filename2 = 'E1.txt'
    elif owner_type == 'Sole Owner, married couple' and num_signatures == 2:
        filename1 = 'I1.txt'
        filename2 = 'SI1.txt'
    elif 'individual' in owner_type.lower():
        # Default individual case
        filename1 = 'I1.txt'
        if num_signatures == 2:
            filename2 = 'I1.txt'
    else:
        # Default entity case
        filename1 = 'E1.txt'
        if num_signatures == 2:
            filename2 = 'E1.txt'
    
    # Load content from filename1 if it exists
    if filename1:
        filename1Content = load_sig_block_template(filename1)
    
    # Load content from filename2 if it exists  
    if filename2:
        filename2Content = load_sig_block_template(filename2)
    
    # Return array with filename1 and filename2 content
    return [filename1Content, filename2Content]

def generator(owner_type, is_notary, notary_block, num_signatures):
    """
    Generate signature blocks using the existing generator logic.
    This is the main function used in the /generate_signature_block route.
    
    Args:
        owner_type (str): Type of owner
        is_notary (bool): Whether to include notary
        notary_block (str): Notary block content
        num_signatures (int): Number of signatures
        
    Returns:
        str: Generated signature block(s)
    """
    # Generate notary block with default parameters
    notary_content = load_notary_template()
    
    # Get signature block content
    filecontent = get_sig_block(owner_type, num_signatures)
    sigB1 = filecontent[0] if filecontent[0] is not None else ''
    sigB2 = filecontent[1] if filecontent[1] is not None else ''
    
    final_string = ""

    # Edge case where there are unique sig blocks 
    if owner_type == 'Sole owner, married couple' and is_notary:
        final_string += sigB1
        if is_notary and notary_content:
            final_string += "\n\n" + notary_content
        final_string += "\n\n" + sigB2
        if is_notary and notary_content:
            final_string += "\n\n" + notary_content
        return final_string
    
    if owner_type == 'Sole owner, married couple' and not is_notary:
        final_string += sigB1
        final_string += "\n\n" + sigB2
        return final_string
    
    # Generate additional signature blocks based on num_signatures
    for i in range(num_signatures):
        if is_notary and notary_content:
            final_string += "\n\n" + sigB1
            final_string += "\n\n" + notary_content
        else:
            final_string += "\n\n" + sigB1

    return final_string

def generate_signature_blocks_from_json(json_data):
    """
    Generate signature blocks with and without notary from JSON data.
    Uses the existing generator() function twice for proper dynamic/nested functionality.
    
    Args:
        json_data (dict): JSON data containing grantor information
        
    Returns:
        dict: JSON response with both signature blocks
    """
    try:
        # Step 1: Extract information from JSON using getter methods
        grantor_name = json_data.get('grantor_name', '')
        grantor_name_1 = json_data.get('grantor_name_1', '')
        grantor_name_2 = json_data.get('grantor_name_2', '')
        trust_entity_name = json_data.get('trust_entity_name', '')
        owner_type = json_data.get('owner_type', 'individual')
        number_of_signatures = json_data.get('number_of_grantor_signatures', 1)
        state = json_data.get('state', '')
        county = json_data.get('county', '')
        
        # Step 2: Call the generator() function twice
        # First call: WITHOUT notary (isNotary = False)
        signature_block_without_notary = generator(
            owner_type=owner_type,
            is_notary=False,  # isNotary = False
            notary_block='',
            num_signatures=number_of_signatures
        )
        
        # Second call: WITH notary (isNotary = True)
        signature_block_with_notary = generator(
            owner_type=owner_type,
            is_notary=True,   # isNotary = True
            notary_block='',
            num_signatures=number_of_signatures
        )
        
        # Step 3: Return both generated blocks in JSON format (standardized keys)
        return {
            "Signature_block": signature_block_without_notary,
            "Signature_Block_With_Notary": signature_block_with_notary
        }
        
    except Exception as e:
        # Return error in the same format
        return {
            "signature_block": f"Error generating signature block: {str(e)}",
            "Signature Block With Notrary": f"Error generating signature block with notary: {str(e)}"
        }

# after that exhibit A is generated and apennded to the JSON
"""
    Build the Exhibit A text string from JSON data by creating parcel objects and generating custom exhibit.
    
    Args:
        json_data: JSON string or dict containing parcel data
    
    Returns:
        dict: JSON object with custom exhibit A string and metadata
"""


def build_exhibit_string_from_json(json_data):
   
    try:
        print("[DEBUG] Starting exhibit string generation from JSON")
        
        # Parse JSON if it's a string
        if isinstance(json_data, str):
            import json
            data = json.loads(json_data)
        else:
            data = json_data
        
        # Extract document information
        document_name = data.get("document_name", "Unknown Document")
        grantor_type = data.get("grantor_type", "Unknown")
        grantor_name = data.get("grantor_name", "Unknown")
        state = data.get("state", "Unknown")
        county = data.get("county", "Unknown")
        total_acres = data.get("total_acres", 0)
        number_of_parcels = data.get("number_of_parcels", 0)
        
        # Extract and create parcel objects
        raw_parcels = data.get("parcels", [])
        
        print(f"[DEBUG] Processing document: {document_name}")
        print(f"[DEBUG] Found {len(raw_parcels)} parcels, total acres: {total_acres}")
        
        # Validate parcels data
        if not isinstance(raw_parcels, list) or len(raw_parcels) == 0:
            raise ValueError("Parcels must be a non-empty list")
        
        # Create parcel objects from the JSON data
        parcel_objects = []
        for i, raw_parcel in enumerate(raw_parcels, 1):
            if not isinstance(raw_parcel, dict):
                print(f"[WARNING] Invalid parcel data at index {i}: {raw_parcel}")
                continue
            
            # Create parcel object with all the data
            parcel_obj = {
                "parcelNumber": i,
                "apn": raw_parcel.get("apn", f"Unknown-{i}"),
                "acres": raw_parcel.get("acres", 0),
                "legal_description": raw_parcel.get("legal_description", "No legal description provided"),
                "isPortion": raw_parcel.get("isPortion", False),
                "templateType": "standard"  # Default template type
            }
            
            parcel_objects.append(parcel_obj)
            print(f"[DEBUG] Created parcel object {i}: APN {parcel_obj['apn']}, {parcel_obj['acres']} acres, isPortion: {parcel_obj['isPortion']}")
        
        # Now use the existing build_exhibit_string function with our parcel objects
        exhibit_string = build_exhibit_string(parcel_objects)
        
        # Create the output JSON structure
        output_json = {
            "document_name": document_name,
            "grantor_type": grantor_type,
            "grantor_name": grantor_name,
            "state": state,
            "county": county,
            "total_acres": total_acres,
            "number_of_parcels": number_of_parcels,
            "exhibit_a_string": exhibit_string,
            "parcels_processed": len(parcel_objects),
            "parcel_objects": parcel_objects,  # Include the created parcel objects
            "generation_timestamp": __import__('datetime').datetime.now().isoformat()
        }
        
        print(f"[DEBUG] Generated exhibit string, length: {len(exhibit_string)}")
        print(f"[DEBUG] Output JSON created with {len(output_json)} fields")
        print(f"[DEBUG] Created {len(parcel_objects)} parcel objects")
        
        return output_json
        
    except Exception as e:
        print(f"[ERROR] Failed to build exhibit string from JSON: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return error JSON
        error_json = {
            "error": str(e),
            "error_type": type(e).__name__,
            "generation_timestamp": __import__('datetime').datetime.now().isoformat()
        }
        return error_json
def build_exhibit_string(parcels):
    """
    Build the Exhibit A text string from parcel objects.
    
    Args:
        parcels: List of parcel objects with parcelNumber, isPortion, and templateType properties
    
    Returns:
        str: The complete Exhibit A text string
    """
    try:
        print(f"[DEBUG] Building exhibit string for {len(parcels)} parcels")
        
        # Validate parcels data
        if not isinstance(parcels, list) or len(parcels) == 0:
            raise ValueError("Parcels must be a non-empty list")
        
        # Start with header
        exhibit_parts = ["EXHIBIT A", "", "General Description of Property", ""]
        
        # Add image placeholder
        exhibit_parts.append("[Image]")
        exhibit_parts.append("")
        
        # Add parcel descriptions using the parcel objects
        for parcel in parcels:
            if not isinstance(parcel, dict):
                print(f"[WARNING] Invalid parcel object: {parcel}")
                continue
            
            parcel_number = parcel.get("parcelNumber", "Unknown")
            apn = parcel.get("apn", "Unknown")
            acres = parcel.get("acres", 0)
            legal_description = parcel.get("legal_description", "No legal description provided")
            is_portion = parcel.get("isPortion", False)
            
            # Create custom description based on whether it's a portion or parcel
            if is_portion:
                parcel_description = f"Portion {parcel_number} (APN: {apn}, {acres} acres):\n\n{legal_description}"
            else:
                parcel_description = f"Parcel {parcel_number} (APN: {apn}, {acres} acres):\n\n{legal_description}"
            
            print(f"[DEBUG] Processing {parcel_number}: APN {apn}, {acres} acres, isPortion: {is_portion}")
            exhibit_parts.append(parcel_description)
            exhibit_parts.append("")  # Add spacing between parcels
        
        # Join all parts
        exhibit_string = "\n".join(exhibit_parts)
        
        print(f"[DEBUG] Generated exhibit string, length: {len(exhibit_string)}")
        return exhibit_string
        
    except Exception as e:
        print(f"[ERROR] Failed to build exhibit string: {str(e)}")
        import traceback
        traceback.print_exc()
        raise










# code to add both to the 






# the final format is a JSON file with the following structure:





# real conversion 
#step one read the JSON file and assign the value on the left to the key and the value on the right to the value

# return the JSON key value mapping pair


json_data = {
  "document_name": "Foster_SK_Lilac Easement Agreement (WA)",
  "grantor_type": "Individual",
  "grantor_name_1": "Stephen Douglas Foster",
  "grantor_name_2": "Karen Rene Foster",
  "trust_entity_name": "NA",
  "grantor_name": "Stephen Douglas Foster and Karen Rene Foster",
  "owner_type": "a married couple",
  "number_of_grantor_signatures": 2,
  "grantor_address_1": "1706 RIVER TRL SUGAR LAND",
  "grantor_address_2": "SUGAR LAND TX 77479",
  "state": "Washington",
  "county": "Spokane",
  "total_acres": 35.2,
  "apn_list": ["16174.908", "16174.9077", "16174.9078"],
  "parcels": [
    {
      "apn": "16174.908",
      "acres": 15.2,
      "legal_description": "17-26-41(SE1/4): THE NORTH 492.68 FT OF THE SOUTH 1645.84 FT OF THE SE1/4; EXCEPT THE WEST 1329.35 FT THEREOF. (PARCEL D ROS AFN 7390810)",
      "isPortion": False
    },
    {
      "apn": "16174.9077",
      "acres": 10,
      "legal_description": "17-26-41(SE1/4): THE WEST 887.00 FT OF THE NORTH 492.68 FT OF THE SOUTH 1645.84 FT OF THE SE1/4; EXCEPT COUNTY ROADS. (PARCEL A ROS AFN 7390810)",
      "isPortion": False
    },
    {
      "apn": "16174.9078",
      "acres": 10,
      "legal_description": "17-26-41(SE1/4): THE WEST 887.00 FT OF THE SOUTH 1153.16 FT OF THE SE1/4; EXCEPT THE S1/2 OF THE S1/2 OF SAID SE1/4; AND EXCEPT COUNTY ROADS. (PARCEL B ROS AFN 7390810)",
      "isPortion": False
    }
  ],
  "number_of_parcels": 3
}




def update_json_with_generated_content(json_data):
    """
    Update the JSON data with generated signature blocks and exhibit A content.
    
    Args:
        json_data (dict): The JSON data dictionary to update
        
    Returns:
        dict: Updated JSON data with signature blocks and exhibit A
    """
    # Generate signature blocks and exhibit A content
    sigBlocks = generate_signature_blocks_from_json(json_data)
    exhibitA = build_exhibit_string_from_json(json_data)
    
    # Add the two signature blocks individually (use standardized keys)
    json_data["Signature_block"] = sigBlocks.get("Signature_block")
    # Backward compatibility for any older key names
    json_data["Signature_Block_With_Notary"] = sigBlocks.get("Signature_Block_With_Notary") or sigBlocks.get("Signature Block With Notrary") or sigBlocks.get("Signature Block With Notary")
    
    # Add the exhibit A content
    json_data["exhibit_a"] = exhibitA
    
    return json_data




def main():
    return update_json_with_generated_content(json_data)

if __name__ == "__main__":
    main()

