import pyaudio
import wave
import math
import pygame
import numpy as np

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
AUDIO_FILE = "assets/music/Alone.wav"  # Replace with your file
wf = wave.open(AUDIO_FILE, 'rb')  # Convert to .wav if necessary (e.g., using pydub)

# PyAudio setup for playback
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
background_image = pygame.image.load("assets/images/background-t.jpeg")
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
    
def draw_circular_sine_wave(amplitude, frequency, base_radius, center):
    """Draws a circular sine wave based on amplitude, frequency, and base radius."""
    #screen.fill((0, 0, 0))
    points = []
    num_points = 125  # Number of points around the circle
    for i in range(num_points):
        # Calculate angle (theta) in radians
        theta = (2 * math.pi) * (i / num_points)

        # Modulate the radius with a sine wave
        r = base_radius + amplitude * math.sin(frequency * theta)

        # Convert polar coordinates to Cartesian
        x = center[0] + r * math.cos(theta)
        y = center[1] + r * math.sin(theta)

        # Add the point
        points.append((x, y))
    #color = list(np.random.choice(range(256), size=3))
    # Draw the circular sine wave
    pygame.draw.lines(screen, (255,255,255), True, points, 2)
    pygame.display.flip()

def game():
    running = True
    frequency = 50
    base_radius = 300
    center = (WIDTH//2,HEIGHT//2)
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
        screen.blit(background_image,(0,0))
        #draw_sine_wave(amplitude)
        draw_circular_sine_wave(amplitude, frequency, base_radius, center)
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
