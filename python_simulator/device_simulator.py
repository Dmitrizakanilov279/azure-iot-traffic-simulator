import time
import json
import random

# ถ้าไม่มี Azure โค้ดจะรันแบบ Local Mode อัตโนมัติ
CONNECTION_STRING = "YOUR_DEVICE_CONNECTION_STRING_HERE"
DEVICE_ID = "SmartTrafficSimulated"

sensor_state = {
    "status": "active",
    "velocity": 45.0
}

# เช็คว่ามี Connection String ของจริงหรือไม่
is_local_mode = (CONNECTION_STRING == "YOUR_DEVICE_CONNECTION_STRING_HERE")

if not is_local_mode:
    from azure.iot.device import IoTHubDeviceClient, Message
    try:
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        client.connect()
    except ValueError:
        print("ERROR: Invalid Connection String")
        exit(1)
else:
    print("=====================================================")
    print("⚠️  Running in LOCAL MOCK MODE (No Azure connection) ⚠️")
    print("💡 โหมดจำลองข้อมูล: สามารถแคปหน้าจอนี้ลง GitHub Portfolio ได้เลย")
    print("=====================================================\n")

def send_telemetry():
    """จำลองการส่งข้อมูลความเร็วรถแบบ Real-time"""
    # จำลองความเร็วรถที่เปลี่ยนไปมา (เช่น รถชะลอตัว หรือเร่งความเร็ว)
    sensor_state["velocity"] += round(random.uniform(-10.0, 5.0), 2)
    if sensor_state["velocity"] < 0: sensor_state["velocity"] = 0

    telemetry_msg = { 
        "deviceId": DEVICE_ID, 
        "current_velocity_kmh": round(sensor_state["velocity"], 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if is_local_mode:
        # รันบนเครื่องตัวเอง จะแสดงผลเป็น JSON สีสวยๆ ให้อ่านง่าย
        print(f"[LOCAL TEST] 🚗 อัปเดตข้อมูลจราจร: {json.dumps(telemetry_msg)}")
        if telemetry_msg["current_velocity_kmh"] < 15.0:
            print("   🚨 [ALERT] ตรวจพบการจราจรติดขัด! ความเร็วต่ำกว่าเกณฑ์")
    else:
        # ส่งขึ้น Azure ของจริง
        client.send_message(Message(json.dumps(telemetry_msg)))
        print(f" Sending Telemetry: {telemetry_msg}")

# --- เริ่มการทำงาน ---
try:
    print("--- Traffic Simulator is running! (Ctrl+C to stop) ---\n")
    while True:
        send_telemetry()
        time.sleep(3) # จำลองการส่งข้อมูลทุกๆ 3 วินาที
except KeyboardInterrupt:
    print("\n🛑 Simulator stopped by user.")
