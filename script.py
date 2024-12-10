import networkx as nx
import matplotlib.pyplot as plt


def find_index(components, vertex):
    # Find the index of the component that contains the given vertex.
    for i, component in enumerate(components):
        if vertex in component:
            return i
    # Return an invalid index if the vertex is not found.
    return -8


def boruvka(vertices, edges):
    mst = []

    # Sort edges by weight
    edges = sorted(edges, key=lambda x: x[2])

    # Each vertex is its own component
    components = [{v} for v in vertices]

    # Continue until there is only one component
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

            # Double-check component validity before merging
            if component1 != -8 and component2 != -8 and component1 != component2:
                # Merge the two components
                merged = components[component1].union(components[component2])

                # Remove old components and add the merged component
                components.pop(max(component1, component2))
                components.pop(min(component1, component2))
                components.append(merged)

                # Add the edge to the Minimum Spanning Tree
                mst.append((u, v, weight))
    return mst


def plotting(edges, mst):
    # Create a NetworkX graph with all original edges
    G = nx.Graph()
    for u, v, weight in edges:
        G.add_edge(u, v, weight=weight)

    # Create a Minimum Spanning Tree graph
    MST = nx.Graph()
    for u, v, weight in mst:
        MST.add_edge(u, v, weight=weight)

    # Create a figure with two subplots for comparison
    plt.figure(figsize=(12, 5))

    # Layout for consistent vertex positioning
    pos = nx.spring_layout(G, seed=42)

    # Original Graph Visualization
    plt.subplot(121)
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=500, font_size=10, font_weight='bold')

    # Draw edge weights on original graph
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Original Graph")

    # Minimum Spanning Tree Visualization
    plt.subplot(122)
    nx.draw(MST, pos, with_labels=True, node_color='lightgreen',
            node_size=500, font_size=10, font_weight='bold')

    # Draw edge weights on MST
    mst_edge_labels = {(u, v): weight for (u, v, weight) in mst}
    nx.draw_networkx_edge_labels(MST, pos, edge_labels=mst_edge_labels)
    plt.title("Minimum Spanning Tree")
    plt.tight_layout()
    plt.show()


vertices = ['A', 'B', 'C', 'D']
edges = [
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 1),
    ('B', 'D', 3),
    ('C', 'D', 5)
]

# Find the MST
result = boruvka(vertices, edges)

# Plotting graph
plotting(edges, result)