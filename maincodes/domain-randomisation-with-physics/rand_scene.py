import omni.replicator.core as rep

with rep.new_layer():

    # Path for gears, work table, and the environment
    GEARS = 'omniverse://localhost/Projects/GearGenerator/Assets/Gears/'
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
    
    # Material choices for plane
    plane_mats = ['omniverse://localhost/NVIDIA/Materials/2023_1/Base/Carpet/Carpet_Berber_Gray.mdl',
                  'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Miscellaneous/Paint_Matte.mdl',
                  'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Stone/Gravel.mdl',
                  'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Metals/Steel_Stainless.mdl',
                  'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Wood/Ash_Planks.mdl']

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
    
    # Adding dome lights from varying environments
    def rand_dome_lights():
        d_lights = rep.create.light(
            light_type="Dome",
            rotation=(270,0,0),
            texture=rep.distribution.choice([
                'omniverse://localhost/NVIDIA/Assets/Skies/Clear/venice_sunset_4k.hdr',
                'omniverse://localhost/NVIDIA/Assets/Skies/Cloudy/lakeside_4k.hdr',
                'omniverse://localhost/NVIDIA/Assets/Skies/Clear/noon_grass_4k.hdr',
                'omniverse://localhost/NVIDIA/Assets/Skies/Indoor/hospital_room_4k.hdr',
                'omniverse://localhost/NVIDIA/Assets/Skies/Indoor/adams_place_bridge_4k.hdr',
                'omniverse://localhost/NVIDIA/Assets/Skies/Indoor/ZetoCGcom_ExhibitionHall_Interior1.hdr'                
            ]),
            intensity=rep.distribution.uniform(100, 1000),
            temperature=rep.distribution.uniform(1000, 10000)
        )
        return d_lights.node
    
    # Create plane and randomise its texture
    def rand_plane_texture():
        # Create plane
        plane = rep.create.plane(position=(0,760,0), scale=8)
        with plane:
            rep.randomizer.materials(plane_mats)
            rep.physics.collider()
        return plane.node

    # Register randomization
    rep.randomizer.register(get_gears)
    rep.randomizer.register(env_props)
    rep.randomizer.register(rand_dome_lights)
    rep.randomizer.register(rand_plane_texture)

    # Disable default lights
    default_light = rep.get.prims(path_pattern=DEF_LIGHT)
    with default_light:
        rep.modify.visibility(False)

    # Generate frames
    with rep.trigger.on_time(interval=2.5, num=200, rt_subframes=10): # num_frames to be changed
        rep.randomizer.get_gears()
        rep.randomizer.env_props()
        rep.randomizer.rand_dome_lights()
        rep.randomizer.rand_plane_texture()
        with camera:
            rep.modify.pose(position=rep.distribution.choice(camera_positions), look_at=(0,760,0))

    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(
        output_dir="~/Documents/GearProject/gearproject/datasets/p11.3_scene",
        rgb=True,
        bounding_box_2d_tight=True
    )

    writer.attach([render_product])

    # Simulate in Omniverse Code
    rep.orchestrator.run()
