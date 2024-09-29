import bpy

from ..properties.gamerig import GAMERIG_PG_bone_retarget, GAMERIG_PG_game_rig


def create_retarget_settings(
    context,
    rig_object: bpy.types.Object,
    bone_name: str,
):

    gamerig: GAMERIG_PG_game_rig = rig_object.data.gamerig
    bone = rig_object.data.bones[bone_name]

    new_retarget: GAMERIG_PG_bone_retarget = gamerig.bones.add()
    new_retarget.name = bone.name
    new_retarget.bone_name = bone.name
    new_retarget.bone_target_name = bone.name
    if gamerig.target_rig:
        match_bone = gamerig.target_rig.data.bones[bone.name]
        if match_bone:
            new_retarget.override_bone = match_bone.name
            pass
        pass
    return new_retarget


def create_root_bone(
    rig_object: bpy.types.Object,
    root_bone_name: str = "Root",
    reparent: bool = False,
):
    """
    Crée un root bone pour une armature spécifiée.
    """
    # Sauvegarder la sélection actuelle et le mode
    original_object = bpy.context.object
    original_mode = bpy.context.object.mode
    bpy.context.view_layer.objects.active = rig_object
    bpy.ops.object.mode_set(mode="EDIT")

    # Créer le root bone
    edit_bones = rig_object.data.edit_bones
    root_bone = edit_bones.new(root_bone_name)
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 1, 0)

    # Ajuster la hiérarchie si nécessaire
    if reparent:
        for bone in edit_bones:
            if bone.parent is None and bone != root_bone:
                bone.parent = root_bone
        pass

    bpy.ops.object.mode_set(mode="OBJECT")

    # Vérifier que l'os a bien été créé
    if root_bone_name not in rig_object.data.bones:
        raise KeyError(
            f"Le root bone '{root_bone_name}' n'a pas été créé correctement."
        )

    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.context.view_layer.objects.active = original_object
    original_object.select_set(True)
    bpy.ops.object.mode_set(mode=original_mode)

    return root_bone


def copy_bone(
    source_rig: bpy.types.Object,
    target_rig: bpy.types.Object,
    source_bone_name: str,
    target_bone_name: str,
    use_deform: False = False,
):
    original_bone = source_rig.data.edit_bones[source_bone_name]

    new_bone = target_rig.data.edit_bones.new(target_bone_name)
    new_bone.head = original_bone.head
    new_bone.head_radius = original_bone.head_radius
    new_bone.tail = original_bone.tail
    new_bone.tail_radius = original_bone.tail_radius
    new_bone.roll = original_bone.roll

    if use_deform:
        new_bone.use_deform = True
        pass
    else:
        new_bone.use_deform = original_bone.use_deform
        pass
    new_bone.envelope_distance = original_bone.envelope_distance
    new_bone.envelope_weight = original_bone.envelope_weight
    
    return new_bone


def constrain_bone(
    source_rig: bpy.types.Object,
    target_rig: bpy.types.Object,
    source_bone_name: str,
    target_bone_name: str,
    target_space: str = "WORLD",
):
    bone = target_rig.pose.bones[target_bone_name]
    constraint = bone.constraints.new(type="COPY_TRANSFORMS")
    constraint.target = source_rig
    constraint.subtarget = source_bone_name
    constraint.target_space = target_space
    constraint.owner_space = target_space
    return constraint


def create_empty_rig(context, name):
    """
    Creates a new empty armature in the scene with the specified name.

    Parameters:
    - name: The name of the new armature (string).

    Returns:
    - armature: The newly created armature object.
    """

    # Créer une nouvelle armature et un objet armature
    armature_data = bpy.data.armatures.new(name)
    armature_object = bpy.data.objects.new(name, armature_data)
    context.view_layer.active_layer_collection.collection.objects.link(armature_object)
    return armature_object
