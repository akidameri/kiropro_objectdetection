import omni.replicator.core as rep

with rep.new_layer():

    # Path for gears and noise objects
    GEARS = 'omniverse://localhost/Projects/GearGenerator/Assets/Gears'
    PROPS = 'omniverse://localhost/NVIDIA/Assets/Isaac/2022.1/Isaac/Props/Shapes/'
    ENVS = 'omniverse://localhost/NVIDIA/Assets/Scenes/Templates/LookDev/Decor_Concrete.usd'

    # Prim path for light sources and the surface
    DEF_LIGHT = '/Environment/defaultLight'
    DOME_LIGHT = '/Replicator/Ref_Xform/Ref/sky_old_bus_depot_4k'
    SURFACE = '/Replicator/Ref_Xform/Ref/Studio_backdrop/table'
    
    # OmniPBR materials used for the gears. More info: https://docs.omniverse.nvidia.com/prod_materials-and-rendering/prod_materials-and-rendering/materials.html
    mats = rep.create.material_omnipbr(diffuse=rep.distribution.uniform((0,0,0),(0.005,0.005,0.005)),
                                       roughness_texture='omniverse://localhost/NVIDIA/Materials/Base/Plastics/Plastic_ABS.mdl',
                                       metallic_texture='omniverse://localhost/NVIDIA/Materials/Base/Plastics/Plastic_ABS.mdl',
                                       emissive_texture='omniverse://localhost/NVIDIA/Materials/Base/Plastics/Plastic_ABS.mdl',
                                       count=20
                                       )

    # Define camera
    camera_positions = [(0,540,500), (0,100,730), (0,740,0), (475,300,475), (245,700,245), (-100,200,701), (-200,400,585), (-382,500,-382), (0,600,-426), (300,150,-655)]
    camera = rep.create.camera(focal_length=26.0, f_stop=1.6)
    render_product = rep.create.render_product(camera, (640, 640))

    # Define randomizer function to create gears
    def get_gears():
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(GEARS, recursive=True), size=rep.distribution.choice([2,3,4]), mode='scene_instance')
        with instances:
            rep.modify.semantics([("class", "gear")])
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 30, -200), (200, 130, 200)),
                rotation=rep.distribution.uniform((-180, -180, -180), (180, 180, 180)),
                scale=1.5)
            rep.randomizer.materials(mats)
            rep.physics.rigid_body(
                velocity=rep.distribution.uniform((-0,0,-0),(0,0,0)),
                angular_velocity=rep.distribution.uniform((-0,0,-100),(0,0,0)))
        return instances.node
    
    # Add noise objects
    def env_props():
        env_instances = rep.randomizer.instantiate(rep.utils.get_usd_files(PROPS), size=rep.distribution.choice([2,3,4]), mode='scene_instance')
        with env_instances:
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 30, -200), (200, 130, 200)),
                rotation=rep.distribution.uniform((-180, -180, -180), (180, 180, 180)),
                scale=100)
            rep.physics.rigid_body(
                velocity=rep.distribution.uniform((-0,0,-0),(0,0,0)),
                angular_velocity=rep.distribution.uniform((-0,0,-100),(0,0,0)))
        return env_instances.node

    # Randomize visibility of default light
    def hide_default_light():
        default_light = rep.get.prims(path_pattern=DEF_LIGHT)
        with default_light:
            rep.modify.visibility(rep.distribution.choice([True,False]))
        return default_light.node
        
    # Add warm light
    light = rep.create.light(light_type="Sphere", intensity=30000, temperature=3000, position=(0, 500, 500), scale=100)

    # Disable dome light
    dome_light = rep.get.prims(path_pattern=DOME_LIGHT)
    with dome_light:
        rep.modify.visibility(False)
    
    # Create environment
    env = rep.create.from_usd(ENVS)
    with env:
        rep.modify.pose(scale=10)
    surface = rep.get.prims(path_pattern=SURFACE)
    with surface:
        rep.physics.collider()

    # Register randomization
    rep.randomizer.register(get_gears)
    rep.randomizer.register(env_props)
    rep.randomizer.register(hide_default_light)

    # Generate frames
    with rep.trigger.on_time(interval=2.5, num=1000, rt_subframes=10): # num_frames to be changed
        rep.randomizer.get_gears()
        rep.randomizer.env_props()
        rep.randomizer.hide_default_light()
        with camera:
            rep.modify.pose(position=rep.distribution.choice(camera_positions), look_at=(0,0,0))
 
    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(
        output_dir="~/Documents/GearProject/gearproject/datasets/synthetic0304",
        rgb=True,
        bounding_box_2d_tight=True
    )

    writer.attach([render_product])

    # Simulate in Omniverse Code
    rep.orchestrator.run()