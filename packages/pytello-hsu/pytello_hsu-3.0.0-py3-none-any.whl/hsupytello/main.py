import socket
import threading
from datetime import datetime


class _direction:
    def __init__(self):
        self.left = "l"
        self.right = "r"
        self.forward = "f"
        self.backward = "b"


class drone:
    def __init__(self, ip="192.168.10.1"):
        """
        :param ip: The ip Address of your drone
        """
        self.direction = _direction()
        self.host = ''
        self.port = 9000
        self.locaddr = (self.host, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tello_address = (ip, 8889)
        self.sock.bind(self.locaddr)
        self.console_output = False
        self.count = 0
        self.messages = {}
        self.receiving_port = 1518
        self.time_format = "%H:%M:%S:%f"

    def send(self, msg):
        """
        :param msg: Message to send to drone
        :return: None
        """
        try:
            if not msg:
                return
            if 'end' in msg:
                print('...')
                self.sock.close()
                return
            msg = msg.encode(encoding="utf-8")
            sent = self.sock.sendto(msg, self.tello_address)
        except KeyboardInterrupt:
            print('\n . . .\n')
            self.sock.close()
            return

    def ipconfig(self, ip):
        """
        :param ip: IP Address to change the drone to
        :return: None
        """
        ip = str(ip)
        self.tello_address = (ip, 8889)

    def recv(self):
        """
        Start getting messages from drone
        :return: None
        """
        while True:
            try:
                data, server = self.sock.recvfrom(self.receiving_port)
                message = data.decode(encoding="utf-8")
                if self.console_output:
                    print(message)
                self.messages[datetime.now().strftime(self.time_format)] = message
            except Exception:
                print('\nExit . . .\n')
                break

    def takeoff(self):
        """
        Auto takeoff
        :return: None
        """
        self.send("takeoff")

    def land(self):
        """
        Auto land
        :return: None
        """
        self.send("land")

    def command(self):
        """
        Enter SDK mode
        :return: None
        """
        self.send("command")

    def eland(self):
        """
        Stop motors immediately
        :return: None
        """
        self.send("emergency")

    def up(self, x):
        """
        Ascend to "x" cm
        :param x: A string of numbers ranging from from 20 to 500
        :return: None
        """
        self.send("up " + x)

    def down(self, x):
        """
        Descend to "x" cm
        :param x: A string of numbers ranging from from 20 to 500
        :return: None
        """
        self.send("down " + x)

    def left(self, x):
        """
        Fly left "x" cm
        :param x: A string of numbers ranging from from 20 to 500
        :return: None
        """
        self.send("left " + x)

    def right(self, x):
        """
        Fly right "x" cm
        :param x: A string of numbers ranging from from 20 to 500
        :return: None
        """
        self.send("right " + x)

    def forward(self, x):
        """
        Fly forward "x" cm
        :param x: A string of numbers ranging from from 20 to 500
        :return: None
        """
        self.send("forward " + x)

    def backward(self, x):
        """
        Fly backward "x" cm
        :param x: A string of numbers ranging from from 20 to 500
        :return: None
        """
        self.send("back " + x)

    def clockwise(self, degrees):
        """
        Turn "degrees" clockwise
        :param degrees: A string of numbers ranging from from 1 to 360
        :return: None
        """
        self.send("cw " + degrees)

    def counterclockwise(self, degrees):
        """
        Turn "degrees" counter-clockwise
        :param degrees: A string of numbers ranging from from 1 to 360
        :return: None
        """
        self.send("ccw " + degrees)

    def flip(self, direction):
        """
        Flip in your desired direction
        :param direction: A direction selected in the direction class embeded within this class
        :return: None
        """
        self.send("flip " + direction)

    def speed(self, x):
        """
        Set "x" to centimeters per second
        :param x: A string of numbers ranging from from 10 to 100
        :return: None
        """
        self.send("speed " + x)

    def go_to_cord(self, x, y, z, speed="60"):
        """
        :param speed: A string of numbers ranging from from 10 to 100. The unit used for this platform is centimeters per second. This is the speed for this operation only.
        :param x: The amount of centimeters on the x-axis you want to go. Range from -500 to 500.
        :param y: The amount of centimeters on the y-axis you want to go. Range from -500 to 500.
        :param z: The amount of centimeters on the z-axis you want to go. Range from -500 to 500.
        :return: None
        """
        self.send("go " + str(int(x)) + " " + str(int(y)) + " " + str(int(z)) + " " + str(int(speed)))

    def stop(self):
        """
        Stops the drone from completing an operation at any given time
        :return: None
        """
        self.send("stop")

    def curve(self, x, y, z, x1, y1, z1, speed="60"):
        """
        Fly in a curve to the specific coordinates. If the arc radius is not within a range of 0.5 to 10 meters, the
         drone will send an error over the recv channel. The variables must be within the integer range of -500 and 500.
        Speed: A string of numbers ranging from from 10 to 60. The unit used for this platform is centimeters per second. This is the speed for this operation only.
        :return: None
        """
        self.send("curve " + str(int(x)) + " " + str(int(y)) + " " + str(int(z)) + " " + str(int(x1)) + " " + str(int(y1)) + " " + str(int(z1)) + " " + str(int(speed)))

    def wifi_config(self, network_name, password, ap=False):
        """
        :param network_name: Name of the network for the drone to broadcast or connect to
        :param password: Password of the network for the drone to require connection or the password for the network for
         the drone to connect to.
        :param ap: If true, then the drone will connect to a network rather than broadcast a network
        :return: None
        """
        if ap:
            self.send("ap" + " " + network_name + " " + password)
        else:
            self.send("wifi" + " " + network_name + " " + password)

    def get_speed(self):
        """
        Obtain current speed. Sends output to recv thread through the recv command
        :return: None
        """
        self.send("speed?")

    def get_battery(self):
        """
        Obtain current battery. Sends output to recv thread through the recv command
        :return: None
        """
        self.send("battery?")

    def get_time(self):
        """
        Obtain current flight time. Sends output to recv thread through the recv command
        :return: None
        """
        self.send("time?")

    def get_serial_number(self):
        """
        Obtain serial number. Sends output to recv thread through the recv command
        :return: None
        """
        self.send("sn?")

    def get_signal_to_noise_ratio(self):
        """
        Obtain current signal to noise ratio. Sends output to recv thread through the recv command
        :return: None
        """
        self.send("wifi?")

    def init(self):
        """
        Initialize communication with the drone
        :return: None
        """
        self.command()
        recvthread = threading.Thread(target=self.recv)
        recvthread.start()
