import bpy
from .utils import constrain_bone, copy_bone, create_empty_rig
from ..properties.gamerig import GAMERIG_PG_game_rig


class GAMERIG_OT_create_target(bpy.types.Operator):
    bl_idname = "gamerig.create_target"
    bl_label = "Create Target"

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == "ARMATURE"

    def execute(self, context):
        if not (context.object and context.object.type == "ARMATURE"):
            self.report({"WARNING"}, "No active Armature")
            return {"CANCELLED"}

        source_rig = context.object
        armature = context.object.data
        gamerig: GAMERIG_PG_game_rig = armature.gamerig

        target_rig = create_empty_rig(
            context=context, name=f"{context.object.name}_target"
        )
        target_rig.data.gamerig_owner = source_rig
        # Sauvegarder la sélection actuelle et le mode
        original_object = context.object
        original_mode = bpy.context.object.mode

        # Sélectionner et activer l'armature cible
        bpy.ops.object.mode_set(mode="OBJECT")
        target_rig.select_set(True)
        context.object.select_set(True)

        bpy.ops.object.mode_set(mode="EDIT")  # Basculer en mode EDIT
        gamerig.target_rig = target_rig
        try:
            target_edit_bones = target_rig.data.edit_bones
            # créer les bones
            for retarget in gamerig.bones:
                new_bone = copy_bone(
                    source_rig=source_rig,
                    target_rig=target_rig,
                    source_bone_name=retarget.name,
                    target_bone_name=retarget.bone_target_name,
                )
                retarget.override_bone = new_bone.name
                pass

            # reparenter les bones
            for retarget in gamerig.bones:
                new_bone = target_edit_bones[retarget.bone_target_name]
                original_bone = armature.edit_bones[retarget.name]
                if original_bone.parent and original_bone.parent.name in gamerig.bones:
                    bone_parent_name = gamerig.bones[
                        original_bone.parent.name
                    ].bone_target_name
                    if bone_parent_name in target_edit_bones:
                        new_bone.parent = target_edit_bones[bone_parent_name]
                        new_bone.use_connect = original_bone.use_connect
                        new_bone.use_local_location = original_bone.use_local_location
                        new_bone.use_inherit_rotation = (
                            original_bone.use_inherit_rotation
                        )
                        new_bone.inherit_scale = original_bone.inherit_scale
                        pass
                    pass
                pass

            # ajouter les contraintes
            bpy.ops.object.mode_set(mode="POSE")
            for retarget in gamerig.bones:
                if retarget.constraint == True:
                    constraint = constrain_bone(
                        source_rig=source_rig,
                        target_rig=target_rig,
                        source_bone_name=retarget.name,
                        target_bone_name=retarget.bone_target_name,
                        target_space="POSE",
                    )
                    pass
        finally:
            bpy.ops.object.mode_set(mode="OBJECT")
            context.view_layer.objects.active = original_object
            target_rig.select_set(False)
            original_object.select_set(True)
            bpy.ops.object.mode_set(mode=original_mode)
            pass

        return {"FINISHED"}
