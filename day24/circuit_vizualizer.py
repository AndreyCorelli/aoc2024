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

        def get_text_size(txt: str) -> Tuple[int, int]:
            bbox = draw.textbbox((0, 0), text, font=FONT)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]

        text = node.operation.operation_code
        text_width, _ = get_text_size(text)
        text_x = l + (w - text_width) // 2
        text_y = t + 5  # Add a small margin from the top
        draw.text((text_x, text_y), text, fill="black", font=FONT)

        # input pins
        draw.line([(l - PIN, input_ys[0]), (l, input_ys[0])], fill="black", width=1)
        draw.line([(l - PIN, input_ys[1]), (l, input_ys[1])], fill="black", width=1)
        # output
        draw.line([(l + NW, pivot[1] + SLOT_H // 2), (l + NW + PIN, pivot[1] + SLOT_H // 2)], fill="green", width=1)

        # draw text on pins
        sizes = (get_text_size(node.operation.a), get_text_size(node.operation.b), get_text_size(node.operation.out_code))
        text_x, text_y = l - PIN + 2, input_ys[0] - sizes[0][1] - 2
        draw.text((text_x, text_y), node.operation.a, fill="black", font=FONT)
        text_x, text_y = l - PIN + 2, input_ys[1] - sizes[1][1] - 2
        draw.text((text_x, text_y), node.operation.a, fill="black", font=FONT)

        text_x, text_y = l + NW + 3, pivot[1] + SLOT_H // 2 - sizes[2][1] - 2
        draw.text((text_x, text_y), node.operation.out_code, fill="black", font=FONT)



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

        for op in z_cluster:
            self._place_node(op, None, 0)

    def _place_node(self, op: Operation, out_op: Optional[Node], x: int) -> Node:
        y = self._next_free_y[x]
        self._next_free_y[x] = y + 1
        node = Node((x, y))
        node.operation = op
        self.nodes.append(node)

        # is it a left-most node?
        if (op.a.startswith("x") or op.a.startswith("y")) and \
            (op.b.startswith("x") or op.b.startswith("y")):
            self.output = out_op
            return node

        node.output = out_op

        def lookup_op_by_output(out_name: str) -> Optional[Operation]:
            for op in self.circuit.operations:
                    if op.out_code == out_name:
                        return op
            return None

        a_op, b_op = lookup_op_by_output(op.a), lookup_op_by_output(op.b)
        if a_op:
            a_child = self._place_node(a_op, node, x - 1)
            node.inputs.append(a_child)
        if b_op:
            b_child = self._place_node(b_op, node, x - 1)
            node.inputs.append(b_child)

        return node


def visualize_trivial(circuit: Circuit):
    # looks crap
    edges = []
    for op in circuit.operations:
        node_code = str(op)
        edges.append((op.a, node_code))
        edges.append((op.b, node_code))

    G = nx.DiGraph()
    G.add_edges_from(edges)
    pos = nx.planar_layout(G)  # Alternative: nx.shell_layout(G), nx.planar_layout(G), spring_layout(G) etc

    # Draw the graph
    plt.figure(figsize=(12, 8))
    nx.draw(
        G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold", arrowsize=20
    )

    #edge_labels = {(u, v): '' for u, v in edges}  # Example: Add labels to edges if necessary
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    plt.title("Graph Visualization", fontsize=14)
    plt.show()


if __name__ == "__main__":
    circuit = Circuit()
    circuit.read_from_file(FILE_PATH)
    circuit.sort_operations()

    visualizer = CircuitVisualizer(circuit)
    visualizer.visualize()
