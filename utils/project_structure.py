from pathlib import Path
from dataclasses import dataclass
import json
key = ""
k = 10
content = ""
# src/utils/project_structure.py


@dataclass
  class TreeNode:
    """Represents a node in the project structure tree."""

    name: str
    path: str
    is_file: bool
    children: List["TreeNode"]
    description: Optional[str] = None

      class ProjectStructure:
        """Manages and displays the project structure."""

          def __init__(self, root_path: str):
            self.root_path = Path(root_path)
            self.structure: Optional[TreeNode] = None
            self.ignored_dirs = {".git", "__pycache__",
                                 "venv", "env", ".pytest_cache"}
            self.ignored_files = {".gitignore",
                                  ".env", "*.pyc", "*.pyo", "*.pyd"}

              def build_tree(self) -> TreeNode:
                """Builds the project structure tree."""
            return self._build_node(self.root_path)

              def _build_node(self, path: Path) -> TreeNode:
                """Recursively builds a tree node."""
                name = path.name
                is_file = path.is_file()
                children = []

                  if not is_file:
                       for item in path.iterdir():
                            if self._should_include(item):
                            children.append(self._build_node(item))

                        return TreeNode(
                            name=name,
                            path=str(path),
                            is_file=is_file,
                            children=sorted(children, key=lambda x: (
                                not x.is_file, x.name)),
                            description=self._get_description(path),
                        )

                          def _should_include(self, path: Path) -> bool:
                            """Determines if a path should be included in the structure."""
                              if path.name in self.ignored_dirs or path.name in self.ignored_files:
                            return False
                        return True

                          def _get_description(self, path: Path) -> Optional[str]:
                            """Gets description from docstring if it's a Python file."""
                              if path.suffix == ".py":
                                   try:
                                        with open(path, "r", encoding="utf-8") as f:
                                        content = f.read()
                                          if '"""' in content:
                                            docstring = content.split('"""')[
                                                1].strip()
                                        return docstring.split("\n")[0]
                                          except Exception:
                                        pass
                                    return None

                                      def display_tree(self, node: Optional[TreeNode] = None, level: int = 0) -> str:
                                        """Returns a string representation of the tree."""
                                          if node is None:
                                            node = self.build_tree()

                                            output = []
                                            indent = "    " * level
                                            prefix = "📄 " if node.is_file else "📁 "

                                            # Add node name and description
                                            line = f"{indent}{prefix}{node.name}"
                                              if node.description:
                                                line += f" - {node.description}"
                                                output.append(line)

                                                # Add children
                                                  for child in node.children:
                                                    output.append(
                                                        self.display_tree(child, level + 1))

                                                return "\n".join(output)

                                                  def export_json(self, output_path: str) -> None:
                                                    """Exports the structure to a JSON file."""

                                                      def node_to_dict(node: TreeNode) -> Dict:
                                                    return {
                                                        "name": node.name,
                                                        "path": node.path,
                                                        "is_file": node.is_file,
                                                        "description": node.description,
                                                        "children": [node_to_dict(child) for child in node.children],
                                                    }

                                                    tree = self.build_tree()
                                                      with open(output_path, "w", encoding="utf-8") as f:
                                                        json.dump(node_to_dict(
                                                            tree), f, indent=2)

                                                          def main():
                                                            """Example usage of ProjectStructure."""
                                                            # Initialize ProjectStructure with your project root
                                                            project_root = Path(
                                                                __file__).parent.parent.parent
                                                            structure = ProjectStructure(
                                                                project_root)

                                                            # Display the tree
                                                            print(
                                                                "\n_project Structure:")
                                                            print(
                                                                "=================")
                                                            print(
                                                                structure.display_tree())

                                                            # Export to JSON
                                                            structure.export_json(
                                                                "project_structure.json")
                                                            print(
                                                                "\n_structure exported to project_structure.json")

                                                              if __name__ == "__main__":
                                                                main()
