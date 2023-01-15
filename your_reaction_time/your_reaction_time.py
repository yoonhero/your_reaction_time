from pcconfig import config
import pynecone as pc
import time
import random
import asyncio


class Score(pc.Model):
    score: int
    time: str


def current_milli_time():
    return round(time.time() * 1000)


class State(pc.State):
    finish_game: bool = True
    game_start: int
    stop: bool = False
    score: int = 0
    con: bool = False

    game_start_time: float = None

    def stop_timer(self):
        self.stop = True
        now = current_milli_time()

        self.score = now - self.game_start

    def start_game(self):
        self.finish_game = False
        to_sleep = random.random() * 10
        to_sleep = to_sleep if to_sleep < 4 else 4

        # print(to_sleep)

        self.game_start_time = current_milli_time() + to_sleep*1000

        return self.tick

    # @pc.var
    # def con(self) -> bool:
    #     print("askdj;f")

    async def tick(self):
        if self.game_start_time == None:
            self.con = False
        now = current_milli_time()
        if now >= self.game_start_time:
            self.game_start = now
            self.con = True
        else:
            await asyncio.sleep(1)

            return self.tick

    def restart(self):
        self.finish_game = True
        self.stop = False
        self.con = False

        self.start_game()

# MODAL


def start_game(State):
    return pc.modal(
        pc.modal_overlay(
            pc.modal_content(
                pc.center(
                    pc.vstack(
                        pc.modal_header(
                            pc.heading("Your Reaction Time!")
                        ),
                        pc.modal_body(
                            pc.button(
                                "Are you Ready?",
                                on_click=State.start_game,
                                bg="#8DCBE6",
                                # bg="rgb(239, 100, 49)",
                                color="#F7F5EB"
                            )
                        )
                    ),
                    padding="30px"

                )

            ),

        ),
        is_open=State.finish_game,
        border_radius="lg",
    )


def index():
    return pc.center(
        pc.cond(
            State.finish_game,
            pc.vstack(
                pc.text("Are You Ready?", font_size="60px"),
                pc.button(
                    "Yes",
                    on_click=State.start_game,
                    bg="#8DCBE6",
                    # bg="rgb(239, 100, 49)",
                    color="#F7F5EB",
                    font_size="30px",
                    padding="20px"
                ),
            ),

            pc.cond(
                State.con,

                pc.center(

                    pc.cond(
                        State.stop,
                        pc.vstack(
                            pc.text(State.score+"ms", font_size="200px"),
                            pc.button("restart", on_click=State.restart)

                        ),

                        pc.button(
                            pc.text("Click!",
                                    font_size="50px", color="#86C8BC"),
                            on_click=State.stop_timer,
                            width="100%",
                            height="100%",
                            is_active=True,
                        ),
                    ),

                    width="100%",
                    height="100%",
                ),
                pc.center(
                    pc.text("Click When Text Gets Green!",
                            font_size="50px"),
                    width="100%",
                    height="100%",
                )
            ),
        ),
        width="100%",
        height="100vh"
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
