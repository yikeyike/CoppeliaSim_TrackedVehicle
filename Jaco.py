from os.path import dirname, join, abspath
from pyrep import PyRep
from pyrep.robots.arms.arm import Arm


from os.path import dirname, join, abspath
from pyrep import PyRep
from pyrep.robots.arms.jaco import Jaco
from pyrep.objects.shape import Shape
from pyrep.const import PrimitiveShape
from pyrep.errors import ConfigurationPathError
import numpy as np
import math

LOOPS = 10
SCENE_FILE = join(dirname(abspath(__file__)), 'Jaco.ttt')
pr = PyRep()
pr.launch(SCENE_FILE, headless=False)
pr.start()
agent = Jaco()

# We could have made this target in the scene, but lets create one dynamically
target = Shape.create(type=PrimitiveShape.SPHERE,
                      size=[0.05, 0.05, 0.05],
                      color=[1.0, 0.1, 0.1],
                      static=True, respondable=False)

position_min, position_max = [-0.2, -0.2, 0.3], [0.2, 0.2, 0.8]

starting_joint_positions = agent.get_joint_positions()

for i in range(LOOPS):

    # Reset the arm at the start of each 'episode'
    agent.set_joint_positions(starting_joint_positions)

    # Get a random position within a cuboid and set the target position
    pos = list(np.random.uniform(position_min, position_max))
    target.set_position(pos)

    # Get a path to the target (rotate so z points down)
    try:
        path = agent.get_path(
            position=pos, euler=[0, math.radians(180), 0])
    except ConfigurationPathError as e:
        print('Could not find path')
        continue

    # Step the simulation and advance the agent along the path
    done = False
    while not done:
        done = path.step()
        pr.step()

    print('Reached target %d!' % i)

pr.stop()
pr.shutdown()

