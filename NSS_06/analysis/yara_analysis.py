import yara

def match_yara(file_path, rule_source):
    """Compile a YARA rule and run it against the target file."""
    rules = yara.compile(source=rule_source)
    return rules.match(file_path)
