from types import GeneratorType
from typing import Any, Callable, Dict, Generator, List, Union, Optional
from typing_extensions import Self


class Node:
    tag: str
    children: List[Union["Node", str]]
    attributes: Dict[str, Any]
    formatters: Dict[str, Callable[[Any], str]]

    def __init__(self, tag: str):
        self.tag = tag
        self.children = []
        self.attributes = {}
        self.formatters = {}

    def __call__(
        self,
        *children: Union["Node", Generator[Union["Node", str, None], None, None], str, None],
        **attributes: Any,
    ) -> Self:
        if len(self.children) > 0 and len(children) > 0:
            raise ValueError("Cannot add children to a node that already has children")

        if len(children) > 0 and len(attributes) > 0:
            raise ValueError(
                f"You should not pass attributes and children in one call. Use "
                f"node(x=4,y=5)(child1, child2, child3)"
            )

        new_node = type(self)(self.tag)
        new_node.children = _flatten(list(children))
        new_node.attributes = {**self.attributes, **attributes}
        new_node.formatters = {**self.formatters}
        return new_node

    def add(self, **attributes: float) -> Self:
        attrs = {k: v for k, v in self.attributes.items()}

        for k, v in attributes.items():
            attrs[k] = float(attrs[k]) + v

        new_node = Node(self.tag)
        new_node.children = [*self.children]
        new_node.attributes = attrs
        new_node.formatters = {**self.formatters}
        return new_node

    def mul(self, **attributes: float) -> Self:
        attrs = {k: v for k, v in self.attributes.items()}

        for k, v in attributes.items():
            attrs[k] = float(attrs[k]) * v

        new_node = Node(self.tag)
        new_node.children = [*self.children]
        new_node.attributes = attrs
        new_node.formatters = {**self.formatters}
        return new_node

    def __str__(self):
        attr_string = "".join(
            [self._format_attribute(*attr) for attr in self.attributes.items()]
        )
        if self.children:
            child_string = "\n".join([_indent(str(c), "  ") for c in self.children])
            return f"<{self.tag}{attr_string}>\n{child_string}\n</{self.tag}>"
        else:
            return f"<{self.tag}{attr_string} />"

    def with_formatter(self, **formatters: Callable[[Any], str]) -> "Node":
        new_node = Node(self.tag)
        new_node.children = [*self.children]
        new_node.attributes = {**self.attributes}
        new_node.formatters = {**self.formatters, **formatters}
        return new_node

    def _format_attribute(self, key: str, value: Any) -> str:
        if value is None:
            return ""

        if key == "className":
            kstr = "class"
        else:
            kstr = key.replace("__", ":").replace("_", "-")

        if key in self.formatters:
            vstr = self.formatters[key](value)
        elif isinstance(value, list):
            vstr = " ".join(value)
        elif isinstance(value, dict):
            vstr = "".join(f"{k}:{v};" for k, v in value.items())
        elif isinstance(value, float):
            vstr = f"{value:g}"
        else:
            vstr = f"{value}"

        return f' {kstr}="{vstr}"'


def _flatten(x: List) -> List:
    r = []
    for y in x:
        if isinstance(y, list):
            r.extend(_flatten(y))
        if isinstance(y, GeneratorType):
            r.extend(_flatten(list(y)))
        else:
            r.append(y)
    return r


def _indent(x: str, indentation: str = "\t") -> str:
    return "".join([indentation + l for l in x.splitlines(keepends=True)])
