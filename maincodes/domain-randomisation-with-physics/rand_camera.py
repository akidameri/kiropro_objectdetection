import omni.replicator.core as rep

with rep.new_layer():

    # Path for gears, work table, and the environment
    GEARS = 'omniverse://localhost/Projects/GearGenerator/Assets/Gears/'
    TABLE = 'omniverse://localhost/Projects/GearGenerator/Assets/Surfaces/KIRoPro_Arbeitstisch.usd'
    ENV = 'omniverse://localhost/NVIDIA/Assets/Scenes/Templates/Interior/ZetCG_ExhibitionHall.usd'
    PROPS = 'omniverse://localhost/NVIDIA/Assets/Isaac/2022.1/Isaac/Props/YCB/Axis_Aligned'

    # Prim path for default light
    DEF_LIGHT = '/Environment/defaultLight'

    # Define camera
    camera_positions = [(0,1300,500), (0,860,730), (0,1500,0), (475,1060,475), (245,1410,245), (-100,960,701), (-200,1160,585), (-382,1260,-382), (0,1360,-426), (300,910,-655)]
    camera = rep.create.camera(focus_distance=725, f_stop=0.5)
    render_product = rep.create.render_product(camera, (640, 640))

    # OmniPBR materials used for the gears. More info: https://docs.omniverse.nvidia.com/prod_materials-and-rendering/prod_materials-and-rendering/materials.html
    mats = rep.create.material_omnipbr(diffuse=rep.distribution.uniform((0,0,0),(0.005,0.005,0.005)),
                                       roughness_texture='omniverse://localhost/NVIDIA/Materials/Base/Plastics/Plastic_ABS.mdl',
                                       metallic_texture='omniverse://localhost/NVIDIA/Materials/Base/Plastics/Plastic_ABS.mdl',
                                       emissive_texture='omniverse://localhost/NVIDIA/Materials/Base/Plastics/Plastic_ABS.mdl',
                                       count=20
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
            rep.randomizer.materials(mats)
            rep.physics.rigid_body(
                velocity=rep.distribution.uniform((-0,0,-0),(0,0,0)),
                angular_velocity=rep.distribution.uniform((-0,0,-100),(0,0,0)))
        return instances.node
    
    # Add flying random objects as distractors
    def env_props():
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(PROPS), size=rep.distribution.choice([0,2,3,5,7]), mode='scene_instance')
        with instances:
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 800, -200), (200, 900, 200)),
                rotation=rep.distribution.uniform((-180, -180, -180), (180, 180, 180)),
                scale=500
            )
        return instances.node
    
    # Register randomization
    rep.randomizer.register(get_gears)
    rep.randomizer.register(env_props)

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
    with rep.trigger.on_time(interval=2.5, num=10, rt_subframes=10): # num_frames to be changed
        rep.randomizer.get_gears()
        rep.randomizer.env_props()
        with camera:
            rep.modify.pose(position=rep.distribution.choice(camera_positions), look_at=(0,760,0))

    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(
        output_dir="~/Documents/GearProject/gearproject/datasets/p07_camera",
        rgb=True,
        bounding_box_2d_tight=True
    )

    writer.attach([render_product])

    # Simulate in Omniverse Code
    rep.orchestrator.run()