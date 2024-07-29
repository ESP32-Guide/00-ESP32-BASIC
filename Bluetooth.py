from machine import Pin, Timer
from time import sleep_ms
import ubluetooth


message: str = ""

class ESP32_BLE:
    def __init__(self, name: str, device_type: int) -> None:
        # Initialize the onboard LED and Timer
        self.led: Pin = Pin(2, Pin.OUT)
        self.timer1: Timer = Timer(0)
        
        # Initialize BLE with the given name and device type
        self.name: str = name
        self.device_type: int = device_type
        self.ble: ubluetooth.BLE = ubluetooth.BLE()
        self.ble.active(True)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self) -> None:
        # LED stable ON when connected
        self.led.value(1)
        self.timer1.deinit()

    def disconnected(self) -> None:
        # LED blinking when no BLE device is connected
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

    def ble_irq(self, event: int, data: Any) -> None:
        global message
        
        if event == 1:  # _IRQ_CENTRAL_CONNECT
            self.connected()

        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT
            self.advertiser()
            self.disconnected()

        elif event == 3:  # _IRQ_GATTS_WRITE
            buffer: bytes = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            print(message)

    def register(self) -> None:
        # Define UUIDs for Nordic UART Service (NUS)
        NUS_UUID: ubluetooth.UUID = ubluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
        RX_UUID: ubluetooth.UUID = ubluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E')
        TX_UUID: ubluetooth.UUID = ubluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E')

        BLE_RX = (RX_UUID, ubluetooth.FLAG_WRITE)
        BLE_TX = (TX_UUID, ubluetooth.FLAG_NOTIFY)

        BLE_UART = (NUS_UUID, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART,)
        ((self.tx, self.rx,),) = self.ble.gatts_register_services(SERVICES)

    def send(self, data: str) -> None:
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self) -> None:
        name: bytes = bytes(self.name, 'UTF-8')
        adv_data: bytearray = bytearray([
            0x02, 0x01, 0x06,  # Flags
            (len(name) + 1), 0x09  # Complete Local Name
        ]) + name
        self.ble.gap_advertise(100, adv_data)
        print(adv_data)
        print("\r\n")

# Initialize pins and BLE
led: Pin = Pin(2, Pin.OUT)
but: Pin = Pin(0, Pin.IN, Pin.PULL_UP)
ble: ESP32_BLE = ESP32_BLE("ESP32", 0x02)

def buttons_irq(pin: Pin) -> None:
    led.value(not led.value())
    ble.send('LED state will be toggled.')
    print('LED state will be toggled.')

# Configure button interrupt
but.irq(trigger=Pin.IRQ_FALLING, handler=buttons_irq)

while True:
    if message == "STATUS":
        message = ""
        print('LED is ON.' if led.value() else 'LED is OFF')
        ble.send('LED is ON.' if led.value() else 'LED is OFF')
    sleep_ms(100)

