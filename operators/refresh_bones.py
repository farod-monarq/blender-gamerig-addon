import bpy
from ..properties.gamerig import GAMERIG_PG_game_rig


class GAMERIG_OT_refresh_bones(bpy.types.Operator):
    bl_idname = "gamerig.refresh_bones"
    bl_label = "Refresh Bones"

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == "ARMATURE"

    def execute(self, context):
        if not (context.object and context.object.type == "ARMATURE"):
            self.report({"WARNING"}, "No active Armature")
            return {"CANCELLED"}

        armature = context.object.data  # Accéder à l'armature liée à l'objet actif
        gamerig: GAMERIG_PG_game_rig = context.object.data.gamerig
        gamerig.bones.clear()

        collection = armature.collections[gamerig.active_collection]

        for bone in collection.bones:
            retarget = gamerig.bones.add()
            retarget.bone_name = bone.name
            retarget.bone_target_name = bone.name
            pass

        return {"FINISHED"}
