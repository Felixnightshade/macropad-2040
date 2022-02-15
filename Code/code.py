import asyncio
import time

# : )
from adafruit_macropad import MacroPad

macropad = MacroPad()
text_lines = macropad.display_text(title="Mode")
key_event = macropad.keys.events.get()
encoder_value = None
modes = ("osu! normal", "osu! single")
current_mode = None
down = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
}


async def poll_keys():
    global macropad
    global key_event
    while True:
        key_event = macropad.keys.events.get()

        await asyncio.sleep(0.001)


async def poll_encoder():
    global macropad
    global encoder_value
    while True:
        encoder_value = macropad.encoder

        await asyncio.sleep(0.04)


async def handle_keys():
    global macropad
    global key_event
    global current_mode
    global down
    while True:
        if key_event:
            if current_mode == "osu! normal":
                if key_event.key_number == 11:  # Left shift
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.SHIFT)
                        down[11] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.SHIFT)
                        down[11] = 0
                elif key_event.key_number == 10:  # Right key
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.X)
                        down[10] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.X)
                        down[10] = 0
                elif key_event.key_number == 9:  # Left key
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.Z)
                        down[9] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.Z)
                        down[9] = 0
                elif key_event.key_number == 8:  # Down arrow
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.DOWN_ARROW)
                        down[8] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.DOWN_ARROW)
                        down[8] = 0
                elif key_event.key_number == 7:  # Up arrow
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.UP_ARROW)
                        down[7] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.UP_ARROW)
                        down[7] = 0
                elif key_event.key_number == 6:
                    if key_event.pressed:
                        down[6] = 1
                    elif key_event.released:
                        down[6] = 0
                elif key_event.key_number == 5:  # Right arrow
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.RIGHT_ARROW)
                        down[5] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.RIGHT_ARROW)
                        down[5] = 0
                elif key_event.key_number == 4:  # Left arrow
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.LEFT_ARROW)
                        down[4] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.LEFT_ARROW)
                        down[4] = 0
                elif key_event.key_number == 3:  # Restart map
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.GRAVE_ACCENT)
                        down[3] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.GRAVE_ACCENT)
                        down[3] = 0
                elif key_event.key_number == 2:  # Enable hidden
                    if key_event.pressed:
                        macropad.keyboard.send(macropad.Keycode.F1)
                        down[2] = 1
                    elif key_event.released:
                        macropad.keyboard.send(macropad.Keycode.F)
                        macropad.keyboard.send(macropad.Keycode.F1)
                        down[2] = 0
                elif key_event.key_number == 1:  # Random map
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.F2)
                        down[1] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.F2)
                        down[1] = 0
                elif key_event.key_number == 0:  # Pause and exit
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.ESCAPE)
                        down[0] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.ESCAPE)
                        down[0] = 0

            if current_mode == "osu! single":
                if key_event.key_number == 11:  # Left shift
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.SHIFT)
                        down[11] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.SHIFT)
                        down[11] = 0
                elif key_event.key_number == 10:  # Left key
                    if key_event.pressed:
                        macropad.keyboard.release(macropad.Keycode.Z)
                        macropad.keyboard.press(macropad.Keycode.Z)
                        down[10] = 1
                    elif key_event.released:
                        if not down[9]:
                            macropad.keyboard.release(macropad.Keycode.Z)
                        down[10] = 0
                elif key_event.key_number == 9:  # Right key
                    if key_event.pressed:
                        macropad.keyboard.release(macropad.Keycode.Z)
                        macropad.keyboard.press(macropad.Keycode.Z)
                        down[9] = 1
                    elif key_event.released:
                        if not down[10]:
                            macropad.keyboard.release(macropad.Keycode.Z)
                        down[9] = 0
                elif key_event.key_number == 8:
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.DOWN_ARROW)
                        down[8] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.DOWN_ARROW)
                        down[8] = 0
                elif key_event.key_number == 7:
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.UP_ARROW)
                        down[7] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.UP_ARROW)
                        down[7] = 0
                elif key_event.key_number == 6:
                    if key_event.pressed:
                        down[6] = 1
                    elif key_event.released:
                        down[6] = 0
                elif key_event.key_number == 5:
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.RIGHT_ARROW)
                        down[5] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.RIGHT_ARROW)
                        down[5] = 0
                elif key_event.key_number == 4:  # Left
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.LEFT_ARROW)
                        down[4] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.LEFT_ARROW)
                        down[4] = 0
                elif key_event.key_number == 3:  # Restart map
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.GRAVE_ACCENT)
                        down[3] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.GRAVE_ACCENT)
                        down[3] = 0
                elif key_event.key_number == 2:  # Enable hidden
                    if key_event.pressed:
                        macropad.keyboard.send(macropad.Keycode.F1)
                        down[2] = 1
                    elif key_event.released:
                        macropad.keyboard.send(macropad.Keycode.F)
                        macropad.keyboard.send(macropad.Keycode.F1)
                        down[2] = 0
                elif key_event.key_number == 1:  # Random map
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.F2)
                        down[1] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.F2)
                        down[1] = 0
                elif key_event.key_number == 0:  # Pause and exit
                    if key_event.pressed:
                        macropad.keyboard.press(macropad.Keycode.ESCAPE)
                        down[0] = 1
                    elif key_event.released:
                        macropad.keyboard.release(macropad.Keycode.ESCAPE)
                        down[0] = 0

            key_event == 0

        await asyncio.sleep(0)


async def handle_encoder():
    global encoder_value
    global modes
    global current_mode
    global text_lines
    while True:
        if current_mode != modes[encoder_value % len(modes)]:
            current_mode = modes[encoder_value % len(modes)]
            text_lines[0].text = modes[encoder_value % len(modes)]
            text_lines.show()

        await asyncio.sleep(0)


async def main():
    key_input_task = asyncio.create_task(poll_keys())
    key_handle_task = asyncio.create_task(handle_keys())
    encoder_input_task = asyncio.create_task(poll_encoder())
    encoder_handle_task = asyncio.create_task(handle_encoder())

    await asyncio.gather(
        key_input_task, key_handle_task, encoder_input_task, encoder_handle_task
    )


asyncio.run(main())
