# Tis But a Scratch

Code to support the physical modeling of a robotic arm.  The arm is driven by
two motors: one at the base and one at tne "elbow." The base experiences the
greatest torque and inertia because it must move both the base arm, the fore-arm
motor, and the fore-arm with its claw attachment.

## Computing the Moment of Inertia

Note that the moment of inertia for an arm with joints is a little tricky to
calculate. But there's a theorem that helps.  The Parallel Axis Theorem
states that if you know the moment of inertia about the centroid of an
object, then the moment of inertia about an axis parallel to that centroid
can be computed as follows:

<img src="https://render.githubusercontent.com/render/math?math=I_{xx} = I_{g} + d^2 A">

Where <img src="https://render.githubusercontent.com/render/math?math=I_{xx}"> is the moment about the new axis, <img src="https://render.githubusercontent.com/render/math?math=I_g"> is the moment
about the centroid, <img src="https://render.githubusercontent.com/render/math?math=d^2"> is the centroid, and <img src="https://render.githubusercontent.com/render/math?math=A"> is the cross-sectional
area of the object.  

Using this theorem, we can conclude that the contribution
of the base arm segment (closest to the robot) remains constant because its
centroid is a fixed distance from the axis.  Only the forearm's contribution
to the total momentum affecting the base drive motor varies.  And it does so
in an easily predictable way.  We just need to know the cross-sectional area
of the part and its centroid distance from the elbow to compute the inertia
contributed by the fore-arm.
