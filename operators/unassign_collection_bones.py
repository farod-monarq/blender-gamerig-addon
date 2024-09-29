import bpy
from ..properties.gamerig import GAMERIG_PG_game_rig


class GAMERIG_OT_unassign_collection_bones(bpy.types.Operator):
    bl_idname = "gamerig.unassign_collection_bones"
    bl_label = "Assign"

    action: bpy.props.EnumProperty(
        name="Action",
        description="Choose an action",
        items=[
            ("OPT_ASSIGN", "Assign", "Assign bones to Target"),
            ("OPT_REMOVE", "Remove", "Remove bones from Target"),
        ],
    )

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == "ARMATURE"

    def execute(self, context):

        if not (context.object and context.object.type == "ARMATURE"):
            self.report({"WARNING"}, "No active Armature")
            return {"CANCELLED"}
        return self._remove_collection(context)

    def _remove_collection(self, context):
        armature = context.object.data  # Accéder à l'armature liée à l'objet actif
        gamerig: GAMERIG_PG_game_rig = context.object.data.gamerig
        names = gamerig.bones.keys()
        for bone in armature.collections[gamerig.active_collection].bones:
            if bone.name in names:
                gamerig.bones.remove(gamerig.bones.find(bone.name))
                pass
            pass
        gamerig.active_bone = -1
        return {"FINISHED"}
