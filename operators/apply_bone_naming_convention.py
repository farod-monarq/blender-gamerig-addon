import bpy

class GAMERIG_OT_apply_bone_naming_convention(bpy.types.Operator):
    bl_idname = "gamerig.apply_bone_naming_convention"
    bl_label = "Template Rename"

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == "ARMATURE"

    def execute(self, context):
        if not (context.object and context.object.type == "ARMATURE"):
            self.report({"WARNING"}, "No active Armature")
            return {"CANCELLED"}
        return {"FINISHED"}
