from i3ipc import Event
from i3ipc.aio import Connection
import asyncio

PHI = (1 + 5**(1 / 2)) / 2

class Fibonacci3:

    async def run(self):
        i3 = await Connection().connect()
        tree = await i3.get_tree()
        rect = tree.workspaces()[0].rect
        self.width = rect.width
        self.height = rect.height
        i3.on(Event.WINDOW_FOCUS, self.on_focus_window)
        i3.on(Event.WINDOW_NEW, self.on_focus_window)
        i3.on(Event.WORKSPACE_FOCUS, self.on_workspace_focus)
        await i3.main()


    async def on_focus_window(self, i3, e):
        tree = await i3.get_tree()
        con = tree.find_focused()
        new_width = int(self.width / PHI)
        new_height = int(self.height / PHI)

        step = 20
        # Annoying animation :)
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

    def on_workspace_focus(self, i3, e):
        self.width = e.current.rect.width
        self.heigth = e.current.rect.height

def main():
    loop = asyncio.get_event_loop()
    f3 = Fibonacci3()
    loop.run_until_complete(f3.run())

if __name__ == "__main__":
    main()
