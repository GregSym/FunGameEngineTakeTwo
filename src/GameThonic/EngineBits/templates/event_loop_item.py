
from abc import ABC, abstractmethod
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
from typing import NoReturn
import asyncio


class EventLoopItem(ABC):
    """
        A general structure for items in an event loop
    """

    @abstractmethod
    def setup():
        """
            run before the start of the loop
             - sets up some initial state
             - can be called as part of __init__()
        """

    @abstractmethod
    def loop_logic():
        """
            update and draw are called iteratively inside this function
        """

    @abstractmethod
    def update():
        """
            The main method to be called iteratively as part of the
            event loop
        """

    @abstractmethod
    def draw():
        """
            A particular section of the update seperated out from update
            because the graphics API shouldn't be too deeply entangled with
            regular business logic
        """


class EventLoopImplementation(EventLoopItem):
    """
        An implementation of a basic event-loop
        - triggered by using the run() -> NoReturn method
    """

    def loop_logic(self):
        self.update()
        self.draw()

    def run(self) -> NoReturn:
        """ runs the event loop """
        self.setup()
        while True:
            self.loop_logic()


class EventLoopMultithreadedDraw(EventLoopImplementation):
    def loop_logic(self):
        processes: list[Future] = []
        with ThreadPoolExecutor() as executor:
            processes.append(executor.submit(lambda: self.update()))
            processes.append(executor.submit(lambda: self.draw()))
            for index, p in enumerate(processes):
                if not p.running():
                    processes.pop(index)
            print(len(processes))


class EventLoopAsync(EventLoopItem):
    async def loop_logic(self):
        await self.update()
        await self.draw()

    async def _asynchronous_loop(self):
        """ backup technique for generating asyncio enabled loop """
        while True:
            await self.loop_logic()

    def run(self) -> NoReturn:
        self.setup()
        loop = asyncio.get_event_loop()
        loop.run_forever(self.loop_logic())
