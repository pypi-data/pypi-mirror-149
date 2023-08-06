from ascratch.basic_physics import ArmPhysics

torque_kw = {
    "theta": 90,
    "omega": 0,
    "omega_int": 0
}


def test_torque():
    """Tests that arms have torques
    """
    arm = ArmPhysics()

    t = arm.torque(**torque_kw)
    assert(abs(t) < 1e-9)
