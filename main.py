from threading import Thread

def main():
    import ui
    import skinchanger

    skinchanger = Thread(target=skinchanger.main)
    ui = Thread(target=ui.main)
    skinchanger.start()
    ui.start()

if __name__ == '__main__':
    main()
    