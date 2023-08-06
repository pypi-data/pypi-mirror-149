from ascratch.arm_model import Arm


def test_arm_step():
    """Test that step works.
    """
    arm = Arm()
    arm.step()
