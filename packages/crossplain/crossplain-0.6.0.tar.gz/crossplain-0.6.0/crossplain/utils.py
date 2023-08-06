def split_expression(expression: str) -> list[str]:
    parts = []
    buffer = ""
    inside_quotes = None # quote type 
    escaped = lambda i: i > 0 and expression[i-1] == "\\"
    for i, character in enumerate(expression):
        if character in ['"', "'"]:
            if inside_quotes is None:
                inside_quotes = character
            elif not escaped(i):
                inside_quotes = None
                parts.append(buffer)
                buffer = ""
        elif character == " " and not inside_quotes:
            parts.append(buffer)
            buffer = ""
        else:
            buffer += character
    
    if buffer:
        parts.append(buffer)

    return parts
