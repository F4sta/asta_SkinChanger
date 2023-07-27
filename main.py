from threading import Thread

def main():
    import ui
    import skinchanger

    ui = Thread(target=ui.main())
    skinchanger = Thread(target=skinchanger.main())
    ui.start()
    skinchanger.start()

if __name__ == '__main__':
    main()
    