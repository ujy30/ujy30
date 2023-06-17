# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import random


def puzzleListCreate(puzzleImage, puzzleSize, iNum, jNum):
    puzzleList = []
    puzzleListInit = []

    for i in range(iNum):
        tempList = []
        tempListInit = []

        for j in range(jNum):
            w, h = puzzleSize[0] / iNum, puzzleSize[1] / jNum
            x, y = i * w, j * h
            partImage = puzzleImage.subsurface((x, y, w, h))

            tempDict = {
                "num": j * jNum + i + 1,
                "image": partImage,
                "pos": (x, y)
            }
            tempList.append(tempDict)
            tempListInit.append(j * jNum + i + 1)

        puzzleList.append(tempList)
        puzzleListInit.append(tempListInit)

    puzzleList[-1][-1]["num"] = 0
    puzzleListInit[-1][-1] = 0

    bs = pygame.Surface((w, h))
    bs.fill((0, 0, 0))
    puzzleList[-1][-1]["image"] = bs

    return puzzleList, puzzleListInit


def show_end_popup():
    messagebox.showinfo("알림", "게임 종료!")
    pygame.time.wait(2000)  # 2초 동안 알림을 표시한 후 게임을 종료합니다.


def show_start_popup():
    messagebox.showinfo("알림", "게임 시작! space를 눌러 퍼즐이 섞고 \n다시 누르면 섞는 것이 멈춥니다."
                              "\n\nBGM볼륨조절:F1로 줄이고 F2로 키움")


def select_difficulty():
    root = tk.Tk()
    root.withdraw()
    difficulty = messagebox.askquestion("난이도 선택", "어떤 난이도로 하시겠습니까?\n\n3x2: Yes\n3x3: No")
    if difficulty == 'yes':
        return 3, 2
    else:
        return 3, 3


# 1. 게임 초기화
pygame.init()

# 2. 파일 선택 대화상자 표시
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

# 3. 이미지 데이터 읽기
puzzleImage = pygame.image.load(file_path)
puzzleSize = (800, 800)  # 퍼즐 이미지와 프레임의 크기를 300x300 픽셀로 고정합니다
puzzleSize = (round(puzzleSize[0] * 0.5), round(puzzleSize[1] * 0.5))
puzzleImage = pygame.transform.smoothscale(puzzleImage, puzzleSize)

# 4. 난이도 선택
iNum, jNum = select_difficulty()

# 5. puzzleList 생성
puzzleList, puzzleListInit = puzzleListCreate(puzzleImage, puzzleSize, iNum, jNum)
w, h = puzzleSize[0] / iNum, puzzleSize[1] / jNum

# 6. 게임창 옵션 설정
size = puzzleSize
screen = pygame.display.set_mode(size)
title = "puzzle/조종:방향키/종료:esc"
pygame.display.set_caption(title)

# 7. 게임 내 필요한 설정
clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
dirDict = {
    "left": (-1, 0), "right": (1, 0),
    "up": (0, -1), "down": (0, 1)
}
keyPress = False
mix = True
gameOver = False
spaceNum = 0
exit = False
shuffle_count = 0

# 8. 메인 이벤트
show_start_popup()

# 9. BGM 추가
pygame.mixer.music.load("ㅇㅅㅇ.mp3")  # BGM 파일 경로를 입력하세요
pygame.mixer.music.play(-1)  # -1을 입력하여 BGM을 반복 재생합니다.
volume = 0.1  # 초기 볼륨 설정
pygame.mixer.music.set_volume(volume)  # 초기 볼륨 적용

while not exit:
    # 9-1. FPS 설정
    clock.tick(60)

    # 9-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            keyName = pygame.key.name(event.key)
            if keyName == "escape":
                exit = True  # "esc" 키를 누를 경우 게임 종료
            if keyName == "f1":
                volume -= 0.1  # 볼륨을 0.1씩 감소
                if volume < 0.0:
                    volume = 0.0  # 최소 볼륨은 0.0
            elif keyName == "f2":
                volume += 0.1  # 볼륨을 0.1씩 증가
                if volume > 1.0:
                    volume = 1.0  # 최대 볼륨은 1.0
            pygame.mixer.music.set_volume(volume)
            for key in dirDict.keys():
                if key == keyName:
                    keyPress = True

    # 9-3. 입력, 시간에 따른 변화
    # Blank 찾기
    for i in range(iNum):
        for j in range(jNum):
            if puzzleList[i][j]["num"] == 0:
                blank = (i, j)

    # 바꾸기
    if keyPress == True or mix == True:
        if mix == True:
            ranIndex = random.randrange(0, 4)
            keyName = list(dirDict.keys())[ranIndex]
        i, j = blank
        ii, jj = dirDict[keyName]
        iNew, jNew = i + ii, j + jj
        shuffle_count += 1
        if iNew >= 0 and iNew < iNum and jNew >= 0 and jNew < jNum:
            puzzleList[i][j]["num"], puzzleList[iNew][jNew]["num"] = \
                puzzleList[iNew][jNew]["num"], puzzleList[i][j]["num"]
            puzzleList[i][j]["image"], puzzleList[iNew][jNew]["image"] = \
                puzzleList[iNew][jNew]["image"], puzzleList[i][j]["image"]
        keyPress = False

        if shuffle_count > 50:
            mix = False

    # 게임 종료 조건
    if mix == False:
        same = True
        for i in range(iNum):
            for j in range(jNum):
                if puzzleList[i][j]["num"] != puzzleListInit[i][j]:
                    same = False
        if same == True:
            if not gameOver:  # 게임 종료 팝업이 띄워지지 않은 경우에만 실행
                show_end_popup()
                gameOver = True

    # 9-4. 그리기
    screen.fill(white)

    # 퍼즐 그리기
    for i in range(iNum):
        for j in range(jNum):
            img = puzzleList[i][j]["image"]
            pos = puzzleList[i][j]["pos"]
            screen.blit(img, pos)
            x, y = pos
            A = (x, y)
            B = (x + w, y)
            C = (x, y + h)
            D = (x + w, y + h)
            pygame.draw.line(screen, white, A, B, 3)
            pygame.draw.line(screen, white, A, C, 3)
            pygame.draw.line(screen, white, D, B, 3)
            pygame.draw.line(screen, white, D, C, 3)

    if gameOver == True:
        screen.blit(puzzleImage, (0, 0))

    # 9-5. 업데이트
    pygame.display.flip()

# 10. 게임 종료
pygame.quit()
