import bpy
from .utils import (
    apply_bone_transform,
    constrain_bone,
    copy_bone,
    copy_target_bone_parent,
)
from ..properties.gamerig import GAMERIG_PG_game_rig


class GAMERIG_OT_update_target(bpy.types.Operator):
    bl_idname = "gamerig.update_target"
    bl_label = "Re-Generate Target"

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
        target_rig = gamerig.target_rig

        if not target_rig:
            self.report({"WARNING"}, "No Target Armature")
            return {"CANCELLED"}

        # Sauvegarder la sélection actuelle et le mode
        original_object = context.object
        original_mode = bpy.context.object.mode

        # Sélectionner et activer l'armature cible
        bpy.ops.object.mode_set(mode="OBJECT")
        target_rig.select_set(True)
        context.object.select_set(True)

        bpy.ops.object.mode_set(mode="EDIT")  # Basculer en mode EDIT

        try:
            target_edit_bones = target_rig.data.edit_bones
            for retarget in gamerig.bones:
                new_bone = None
                if (
                    retarget.override_bone
                    and retarget.override_bone in target_edit_bones
                ):
                    new_bone = target_edit_bones[retarget.override_bone]
                elif retarget.bone_target_name in target_edit_bones:
                    new_bone = target_edit_bones[retarget.bone_target_name]
                    pass
                else:
                    new_bone = copy_bone(
                        source_rig=source_rig,
                        target_rig=target_rig,
                        source_bone_name=retarget.name,
                        target_bone_name=retarget.bone_target_name,
                    )
                    pass
                new_bone.name = retarget.bone_target_name

                retarget.override_bone = new_bone.name
                retarget.bone_target_name = new_bone.name

                # appliquer les transforms
                apply_bone_transform(armature.edit_bones[retarget.name], new_bone)
                pass

            # reparenter les bones
            for retarget in gamerig.bones:
                copy_target_bone_parent(source_rig, target_rig, retarget, gamerig)
                pass

            # supprimer les bones inexistants
            for bone in target_edit_bones:
                keep = False
                for retarget in gamerig.bones:
                    if bone.name == retarget.bone_target_name:
                        keep = True
                        break
                    pass
                if not keep:
                    target_edit_bones.remove(bone)
                    pass
                pass

            # appliquer les contraintes
            bpy.ops.object.mode_set(mode="POSE")
            for retarget in gamerig.bones:
                if retarget.constraint == True:
                    bone = target_rig.pose.bones[retarget.bone_target_name]
                    for cnt in bone.constraints:
                        bone.constraints.remove(cnt)
                        pass
                    constrain_bone(
                        source_rig=source_rig,
                        target_rig=target_rig,
                        source_bone_name=retarget.name,
                        target_bone_name=retarget.bone_target_name,
                        target_space="POSE",
                    )
                    pass
                pass
        finally:
            bpy.ops.object.mode_set(mode="OBJECT")
            context.view_layer.objects.active = original_object
            target_rig.select_set(False)
            original_object.select_set(True)
            bpy.ops.object.mode_set(mode=original_mode)
            pass

        return {"FINISHED"}
