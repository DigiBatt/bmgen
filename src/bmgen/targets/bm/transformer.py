import ast
from bmgen.transformer import Transformer as _Transformer


class Transformer(_Transformer):
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
        if node.orelse:
            elsenode = ast.With(
                items=[
                    ast.withitem(
                        context_expr=ast.Call(
                            func=ast.Name(id="ctrl_else", ctx=ast.Load()),
                            args=[],
                            keywords=[],
                        )
                    )
                ],
                body=node.orelse,
            )
            a.body.append(elsenode)
            a.items[0].context_expr.args.append(ast.Constant(value=True))
            self.imports["ctrl"].add("ctrl_else")
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
        self.imports["program"].add("variable")
        self.generic_visit(node)
        return a
