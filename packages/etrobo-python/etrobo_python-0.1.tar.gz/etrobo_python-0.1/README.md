## pythonを使ってETロボコンに出場するためのミドルウェア

2022年度のETロボコンはリアル大会とシミュレーション大会の両方が行われることになりました。
リアル大会ではLEGO Mindstorms EV3かSPIKEの実機を制御するプログラムを開発することになりますが、大会運営よりUnityを使ったシミュレータが公開されていますので、シミュレータを使って制御プログラムの開発とデバッグを行い、実機でパラメータの調整を行う方法を使えば効率よく制御プログラムを開発できそうです。
シミュレータを使って実機用のプログラムを開発するという方法は大会運営側も想定していまして、公式の開発環境である[EV3RT](https://dev.toppers.jp/trac_user/ev3pf/wiki/WhatsEV3RT)を使った場合はシミュレータと実機の両方で動作する制御プログラムを開発できます。
ただ、EV3RTはC/C++での開発のみをサポートしていますので、pythonを使った制御プログラムを開発できません。

ただ、実機であるEV3やSPIKEの制御を行うRaspberry Piではmicropythonが動作しますので、実機を使うリアル大会についてはpythonを用いて開発した制御プログラムで出場できます。
また、シミュレータについても、[ETロボコンシミュレータのPython用クライアントライブラリ](https://github.com/YoshitakaAtarashi/ETroboSimController)が公開されていますので、pythonを使って開発した制御プログラムをシミュレータ環境で実行することも可能です。
しかし、シミュレータ環境とEV3環境で使用するpythonライブラリが異なりますので、シミュレータで開発した制御プログラムをEV3環境やSPIKE環境で動かすことはできませんでした。

そこで、**シミュレータ環境とEV3環境の両方に対応した制御プログラムをpythonで開発するためのミドルウェア**を作りました。
それぞれの環境で共通となる部分をAPIとして公開し、それぞれの環境で異なる部分はバックエンドとして隠蔽する構成になっています。
そのため、このミドルウェアで開発した制御プログラムは、バックエンドを変更することにより、シミュレータ環境とEV3環境のどちらでも動作します。
詳しくは[samplesディレクトリ](samples)に置いてあるサンプルプログラムを参考にしてください。

現在のバージョンではシミュレータ環境とEV3環境のみをサポートしています。
SPIKE環境(RasPike環境)については実機を入手できましたら開発をはじめます。

## インストール
Windows/MaxOSX/Linuxなどのpython（バージョン3.7以上）環境には`pip`を用いてインストールできます。
また、EV3でこのミドルウェアを使用する場合は[etrobo_pythonを含むEV3-MicroPythonのイメージファイル](https://github.com/takedarts/etrobo-python/releases/latest/download/ev3micropythonv200etrobosdcardimage.zip)を使用してください。

詳しいインストール方法については[Wiki](https://github.com/takedarts/etrobo-python/wiki)を参照してください。

## サンプルプログラム
```python
from etrobo_python import (ColorSensor, ETRobo, GyroSensor, Hub, Motor,
                           SonarSensor, TouchSensor)

# センサやモータを制御するプログラムは制御ハンドラとして登録します。
# 実行時に登録されたデバイスは、制御ハンドラに渡される引数を介して制御します。
# 以下の制御ハンドラは、センサやモータの観測値を出力するプログラムです。
def print_obtained_values(
    hub: Hub,
    right_motor: Motor,
    left_motor: Motor,
    touch_sensor: TouchSensor,
    color_sensor: ColorSensor,
    sonar_sensor: SonarSensor,
    gyro_sensor: GyroSensor,
) -> None:
    lines = [
        'Hub: battery_voltage={}'.format(hub.get_battery_voltage()),
        'RightMotor: count={}'.format(right_motor.get_count()),
        'LeftMotor: count={}'.format(left_motor.get_count()),
        'TouchSensor: pressed={}'.format(touch_sensor.is_pressed()),
        'ColorSensor: raw_color={}'.format(color_sensor.get_raw_color()),
        'SonarSensor: distance={}'.format(sonar_sensor.get_distance()),
        'GyroSensor: velocity={}'.format(gyro_sensor.get_angler_velocity()),
    ]
    print('\n'.join(lines))

# シミュレータ環境で上記の制御ハンドラを実行するコードです。
# 制御対象のデバイスを登録し、上記の制御ハンドラを登録しています。
# backendを'pybricks'に変更することでEV3環境でも動作します。
(ETRobo(backend='simulator')
 .add_hub(name='hub')
 .add_device('right_motor', device_type='motor', port='B')
 .add_device('left_motor', device_type='motor', port='C')
 .add_device('touch_sensor', device_type='touch_sensor', port='1')
 .add_device('color_sensor', device_type='color_sensor', port='2')
 .add_device('sonar_sensor', device_type='sonar_sensor', port='3')
 .add_device('gyro_sensor', device_type='gyro_sensor', port='4')
 .add_handler(print_obtained_values)
 .dispatch(course='left', interval=0.1))
```
