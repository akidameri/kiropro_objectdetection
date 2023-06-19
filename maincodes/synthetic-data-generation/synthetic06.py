import omni.replicator.core as rep

with rep.new_layer():

    # Path for gears and noise objects
    GEARS = 'omniverse://localhost/Projects/GearGenerator/Assets/Gears'

    # Prim path for light sources and the surface
    DEF_LIGHT = '/Environment/defaultLight'
    
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
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(GEARS, recursive=True), size=3, mode='scene_instance')
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

    # Disable default light
    def_light = rep.get.prims(path_pattern=DEF_LIGHT)
    with def_light:
        rep.modify.visibility(False)

    # Add dome light
    d_lights = rep.create.light(
        light_type="Dome",
        rotation=(270,0,0),
        texture='omniverse://localhost/NVIDIA/Assets/Skies/Clear/noon_grass_4k.hdr',
        intensity=600
    )

    # Create plane
    plane = rep.create.plane(position=(0,10,0), scale=10)
    with plane:
        rep.physics.collider()
        rep.randomizer.texture(textures=['omniverse://localhost/NVIDIA/Assets/Isaac/2022.1/Isaac/Materials/Textures/Patterns/nv_stone_granite_mixed_grey.jpg'])

    # Register randomization
    rep.randomizer.register(get_gears)

    # Generate frames
    with rep.trigger.on_time(interval=2.5, num=100, rt_subframes=10): # num_frames to be changed
        rep.randomizer.get_gears()
        with camera:
            rep.modify.pose(position=rep.distribution.choice(camera_positions), look_at=(0,0,0))
 
    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(
        output_dir="~/Documents/GearProject/gearproject/datasets/synthetic06",
        rgb=True,
        bounding_box_2d_tight=True
    )

    writer.attach([render_product])

    # Simulate in Omniverse Code
    rep.orchestrator.run()