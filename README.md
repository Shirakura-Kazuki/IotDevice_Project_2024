# IotDevice_Project_2024 (©2024年度 安田研究室 教育デバイス)
このプロジェクトは、Raspberry Piに接続された様々なセンサーを管理・制御するためのウェブインターフェースとバックエンドサービスを提供します。ユーザーはウェブベースのインターフェースを介して、センサーを選択し、デバイスに制御信号を送信することができます。また、Raspberry Pi側のバックエンドがハードウェアとの通信を処理します。

## 機能

- **センサー選択**: ウェブインターフェースを使用して、異なるセンサー（温湿度センサー、LED、ブザーなど）を選択し、3つのポートに割り当てます。
- **リアルタイムセンサーデータ**: AM2320センサーからの温度・湿度データを取得し、表示します。
- **LED制御**: 白色LEDおよび赤色LEDを制御可能です。
- **停止・リセット**: ウェブインターフェースから、すべてのプロセスを停止・リセットする機能を提供します。
  
## 動作原理

1. **ウェブインターフェース**:
    - ユーザーは、温湿度センサーやLEDなどのセンサーを選択し、PORT1, PORT2, PORT3に割り当てます。
    - 「送信」ボタンを押すと、センサー設定がRaspberry PiのバックエンドAPIに送信されます。
    - 「リセット」ボタンで設定をクリアし、「再挑戦」ボタンで処理を停止できます。

2. **バックエンドサービス**:
    - バックエンドはRaspberry Pi上でFlaskサーバーとして動作し、GPIOピンを介してセンサーやデバイスと通信します。
    - AM2320センサーからI2Cを通じて温湿度データを取得します。

# ©2024年度 安田研究室 教育デバイス