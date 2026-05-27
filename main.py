import sounddevice as sd
import scipy.io.wavfile as wav
from pygame import *

# === Налаштування ===
WIDTH, HEIGHT = 800, 400
fs = 44100
chunk = 1024
seconds = 3

init()
mixer.init()

screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Karaoke")
clock = time.Clock()

# === Кнопка ===
button = Rect(300, 250, 200, 80)
font1 = font.Font(None, 50)
text = font1.render("Запис", True, (255, 255, 255))

# === Для хвилі ===
data_wave = [0.0] * chunk
recording = False

# === Callback для live аудіо ===
def audio_callback(indata, frames, time_info, status):
    global data_wave
    if status:
        print(status)
    data_wave = [s * (HEIGHT // 2) for s in indata[:, 0].tolist()]


# === Старт live потоку (мікрофон завжди активний) ===
stream = sd.InputStream(
    callback=audio_callback,
    channels=1,
    samplerate=fs,
    blocksize=chunk,
    dtype='float32'
)
stream.start()

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

        if e.type == MOUSEBUTTONDOWN:
            if button.collidepoint(e.pos) and not recording:
                print("Йде запис...")
                recording = True

                audio = sd.rec(int(seconds * fs),
                               samplerate=fs,
                               channels=1,
                               dtype='int16',
                               blocking=True)

                wav.write("record.wav", fs, audio)
                print("Запис завершено")

                mixer.music.load("record.wav")
                mixer.music.play()

                recording = False

    screen.fill((0, 0, 0))

    # === Малювання хвилі ===
    points = []
    for i, sample in enumerate(data_wave):
        x = int(i * WIDTH / chunk)
        y = int(HEIGHT / 2 + sample)
        points.append((x, y))

    if len(points) > 1:
        draw.lines(screen, (0, 255, 0), False, points, 2)

    # === Кнопка ===
    draw.rect(screen, (0, 205, 0), button)
    screen.blit(text, (button.x + 40, button.y + 20))

    display.update()
    clock.tick(60)

stream.stop()
quit()