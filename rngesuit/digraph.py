# Copyright (C) 2024 Anish Sinha
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import defaultdict


class Digraph[T]:
    """
    Directed graph implementation.
    """

    def __init__(self):
        self.adjacency_list = defaultdict(set[T])
        self.reverse_adjacency_list = defaultdict(set[T])
        self.nodes = set[T]()

    def add_edge(self, from_node: T, to_node: T):
        self.adjacency_list[from_node].add(to_node)
        self.reverse_adjacency_list[to_node].add(from_node)
        self.nodes.add(from_node)
        self.nodes.add(to_node)

    def get_sinks(self) -> set[T]:
        return set([node for node in self.nodes if not self.adjacency_list[node]])

    def get_dependencies(self, node: T) -> set[T]:
        """
        Returns all dependencies of the given node.

        Args:
            node: The node whose dependencies are to be fetched.

        Returns:
            A list of nodes that the given node depends on.
        """
        return self.adjacency_list.get(node, set())

    def get_dependents(self, node) -> set[T]:
        """
        Get all nodes that are direct dependents of the given node.
        """

        return self.reverse_adjacency_list.get(node, set())

    def __repr__(self) -> str:
        return f"Digraph({dict(self.adjacency_list)})"
