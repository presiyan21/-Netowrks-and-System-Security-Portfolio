import pefile

def inspect_pe(file_path):
    """Read PE headers: Entry Point, Image Base, Imports."""
    try:
        pe = pefile.PE(file_path)
        entry_point = hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
        image_base = hex(pe.OPTIONAL_HEADER.ImageBase)
        imports = {}
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll_name = entry.dll.decode()
                func_names = [imp.name.decode() if imp.name else "None" for imp in entry.imports]
                imports[dll_name] = func_names
        return {
            'entry_point': entry_point,
            'image_base': image_base,
            'imports': imports
        }
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except pefile.PEFormatError:
        print(f"File {file_path} is not a valid PE file.")
        return None
