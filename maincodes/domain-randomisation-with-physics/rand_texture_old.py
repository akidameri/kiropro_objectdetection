import omni.replicator.core as rep

with rep.new_layer():

    # Path for gears, work table, and the environment
    HOR_GEARS = 'omniverse://localhost/Projects/GearGenerator/Gears/Horizontal'
    VER_GEARS = 'omniverse://localhost/Projects/GearGenerator/Gears/Vertical'
    PROPS = 'omniverse://localhost/NVIDIA/Assets/Isaac/2022.1/Isaac/Props/YCB/Axis_Aligned'

    # Prim path for default light
    LIGHT_PRIM_PATH_0 = '/Environment/defaultLight'

    # Define camera
    camera_positions = [(0,1300,500), (0,860,730), (0,1500,0), (475,1060,475), (245,1410,245), (-100,960,701), (-200,1160,585), (-382,1260,-382), (0,1360,-426), (300,910,-655)]
    camera = rep.create.camera(focus_distance=725, f_stop=0.5)
    render_product = rep.create.render_product(camera, (640, 640))

    # Define gear materials
    mats = ('omniverse://localhost/NVIDIA/Materials/2023_1/Base/Metals/Iron.mdl',
            'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Plastics/Plastic_ABS.mdl',
            'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Metals/Aluminum_Anodized_Black.mdl',
            'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Plastics/Rubber_Textured.mdl',
            'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Textiles/Cloth_Black.mdl',
            'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Textiles/Leather_Black.mdl',
            'omniverse://localhost/NVIDIA/Materials/2023_1/vMaterials_2/Composite/Carbon_Fiber.mdl'
            )
  
    # Material choices for plane
    plane_mats = ['omniverse://localhost/NVIDIA/Materials/2023_1/Base/Carpet/Carpet_Berber_Gray.mdl',
                  'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Miscellaneous/Paint_Matte.mdl',
                  'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Stone/Gravel.mdl',
                  'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Metals/Steel_Stainless.mdl',
                  'omniverse://localhost/NVIDIA/Materials/2023_1/Base/Wood/Ash_Planks.mdl']
    
    # Define randomizer function for horizontal gears
    def get_hor_gears():
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(HOR_GEARS, recursive=True), size=2, mode='scene_instance')
        with instances:
            rep.modify.semantics([("class", "gear")])
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 760, -200), (200, 760, 200)),
                rotation=rep.distribution.uniform((0, -180, 0), (0, 180, 0)),
                scale=1.5
            )
            rep.randomizer.materials(mats)
        return instances.node

    # Define randomizer function for vertical gears
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
    
    # Add flying random objects as obstacles
    def env_props():
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(PROPS), size=rep.distribution.choice([3,4,5,6,7]), mode='scene_instance')
        with instances:
            rep.modify.pose(
                position=rep.distribution.uniform((-200, 800, -200), (200, 900, 200)),
                rotation=rep.distribution.uniform((-180, -180, -180), (180, 180, 180)),
                scale=500
            )
        return instances.node
    
    # Adding dome lights from varying environments
    def env_dome_lights():
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
    
    def randomize_plane_texture():
        # Create plane
        plane = rep.create.plane(position=(0,760,0), scale=8)
        with plane:
            rep.randomizer.materials(plane_mats)
        return plane.node

    # Register randomization
    rep.randomizer.register(get_hor_gears)
    rep.randomizer.register(get_ver_gears)
    rep.randomizer.register(env_props)
    rep.randomizer.register(env_dome_lights)
    rep.randomizer.register(randomize_plane_texture)

    # Disable default lights
    default_light = rep.get.prims(path_pattern=LIGHT_PRIM_PATH_0)
    with default_light:
        rep.modify.visibility(False)

    # Generate frames
    with rep.trigger.on_frame(num_frames=800, rt_subframes=10):
        rep.randomizer.get_hor_gears()
        rep.randomizer.get_ver_gears()
        rep.randomizer.env_props()
        rep.randomizer.env_dome_lights()
        rep.randomizer.randomize_plane_texture()
        with camera:
            rep.modify.pose(position=rep.distribution.choice(camera_positions), look_at=(0,760,0))

    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(
        output_dir="~/Documents/GearProject/gearproject/datasets/08_texture",
        rgb=True,
        bounding_box_2d_tight=True
    )

    writer.attach([render_product])

    # Simulate in Omniverse Code
    rep.orchestrator.run()