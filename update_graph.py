import os
import json
import pydot

def generate_dot_file(directory):
    dot_content = "digraph G {\n"
    dot_content += '    node [shape=box];\n'  # Set node shape to box for better visibility

    
    # Traverse the directory structure
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Add each file as a node in the graph
            dot_content += f'    "{file_path}" [label="{file}", shape=box];\n'

            
            # Example: Add edges based on file dependencies (if applicable)
            if file.endswith('.py'):  # Check for Python files
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if 'import' in line or 'from' in line:
                            parts = line.split()
                            if len(parts) > 1:  # Ensure there are enough parts
                                imported_file = parts[1].replace('.', '/') + '.py'  # Correct extraction for file path

                                imported_file_path = os.path.join(root, imported_file)
                                # Check if the imported file exists in the same directory
                                if os.path.exists(os.path.join(root, imported_file)):

                                    dot_content += f'    "{file_path}" -> "{imported_file_path}";\n'
    
    dot_content += "}\n"
    
    # Write the .dot file
    with open("project_structure.dot", "w") as dot_file:
        dot_file.write(dot_content)

def parse_dot_file(file_path):
    # Load the graph from the .dot file using pydot
    graphs = pydot.graph_from_dot_file(file_path)
    graph_data = {
        "nodes": [],
        "edges": []
    }
    
    # Add nodes and edges from the parsed graph
    for graph in graphs:
        for node in graph.get_nodes():
            graph_data["nodes"].append({"name": node.get_name().strip('"')})
        
        for edge in graph.get_edges():
            graph_data["edges"].append({"source": edge.get_source(), "target": edge.get_destination()})
    
    return graph_data

def save_graph_as_json(graph_data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(graph_data, json_file, indent=4)

def update_workflow_yaml():
    workflow_file_path = ".github/workflows/generate_code_graph.yml"
    
    with open(workflow_file_path, "r") as file:
        lines = file.readlines()
    
    # Update the lines to reference the new .dot file
    for i, line in enumerate(lines):
        if "input.dot" in line:
            lines[i] = line.replace("input.dot", "project_structure.dot")
    
    with open(workflow_file_path, "w") as file:
        file.writelines(lines)

if __name__ == "__main__":
    project_directory = "c:/Users/clabb/Desktop/BugHunter"  # Path to your BugHunter repository
    generate_dot_file(project_directory)
    
    # Parse the generated .dot file
    graph_data = parse_dot_file("project_structure.dot")
    
    # Save the parsed data as JSON
    save_graph_as_json(graph_data, "project_structure.json")
    
    # Update the workflow YAML file
    update_workflow_yaml()
