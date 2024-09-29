import bpy
from ..properties.gamerig import (GAMERIG_PG_game_rig)

class GAMERIG_OT_gamerig_setup(bpy.types.Operator):
    bl_idname = "gamerig.setup"
    bl_label = "Setup GameRig"

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'ARMATURE')
    
    def execute(self, context):
        if not (context.object and context.object.type == "ARMATURE"):
            self.report({"WARNING"}, "No active Armature")
            return {"CANCELLED"}

        armature = context.object.data  # Accéder à l'armature liée à l'objet actif
        gamerig :GAMERIG_PG_game_rig= context.object.data.gamerig  # Accéder à l'armature liée à l'objet actif
        gamerig.active_collection = -1
        return {"FINISHED"}