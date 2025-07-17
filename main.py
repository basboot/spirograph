import math
import time

import numpy as np
import pygame

import sys
# TODO: find out why this is needed, because there is no recursion (although there are a lot of circle calls on the stack)
sys.setrecursionlimit(30000)

STACK_ROTATION = False # not needed anymore, we have verified that all rotations are independend
ROTATION_SPEED = math.pi / 500
SCALE = 1.2

# circle class, both for updating and drawing the circles
class Circle:
    def __init__(self, r, omega, x = 0, y = 0, child = None, angle = 0):
        self.r = r * SCALE
        self.omega = omega
        self.x = x
        self.y = y
        self.angle = angle
        self.child = child
        self.child_x, self.child_y = 0, 0
        self.path = []

    def update(self, x = None, y = None, angle_offset = 0):
        # update angle and postion, and calculate child position

        if not STACK_ROTATION:
            angle_offset = 0

        if x is not None: # used for root circle
            self.x, self.y = x, y
        self.angle -= self.omega * ROTATION_SPEED
        self.child_x = self.x + self.r * math.cos(self.angle + angle_offset)
        self.child_y = self.y + self.r * math.sin(self.angle + angle_offset)

        if self.child is not None:
            # upadte child
            self.child.update(self.child_x, self.child_y, self.angle + angle_offset)
        else:
            # no child, so this is the circle that draws the path
            self.path.append((self.child_x, self.child_y))

    def draw(self, screen):
        if self.child is not None:
            self.child.draw(screen)
        pygame.draw.circle(screen, (200, 200, 200), (int(self.x), int(self.y)), self.r, width=1)
        pygame.draw.circle(screen, (255, 0, 0) if self.child is None else (200, 200, 200), (int(self.child_x), int(self.child_y)), 2)
        pygame.draw.line(screen, (200, 200, 200), (int(self.x), int(self.y)), (int(self.child_x), int(self.child_y)), width=1)

    def get_path(self):
        if self.child is None:
            return self.path
        else:
            return self.child.get_path()
        

# intepolate path, to avoid gaps
def interpolate_path(path, max_distance=0.5):
    assert len(path) > 1, "cannot interpolate a single point"
    
    interpolated_path = [path[0]]  # Start with the first point
    
    for i in range(1, len(path)):
        current_point = interpolated_path[-1]
        next_point = path[i]
        
        distance = abs(next_point - current_point)
        
        if distance <= max_distance:
            interpolated_path.append(next_point)
        else:
            # add point in the middle
            num_segments = int(np.ceil(distance / max_distance))

            for j in range(1, num_segments + 1):
                t = j / num_segments
                interpolated_point = current_point + t * (next_point - current_point)
                interpolated_path.append(interpolated_point)
    
    return interpolated_path

import json

# save frequency data, to reuse the analysis in a javascript project
def save_frequency_data_to_json(frequencies, radiuses, phases, filename="frequency_data.json"):
    data_tuples = list(reversed(list(zip(frequencies, radiuses, phases))))

    data_list = []
    for i, (freq, radius, phase) in enumerate(data_tuples):
        data_list.append({
            "index": i,
            "frequency": float(freq),
            "radius": float(radius),
            "phase": float(phase)
        })

    with open(filename, 'w') as f:
        json.dump(data_list, f, indent=2)

    print(f"Saved {len(data_list)} frequency components to {filename}")
    return filename

# generate different shapes to draw
def generate_path(shape='circle', show_path=False, json_file=None):

    path = []

    match(shape):
        case 'circle':
            radius = 200
            steps = 200
            for i in range(steps):
                angle = 2 * math.pi * i / steps
                x = radius * math.cos(angle)
                y = radius * math.sin(2 * angle) * 1
                path.append(x + y * 1j)
        case 'square':
            side_length = 400
            # Create path of four corners + closure
            corners = [
                complex(-side_length/2, -side_length/2),  # bottom-left
                complex(side_length/2, -side_length/2),   # bottom-right
                complex(side_length/2, side_length/2),    # top-right
                complex(-side_length/2, side_length/2),   # top-left
                complex(-side_length/2, -side_length/2)   # closure
            ]
            
            # Interpolate between corners
            path = interpolate_path(corners, max_distance=2.0)
        case 'star':

            outer_radius=300
            inner_radius=120
            num_points=5
            total_segments = num_points * 2  # outer and inner points
    
            # generate the key vertices of the star
            vertices = []
            for i in range(total_segments):
                radius = outer_radius if i % 2 == 0 else inner_radius
                angle = 2 * math.pi * i / total_segments
                x = radius * math.cos(angle - math.pi/2)
                y = radius * math.sin(angle - math.pi/2)
                vertices.append(x + y * 1j)
            
            # close the star
            vertices.append(vertices[0])

            # interpolate
            path = interpolate_path(vertices)

        case 'json':
            assert json_file is not None, "Need to add path to json-file"

            json_path = f"paths/{json_file}"
            print("FILE", json_path)
            with open(json_path, "r") as f:
                data = json.load(f)
                path_points = data["path_points"]            

            path = [complex(x/2, y/2) for x, y in path_points]
            
            # Find center of path
            center_x = sum(point.real for point in path) / len(path)
            center_y = sum(point.imag for point in path) / len(path)
            center = complex(center_x, center_y)
            
            # Shift path to center it
            path = [point - center for point in path]
            # close path
            path.append(path[0])
            path = interpolate_path(path, max_distance=2.0)

            

    import matplotlib.pyplot as plt

    # plot for visual inspection
    if show_path:
        # extract x and y coordinates, from complex numbers
        path_array = np.array(path)  
        x_coords = path_array.real
        y_coords = path_array.imag

        
        plt.figure(figsize=(8, 8))
        plt.plot(x_coords, y_coords, 'b-', linewidth=2)
        plt.plot(x_coords, y_coords, 'ro', markersize=4)

        plt.axis('equal')
        plt.title('Path')
        plt.show()

    return path

if __name__ == '__main__':
    path = np.array(generate_path('json', show_path=False, json_file='einstein_tsp_path_points.json'))

    # path = np.array(generate_path('circle', show_path=False))

    # fft the path
    fft_result = np.fft.fft(path)

    time.sleep(5)

    epsilon = 100

    # ignore near zero magnitudes 
    magnitudes = np.abs(fft_result)
    non_zero_indices = magnitudes > epsilon
    phases = np.angle(fft_result[non_zero_indices])  
    length = len(magnitudes)
    frequencies = np.where(non_zero_indices)[0]
    frequencies = np.array([freq if freq <= length // 2 else freq - length for freq in frequencies])
    # print("Frequencies:", frequencies)
    # print("Phases:", phases)
    # print("Magnitudes", magnitudes[non_zero_indices])
    radiuses = (magnitudes[non_zero_indices]) / len(path)
    # print("R:", radiuses)

    # bin is frequency or n - frequency when above nyquist -> rotation negative
    # magnitude is circle diameter * 100
    # phase is angle

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    
    c = None

    print("Number of circles: ", len(radiuses))

    # start with outer circle
    for omega, r, angle in reversed(list(zip(frequencies, radiuses, phases))):
        c = Circle(r, omega, x = 400, y = 400, angle=angle, child=c)

    # for javascript animation
    save_frequency_data_to_json(frequencies, radiuses, phases)

    # pause for making a video
    # time.sleep(5)

    running = True
    while running:
        screen.fill((255, 255, 255))
        
        # will update all circles
        c.update()

        path = c.get_path()

        c.draw(screen)
        
        if len(path) > 1:
            pygame.draw.lines(screen, (128, 0, 0), False, [(int(x), int(y)) for x, y in path], 2)


        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

