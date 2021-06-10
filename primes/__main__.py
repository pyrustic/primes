from pyrustic.app import App
from cyberpunk_theme import Cyberpunk
from primes.view.main_view import MainView


def main():
    # The App
    app = App()
    # Title
    app.title = "Hubstore"
    # Resizable
    app.resizable = (False, False)
    # Set theme
    app.theme = Cyberpunk()
    # Set view
    app.view = MainView(app)
    # Center the window
    app.center()
    # Lift off !
    app.start()


if __name__ == "__main__":
    main()
