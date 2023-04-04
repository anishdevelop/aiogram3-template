if __name__ == "__main__":
    import sys

    if sys.version_info < (3, 8):
        sys.exit("Please use Python 3.8+")

    from app.main import run

    run()
