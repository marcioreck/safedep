import ast

DANGEROUS_FUNCTIONS = {
    "eval", "exec", "os.system", "os.popen",
    "subprocess.run", "subprocess.call", "subprocess.Popen",
    "requests.post", "requests.put", "urllib.request.urlopen"
}

class SecurityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.findings = []

    def visit_Call(self, node):
        func_name = self._get_func_name(node.func)
        if func_name in DANGEROUS_FUNCTIONS:
            self.findings.append({
                "function": func_name,
                "line": node.lineno,
                "col": node.col_offset
            })
        self.generic_visit(node)

    def _get_func_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value = self._get_func_name(node.value)
            if value:
                return f"{value}.{node.attr}"
        return None

def scan_static_code(code_content):
    """
    Scan code for dangerous function calls using AST.
    """
    try:
        tree = ast.parse(code_content)
        visitor = SecurityVisitor()
        visitor.visit(tree)
        return visitor.findings
    except SyntaxError:
        return [{"error": "Syntax error in code, could not scan."}]
