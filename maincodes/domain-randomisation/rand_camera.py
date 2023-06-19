import omni.replicator.core as rep

with rep.new_layer():

    # Path for gears, work table, environment, and noise objects
    GEARS = 'omniverse://localhost/Projects/GearGenerator/Assets/Gears'
    TABLE = 'omniverse://localhost/Projects/GearGenerator/Assets/Surfaces/KIRoPro_Arbeitstisch.usd'
    ENVS = 'omniverse://localhost/NVIDIA/Assets/Scenes/Templates/Interior/ZetCG_ExhibitionHall.usd'
    PROPS = 'omniverse://localhost/NVIDIA/Assets/Isaac/2022.1/Isaac/Props/YCB/Axis_Aligned'

    # Prim path for light sources
    LIGHT_PRIM_PATH_0 = '/Environment/defaultLight'
    LIGHT_PRIM_PATH_1 = '/Replicator/Ref_Xform/Ref/sky'
    
    # OmniPBR materials used for the gears. More info: https://docs.omniverse.nvidia.com/prod_materials-and-rendering/prod_materials-and-rendering/materials.html
    mats = rep.create.material_omnipbr(diffuse=rep.distribution.uniform((0,0,0), (1,1,1)),
                                       metallic=rep.distribution.choice([0, 0.5, 0.75, 1]),
                                       count=50
                                       )

    # Define camera
    camera_positions = [(0,1300,500), (0,860,730), (0,1500,0), (475,1060,475), (245,1410,245), (-100,960,701), (-200,1160,585), (-382,1260,-382), (0,1360,-426), (300,910,-655)]
    camera = rep.create.camera(focus_distance=725, f_stop=0.5)
    render_product = rep.create.render_product(camera, (640, 640))

    # Define randomizer function for gears
    def get_gears(size=3):
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(GEARS, recursive=True), size=size, mode='scene_instance')
        with instances:
            rep.modify.semantics([("class", "gear")])
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 800, -200), (200, 900, 200)),
                rotation=rep.distribution.uniform((-180, -180, -180), (180, 180, 180)),
                scale=1.5
            )
            rep.randomizer.materials(mats)
        return instances.node
    
    # Adding and randomizing light source
    def sphere_lights():
        lights = rep.create.light(
            light_type="Sphere",
            color=rep.distribution.uniform((0, 0, 0), (255, 255, 255)),
            intensity=rep.distribution.uniform(1000, 35000),
            position=rep.distribution.uniform((-500, 800, -500), (500, 1600, 500)),
            scale=rep.distribution.uniform(50, 100)
        )
        return lights.node
    
    def env_props():
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(PROPS), size=5, mode='scene_instance')
        with instances:
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 800, -200), (200, 900, 200)),
                rotation=rep.distribution.uniform((-180, -180, -180), (180, 180, 180)),
                scale=500
            )
        return instances.node

    # Register randomization
    rep.randomizer.register(get_gears)
    rep.randomizer.register(sphere_lights)
    rep.randomizer.register(env_props)

    # Create environment and work table
    env = rep.create.from_usd(ENVS)
    surface = rep.create.from_usd(TABLE)
    with surface:
        rep.modify.pose(
            position = (0, 435, 0),
            rotation = (-90, 0, 0),
            scale = 1000
        )

    # Disable default and dome lights
    default_light = rep.get.prims(path_pattern=LIGHT_PRIM_PATH_0)
    with default_light:
        rep.modify.visibility(False)
    
    dome_light = rep.get.prims(path_pattern=LIGHT_PRIM_PATH_1)
    with dome_light:
        rep.modify.visibility(False)

    # Generate frames
    with rep.trigger.on_frame(num_frames=1000, rt_subframes=10):
        rep.randomizer.get_gears()
        rep.randomizer.sphere_lights()
        rep.randomizer.env_props()
        with camera:
            rep.modify.pose(position=rep.distribution.choice(camera_positions), look_at=(0,760,0))
 
    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(
        output_dir="~/Documents/GearProject/gearproject/datasets/08_rand_camera",
        rgb=True,
        bounding_box_2d_tight=True
    )

    writer.attach([render_product])

    # Simulate in Omniverse Code
    rep.orchestrator.run()