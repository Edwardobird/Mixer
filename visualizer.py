import pygame
import wave
import pyaudio
import math
import colorsys
import time

# Pygame initialization
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Visualizer")
clock = pygame.time.Clock()

# Audio constants
CHUNK = 1024

# Background image (optional)
background_image = pygame.image.load("assets/images/background-t.jpeg").convert()
background_image.set_alpha(128)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

def get_audio_amplitude(data):
    rms = 0
    for i in range(0, len(data), 2):
        sample = int.from_bytes(data[i:i+2], byteorder='little', signed=True)
        rms += sample * sample
    rms = math.sqrt(rms / (len(data) / 2))
    return rms

def draw_circular_sine_wave(amplitude, frequency, base_radius, center, time_offset):
    points = []
    colors = []
    num_points = 125

    for i in range(num_points):
        theta = (2 * math.pi) * (i / num_points)
        r = base_radius + amplitude * math.sin(frequency * theta)
        if r < base_radius * 0.7:
            r = base_radius

        x = center[0] + r * math.cos(theta)
        y = center[1] + r * math.sin(theta)

        points.append((x, y))
        hue = (i / num_points + time_offset) % 1
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)
        color = tuple(int(c * 255) for c in rgb)
        colors.append(color)

    for i in range(num_points - 1):
        pygame.draw.line(screen, colors[i], points[i], points[i + 1], 2)

    pygame.draw.line(screen, colors[-1], points[-1], points[0], 2)
    pygame.display.flip()

def run_visualizer(audio_file):
    try:
        # Audio setup
        wf = wave.open(audio_file, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        running = True
        frequency = 50
        base_radius = 300
        center = (WIDTH // 2, HEIGHT // 2)
        start_time = time.time()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            data = wf.readframes(CHUNK)
            if not data:
                wf.rewind()
                data = wf.readframes(CHUNK)

            stream.write(data)
            amplitude = get_audio_amplitude(data) / 200
            amplitude = max(10, amplitude)
            current_time = time.time() - start_time
            time_offset = (current_time * 0.1) % 1
            screen.blit(background_image, (0, 0))
            draw_circular_sine_wave(amplitude, frequency, base_radius, center, time_offset)
            clock.tick(120)

        pygame.quit()
        stream.stop_stream()
        stream.close()
        p.terminate()
    except Exception as e:
        print(f"Error in visualizer: {e}")
