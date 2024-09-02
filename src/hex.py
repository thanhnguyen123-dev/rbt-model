import df_model
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

# Function to create hexagon vertices
def create_hexagon(proportion, N):
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    x = np.sin(theta) * proportion
    y = np.cos(theta) * proportion
    x = np.append(x, 0)
    y = np.append(y, 0)
    triangles = [[N, i, (i + 1) % N] for i in range(N)]
    return x, y, triangles


def get_hex_graph(cs_question_type:int):
    if (cs_question_type < 0 or cs_question_type > 12):
        return

    scales_map = {'N': 0, 'L': 1, 'M': 2, 'H': 3}
    question_type_df = df_model.get_question_type_df(df_model.get_df(), cs_question_type)
    # Cognitive skills - Vertices labels
    labels = list(question_type_df.index)

    # Main proportions and labels
    proportions = list(question_type_df['MAJORITY'])
    proportions = [scales_map[x[-1]] / 3 for x in proportions]
    N = len(proportions)
    main_proportion = 1

    full_proportions = np.append(proportions, main_proportion)

    # Create the main hexagon vertices
    x, y, triangles = create_hexagon(main_proportion, N)
    triang_backgr = tri.Triangulation(x, y, triangles)
    triang_foregr = tri.Triangulation(x * full_proportions, y * full_proportions, triangles)

    # Create vertices for additional nested hexagons
    nested_proportions = [2/3, 1/3]
    nested_hexagons = [create_hexagon(p, N) for p in nested_proportions]

    # Create the proportions vertices for the foreground
    x_prop = x[:-1] * proportions
    y_prop = y[:-1] * proportions

    # Plotting
    colors = np.ones(N + 1)  # Set all colors to 1 (white)

    plt.figure(figsize=(8, 8))
    plt.tripcolor(triang_backgr, colors, color='white', alpha=0)
    plt.tripcolor(triang_foregr, colors, color='white', alpha=0.27)
    plt.triplot(triang_backgr, color='gray', lw=2, linestyle='--')

    # Plot nested hexagons
    for x_nested, y_nested, _ in nested_hexagons:
        plt.triplot(x_nested, y_nested, color='gray', lw=2, linestyle='--')

    # Plot the proportions data with a solid line
    plt.plot(np.append(x_prop, x_prop[0]), np.append(y_prop, y_prop[0]), color='black', lw=2, linestyle='-')

    # Adding labels
    for label, color, xi, yi in zip(labels, colors, x[:-1], y[:-1]):
        plt.text(xi * 1.05, yi * 1.05, label,
                ha='left' if xi > 0 else 'right' if xi < 0 else 'center',
                va='bottom' if yi > 0.1 else 'top' if yi < -0.1 else 'center',
                fontsize=16)
        

    plt.axis('off')
    plt.gca().set_aspect('equal')
    plt.show()


