import signal
import sys
import tty
import termios




def wait_key(timeout_sec):

    def timeout(signum, frame):
        raise RuntimeError('timeout')

    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(timeout_sec)
    try:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
            if ord(key) == 3:
                raise KeyboardInterrupt()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    except RuntimeError:
        key = None
    finally:
        signal.alarm(0)

    return key


def take_test(a):
    while True:
        key = wait_key(1)
        print('>')
        if key is not None:
            if key == a:
                print('正解!')
            else:
                print('違うよ')


if __name__ == "__main__":
    take_test('3')
