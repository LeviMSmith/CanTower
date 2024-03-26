import sys


def find_next_pyramid(N, include_rectangular=True):
    while True:
        shape, layers = find_pyramid_details(N, include_rectangular)
        if shape:  # If a shape is found, it already meets the criteria
            return N, shape, layers
        N += 1  # Increment N if no suitable pyramid is found


def find_pyramid_details(N, include_rectangular):
    # Triangular base: The top layer is always a single ball
    for n_triangular in range(1, N + 1):
        if (n_triangular * (n_triangular + 1) * (n_triangular + 2)) // 6 == N:
            return "Triangular", [
                (i, i * (i + 1) // 2, (i * (i + 1) * (i + 2)) // 6)
                for i in range(n_triangular, 0, -1)
            ]

    # Square base: The top layer is always a single ball
    for n_square in range(1, N + 1):
        if (n_square * (n_square + 1) * (2 * n_square + 1)) // 6 == N:
            return "Square", [
                (i, i**2, (i * (i + 1) * (2 * i + 1)) // 6)
                for i in range(n_square, 0, -1)
            ]

    # Rectangular base: The top layer consists of only a single row or column (if enabled)
    if include_rectangular:
        for L in range(2, int(N ** (1 / 2)) + 1):
            for W in range(L, N // L + 1):
                if L * W > N:  # Exclude solutions that cannot be formed
                    break
                total_used = 0
                layers = []
                l, w = L, W
                while total_used + l * w <= N and l > 0 and w > 0:
                    total_used += l * w
                    layers.append((l, w, l * w, total_used))
                    l -= 1
                    w -= 1
                if total_used == N and (
                    (len(layers) > 1 and (layers[-1][0] == 1 or layers[-1][1] == 1))
                    or (L == 1 or W == 1)
                ):
                    return "Rectangular", layers

    return None, []


# Main execution
if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            N = int(sys.argv[1])
            include_rectangular = "--no-rect" not in sys.argv
            next_N, shape, layers = find_next_pyramid(N, include_rectangular)
            print(
                f"The next suitable pyramid uses {next_N} balls with a {shape} base, tapering to the smallest top layer."
            )
            for i, layer in enumerate(layers, 1):
                if shape == "Triangular" or shape == "Square":
                    print(
                        f"Layer {i}: Width of one side = {layer[0]}, Balls in layer = {layer[1]}, Running total = {layer[2]}"
                    )
                else:
                    print(
                        f"Layer {i}: Length = {layer[0]}, Width = {layer[1]}, Balls in layer = {layer[2]}, Running total = {layer[3]}"
                    )
        except ValueError:
            print("Please provide a valid integer for N.")
    else:
        print("Usage: python tower.py <N> [--no-rect]")
