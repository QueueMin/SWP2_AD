
import sys
import time
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QFrame)

import player
from map_objects import SolidRect, f_door, w_door, PoolFire, PoolWater

SCREEN_WIDTH            = 800
SCREEN_HEIGHT           = 600
FRAME_TIME_MS           = 16  # 0.016s=16ms에 1번 = 960ms(0.96초)에 60번!



class Title(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        self.mainscene = True
        self.keys_pressed = set()
        self.cleared = False

        bg = QGraphicsPixmapItem()
        bg.setPixmap(QPixmap("title.png"))
        bg.setScale(0.57)
        self.addItem(bg)
        start = QGraphicsPixmapItem(QPixmap("start.png"))
        start.setScale(0.5)

        self.addItem(start)
        start.setPos(127, 400)

    def timerEvent(self, event):
        if len(self.keys_pressed) > 0:
            self.cleared = True
        # print(self.cleared)

    def keyPressEvent(self, event):  # 키 입력 이벤트 핸들러
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):  # 키 입력 해제 이벤트 핸들러
        try:
            self.keys_pressed.remove(event.key())
        except KeyError:
            pass


class Scene0(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)
        self.cleared = False
        self.gameover = False
        self.gameover_bg = QGraphicsPixmapItem(QPixmap("gameover.png"))
        self.gameover_bg.setScale(0.57)

        # 배경 사진 설정
        bg = QGraphicsPixmapItem()
        bg.setPixmap(QPixmap("bg_brick.png"))
        bg.setScale(0.25)
        self.addItem(bg)

        # 맵 조성
        self.terrain1 = SolidRect(0, 560, 800, 40)  # 제일 밑 땅.
        self.addItem(self.terrain1)

        # 맵 object 추가
        self.f_door = f_door()
        self.f_door.setPos(0, 496)
        self.addItem(self.f_door)

        self.w_door = w_door()
        self.w_door.setPos(750, 496)
        self.addItem(self.w_door)

        # 파이어보이 생성 및 좌표 지정
        self.player1 = player.Player1()
        self.player1.setPos(600, 0)
        self.addItem(self.player1)

        # 워터걸 생성 및 좌표 지정
        self.player2 = player.Player2()
        self.player2.setPos(200, 0)
        self.addItem(self.player2)

    def terrain_detect(self):  # 플레이어와 모든 지형의 접촉을 감지해줘야 함.
        self.player1.ground_detect(self.terrain1)
        self.player2.ground_detect(self.terrain1)

    def object_update(self):  # 맵에 있는 오브젝트들의 변화를 감지.
        self.f_door.open(self.player1)
        self.w_door.open(self.player2)
        self.stage_clear_detect()

    def stage_clear_detect(self):
        if self.f_door.opened and self.w_door.opened:
            self.cleared = True
        else:
            self.cleared = False

    def keyPressEvent(self, event):  # 키 입력 이벤트 핸들러
        self.player1.keys_pressed.add(event.key())
        self.player2.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):  # 키 입력 해제 이벤트 핸들러
        try:
            self.player1.keys_pressed.remove(event.key())
            self.player2.keys_pressed.remove(event.key())
        except KeyError:
            pass

    def game_update(self):
        self.terrain_detect()
        self.player1.player1_update()
        self.player2.player2_update()
        self.object_update()
        # print(self.cleared)

# 디버그용 출력들
        # print(self.cleared)
        # print(self.player1.jumped)  # 키 인식 체크용
        # print(self.player1.excel_vertical)
        # print(self.player1.standing)
        # print(self.player1.foot_y)
        # print(self.player1.y())
        # print(self.player1.collidingItems())

    def timerEvent(self, event):
        self.game_update()
        self.update()


class Scene1(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)
        self.cleared = False

        # 배경 사진 설정
        bg = QGraphicsPixmapItem()
        bg.setPixmap(QPixmap("bg_brick.png"))
        bg.setScale(0.25)
        self.addItem(bg)

        # 맵 조성
        self.terrain1 = SolidRect(0, 560, 800, 40)  # 제일 밑 땅.
        self.addItem(self.terrain1)

        self.terrain2 = SolidRect(60, 440, 120, 40)
        self.addItem(self.terrain2)

        self.terrain3 = SolidRect(620, 440, 120, 40)
        self.addItem(self.terrain3)

        self.terrain4 = SolidRect(120, 320, 560, 40)
        self.addItem(self.terrain4)

        # 맵 object 추가
        self.f_door = f_door()
        self.f_door.setPos(629, 320-64)
        self.addItem(self.f_door)

        self.w_door = w_door()
        self.w_door.setPos(121, 320-64)
        self.addItem(self.w_door)

        # 파이어보이 생성 및 좌표 지정
        self.player1 = player.Player1()
        self.player1.setPos(100, 500)
        self.addItem(self.player1)

        # 워터걸 생성 및 좌표 지정
        self.player2 = player.Player2()
        self.player2.setPos(700, 500)
        self.addItem(self.player2)

    def terrain_detect(self):  # 플레이어와 모든 지형의 접촉을 감지해줘야 함.
        self.player1.ground_detect(self.terrain1)
        self.player1.ground_detect(self.terrain2)
        self.player1.ground_detect(self.terrain3)
        self.player1.ground_detect(self.terrain4)

        self.player2.ground_detect(self.terrain1)
        self.player2.ground_detect(self.terrain2)
        self.player2.ground_detect(self.terrain3)
        self.player2.ground_detect(self.terrain4)

    def object_update(self):  # 맵에 있는 오브젝트들의 변화를 감지.
        self.f_door.open(self.player1)
        self.w_door.open(self.player2)
        self.stage_clear_detect()

    def stage_clear_detect(self):
        if self.f_door.opened and self.w_door.opened:
            self.cleared = True

    def keyPressEvent(self, event):  # 키 입력 이벤트 핸들러
        self.player1.keys_pressed.add(event.key())
        self.player2.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):  # 키 입력 해제 이벤트 핸들러
        try:
            self.player1.keys_pressed.remove(event.key())
            self.player2.keys_pressed.remove(event.key())
        except KeyError:
            pass

    def game_update(self):
        self.terrain_detect()
        self.player1.player1_update()
        self.player2.player2_update()
        self.object_update()

    def timerEvent(self, event):
        self.game_update()
        self.update()


class Scene2(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)
        self.cleared = False

        # 배경 사진 설정
        bg = QGraphicsPixmapItem()
        bg.setPixmap(QPixmap("bg_brick.png"))
        bg.setScale(0.25)
        self.addItem(bg)

        # 맵 조성
        self.terrain1 = SolidRect(0, 560, 800, 40)  # 제일 밑 땅.
        self.addItem(self.terrain1)
        self.pool1 = PoolWater(200, 560)
        self.addItem(self.pool1)

        # 맵 object 추가
        self.f_door = f_door()
        self.f_door.setPos(729, 560-64)
        self.addItem(self.f_door)

        self.w_door = w_door()
        self.w_door.setPos(669, 560-64)
        self.addItem(self.w_door)

        self.spawn()

    def spawn(self):
        # 파이어보이 생성 및 좌표 지정
        self.player1 = player.Player1()
        self.player1.setPos(100, 500)
        self.addItem(self.player1)

        # 워터걸 생성 및 좌표 지정
        self.player2 = player.Player2()
        self.player2.setPos(100-50, 500)
        self.addItem(self.player2)

    def terrain_detect(self):  # 플레이어와 모든 지형의 접촉을 감지해줘야 함.
        self.player1.ground_detect(self.terrain1)

        self.player2.ground_detect(self.terrain1)

    def object_update(self):  # 맵에 있는 오브젝트들의 변화를 감지.
        self.f_door.open(self.player1)
        self.w_door.open(self.player2)
        self.pool1.kill_fire(self.player1)
        self.death()
        self.stage_clear_detect()

    def death(self):
        if self.player1.isVisible() & self.player2.isVisible() is False:
            self.player1.setVisible(False)
            self.player2.setVisible(False)
            time.sleep(1)
            self.spawn()


    def stage_clear_detect(self):
        if self.f_door.opened and self.w_door.opened:
            self.cleared = True

    def keyPressEvent(self, event):  # 키 입력 이벤트 핸들러
        self.player1.keys_pressed.add(event.key())
        self.player2.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):  # 키 입력 해제 이벤트 핸들러
        try:
            self.player1.keys_pressed.remove(event.key())
            self.player2.keys_pressed.remove(event.key())
        except KeyError:
            pass

    def game_update(self):
        self.terrain_detect()
        self.player1.player1_update()
        self.player2.player2_update()
        self.object_update()

    def timerEvent(self, event):
        self.game_update()
        self.update()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = Scene0()
    sys.exit(app.exec_())

