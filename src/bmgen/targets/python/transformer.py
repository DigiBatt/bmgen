import ast

import astor

from bmgen.transformer import Transformer as _Transformer


class Transformer(_Transformer):

    def __init__(self, *args, **kwargs):
        self.loop_idx = 0
        super().__init__(*args, **kwargs)

    def visit_For(self, node):
        loop_name = f"bmgen_loop_{self.loop_idx}"
        loop_body = ast.Module(body=node.body, type_ignores=[])
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

    def visit_Constant(self, node):
        a = ast.copy_location(
            ast.Call(
                func=ast.Name(id="constant", ctx=ast.Load()),
                args=[
                    ast.Constant(value=node.value),
                ],
                keywords=[],
            ),
            node,
        )
        self.generic_visit(node)
        return a
