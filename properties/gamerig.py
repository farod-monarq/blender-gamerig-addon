import bpy


class GAMERIG_PG_bone_retarget(bpy.types.PropertyGroup):
    bone_name: bpy.props.StringProperty(name="Bone")
    bone_target_name: bpy.props.StringProperty(name="Bone Target")
    override_bone: bpy.props.StringProperty(name="Override Bone")
    constraint: bpy.props.BoolProperty(name="Use Constraint", default=True)
    use_bone: bpy.props.BoolProperty(name="Use Bone", default=True)
    use_deform: bpy.props.BoolProperty(name="Use Deform", default=True)


class GAMERIG_PG_game_rig(bpy.types.PropertyGroup):
    """Conteneur pour les items de la collection de l'armature"""

    target_rig: bpy.props.PointerProperty(
        name="Target Rig",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type
        == "ARMATURE",  # Limite la recherche aux objets de type 'ARMATURE'
    )

    bones: bpy.props.CollectionProperty(type=GAMERIG_PG_bone_retarget, name="Bones")
    remove_unused_bones: bpy.props.BoolProperty(name="Use Bone", default=True)
    add_root_bone: bpy.props.BoolProperty(name="Use Bone", default=True)
    root_bone_name: bpy.props.StringProperty(name="root")
    reparent_root: bpy.props.BoolProperty(name="Use Bone", default=False)
    active_bone: bpy.props.IntProperty(name="Active bone index", default=-1)
    active_collection: bpy.props.IntProperty(name="Active collection Index", default=-1)


def register():
    bpy.types.Armature.gamerig = bpy.props.PointerProperty(type=GAMERIG_PG_game_rig)
    bpy.types.Armature.gamerig_owner = bpy.props.PointerProperty(
        name="Game Rig owner",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type
        == "ARMATURE",  # Limite la recherche aux objets de type 'ARMATURE'
    )
    pass


def unregister():
    del bpy.types.Armature.gamerig
    del bpy.types.Armature.gamerig_owner
    pass
