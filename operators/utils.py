import bpy

from ..properties.gamerig import GAMERIG_PG_bone_retarget, GAMERIG_PG_game_rig


def create_retarget_settings(
	context,
	rig_object: bpy.types.Object,
	bone_name: str,
):

	gamerig: GAMERIG_PG_game_rig = rig_object.data.gamerig
	bone = rig_object.data.bones[bone_name]

	new_retarget: GAMERIG_PG_bone_retarget = gamerig.bones.add()
	new_retarget.name = bone.name
	new_retarget.bone_name = bone.name
	new_retarget.bone_target_name = bone.name
	if gamerig.target_rig and bone.name in gamerig.target_rig.data.bones:
		match_bone = gamerig.target_rig.data.bones[bone.name]
		if match_bone:
			new_retarget.override_bone = match_bone.name
			pass
		pass
	return new_retarget


def create_root_bone(
	rig_object: bpy.types.Object,
	root_bone_name: str = "Root",
	reparent: bool = False,
):
	"""
	Crée un root bone pour une armature spécifiée.
	"""
	# Sauvegarder la sélection actuelle et le mode
	original_object = bpy.context.object
	original_mode = bpy.context.object.mode
	bpy.context.view_layer.objects.active = rig_object
	bpy.ops.object.mode_set(mode="EDIT")

	# Créer le root bone
	edit_bones = rig_object.data.edit_bones
	root_bone = edit_bones.new(root_bone_name)
	root_bone.head = (0, 0, 0)
	root_bone.tail = (0, 1, 0)

	# Ajuster la hiérarchie si nécessaire
	if reparent:
		for bone in edit_bones:
			if bone.parent is None and bone != root_bone:
				bone.parent = root_bone
		pass

	bpy.ops.object.mode_set(mode="OBJECT")

	# Vérifier que l'os a bien été créé
	if root_bone_name not in rig_object.data.bones:
		raise KeyError(
			f"Le root bone '{root_bone_name}' n'a pas été créé correctement."
		)

	bpy.ops.object.mode_set(mode="OBJECT")
	bpy.ops.context.view_layer.objects.active = original_object
	original_object.select_set(True)
	bpy.ops.object.mode_set(mode=original_mode)

	return root_bone


def apply_bone_transform(
	source_bone: bpy.types.PoseBone,
	target_bone: bpy.types.PoseBone,
	use_deform: False = False,
):
	target_bone.head = source_bone.head
	target_bone.head_radius = source_bone.head_radius
	target_bone.tail = source_bone.tail
	target_bone.tail_radius = source_bone.tail_radius
	target_bone.roll = source_bone.roll

	if use_deform:
		target_bone.use_deform = True
		pass
	else:
		target_bone.use_deform = source_bone.use_deform
		pass
	target_bone.envelope_distance = source_bone.envelope_distance
	target_bone.envelope_weight = source_bone.envelope_weight
	return target_bone


def copy_bone(
	source_rig: bpy.types.Object,
	target_rig: bpy.types.Object,
	source_bone_name: str,
	target_bone_name: str,
	use_deform: False = False,
):
	original_bone = source_rig.data.edit_bones[source_bone_name]
	new_bone = target_rig.data.edit_bones.new(target_bone_name)
	return apply_bone_transform(original_bone, new_bone, use_deform)


def constrain_bone(
	source_rig: bpy.types.Object,
	target_rig: bpy.types.Object,
	source_bone_name: str,
	target_bone_name: str,
	target_space: str = "WORLD",
):
	bone = target_rig.pose.bones[target_bone_name]
	constraint = bone.constraints.new(type="COPY_TRANSFORMS")
	constraint.target = source_rig
	constraint.subtarget = source_bone_name
	constraint.target_space = target_space
	constraint.owner_space = target_space
	return constraint


def copy_target_bone_parent(
	source_rig: bpy.types.Object,
	target_rig: bpy.types.Object,
	retarget: GAMERIG_PG_bone_retarget,
	gamerig:GAMERIG_PG_game_rig
):
	source_edit_bones = source_rig.data.edit_bones
	target_edit_bones = target_rig.data.edit_bones

	target_edit_bone = target_edit_bones[retarget.bone_target_name]
	source_edit_bone = source_edit_bones[retarget.name]
	if source_edit_bone.parent and source_edit_bone.parent.name in gamerig.bones:
		source_parent_name = gamerig.bones[source_edit_bone.parent.name].bone_target_name

		if source_parent_name in target_edit_bones:
			target_edit_bone.parent = target_edit_bones[source_parent_name]
			target_edit_bone.use_connect = source_edit_bone.use_connect
			target_edit_bone.use_local_location = source_edit_bone.use_local_location
			target_edit_bone.use_inherit_rotation = source_edit_bone.use_inherit_rotation
			target_edit_bone.inherit_scale = source_edit_bone.inherit_scale
			pass
		pass
	return


def create_empty_rig(context, name):
	"""
	Creates a new empty armature in the scene with the specified name.

	Parameters:
	- name: The name of the new armature (string).

	Returns:
	- armature: The newly created armature object.
	"""

	# Créer une nouvelle armature et un objet armature
	armature_data = bpy.data.armatures.new(name)
	armature_object = bpy.data.objects.new(name, armature_data)
	context.view_layer.active_layer_collection.collection.objects.link(armature_object)
	return armature_object


def has_root_bone(armature, bone_name: str) -> bool:
	# Vérifier que l'objet fourni est bien une armature
	if armature.type != "ARMATURE":
		print(f"L'objet fourni n'est pas une armature.")
		return False

	# Récupérer le bone dans l'armature
	bone = armature.data.bones.get(bone_name)

	if not bone:
		return False

	if bone.parent is None:
		return True
	return False


def get_armature_selection() -> list:
	"""Retourne la liste des armatures sélectionnées dans la scène."""
	return [obj for obj in bpy.context.selected_objects if obj.type == "ARMATURE"]


def get_actions_for_armature(rig_object: bpy.types.Object) -> list:
	"""Retourne la liste des actions liées à une armature."""
	if rig_object.type != "ARMATURE":
		return []

	linked_actions = []
	for action in bpy.data.actions:
		if any(fcurve.data_path.startswith("pose.bones") for fcurve in action.fcurves):
			linked_actions.append(action)
	return linked_actions


def reset_armature_pose(rig_object):
	for bone in rig_object.pose.bones:
		bone.location = (0, 0, 0)
		bone.rotation_quaternion = (1, 0, 0, 0)
		bone.rotation_euler = (0, 0, 0)
		bone.scale = (1, 1, 1)
