import bpy
from ..properties.gamerig import GAMERIG_PG_game_rig

class GAMERIG_OT_bone_list_context_menu(bpy.types.Operator):
    bl_idname = "gamerig.bone_list_context_menu"
    bl_label = "Add Bone"

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == "ARMATURE"

    def execute(self, context):
        if not (context.object and context.object.type == "ARMATURE"):
            self.report({"WARNING"}, "No active Armature")
            return {"CANCELLED"}
        return {"FINISHED"}
