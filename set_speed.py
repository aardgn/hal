
import asyncio
from bleak import BleakClient, BleakScanner

CONTROL_POINT = "00002ad9-0000-1000-8000-00805f9b34fb"


async def main():
    speed_text = input("Hedef hız (1.0–8.0 km/sa): ").strip()

    try:
        speed = float(speed_text)
    except ValueError:
        print("Geçerli bir sayı gir.")
        return

    if not 1.0 <= speed <= 8.0:
        print("Hız 1.0 ile 8.0 km/sa arasında olmalı.")
        return

    if abs(speed * 10 - round(speed * 10)) > 1e-6:
        print("Hız 0.1 km/sa adımlarla ayarlanmalı.")
        return

    print("\nKoşu bandı BOŞ ve DURUYOR olmalı.")
    confirm = input(f"{speed:.1f} km/sa hedef hızını gönder? (EVET): ")
    if confirm != "EVET":
        print("İptal edildi.")
        return

    print("Bluetooth cihazları aranıyor...")
    devices = await BleakScanner.discover(timeout=8)

    candidates = [
        d for d in devices
        if d.name and d.name.startswith("FS-")
    ]

    if not candidates:
        print("Koşu bandı bulunamadı. Bandın Bluetooth'unu kontrol et.")
        return

    device = next(
        (d for d in candidates if d.name == "FS-613934"),
        candidates[0],
    )
    print(f"Bağlanılıyor: {device.name}")

    async with BleakClient(device) as client:
        responses = asyncio.Queue()

        def on_control_point(sender, data):
            responses.put_nowait(bytes(data))

        await client.start_notify(CONTROL_POINT, on_control_point)

        async def send_command(command):
            await client.write_gatt_char(
                CONTROL_POINT, command, response=True
            )
            try:
                response = await asyncio.wait_for(
                    responses.get(), timeout=5
                )
            except asyncio.TimeoutError:
                raise RuntimeError("Cihazdan yanıt gelmedi.")

            print("Yanıt:", response.hex(" "))

            if (
                len(response) < 3
                or response[0] != 0x80
                or response[1] != command[0]
                or response[2] != 0x01
            ):
                raise RuntimeError("Komut onaylanmadı.")

        try:
            print("Kontrol izni isteniyor...")
            await send_command(bytes([0x00]))

            value = round(speed * 100)
            command = bytes([
                0x02,
                value & 0xFF,
                (value >> 8) & 0xFF,
            ])

            print(f"{speed:.1f} km/sa hız komutu gönderiliyor...")
            await send_command(command)
            print("Hız komutu cihaz tarafından onaylandı.")
            print("Bu program bandı BAŞLATMAZ.")

        finally:
            await client.stop_notify(CONTROL_POINT)


if __name__ == "__main__":
    asyncio.run(main())
