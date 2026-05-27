import typing


class ConverterError(Exception):
    pass


class Converter:

    fallback: "Converter | None" = None

    def convert(self, ast):
        return self.convert_node(ast)

    def convert_node(self, node):
        nodetype = node.__class__.__name__
        fConvert = getattr(self, "convert_" + nodetype, None)
        if fConvert is None:
            if self.fallback is not None:
                fConvert = self.fallback.convert_node
            else:
                raise ConverterError(
                    f"No converter for node type {nodetype} (Node: {node})"
                )
        try:
            return fConvert(node)
        except ConverterError as e:
            raise e
        except Exception as e:
            print("Exception during conversion of node")
            print(node)
            raise ConverterError(e)
