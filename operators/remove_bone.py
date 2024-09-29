import bpy
from ..properties.gamerig import GAMERIG_PG_bone_retarget, GAMERIG_PG_game_rig


class GAMERIG_OT_remove_bone(bpy.types.Operator):
    bl_idname = "gamerig.remove_bone"
    bl_label = "Remove Bone"

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == "ARMATURE"

    def execute(self, context):
        if not (context.object and context.object.type == "ARMATURE"):
            self.report({"WARNING"}, "No active Armature")
            return {"CANCELLED"}

        gamerig: GAMERIG_PG_game_rig = context.object.data.gamerig
        if gamerig.active_bone >= 0 and gamerig.active_bone < len(gamerig.bones):
            gamerig.bones.remove(gamerig.active_bone)
            gamerig.active_bone = (
                gamerig.active_bone - 1 if gamerig.active_bone > 0 else 0
            )
            pass
        return {"FINISHED"}
