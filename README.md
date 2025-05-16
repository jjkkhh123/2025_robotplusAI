# 2025_robotplusAI
yolo를 이용하여 주차장 빈자리 찾는 이미지 학습을 시킨 best.pt를 이용하여 만든 app과 로봇 컨트롤러의 기능들을 모두 합쳐서 만들어 보았습니다.

## 프로그램 실행하기 위한 절차   
## 1.프로젝트 환경 구축
위의 파일들을 모두 다운로드 후 프로젝트 파일을 다음 그림과 같이 생성 후 옮겨줍니다.
![프로젝트 환경 구축](https://github.com/jjkkhh123/2025_robotplusAI/blob/main/images/img1.png)

그 다음 가상환경 생성을 위해 저 같은 경우 miniconda를 이용하였고 가상환경을 다음의 코드를 통해 만들어줍니다.
```
conda create -n <가상환경 이름> python=3.9
```

이 가상환경에 프로그램을 실행시키기 위한 패키지들을 다음의 코드를 통해 다운로드를 진행시켜줍니다.
```
pip install -r requirements.txt
```

## 2. 로봇을 실행환경과 연결
프로그램이 로봇에게 프로그램의 흐름에 맞는 행동을 시키기 위해 COM포트를 PC와 연결하여 줍니다.
※주의사항※ COM포트가 잘 인식이 되는지 장치관리자에서 확인하시고 만약 그림과 다르다면 아래의 내용을 따라해주시길 바랍니다.
![장치 관리자](https://github.com/jjkkhh123/2025_robotplusAI/blob/main/images/img2.png)

## 2.1. COM포트가 인식이 안될 경우
만약 인식아 안되는 포트의 이름 현재 위의 이미지에선 CP2104이므로 Google에 "CP2104 드라이버" 를 검색하여 드라이브를 다운로드를 해줍니다.    
https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads    
CP2104 드라이버와 같은 경우는 위의 링크를 들어가서 아래의 그림과 같은 것으로 다운로드   
![드라이버 다운로드](https://github.com/jjkkhh123/2025_robotplusAI/blob/main/images/img3.png)









다음은 실행 장면입니다. 
![실행 장면](https://github.com/jjkkhh123/2025_robotplusAI/blob/main/images/scene_1.png)
## 밑의 장면은 빈자리를 찾으면 로봇이 방향을 주먹으로 가리키고 인사를 하는 모습입니다.
이를 통해 기대할 수 있는 효과로 주차장에 진입하는 차들에게 빈자리의 위치를 대략적으로 가리켜 보다 수월한 주차공간 찾기가 될것으로 예상됩니다.
![실행 비디오](https://github.com/jjkkhh123/2025_robotplusAI/blob/main/images/video_1.gif)
