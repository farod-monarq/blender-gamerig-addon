import bpy
from .utils import create_retarget_settings
from ..properties.gamerig import GAMERIG_PG_bone_retarget, GAMERIG_PG_game_rig

class GAMERIG_OT_assign_collection_bones(bpy.types.Operator):
    bl_idname = "gamerig.assign_collection_bones"
    bl_label = "Assign"

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == "ARMATURE"

    def execute(self, context):

        if not (context.object and context.object.type == "ARMATURE"):
            self.report({"WARNING"}, "No active Armature")
            return {"CANCELLED"}
        return self._assign_collection(context)


    def _assign_collection(self, context):
        armature = context.object.data  # Accéder à l'armature liée à l'objet actif
        gamerig: GAMERIG_PG_game_rig = context.object.data.gamerig
        collections = armature.collections.keys()
        bone_names = map(lambda v: (v.name), gamerig.bones)

        for bone in armature.collections[collections[gamerig.active_collection]].bones:
            if bone.name in bone_names:
                continue

            # create retarget settings
            new_retarget: GAMERIG_PG_bone_retarget = create_retarget_settings(
                context=context, rig_object=context.object, bone_name=bone.name
            )
            pass

        return {"FINISHED"}
