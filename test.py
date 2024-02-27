import time
import odrive
from odrive.enums import *

# ODriveを検出
print("ODriveを検出中...")
odrv0 = odrive.find_any()
print("ODriveが検出されました。")

# モーターの設定を行う
# ここでは、例としてモーター0を使用
axis = odrv0.axis0

# モーターを閉ループ制御モードに設定
axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# 制御モードを速度制御に設定
axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

# モーターを定速で回転させる
# ここでは、例として1000counts/sで回転させる
desired_velocity = 1000 # この値は実際の要件に応じて調整してください
axis.controller.vel_setpoint = desired_velocity

print(f"モーターを{desired_velocity}counts/sで回転中...")

# ここでは、10秒間回転させてから停止
time.sleep(10)

# モーターを停止
axis.controller.vel_setpoint = 0
print("モーターを停止しました。")

# ODriveをディスエンゲージ
axis.requested_state = AXIS_STATE_IDLE
