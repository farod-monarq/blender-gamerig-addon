from cgitb import text
import bpy
from ..properties.gamerig import GAMERIG_PG_game_rig


def register():
    return


def unregister():
    return


class GAMERIG_PT_source_rig_panel(bpy.types.Panel):
    bl_label = "Game Rig Source"
    bl_idname = __package__
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(cls, context):
        # Vérifier s'il y a un objet actif et s'il s'agit d'une armature
        obj = context.active_object
        if obj and obj.type == "ARMATURE":
            return True
        return False

    def _draw_retarget_list(
        self,
        context: bpy.types.Context,
        layout: bpy.types.UILayout,
        rig_object: GAMERIG_PG_game_rig,
    ):
        gamerig = rig_object.data.gamerig
        collection_header, collection_layout = layout.panel("gamerig.retargets")
        collection_header.label(text="Bones")
        if collection_layout:
            row_list = collection_layout.row()
            row_list.template_list(
                "GAMERIG_UL_bone_retarget_list",
                "",
                gamerig,
                "bones",
                gamerig,
                "active_bone",
            )
            col_list_action = row_list.column()
            col_list_action.operator("gamerig.add_bone_target", text="", icon="ADD")
            col_list_action.operator("gamerig.remove_bone", text="", icon="REMOVE")
            # col_list_action.operator(
            # 	"gamerig.", text="", icon="DOWNARROW_HLT"
            # )
            pass
        return

    def _draw_bone_collections(self, context, layout):
        collection_header, collection_layout = layout.panel("gamerig.collections")
        collection_header.label(text="Bone Collections")
        if collection_layout:
            collection_layout.template_list(
                "GAMERIG_UL_bone_collection_list",
                "",
                context.object.data,
                "collections",
                context.object.data.gamerig,
                "active_collection",
            )
            row = collection_layout.row()
            row.operator("gamerig.assign_collection_bones", text="Assign")
            row.operator("gamerig.unassign_collection_bones", text="Remove")
            pass
        return

    def draw(self, context):

        if not (context.object or context.object.type == "ARMATURE"):
            return

        if context.object.data.gamerig_owner:
            return

        layout = self.layout
        armature = context.object.data

        gamerig: GAMERIG_PG_game_rig = context.object.data.gamerig

        self._draw_bone_collections(context, layout)
        self._draw_retarget_list(
            context=context, layout=layout, rig_object=context.object
        )
        row = layout.row()

        if gamerig.target_rig:
            row.operator("gamerig.update_target", icon="ARMATURE_DATA")
            pass
        else:
            row.operator("gamerig.create_target", icon="ARMATURE_DATA")
            pass

        row.operator("gamerig.remove_bones_prefix", text="", icon="TEXT")

        layout.prop_search(
            gamerig, "target_rig", bpy.data, "objects", text="", icon="CON_ARMATURE"
        )
        return


class GAMERIG_UL_bone_retarget_list(bpy.types.UIList):
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if not (context.object and context.object.type == "ARMATURE"):
            return

        armature = context.object.data
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row()

            row.label(
                text="",
                icon="BONE_DATA" if item.name in armature.bones else "ERROR",
            )
            row.label(text=f"{item.name}", icon="NONE")
            row.label(text="", icon="TRIA_RIGHT")
            if active_data.target_rig:
                row.prop_search(
                    item, "override_bone", active_data.target_rig.data, "bones", text=""
                )
            else:
                row.label(text=f"{item.bone_target_name}", icon="LINKED")
                pass
            row.label(text="", icon="TAG")
            row.prop(item, "bone_target_name", text="")
            row.prop(
                item,
                "use_deform",
                icon="MOD_VERTEX_WEIGHT" if item.use_deform else "RADIOBUT_OFF",
                emboss=False,
                text="",
            )
            row.prop(
                item,
                "constraint",
                icon="CONSTRAINT_BONE" if item.constraint else "RADIOBUT_OFF",
                emboss=False,
                text="",
            )

            pass
        elif self.layout_type == "GRID":
            row.alignment = "CENTER"
            row.label(text="", icon="BONE_DATA")
            pass
        return


class GAMERIG_UL_bone_collection_list(bpy.types.UIList):

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):

        if not (context.object and context.object.type == "ARMATURE"):
            return

        armature = context.object.data

        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row()
            bone_count = len(item.bones.keys())
            row.label(text=item.name, icon="GROUP_BONE")
            if bone_count <= 0:
                sub_row = row.row()
                sub_row.label(text="Empty", icon="PANEL_CLOSE")
                pass
            else:
                row.prop(item, "bones", icon="BONE_DATA")
                pass
        elif self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text="", icon="GROUP_BONE")
            layout.prop(item, "is_active", text="")
