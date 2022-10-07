from pynput.mouse import Button, Controller

mouse = Controller()

# Read pointer position
print('The current pointer position is {0}'.format(
    mouse.position))

# Set pointer position
mouse.position = (50, 100)
print('Now we have moved it to {0}'.format(
    mouse.position))

# Move pointer relative to current position
# mouse.move(5, -5)

# Press and release
mouse.press(Button.left)
mouse.release(Button.left)


# Double click; this is different from pressing and releasing
# twice on macOS
# mouse.click(Button.left, 2)

# Scroll two steps down
# mouse.scroll(0, 2)

def select_e7_window():
    m = Controller()
    m.position = (50, 100)
    m.press(Button.left)
    m.release(Button.left)
    print('Now we have moved it to {0}'.format(m.position))
