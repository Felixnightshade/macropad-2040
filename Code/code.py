"""
Formatted with Black.
"""

import asyncio
import time

from adafruit_macropad import MacroPad

macropad = MacroPad()
text_lines = macropad.display_text(title="Mode")
key_event = macropad.keys.events.get()
encoder_value = None
modes = ("osu! normal", "osu! single")
current_mode = None
# fmt: off
down = [
    0, 0, 0,
    0, 0, 0,
    0, 0, 0,
    0, 0, 0
]
# fmt: on


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


def update_down():
    global key_event
    global down
    if key_event.pressed:
        down[key_event.key_number] = 1
    if key_event.released:
        down[key_event.key_number] = 0


def macro_enable_hidden():
    global macropad
    global key_event
    if key_event.pressed:
        macropad.keyboard.send(macropad.Keycode.F1)
        time.sleep(0.008)
        macropad.keyboard.send(macropad.Keycode.F)
        time.sleep(0.008)
        macropad.keyboard.send(macropad.Keycode.F1)


def macro_single_tap():
    global macropad
    global key_event
    global down
    if key_event.pressed:
        macropad.keyboard.release(macropad.Keycode.Z)
        macropad.keyboard.press(macropad.Keycode.Z)
    elif key_event.released:
        if sum(down) == 0:
            macropad.keyboard.release(macropad.Keycode.Z)


def macro_empty():
    pass


async def handle_keys():
    global macropad
    global key_event
    global current_mode
    global down
    # fmt: off
    remaps = {
        "osu! normal" : (
            macropad.Keycode.ESCAPE,       macropad.Keycode.F2,         macro_enable_hidden,
            macropad.Keycode.GRAVE_ACCENT, macropad.Keycode.UP_ARROW,   macropad.Keycode.ENTER,
            macropad.Keycode.LEFT_ARROW,   macropad.Keycode.DOWN_ARROW, macropad.Keycode.RIGHT_ARROW,
            macropad.Keycode.Z,            macropad.Keycode.X,          macropad.Keycode.SHIFT
        ),
        "osu! single" : (
            macropad.Keycode.ESCAPE,       macropad.Keycode.F2,         macro_enable_hidden,
            macropad.Keycode.GRAVE_ACCENT, macropad.Keycode.UP_ARROW,   macropad.Keycode.ENTER,
            macropad.Keycode.LEFT_ARROW,   macropad.Keycode.DOWN_ARROW, macropad.Keycode.RIGHT_ARROW,
            macro_single_tap,              macro_single_tap,            macropad.Keycode.SHIFT
        )
    }
    # fmt: on

    while True:
        if key_event:
            update_down()
            if type(remaps[current_mode][key_event.key_number]) == int:
                if key_event.pressed:
                    macropad.keyboard.press(remaps[current_mode][key_event.key_number])
                elif key_event.released:
                    macropad.keyboard.release(
                        remaps[current_mode][key_event.key_number]
                    )
            else:
                remaps[current_mode][key_event.key_number]()

            key_event == 0

        await asyncio.sleep(0.001)


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

        await asyncio.sleep(0.04)


async def main():
    key_input_task = asyncio.create_task(poll_keys())
    key_handle_task = asyncio.create_task(handle_keys())
    encoder_input_task = asyncio.create_task(poll_encoder())
    encoder_handle_task = asyncio.create_task(handle_encoder())

    await asyncio.gather(
        key_input_task, key_handle_task, encoder_input_task, encoder_handle_task
    )


asyncio.run(main())
