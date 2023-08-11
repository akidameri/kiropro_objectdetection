import omni.replicator.core as rep

with rep.new_layer():

    # Path for gears, work table, and the environment
    GEARS = 'omniverse://localhost/Projects/GearGenerator/Assets/Gears/'
    TABLE = 'omniverse://localhost/Projects/GearGenerator/Assets/Surfaces/KIRoPro_Arbeitstisch.usd'
    ENV = 'omniverse://localhost/NVIDIA/Assets/Scenes/Templates/Interior/ZetCG_ExhibitionHall.usd'

    # Prim path for default light
    DEF_LIGHT = '/Environment/defaultLight'

    # Define camera
    camera = rep.create.camera(position=(0, 1200, 500), rotation=(-45, 0, 0), focus_distance=725, f_stop=0.5)
    render_product = rep.create.render_product(camera, (640, 640))

    # Define gear materials
    mat_choices = ('omniverse://localhost/NVIDIA/Materials/2023_1/vMaterials_2/Metal/Stainless_Steel.mdl',
                   'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Metals/Steel_Carbon.mdl',
                   'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Plastics/Plastic_ABS.mdl'
                   )

    # Define randomizer function for gears
    def get_gears():
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(GEARS, recursive=True), size=rep.distribution.choice([2,3,4]), mode='scene_instance')
        with instances:
            rep.modify.semantics([("class", "gear")])
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 800, -200), (200, 900, 200)),
                rotation=rep.distribution.uniform((-180, -180, -180), (180, 180, 180)),
                scale=1.5
            )
            rep.randomizer.materials(mat_choices)
            rep.physics.rigid_body(
                velocity=rep.distribution.uniform((-0,0,-0),(0,0,0)),
                angular_velocity=rep.distribution.uniform((-0,0,-100),(0,0,0)))
        return instances.node
    
    # Register randomization
    rep.randomizer.register(get_gears)

    # Create environment and work table
    env = rep.create.from_usd(ENV)
    surface = rep.create.from_usd(TABLE)
    with surface:
        rep.modify.pose(
            position = (0, 435, 0),
            rotation = (-90, 0, 0),
            scale = 1000
        )
        rep.physics.collider()

    # Disable default lights
    default_light = rep.get.prims(path_pattern=DEF_LIGHT)
    with default_light:
        rep.modify.visibility(False)

    # Generate frames
    with rep.trigger.on_time(interval=2.5, num=800, rt_subframes=10): # num_frames to be changed
        rep.randomizer.get_gears()

    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(
        output_dir="~/Documents/GearProject/gearproject/datasets/p03.3_material",
        rgb=True,
        bounding_box_2d_tight=True
    )

    writer.attach([render_product])

    # Simulate in Omniverse Code
    rep.orchestrator.run()