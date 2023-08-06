import numpy as np
from logging import warning


class MotorAndGearbox:
    def __init__(self, free_speed=150*360/60/60, stall_torque=4.2, gearbox_k=10, backlash=1.5, theta_int=0.0):
        """Initialize the Motor and Gearbox combo

        :param: free_speed (float) rotational speed (deg/sec) with no torque
        :param: stall_torque (float) Stall torque in N m
        :param: gearbox_k (float) Gearbox spring constant (N m / deg)
        :param: backlash (float) amount of backlash (degrees)
        :param: theta_int (float) internal angle (before backlash) 
        """
        self.free_speed = free_speed
        self.stall_torque = stall_torque
        self.gearbox_k = gearbox_k
        self.backlash = backlash
        self.theta_int = theta_int
        # Power applied to the motor.
        self.power = 0.0

    def backlash_torque(self, delta_theta):
        """Return the backlash torque applied to the load as a function of delta_theta 

        Note that the force on the motor is negative of this value.
        """
        # return -np.sign(delta_theta) * np.maximum(self.gearbox_k * (np.abs(delta_theta) - self.backlash), 0)
        # Note: This needs to be continuously differentiable to make solvers happy.

        return -np.tanh(0.4*delta_theta/self.backlash)**2 * self.gearbox_k * delta_theta
        # return np.clip(calc, -50, 50)

    def torque(self, theta_ext):
        """Motor torque. Positive torque makes the motor go faster.
        """
        return self.backlash_torque(theta_ext - self.theta_int)

    def speed(self, power=None, motor_torque=0.0):
        """Compute the motor speed (deg/sec) given power (%) and external torque (Nm)

        Accepts motor power and the torque experienced by the motor (negative of the torque applied to the load.)
        """
        if power is None:
            power = self.power
        # Assume speed decreases linearly until we hit the stall torque.
        torque_speed = (np.clip(motor_torque, -self.stall_torque,
                        self.stall_torque) / self.stall_torque) * self.free_speed
        clip_speed = self.free_speed * 1.5
        return np.clip(self.free_speed * power + torque_speed, -clip_speed, clip_speed)

    def dtheta_dt(self, theta_ext):
        """The change in motor angle with timestep
        """
        # Compute Torque given the external angle.
        # Note that The torque on the motor is opposite the torque on the load.
        motor_torque = -self.torque(theta_ext)
        return self.speed(motor_torque=motor_torque)

    def step(self, dt, theta_ext):
        """Step forward by a timestep.
        """
        # Compute Torque given the external angle.
        self.theta_int += dt * self.dtheta_dt(theta_ext)
