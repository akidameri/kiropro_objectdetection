import omni.replicator.core as rep

with rep.new_layer():

    # Path for gears, work table, and the environment
    HOR_GEARS = 'omniverse://localhost/Projects/GearGenerator/Gears/Horizontal'
    VER_GEARS = 'omniverse://localhost/Projects/GearGenerator/Gears/Vertical'
    TABLE = 'omniverse://localhost/Projects/GearGenerator/Assets/Surfaces/KIRoPro_Arbeitstisch.usd'
    ENVS = 'omniverse://localhost/NVIDIA/Assets/Scenes/Templates/Interior/ZetCG_ExhibitionHall.usd'

    # Define camera
    camera = rep.create.camera(position=(0, 1200, 500), rotation=(-45, 0, 0))
    render_product = rep.create.render_product(camera, (640, 640))

    # OmniPBR materials used for the gears. More info: https://docs.omniverse.nvidia.com/prod_materials-and-rendering/prod_materials-and-rendering/materials.html
    mats = rep.create.material_omnipbr(diffuse=rep.distribution.uniform((0,0,0),(0.005,0.005,0.005)),
                                       roughness_texture='omniverse://localhost/NVIDIA/Materials/Base/Plastics/Plastic_ABS.mdl',
                                       metallic_texture='omniverse://localhost/NVIDIA/Materials/Base/Plastics/Plastic_ABS.mdl',
                                       emissive_texture='omniverse://localhost/NVIDIA/Materials/Base/Plastics/Plastic_ABS.mdl',
                                       count=20
                                       )

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
    
    # Register randomization
    rep.randomizer.register(get_hor_gears)
    rep.randomizer.register(get_ver_gears)

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
        rep.randomizer.get_hor_gears()
        rep.randomizer.get_ver_gears()
 
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