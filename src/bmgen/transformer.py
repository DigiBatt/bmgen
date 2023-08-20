import ast


class Transformer(ast.NodeTransformer):
    def __init__(self, target):
        self.target = target
        self.imports = {"ctrl": set(), "program": set()}

    def visit_Module(self, node):
        self.generic_visit(node)
        for module, names in self.imports.items():
            if not names:
                continue
            importnode = ast.ImportFrom(
                module="bmgen.targets." + self.target + "." + module,
                names=[ast.alias(name=n) for n in names],
                level=0,
            )
            node.body.insert(0, importnode)
        return node

    def visit_Import(self, node):
        for i in node.names:
            if i.name.startswith("bmgen"):
                i.name = "bmgen.targets." + self.target + i.name[5:]
        self.generic_visit(node)
        return node

    def visit_ImportFrom(self, node):
        if node.module.startswith("bmgen"):
            node.module = "bmgen.targets." + self.target + node.module[5:]
        self.generic_visit(node)
        return node

    def visit_If(self, node):
        a = ast.copy_location(
            ast.With(
                items=[
                    ast.withitem(
                        context_expr=ast.Call(
                            func=ast.Name(id="ctrl_if", ctx=ast.Load()),
                            args=[node.test],
                            keywords=[],
                        )
                    )
                ],
                body=node.body,
            ),
            node,
        )
        self.imports["ctrl"].add("ctrl_if")
        self.generic_visit(node)
        return a

    def visit_For(self, node):
        a = ast.copy_location(
            ast.With(
                items=[
                    ast.withitem(
                        context_expr=ast.Call(
                            func=ast.Name(id="ctrl_for", ctx=ast.Load()),
                            args=[
                                ast.Call(
                                    func=ast.Name(id="variable", ctx=ast.Load()),
                                    args=[ast.Constant(value=node.target.id)],
                                    keywords=[],
                                ),
                                node.iter,
                            ],
                            keywords=[],
                        ),
                        optional_vars=ast.Name(id=node.target.id, ctx=ast.Store()),
                    )
                ],
                body=node.body,
            ),
            node,
        )
        self.imports["ctrl"].add("ctrl_for")
        self.generic_visit(node)
        return a

    def visit_Assign(self, node):
        a = ast.copy_location(
            ast.Assign(
                value=ast.Call(
                    func=ast.Name(id="variable", ctx=ast.Load()),
                    args=[
                        ast.Constant(value=node.targets[0].id),
                        node.value,
                    ],
                    keywords=[],
                ),
                targets=[node.targets[0]],
            ),
            node,
        )
        self.imports["program"].add("variable")
        self.generic_visit(node)
        return a
