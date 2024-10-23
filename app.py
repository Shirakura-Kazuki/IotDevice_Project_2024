# ラズパイ実機操作・バックエンド用
#・LED（白色）・LED（赤色）

import RPi.GPIO as GPIO
import time
import smbus2  # smbus2のインポートを追加
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

import struct  # データを構造化して扱うためのライブラリ

# I2Cアドレスの設定
AM2320_I2C_ADDR = 0x5C  # AM2320のI2Cアドレス


app = Flask(__name__)
CORS(app)

# GPIOピンの設定
LED_PINS = {
    'port1': 17,  # GPIO17
    'port2': 27,  # GPIO27
    'port3': 22   # GPIO22
}

stop_all = False  # 停止フラグ

GPIO.setmode(GPIO.BCM)
for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)

# 処理を中断するための関数
@app.route('/api/stop', methods=['POST'])
def stop_processing():
    global stop_all
    stop_all = True
    print("すべての処理が中断されました。")
    return jsonify({"message": "すべての処理を中断しました"}), 200

# LEDの点滅制御関数：白色
def control_led(pin, duration=6):
    global stop_all
    print(f"GPIOピン {pin} のLED(白色)を{duration}秒間、1秒間隔で点滅させます")
    end_time = time.time() + duration
    while time.time() < end_time:
        if stop_all:
            print(f"GPIOピン {pin} のLED点滅が中断されました")
            return f"GPIOピン {pin} のLED点滅が中断されました"
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(1)
    return f"GPIOピン {pin} の白LED点滅が完了しました"

# LEDの点灯制御関数：赤色
def control_redled(pin, duration=5):
    global stop_all
    print(f"GPIOピン {pin} のLED(赤色)を{duration}秒間点灯します")
    end_time = time.time() + duration
    while time.time() < end_time:
        if stop_all:
            print(f"GPIOピン {pin} の赤LED点灯が中断されました")
            return f"GPIOピン {pin} の赤LED点灯が中断されました"
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(9.5)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5)
    return f"GPIOピン {pin} の赤LED点灯が完了しました"

# 温湿度計制御関数
def read_am2320():
    bus = smbus2.SMBus(1)  # I2Cバス1に接続
    AM2320_I2C_ADDR = 0x5C

    # 測定開始
    print("温湿度センサーAM2320の測定を開始します。")

    # AM2320センサーにデータ送信を開始
    try:
        bus.write_i2c_block_data(AM2320_I2C_ADDR, 0x00, [])
    except Exception as e:
        pass  # センサーウェイクアップ

    time.sleep(0.002)

    # センサーからデータを読み取る
    bus.write_i2c_block_data(AM2320_I2C_ADDR, 0x03, [0x00, 0x04])
    time.sleep(0.002)
    data = bus.read_i2c_block_data(AM2320_I2C_ADDR, 0x00, 6)

    humidity = ((data[2] << 8) | data[3]) / 10.0
    temperature = ((data[4] & 0x7F) << 8 | data[5]) / 10.0
    if data[4] & 0x80:
        temperature = -temperature

     # 測定結果の表示
    print(f"温度: {temperature}°C, 湿度: {humidity}%")

    return {"temperature": temperature, "humidity": humidity}

# 各ポートのエンドポイント
@app.route('/api/sensors/<port>', methods=['POST'])
def control_sensor(port):
    global stop_all
    stop_all = False  # 処理開始時にフラグをリセット
    sensor_type = request.json.get('sensor')
    pin = LED_PINS.get(port)

    if sensor_type == 'LED' and pin:
        result = control_led(pin)
        return jsonify({f'{port}_result': result})
    elif sensor_type == "赤色LED" and pin:
        result = control_redled(pin)
        return jsonify({f'{port}_result': result})
    elif sensor_type == "温湿度センサー":
        am2320_data = read_am2320()
        result = {
            "temperature": am2320_data["temperature"],
            "humidity": am2320_data["humidity"]
        }
        return jsonify(result)
    else:
        result = 'NoDevice'
    return jsonify({f'{port}_result': result})

    # return jsonify(result)
    # return jsonify({f'{port}_result': result})


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()

