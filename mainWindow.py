import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import cv2
import csv
from pathlib import Path
import torch  # YOLOv5 모델 로드에 필요
from serial_port_selector import SerialPortSelector
from motion_controller import execute_motion

# YOLOv5 디렉터리 경로 추가
yolov5_path = Path("c:/2025_robot/pyQT002_yolov5/yolov5")
sys.path.append(str(yolov5_path))
from detect import run

# 리소스 경로 설정 함수
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 동적으로 리소스 파일 경로 설정
ui_file_path = resource_path("res/mainWindow.ui")
Form, Window = uic.loadUiType(ui_file_path)

class MainWindow(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 실행 플래그 초기화
        self.motion_ready = False
        self.is_waiting = False  # 감지 후 대기 상태 플래그

        # lblPort 초기화
        self.lblPort = self.lblPort  # UI에서 lblPort 위젯 참조

        # 카메라 초기화
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            QMessageBox.critical(self, "카메라 오류", "카메라를 열 수 없습니다. 연결 상태를 확인하세요.")
            return

        # 타이머 설정
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # YOLOv5 모델 로드
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

        # 버튼 메뉴 연결
        self.pushButton_6.clicked.connect(self.open_port_selector)
        self.pushButton_1.clicked.connect(lambda: self.exeHumanoidMotion(19))
        self.pushButton_2.clicked.connect(lambda: self.exeHumanoidMotion(17))
        self.pushButton_3.clicked.connect(lambda: self.exeHumanoidMotion(18))
        self.pushButton_4.clicked.connect(lambda: self.exeHumanoidMotion(16))
        self.pushButton_5.clicked.connect(lambda: self.exeHumanoidMotion(22))
        self.pushButton_7.clicked.connect(lambda: self.exeHumanoidMotion(int(self.textEdit.toPlainText())))

        # 메뉴 액션 연결
        self.actionSerial_Port.triggered.connect(self.open_port_selector)

    def update_frame(self):
        if self.is_waiting:  # 대기 상태에서는 동작하지 않음
            return

        ret, frame = self.capture.read()
        if ret:
            # YOLOv5 모델로 객체 감지
            results = self.model(frame)

            # 사람이 감지되었는지 확인
            detected_space = False
            for obj in results.xyxy[0]:  # 감지된 객체 리스트
                if int(obj[5]) == 0:  # 클래스 ID가 0이면 
                    detected_space = True
                    break

            # 사람이 감지되었을 경우 모션 실행
            if detected_space:
                if self.motion_ready:
                    print("주차 공간이 탐지되었습니다!")
                    self.exeHumanoidMotion(1)  # 첫 번째 동작 실행
                    self.is_waiting = True  # 대기 상태 활성화

                    # 2초 뒤에 두 번째 동작 실행
                    QTimer.singleShot(2000, lambda: self.exeHumanoidMotion(33))

                    # 4초 뒤에 세 번째 동작 실행
                    QTimer.singleShot(4000, lambda: self.exeHumanoidMotion(19))

                    # 15초 뒤에 대기 상태 해제
                    QTimer.singleShot(15000, self.reset_waiting_state)

            # 감지된 객체의 정보를 프레임에 그리기
            annotated_frame = results.render()[0]  # YOLOv5가 그린 프레임
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

            # OpenCV 이미지를 PyQt 이미지로 변환
            h, w, ch = annotated_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(annotated_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            self.lb_video.setPixmap(QPixmap.fromImage(qt_image))

    def reset_waiting_state(self):
        """5초 대기 후 대기 상태 해제"""
        self.is_waiting = False

    def exeHumanoidMotion(self, motion_id):
        if not self.motion_ready:
            QMessageBox.warning(self, "Motion Error", "Motion is not ready. Please select a port first.")
            return

        # 모션 실행
        execute_motion(self.lblPort.text(), motion_id, self)

    def open_port_selector(self):
        selected_port = SerialPortSelector.launch(self)
        if selected_port:
            print("선택한 포트:", selected_port)
            self.lblPort.setText(selected_port)
            # 포트가 선택되면 플래그 활성화
            self.motion_ready = True

    def take_picture(self):
        ret, frame = self.capture.read()
        if ret:
            # photos 폴더가 없으면 생성
            if not os.path.exists("photos"):
                os.makedirs("photos")

            # 파일명 처리
            raw_name = self.ed_name.text().strip() or "untitled"
            safe_name = "".join(c if c.isalnum() else "_" for c in raw_name)
            filename = os.path.join("photos", f"{safe_name}.jpg")

            # 이미지 저장
            try:
                cv2.imwrite(filename, frame)
                QMessageBox.information(self, "사진 저장", f"사진이 {filename}로 저장되었습니다!")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"사진을 저장할 수 없습니다: {e}")
        else:
            QMessageBox.critical(self, "오류", "사진을 저장할 수 없습니다.")

    def save_data(self):
        name = self.ed_name.text().strip()
        phone = self.ed_phone.text().strip()
        memo = self.ed_memo.toPlainText().strip()

        if not name or not phone or not memo:
            QMessageBox.warning(self, "입력 오류", "모든 필드를 입력해주세요!")
            return

        try:
            with open("studentList.txt", "a", encoding="utf-8") as txtfile:
                txtfile.write(f"{name}\t{phone}\t{memo}\n")
            QMessageBox.information(self, "저장 완료", "데이터가 성공적으로 저장되었습니다!")
        except Exception as e:
            QMessageBox.critical(self, "저장 실패", f"오류가 발생했습니다: {e}")

    def exit(self):
        self.capture.release()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())