import omni.replicator.core as rep

with rep.new_layer():

    # Path for gears, work table, and the environment
    GEAR = 'omniverse://localhost/Projects/GearGenerator/Assets/Gears/Spur/gear_01.usd'
    TABLE = 'omniverse://localhost/Projects/GearGenerator/Assets/Surfaces/KIRoPro_Arbeitstisch.usd'
    ENVS = 'omniverse://localhost/NVIDIA/Assets/Scenes/Templates/Interior/ZetCG_ExhibitionHall.usd'

    # Define camera
    camera = rep.create.camera(position=(0, 1200, 500), rotation=(-45, 0, 0))

    # Define randomizer function for gear
    def get_gears():
        gear = rep.create.from_usd(GEAR, count=3)
        with gear:
            rep.modify.semantics([('class', 'gear')])
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 760, -200), (200, 760, 200)),
                rotation=rep.distribution.uniform((0, -180, 0), (0, 180, 0)),
                scale=1.5
            )
        return gear

    # Register randomization
    rep.randomizer.register(get_gears)

    # Create environment and work table
    env = rep.create.from_usd(ENVS)
    surface = rep.create.from_usd(TABLE)
    with surface:
        rep.modify.pose(
            position = (0, 435, 0),
            rotation = (-90, 0, 0),
            scale = 1000
        )

    # Generate frames
    with rep.trigger.on_frame(num_frames=1000, rt_subframes=10):
        rep.randomizer.get_gears()
 
render_product = rep.create.render_product(camera, (640, 640))

# Initialize and attach writer
writer = rep.WriterRegistry.get("BasicWriter")
writer.initialize(
    output_dir="~/Documents/GearProject/gearproject/datasets/01_single",
    rgb=True,
    bounding_box_2d_tight=True
)

writer.attach([render_product])

# Simulate in Omniverse Code
rep.orchestrator.run()