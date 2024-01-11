import pygame, os, time
import win32api
import win32con
import win32gui
import ctypes
import pet
import requests
from io import BytesIO
from PIL import Image
import time

pygame.init()

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
screen = pygame.display.set_mode(screensize, pygame.NOFRAME)
done = False
fuchsia = (255, 0, 128)  # Transparency color
dark_red = (139, 0, 0)

win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()


# 다운받을 이미지 url
url = "https://raw.githubusercontent.com/ldh-Hoon/ScreenPet/main/penguin.png"

# request.get 요청
res = requests.get(url)

image = Image.open(BytesIO(res.content)).convert('RGBA')
#image = Image.open("image/penguin.png").convert('RGBA')
image = image.resize((image.width//2, image.height//2))
images = []

p = pet.Pet()
p.MAX_x, p.MAX_y = screensize
p.imgdx = 64
p.imgdy = 64

p.dragging = False

for i in range(image.height//p.imgdy):
    temp = []
    for j in range(image.width//p.imgdx):
        image_c = image.crop((j*p.imgdx,i*p.imgdy,j*p.imgdx+p.imgdx,i*p.imgdy+p.imgdy))
        
        # Convert PIL image to pygame surface image 
        py_image = pilImageToSurface(image_c)
        temp.append(py_image)

    images.append(temp)


def draw(p, images, screen):
        # Pet 이미지 크기 조정 (예: imgdx, imgdy는 이미지의 원본 크기)
        # Pet 이미지 뒤집기 (flip 여부에 따라)
        img = images[p.imgcropy][p.imgcropx]

        if p.flip:
            img = pygame.transform.flip(img, True, False)
        # 이미지의 특정 부분을 잘라내어 화면에 그립니다.
        # (예: imgcropx, imgcropy는 잘라낼 이미지의 시작 좌표)
        screen.blit(img, (p.x, p.y))

        

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    p.update_frame()
    
    p.acting()
    # 프레임 업데이트
    # 화면 채우기
    screen.fill(fuchsia)

    # Pet 그리기
    draw(p, images, screen)
    # 화면 업데이트
    pygame.display.update()    
    time.sleep(0.05)
    print("\r", end="")
