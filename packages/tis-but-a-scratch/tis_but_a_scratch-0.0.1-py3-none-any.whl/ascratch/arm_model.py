from ascratch.motor import MotorAndGearbox
from ascratch.basic_physics import ArmPhysics
from scipy.integrate import solve_ivp
from typing import List

import numpy as np


class Arm:
    def __init__(self):
        mot = MotorAndGearbox(free_speed=360, gearbox_k=10)
        phys = ArmPhysics()
        phys.I *= 10
        self.mot = mot
        self.phys = phys
        self.time = 0
        self.state = (0, 0, 0)
        self.times = []
        self.powers = []
        self.states = []

    def ode_function(self, t, y):
        # This is one way to implement the PID control.  It's probably better to run
        # solve_ivp in X millisecond steps, then update p using a PID control and
        # simulate again.

        theta_ext, omega, theta_int = y
        self.mot.theta_int = theta_int
        kw = {"theta": theta_ext, "omega": omega,
              "delta_theta": theta_ext-theta_int}
        load_torque = self.mot.backlash_torque(kw['delta_theta'])
        dtheta_int = self.mot.speed(motor_torque=-load_torque)
        kw["omega_int"] = dtheta_int

        # Sum all the taus we compute.
        sigmatau = self.phys.torque(**kw) + self.mot.torque(theta_ext)
        # if F = ma , then a = F / m (or \alpha = \tau / I)
        # Omega is dtheta/dt. sum of torques / I is domega/dt, dtheta_dt is driven by the motor only.
        return [omega, sigmatau / self.phys.I, dtheta_int]

    def step(self, dt: float = 0.001) -> List[float]:
        """This moves the system forward one time tick. 

        :param: dt the size of the time tick
        :returns: the time and the measured angle.
        """
        t_end = self.time + dt
        bunch = solve_ivp(self.ode_function, [self.time, t_end], self.state,
                          method='RK45',
                          vetorized=True,
                          t_eval=[t_end])  # , tfirst=True, full_output=1)

        # Save the state
        self.state = bunch['y'].flatten()
        self.states.append(self.state)

        # Save the time in t and times.
        self.time = bunch['t'][0]
        self.times.append(self.time)

        self.powers.append(self.mot.power)

        # Return only the external observables!
        return self.time, self.state[0]
