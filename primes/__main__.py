from pyrustic.app import App
from tk_cyberpunk_theme.main import Cyberpunk
from primes.view.main_view import MainView


def main():
    # The App
    app = App(__package__)
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
