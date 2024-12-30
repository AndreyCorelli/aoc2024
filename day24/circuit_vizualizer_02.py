from collections import deque
from typing import Tuple, List, Optional, Dict

import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

from day24.solution_base import Circuit, Operation

Coords = Tuple[int, int]

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day24/input.txt"


SLOT_W = 180
SLOT_H = 180
PADDING = 60
PIN = 25
NW, NH = SLOT_W - PADDING * 2, SLOT_H - PADDING * 2

FONT_SIZE = 15
FONT = ImageFont.load_default()


class Node:
    def __init__(self, slot: Coords):
        self.operation: Optional[Operation] = None
        self.slot: Coords = slot
        self.inputs: List[Node] = []
        self.output: Optional[Node] = None


class CircuitVisualizer:
    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        self.nodes: List[Node] = []
        self._next_free_y: Dict[int, int] = {i: 0 for i in range(-100, 1)}

    def visualize(self):
        self._build_nodes()

        # determine size
        min_x, max_y = 0, 0
        for k, v in self._next_free_y.items():
            if not v:
                continue
            max_y = max(max_y, v)
            min_x = min(min_x, k)

        w, h = abs(min_x), max_y
        # invert x of all nodes (make it positive)
        for node in self.nodes:
            node.slot = -node.slot[0], node.slot[1]

        canvas_w, canvas_h = (w + 1) * SLOT_W, (h + 1) * SLOT_H
        canvas_color = "white"
        canvas = Image.new("RGB", (canvas_w, canvas_h), canvas_color)
        draw = ImageDraw.Draw(canvas)

        for node in self.nodes:
            self._draw_node(draw, node)

        canvas.show()

    def _draw_node(self, draw: ImageDraw, node: Node) -> None:
        pivot = node.slot[0] * SLOT_W, node.slot[1] * SLOT_H
        l, t, w, h = pivot[0] + PADDING, pivot[1] + PADDING, NW, NH

        input_ys = [pivot[1] + PADDING + NH // 4,
                    pivot[1] + PADDING + NH - NH // 4]

        draw.rectangle([l, t, l + w, t + h], outline="black", fill="white")

        text = str(node.operation)
        bbox = draw.textbbox((0, 0), text, font=FONT)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        text_x = l + (w - text_width) // 2
        text_y = t + 5  # Add a small margin from the top

        draw.text((text_x, text_y), text, fill="black", font=FONT)

        # input pins
        draw.line([(l - PIN, input_ys[0]), (l, input_ys[0])], fill="black", width=1)
        draw.line([(l - PIN, input_ys[1]), (l, input_ys[1])], fill="black", width=1)
        # output
        draw.line([(l + NW, pivot[1] + SLOT_H // 2), (l + NW + PIN, pivot[1] + SLOT_H // 2)], fill="green", width=1)

        # draw lines to inputs
        for i, inp in enumerate(node.inputs):
            end_x, end_y = l - PIN, input_ys[i]
            inp_pivot = inp.slot[0] * SLOT_W, inp.slot[1] * SLOT_H

            s_x = inp_pivot[0] + PADDING + NW + PIN
            s_y = inp_pivot[1] + PADDING + NH // 2

            draw.line([(s_x, s_y), (end_x, end_y)], fill="black", width=1)

    def _build_nodes(self) -> None:
        z_cluster = self.circuit.operations_ordered[-1]
        z_cluster.sort(key=lambda x: x.out_code)

        queue = deque()
        visited = set()

        # Initialize the BFS queue with the "root" operations
        for op in z_cluster:
            root_node = self._place_node(op, None, 0)
            queue.append((op, root_node, 0))

        while queue:
            op, parent_node, x = queue.popleft()

            # Lookup the input operations
            def lookup_op_by_output(out_name: str) -> Optional[Operation]:
                for op in self.circuit.operations:
                    if op.out_code == out_name:
                        return op
                return None

            a_op, b_op = lookup_op_by_output(op.a), lookup_op_by_output(op.b)

            # Process `a_op` and `b_op` equally
            for input_op in [a_op, b_op]:
                if input_op and input_op not in visited:
                    visited.add(input_op)
                    child_node = self._place_node(input_op, parent_node, x - 1)
                    parent_node.inputs.append(child_node)
                    queue.append((input_op, child_node, x - 1))

    def _place_node(self, op: Operation, out_op: Optional[Node], x: int) -> Node:
        # Determine the y-coordinate and create the node
        y = self._next_free_y[x]
        self._next_free_y[x] = y + 1
        node = Node((x, y))
        node.operation = op
        self.nodes.append(node)

        # Check if it's a left-most node
        if (op.a.startswith("x") or op.a.startswith("y")) and \
                (op.b.startswith("x") or op.b.startswith("y")):
            self.output = out_op
            return node

        node.output = out_op
        return node


if __name__ == "__main__":
    circuit = Circuit()
    circuit.read_from_file(FILE_PATH)
    circuit.sort_operations()

    visualizer = CircuitVisualizer(circuit)
    visualizer.visualize()
