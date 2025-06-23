from PIL import Image
import numpy as np
import json
from scipy.spatial.distance import cdist
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.sparse import csr_matrix
import networkx as nx


INPUT_FILE = "einstein2.png"  
OUTPUT_FILE = "einstein2_tsp_path_points.json"
RESIZE_WIDTH = 256    # Resize image to this width (height will be proportional)
THRESHOLD = 200       # Pixel threshold
MAX_POINTS = 10000    # Maximum number of points to use for TSP


# 2-approximation for tsp, using mst and dfs
def find_tsp_path(points):
    
    distances = cdist(points, points)
    
    mst = minimum_spanning_tree(csr_matrix(distances))
    
    G = nx.from_scipy_sparse_array(mst)
    
    # find path, starting from node 0
    path = list(nx.dfs_preorder_nodes(G, source=0))
    
    # reconstruct path from nodes
    return [points[i] for i in path]

def extract_image_points(image_path, threshold=128, max_points=2000, resize_width=None):
    print(f"Loading image: {image_path}")
    image = Image.open(image_path).convert("L") # convert to greyscale
    
    if resize_width:
        original_size = image.size
        aspect_ratio = original_size[1] / original_size[0]
        new_height = int(resize_width * aspect_ratio)
        image = image.resize((resize_width, new_height), Image.Resampling.LANCZOS)
        print(f"Resized image from {original_size} to {image.size}")
    
    image_np = np.array(image)
    
    # find pixels 
    dark_pixels = np.where(image_np < threshold)
    points = [(int(x), int(y)) for y, x in zip(dark_pixels[0], dark_pixels[1])]
    
    print(f"Found {len(points)} dark pixels")
    
    # reduce number of points by taking a random subset 
    if len(points) > max_points:
        print(f"Subsampling to {max_points} points...")
        indices = np.random.choice(len(points), max_points, replace=False)
        points = [points[i] for i in indices]
    
    return points

if __name__ == '__main__':    
    # Load image and extract points
    image_path = f"images/{INPUT_FILE}"
    points = extract_image_points(image_path, threshold=THRESHOLD, max_points=MAX_POINTS, resize_width=RESIZE_WIDTH)
    
    assert len(points) > 0, "No points found! Try adjusting the threshold."
    
    print(f"Extracted {len(points)} points from image")
    
    tsp_path = find_tsp_path(points)
    
    # Save to JSON file
    output_path = f"paths/{OUTPUT_FILE}"
    with open(output_path, "w") as f:
        json.dump({"path_points": tsp_path}, f, indent=2)
    
    print(f"TSP path saved to {output_path}")
    print(f"Path contains {len(tsp_path)} points")
    
   