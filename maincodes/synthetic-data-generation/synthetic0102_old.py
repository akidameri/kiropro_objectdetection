import omni.replicator.core as rep

with rep.new_layer():

    # Path for gears and noise objects
    HOR_GEARS = 'omniverse://localhost/Projects/GearGenerator/Gears/Horizontal'
    VER_GEARS = 'omniverse://localhost/Projects/GearGenerator/Gears/Vertical'
    TABLE = 'omniverse://localhost/Projects/GearGenerator/Assets/Surfaces/KIRoPro_Arbeitstisch.usd'
    PROPS = 'omniverse://localhost/NVIDIA/Assets/Isaac/2022.1/Isaac/Props/YCB/Axis_Aligned_Physics'
    ENVS = 'omniverse://localhost/NVIDIA/Assets/Scenes/Templates/Interior/ZetCG_ExhibitionHall.usd'

    # Prim path for light sources
    LIGHT_PRIM_PATH_0 = '/Environment/defaultLight'
    LIGHT_PRIM_PATH_1 = '/Replicator/Ref_Xform/Ref/sky'
    
    # OmniPBR materials used for the gears. More info: https://docs.omniverse.nvidia.com/prod_materials-and-rendering/prod_materials-and-rendering/materials.html
    mats = rep.create.material_omnipbr(diffuse=rep.distribution.uniform((0,0,0),(0.005,0.005,0.005)),
                                       roughness_texture='omniverse://localhost/NVIDIA/Materials/Base/Plastics/Plastic_ABS.mdl',
                                       metallic_texture='omniverse://localhost/NVIDIA/Materials/Base/Plastics/Plastic_ABS.mdl',
                                       emissive_texture='omniverse://localhost/NVIDIA/Materials/Base/Plastics/Plastic_ABS.mdl',
                                       count=20
                                       )

    # Define camera
    camera_positions = [(0,1300,500), (0,860,730), (0,1500,0), (475,1060,475), (245,1410,245), (-100,960,701), (-200,1160,585), (-382,1260,-382), (0,1360,-426), (300,910,-655)]
    camera = rep.create.camera(focal_length=26.0, f_stop=1.6)
    render_product = rep.create.render_product(camera, (640, 640))

    # Define horizontal gears
    def get_hor_gears():
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(HOR_GEARS, recursive=True), size=2, mode='scene_instance')
        with instances:
            rep.modify.semantics([("class", "gear")])
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 760, -200), (200, 760, 200)),
                rotation=(0,0,0),
                scale=1.5
            )
            rep.randomizer.materials(mats)
        return instances.node
    
    # Define vertical gears
    def get_ver_gears():
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(VER_GEARS, recursive=True), size=1, mode='scene_instance')
        with instances:
            rep.modify.semantics([("class", "gear")])
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 760, -200), (200, 760, 200)),
                rotation=rep.distribution.uniform((0, -180, 0), (0, 180, 0)),
                scale=1.5
            )
            rep.randomizer.materials(mats)
        return instances.node
    
    # Add noise objects
    def env_props():
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(PROPS), size=3, mode='scene_instance')
        with instances:
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 775, -200), (200, 775, 200)),
                #rotation=rep.distribution.uniform((-180,90,90),(180,90,90)),
                rotation=rep.distribution.choice([(180, -90, 90), (0, 90, 90), (90, 0, 0), (-90, 0, 0)]),
                scale=500
            )
        return instances.node

    # Randomize visibility of dome light
    def hide_dome_light():
        dome_light = rep.get.prims(path_pattern=LIGHT_PRIM_PATH_1)
        with dome_light:
            rep.modify.visibility(rep.distribution.choice([True,False]))
        return dome_light.node
        
    # Add warm light
    light = rep.create.light(light_type="Sphere", intensity=30000, temperature=3000, position=(0, 1600, 0), scale=50)

    # Disable default light
    default_light = rep.get.prims(path_pattern=LIGHT_PRIM_PATH_0)
    with default_light:
        rep.modify.visibility(False)
    
    # Create environment and work table
    env = rep.create.from_usd(ENVS)
    surface = rep.create.from_usd(TABLE)
    with surface:
        rep.modify.pose(
            position = (0, 435, 0),
            rotation = (-90, 0, 0),
            scale = 1000
        )

    # Register randomization
    rep.randomizer.register(get_hor_gears)
    rep.randomizer.register(get_ver_gears)
    rep.randomizer.register(env_props)
    rep.randomizer.register(hide_dome_light)

    # Generate frames
    with rep.trigger.on_frame(num_frames=10, rt_subframes=10): # num_frames to be changed
        rep.randomizer.get_hor_gears()
        rep.randomizer.get_ver_gears()
        rep.randomizer.env_props()
        rep.randomizer.hide_dome_light()
        with camera:
            rep.modify.pose(position=rep.distribution.choice(camera_positions), look_at=(0,760,0))
 
    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(
        output_dir="~/Documents/GearProject/gearproject/datasets/synthetic",
        rgb=True,
        bounding_box_2d_tight=True
    )

    writer.attach([render_product])

    # Simulate in Omniverse Code
    rep.orchestrator.run()