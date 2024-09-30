import bpy
from ..properties.gamerig import GAMERIG_PG_bone_retarget, GAMERIG_PG_game_rig

class GAMERIG_OT_add_bone_target(bpy.types.Operator):
    bl_idname = "gamerig.add_bone_target"
    bl_label = "Add Bone"

    bone_name: bpy.props.StringProperty(name="Bone")

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == "ARMATURE"

    def execute(self, context):
        if not (context.object and context.object.type == "ARMATURE"):
            self.report({"WARNING"}, "No active Armature")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Input Value: {self.bone_name}")

        gamerig: GAMERIG_PG_game_rig = context.object.data.gamerig

        if self.bone_name in gamerig.bones:
            self.report({"WARNING"}, f"Bone already exists: {self.bone_name}")
            return {"CANCELLED"}

        new_retarget: GAMERIG_PG_bone_retarget = gamerig.bones.add()
        new_retarget.name = self.bone_name
        new_retarget.bone_name = self.bone_name
        new_retarget.bone_target_name = self.bone_name
        new_retarget.constraint = True

        self.bone_name = ""
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        # Utilisation de prop_search pour rechercher un objet dans la scène
        layout.prop_search(self, "bone_name", context.object.data, "bones", text="Bone")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
