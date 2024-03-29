import PySimpleGUIQt as GUI

from inspyre_toolbox import live_timer as timekeep

timer = timekeep.Timer()
timer.start()

layout = [
        [GUI.Text("00:00:00", key="TIMER")],
        [GUI.Button("Quit", tooltip="Quit the program", enable_events=True, key="QUIT_BUTTON")]
]


def run_window():
    window = GUI.Window("Test Timer", layout=layout)
    while True:
        event, vals = window.read(timeout=100)
        window['TIMER'].update(timer.get_elapsed())

        if event is None:
            print(f"Exiting program. Final elapsed time: {timer.get_elapsed()}")
            window.close()
            exit(0)

        if event == "QUIT_BUTTON":
            print("User pressed the quit button!")
            print(f"Exiting program. Final elapsed time: {timer.get_elapsed()}")
            window.close()
            exit(0)


run_window()
