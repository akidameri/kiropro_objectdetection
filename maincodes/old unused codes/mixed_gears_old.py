import omni.replicator.core as rep

with rep.new_layer():

    # Path for gears, work table, and the environment
    GEARS = 'omniverse://localhost/Projects/GearGenerator/Assets/Gears'
    TABLE = 'omniverse://localhost/Projects/GearGenerator/Assets/Surfaces/KIRoPro_Arbeitstisch.usd'
    ENVS = 'omniverse://localhost/NVIDIA/Assets/Scenes/Templates/Interior/ZetCG_ExhibitionHall.usd'

    # Define camera
    camera = rep.create.camera(position=(0, 1200, 500), rotation=(-45, 0, 0))
    render_product = rep.create.render_product(camera, (640, 640))

    # Define randomizer function for gears
    def get_gears(size=3):
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(GEARS, recursive=True), size=size, mode='scene_instance')
        with instances:
            rep.modify.semantics([("class", "gear")])
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 760, -200), (200, 760, 200)),
                rotation=rep.distribution.uniform((0, -180, 0), (0, 180, 0)),
                scale=1.5
            )
        return instances.node

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
 
    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(
        output_dir="~/Documents/GearProject/gearproject/datasets/03_mixed",
        rgb=True,
        bounding_box_2d_tight=True
    )

    writer.attach([render_product])

    # Simulate in Omniverse Code
    rep.orchestrator.run()