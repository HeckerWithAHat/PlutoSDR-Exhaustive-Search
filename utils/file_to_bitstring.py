def file_to_bitstring(filepath: str) -> str:
    """
    Reads a file and converts its content to a bitstring.
    
    Parameters:
        filepath - Path to the file to be read
    
    Returns:
        A string representing the content of the file as a bitstring.
    """
    try:
        with open(filepath, "rb") as f:
            content = f.read()  # Read the entire file content as bytes
            bitstring = "".join(f"{byte:08b}" for byte in content)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
    return bitstring
