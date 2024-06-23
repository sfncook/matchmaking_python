import matplotlib.pyplot as plt

def update_drawing_surface(points, ax):
    if not points:
        return

    light_blue = "lightblue"
    red = "red"

    # Extract x and y coordinates
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]

    # Plot all but the last point in light blue
    ax.scatter(x_coords[:-1], y_coords[:-1], color=light_blue)

    # Plot the last point in red
    ax.scatter(x_coords[-1], y_coords[-1], color=red)

    # Draw lines connecting the points in light blue
    for i in range(len(points) - 1):
        ax.plot(x_coords[i:i+2], y_coords[i:i+2], color=light_blue)

if __name__ == '__main__':
    # Example usage
    points = [(10, 10), (20, 20), (30, 15), (40, 25)]

    fig, ax = plt.subplots()
    update_drawing_surface(points, ax)
    plt.show()
