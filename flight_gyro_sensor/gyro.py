import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# helpers
def dist(a,b):
        return math.sqrt((a*a)+(b*b))

def get_z_rotation(x,y,z):
    radians = math.atan2(z, dist(y,x))
    return -math.degrees(radians)

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)

class GYRO:
    def __init__(self, timestamp, **kwargs):
        self.enabled = False
        self.stop_gyro_thread = False
        self.bus = None
        self.address = 0x68 # default for gyro sensor
        self.orientation = {
            "acceleration": { "x": None, "y": None, "z": None },
            "rotation": { "x": None, "y": None, "z": None }
        }
        self.logfile = open("aether-log-gyro-"+timestamp, "w+")
        self.logfile.write(
            "accel_xout_scaled"
            +"\t"+
            "accel_yout_scaled"
            +"\t"+
            "accel_zout_scaled"
            +"\t"+
            "x_rotation"
            +"\t"+
            "y_rotation"
            +"\t"+
            "z_rotation"
            +"\n"
        )

    def is_enabled(self):
        return self.enabled

    def enable_gyro(self):
        # wake up the gyro sensor here
        self.bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
        self.address = 0x68       # This is the address value read via the i2cdetect command
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, power_mgmt_1, 0)
        self.enabled = True

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def get_current_orientation(self):
        return self.orientation

    def read_orientation_from_sensor(self):
        while True:
            if self.stop_gyro_thread:
                #print("stopping current val = ", self.stop_gyro_thread)
                break
            # scaling gyro output
            try:
                gyro_xout = self.read_word_2c(0x43) / 131
                gyro_yout = self.read_word_2c(0x45) / 131
                gyro_zout = self.read_word_2c(0x47) / 131

                accel_xout = self.read_word_2c(0x3b)
                accel_yout = self.read_word_2c(0x3d)
                accel_zout = self.read_word_2c(0x3f)

                accel_xout_scaled = accel_xout / 16384.0
                accel_yout_scaled = accel_yout / 16384.0
                accel_zout_scaled = accel_zout / 16384.0

                x_rotation = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
                y_rotation = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
                z_rotation = get_z_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

                self.orientation = {
                    "acceleration": { "x": accel_xout_scaled, "y": accel_yout_scaled, "z": accel_zout_scaled },
                    "rotation": { "x": x_rotation, "y": y_rotation, "z": z_rotation }
                }
                self.logfile.write(
                    str(accel_xout_scaled)
                    +"\t"+
                    str(accel_yout_scaled)
                    +"\t"+
                    str(accel_zout_scaled)
                    +"\t"+
                    str(x_rotation)
                    +"\t"+
                    str(y_rotation)
                    +"\t"+
                    str(z_rotation)
                    +"\n"
                )
            except Exception as e:
                print("Got exception " + str(e))

    def stop_gyro(self):
        #print("Stopping gps now")
        self.stop_gyro_thread = True
        self.logfile.close()

    def start_gyro(self):
        self.stop_gyro_thread = False



