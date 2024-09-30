import re
import bpy
from ..properties.gamerig import GAMERIG_PG_game_rig


class GAMERIG_OT_remove_bones_prefix(bpy.types.Operator):
    bl_idname = "gamerig.remove_bones_prefix"
    bl_label = "Remove Bone"

    prefix_pattern: bpy.props.StringProperty(
        name="Prefix Pattern",
        description="Pattern to remove from the beginning of bone names",
        default="ORG-",
    )

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == "ARMATURE"

    def execute(self, context):
        if not (context.object and context.object.type == "ARMATURE"):
            self.report({"WARNING"}, "No active Armature")
            return {"CANCELLED"}

        # Accéder à l'armature active
        armature = context.object.data

        # Préparer le pattern pour la suppression du préfixe
        prefix = self.prefix_pattern
        pattern = re.compile(re.escape(prefix))

        # Compter le nombre d'os modifiés
        bones_renamed = 0
        # Itérer sur tous les os de l'armature et enlever le préfixe s'il est présent
        for bone in armature.gamerig.bones:
            if bone.bone_target_name.startswith(prefix):
                # Enlever le préfixe du nom
                new_name = pattern.sub("", bone.bone_target_name, count=1)
                bone.bone_target_name = new_name
                bones_renamed += 1
            pass

        # Rapport de réussite
        self.report({"INFO"}, f"Removed prefix from {bones_renamed} bones.")
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        # Utilisation de prop_search pour rechercher un objet dans la scène
        layout.prop(self, "prefix_pattern", text="Prefix")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)