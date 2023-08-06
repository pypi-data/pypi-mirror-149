from math import pi
from typing import Optional
from numpy import cos, tanh

m = 0.25                # Mass of the arm (kg)
I = m * (6.5e-5)    # kg * sqrt(m^4) -> kg m^2
g = 9.8                 # Gravitational Constant m/s^2
# Distance from the axis to the center of mass (Estimate: 20 cm)
r = 0.15
friction = 1e-3


def tau_gravity(**kw):
    """Torque due to gravity

    This function computes the torque due to gravity for given mass and radius.
    """
    return - r * m * cos(kw['theta'] * pi/180.0)


def tau_friction(**kw):
    """Friction is a constant force that points in the direction opposite motion.
    """
    # This can't be nonlinear or else the solver goes crazy.
    # Use tanh because it's almost sign(omega)
    return - friction * tanh(kw['omega'])
    # return - friction * np.sign(kw['omega'])


class ArmPhysics:
    m = 1.5                 # Mass of the arm (kg)
    I = m * (6.5e-5)        # kg * sqrt(m^4) -> kg m^2
    g = 9.8                 # Gravitational Constant m/s^2
    # Distance from the axis to the center of mass (Estimate: 20 cm)
    r = 0.20

    friction = 1e-3
    friction_int = 5e-4

    def tau_gravity(self, theta=None, **kw):
        """Torque due to gravity

        This function computes the torque due to gravity for given mass and radius.
        """
        return - self.r * self.m * cos(theta * pi/180.0)

    def tau_friction(self, omega: Optional[float] = None, **kw) -> float:
        """Friction is a constant force that points in the direction opposite motion.
        """
        # This can't be nonlinear or else the solver goes crazy.
        # Use tanh because it's almost sign(omega)
        return - self.friction * tanh(omega)
        # return - friction * np.sign(kw['omega'])

    def tau_internal_friction(self, omega=None, omega_int=None, **kw) -> float:
        """Computes internal friction (between motor and arm)
        """
        if omega_int is None:
            return 0.0
        delta_omega = omega - omega_int
        return -self.friction_int * delta_omega

    def torque(self, **kw) -> float:
        """Compute the total torque applied to the load.
        """
        # Return the total torque from gravity and friction.
        return sum([x(**kw) for x in (self.tau_gravity, self.tau_friction, self.tau_internal_friction)])
