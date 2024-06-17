import ast

import astor

from bmgen.transformer import Transformer as _Transformer


class Transformer(_Transformer):

    def __init__(self, *args, **kwargs):
        self.loop_idx = 0
        super().__init__(*args, **kwargs)

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
        loop_name = f"bmgen_loop_{self.loop_idx}"
        loop_body = ast.Module(body=node.body, type_ignores=[])
        self.generic_visit(loop_body)
        loop_code = ast.copy_location(
            ast.Assign(
                targets=[ast.Name(id=loop_name, ctx=ast.Store())],
                value=ast.Constant(value=astor.to_source(loop_body)),
            ),
            node,
        )
        loop_call = ast.copy_location(
            ast.Expr(
                value=ast.Call(
                    func=ast.Name(id="ctrl_for", ctx=ast.Load()),
                    args=[
                        node.iter,
                        ast.Name(id=loop_name, ctx=ast.Load()),
                        ast.Constant(value=node.target.id),
                        ast.Call(
                            func=ast.Name(id="globals", ctx=ast.Load()),
                            args=[],
                            keywords=[],
                        ),
                        ast.Call(
                            func=ast.Name(id="locals", ctx=ast.Load()),
                            args=[],
                            keywords=[],
                        ),
                    ],
                    keywords=[],
                )
            ),
            node,
        )
        self.loop_idx += 1
        self.imports["ctrl"].add("ctrl_for")
        self.imports["program"].add("variable")
        self.generic_visit(node)
        return [loop_code, loop_call]
