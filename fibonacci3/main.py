from i3ipc import Event
from i3ipc.aio import Connection
import asyncio

PHI = (1 + 5**(1 / 2)) / 2

async def on_focus_window(i3, e):
    print(f"a new window opened: {e.container.name}")
    tree = await i3.get_tree()

    con = tree.find_focused()
    root =  con.root()

    rect = con.rect
    width = rect.width
    height = rect.height

    new_width = int(min(width * PHI, 1920 / PHI))
    new_height = int(min(height * PHI, 1080 / PHI))
    print(new_width, new_height)

    step = 20
    """
    while new_width > width:
        width += step
        result = await con.command(f"resize grow width {step}")
    while new_width < width:
        width -= step
        result = await con.command(f"resize shrink width {step}")
    while new_height > height:
        height += step
        result = await con.command(f"resize grow height {step}")
    while new_height < height:
        height -= step
        result = await con.command(f"resize shrink height {step}")
    """
    result = await con.command(f"resize set width {new_width}")
    result = await con.command(f"resize set height {new_height}")


async def fibonacci3():
    i3 = await Connection().connect()
    i3.on(Event.WINDOW_FOCUS, on_focus_window)
    i3.on(Event.WINDOW_NEW, on_focus_window)
    await i3.main()

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fibonacci3())

if __name__ == "__main__":
    main()
