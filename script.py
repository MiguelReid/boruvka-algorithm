import networkx as nx
import matplotlib.pyplot as plt


def find_index(components, vertex):
    # Finds which component (set of connected vertices) a given vertex belongs to
    for i, component in enumerate(components):
        if vertex in component:
            return i
    # Return an invalid index if the vertex is not found.
    return -8


def boruvka(vertices, edges):
    mst = []
    steps = []

    # Sort edges by weight
    edges = sorted(edges, key=lambda x: x[2])

    # Each vertex is its own component
    components = [{v} for v in vertices]

    # Initial step: show original components
    steps.append({
        'components': components.copy(),
        'mst_edges': [],
        'description': 'Initial state: Each vertex is a separate component'
    })

    # Continue until there is only one component
    iteration = 1
    while len(components) > 1:
        cheapest_edges = {}

        # Find cheapest edges
        for u, v, weight in edges:
            # Find components
            component1 = find_index(components, u)
            component2 = find_index(components, v)

            # Check if vertices are in different components
            if component1 != -8 and component2 != -8 and component1 != component2:
                # Create a unique key for component pair to avoid duplicates
                key = (min(component1, component2), max(component1, component2))

                # Update cheapest edge
                if key not in cheapest_edges or weight < cheapest_edges[key][2]:
                    cheapest_edges[key] = (u, v, weight)

        # Merge components
        for _, (u, v, weight) in cheapest_edges.items():
            component1 = find_index(components, u)
            component2 = find_index(components, v)

            if component1 != -8 and component2 != -8 and component1 != component2:
                # Merge the two components
                merged = components[component1].union(components[component2])

                # Remove old components and add the merged component
                components.pop(max(component1, component2))
                components.pop(min(component1, component2))
                components.append(merged)

                # Add the edge to the Minimum Spanning Tree
                mst.append((u, v, weight))

                # Store the step
                steps.append({
                    'components': components.copy(),
                    'mst_edges': mst.copy(),
                    'description': f'Iteration {iteration}: Merged {u} - {v} with weight {weight}'
                })
                iteration += 1

    return mst, steps


def plot_boruvka_steps(edges, steps):
    # Create a NetworkX graph with all original edges
    G = nx.Graph()
    for u, v, weight in edges:
        G.add_edge(u, v, weight=weight)

    # Consistent layout for all plots
    pos = nx.spring_layout(G, seed=42)

    # Create a figure with enough subplots
    num_steps = len(steps)
    fig = plt.figure(figsize=(15, 3 * ((num_steps + 1) // 2)), constrained_layout=True)

    # Create subplot grid
    subfigs = fig.subfigures(((num_steps + 1) // 2), 2)

    # Flatten subfigs in case of multiple rows
    if num_steps > 2:
        subfigs = subfigs.flatten()

    # Plot each step
    for i, step in enumerate(steps):
        # Choose subplot
        if num_steps > 2:
            ax = subfigs[i].subplots()
            subfigs[i].suptitle(step['description'])
        else:
            ax = subfigs[i].subplots()
            subfigs[i].suptitle(step['description'])

        # Create a graph for this step
        current_graph = nx.Graph()

        # Add all original edges
        for u, v, weight in edges:
            current_graph.add_edge(u, v, weight=weight)

        # Highlight MST edges
        mst_graph = nx.Graph()
        for u, v, weight in step['mst_edges']:
            mst_graph.add_edge(u, v, weight=weight)

        # Draw the graph
        nx.draw(current_graph, pos, ax=ax, with_labels=True,
                node_color='lightblue', node_size=500,
                font_size=8, font_weight='bold')

        # Highlight MST edges in red
        nx.draw_networkx_edges(current_graph, pos,
                               edgelist=step['mst_edges'],
                               edge_color='r',
                               width=2,
                               ax=ax)

        # Draw edge weights
        edge_labels = nx.get_edge_attributes(current_graph, 'weight')
        nx.draw_networkx_edge_labels(current_graph, pos,
                                     edge_labels=edge_labels,
                                     ax=ax)

    plt.show()


# Example with cities in Moravia
vertices = ['Brno', 'Olomouc', 'Ostrava', 'Zlín']
edges = [
    ('Brno', 'Olomouc', 4),
    ('Brno', 'Ostrava', 2),
    ('Olomouc', 'Ostrava', 1),
    ('Olomouc', 'Zlín', 3),
    ('Ostrava', 'Zlín', 5)
]

# Find the MST and get step-by-step details
result, steps = boruvka(vertices, edges)

# Plot the steps
plot_boruvka_steps(edges, steps)

# Print the final Minimum Spanning Tree
print("Minimum Spanning Tree Edges:")
for edge in result:
    print(f"{edge[0]} -- {edge[1]} : {edge[2]}")