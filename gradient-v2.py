import pyaudio
import wave
import math
import pygame
import numpy as np
import colorsys  
import time

# Pygame initialization
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Visualizer")
clock = pygame.time.Clock()

# Audio setup
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Load the audio file
AUDIO_FILE = "assets/music/saxobeat.wav"  # Replace with your file
wf = wave.open(AUDIO_FILE, 'rb')  # Convert to .wav if necessary (e.g., using pydub)

# PyAudio setup for playback
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
background_image = pygame.image.load("assets/images/background-t.jpeg").convert()
# Set transparency
background_image.set_alpha(128) 
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

def get_audio_amplitude(data):
    rms = 0
    for i in range(0, len(data), 2):
        sample = int.from_bytes(data[i:i+2], byteorder='little', signed=True)
        rms += sample * sample
    rms = math.sqrt(rms / (len(data) / 2))
    return rms

def draw_sine_wave(amplitude):
    screen.fill((0, 0, 0))
    points = []
    if amplitude > 10:
        for x in range(WIDTH):
            y = HEIGHT / 2 + int(amplitude * math.sin(x * 0.02))
            points.append((x, y))
    else:
        points.append((0, HEIGHT / 2))
        points.append((WIDTH, HEIGHT / 2))
    pygame.draw.lines(screen, (255, 255, 255), False, points, 2)
    pygame.display.flip()
  

def draw_circular_sine_wave(amplitude, frequency, base_radius, center, time_offset):
    """Draws a circular sine wave with a time-based gradient color change."""
    points = []
    colors = []
    num_points = 125  # Number of points around the circle

    for i in range(num_points):
        # Calculate angle (theta) in radians
        theta = (2 * math.pi) * (i / num_points)

        # Modulate the radius with a sine wave
        r = base_radius + amplitude * math.sin(frequency * theta)
        if (r < base_radius * 0.7):
            r = base_radius

        # Convert polar coordinates to Cartesian
        x = center[0] + r * math.cos(theta)
        y = center[1] + r * math.sin(theta)

        # Add the point
        points.append((x, y))

        # Adjust hue with a time offset for gradual color change
        hue = (i / num_points + time_offset) % 1  # Wrap hue around 0 to 1
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)  # Convert HSV to RGB
        color = tuple(int(c * 255) for c in rgb)  # Scale to 0-255 for Pygame
        colors.append(color)

    # Draw the circular sine wave with gradient
    for i in range(num_points - 1):
        pygame.draw.line(screen, colors[i], points[i], points[i + 1], 2)

    # Close the loop (connect last point to the first)
    pygame.draw.line(screen, colors[-1], points[-1], points[0], 2)

    pygame.display.flip()

def game():
    running = True
    frequency = 50
    base_radius = 300
    center = (WIDTH//2,HEIGHT//2)
    start_time = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Read audio chunk and play it
        data = wf.readframes(CHUNK)
        if not data:
            wf.rewind()  # Restart playback if the audio ends
            data = wf.readframes(CHUNK)

        stream.write(data)  # Play the audio chunk

        # Calculate amplitude for visualization
        amplitude = get_audio_amplitude(data) / 200  # Scale for visualizer
        amplitude = max(10, amplitude)
        current_time = time.time() - start_time
        time_offset = (current_time * 0.1) % 1
        screen.blit(background_image,(0,0))
        #draw_sine_wave(amplitude)
        draw_circular_sine_wave(amplitude, frequency, base_radius, center, time_offset)
        # CIRCLE_COLOR = (255, 0, 0)
        # circle_radius = 100
        # circle_center = (WIDTH // 2, HEIGHT // 2)
        # pygame.draw.circle(screen, CIRCLE_COLOR, circle_center, circle_radius)
        clock.tick(60)

    pygame.quit()
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    game()
