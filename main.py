import queue
import sys
import CCP


def main():
    if len(sys.argv) > 1:
        #computer
        import computer

        computer.server()
        q = queue.Queue()


    else:
        #car
        pass


if __name__ == '__main__':
    main()