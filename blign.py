import math
import mathutils
from mathutils import Vector
import bpy
import numpy as np

bl_info = {
    "name": "Blign",
    "author": "Wilmer Lab Group",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D View Sidebar > Geometry tab",
    "description": "Align and distribute objects about an axis or between objects",
    "tracker_url": "",
    "category": "Geometry"
}

# ********** bounding box **********
# to get boundibng box use dimension.x instead of location.x


class Add_Object(bpy.types.Operator):
    """Class that defines the Add Object button."""
    bl_idname = "rigidbody.blign_add_object"
    bl_label = "Add Object"
    bl_description = "Set selected object as a blign object"

    def execute(self, context):
        """Sets the object as object.blign."""

        if len(context.selected_objects) == 1:
            for object in context.selected_objects:
                if not object.blign:
                    context.view_layer.objects.active = object
                    object.blign = True
        else:
            pass

        return {'FINISHED'}


class Remove_Object(bpy.types.Operator):
    """Class that defines the Remove Object button."""
    bl_idname = "rigidbody.blign_remove_object"
    bl_label = "Remove Object"
    bl_description = "Remove object from as a blign object"

    @classmethod
    def poll(cls, context):
        if context.object:
            return context.object.blign

    def execute(self, context):
        """Unsets object as object.blign."""
        for object in context.selected_objects:
            if object.blign:
                context.view_layer.objects.active = object
                context.object.blign = False

        return {'FINISHED'}


class Blign_Align_Button0(bpy.types.Operator):
    """Defines the Align button."""
    bl_idname = "rigidbody.blign_align_button0"
    bl_label = "Align"
    bl_description = "Align selected objects"

    def execute(self, context):
        """Iterates through all objects, counts number of blign objects.

        If number of blign objects = 0, aligns selected objects to the selected axis.
        """
        axis = bpy.context.scene.object_settings.Axis0
        oblist = bpy.context.selected_objects
        align = bpy.context.scene.object_settings.align_to0

        i = 0
        for object in list(bpy.data.objects):
            if object.blign == True:
                i += 1

        if align == 'center':
            if i == 0:
                if axis == 'x-axis':
                    for object in oblist:
                        object.location.y = 0
                        object.location.z = 0
                elif axis == 'y-axis':
                    for object in oblist:
                        object.location.x = 0
                        object.location.z = 0
                elif axis == 'z-axis':
                    for object in oblist:
                        object.location.x = 0
                        object.location.y = 0
            else:
                pass
        elif align == 'top':
            if i == 0:
                if axis == 'x-axis':
                    for object in oblist:
                        delta_h = object.dimensions.z / 2
                        object.location.y = 0
                        object.location.z = 0 - delta_h
                elif axis == 'y-axis':
                    for object in oblist:
                        delta_h = object.dimensions.z / 2
                        object.location.x = 0
                        object.location.z = 0 - delta_h
                elif axis == 'z-axis':
                    for object in oblist:
                        object.location.x = 0
                        object.location.y = 0
            else:
                pass
        elif align == 'bottom':
            if i == 0:
                if axis == 'x-axis':
                    for object in oblist:
                        delta_h = object.dimensions.z / 2
                        object.location.y = 0
                        object.location.z = 0 + delta_h
                elif axis == 'y-axis':
                    for object in oblist:
                        delta_h = object.dimensions.z / 2
                        object.location.x = 0
                        object.location.z = 0 + delta_h
                elif axis == 'z-axis':
                    for object in oblist:
                        object.location.x = 0
                        object.location.y = 0
            else:
                pass

        return {'FINISHED'}


class Blign_Align_Button1(bpy.types.Operator):
    """Defines the Align button."""
    bl_idname = "rigidbody.blign_align_button1"
    bl_label = "Align"
    bl_description = "Align selected objects"

    def execute(self, context):
        """Iterates through all objects, counts number of blign objects.

        If number of blign objects = 1, aligns selected objects to that one object.
        """
        axis = bpy.context.scene.object_settings.Axis1
        oblist = bpy.context.selected_objects
        align = bpy.context.scene.object_settings.align_to1

        i = 0
        for object in list(bpy.data.objects):
            if object.blign == True:
                i += 1

        if align == 'center':
            if i == 1:
                for object in list(bpy.data.objects):
                    if object.blign == True:
                        locx = object.location.x
                        locy = object.location.y
                        locz = object.location.z
                if axis == 'x-axis':
                    for object in oblist:
                        object.location.y = locy
                        object.location.z = locz
                if axis == 'y-axis':
                    for object in oblist:
                        object.location.x = locx
                        object.location.z = locz
                if axis == 'z-axis':
                    for object in oblist:
                        object.location.x = locx
                        object.location.y = locy
            else:
                pass
        elif align == 'top':
            if i == 1:
                for obj in list(bpy.data.objects):
                    if obj.blign == True:
                        vertices = np.array([obj.matrix_world @ Vector(c) for c in obj.bound_box])
                        top_blign = vertices[np.argsort(vertices[:, 2])[-1]]
                for obj in oblist:
                    vertices = np.array([obj.matrix_world @ Vector(c) for c in obj.bound_box])
                    top_obj = vertices[np.argsort(vertices[:, 2])[-1]]
                    delta = top_blign - top_obj
                    if axis == 'x-axis':
                        obj.location.y += delta[1]
                        obj.location.z += delta[2]
                    if axis == 'y-axis':
                        obj.location.x += delta[0]
                        obj.location.z += delta[2]
                    if axis == 'z-axis':
                        obj.location.x += delta[0]
                        obj.location.y += delta[1]
            else:
                pass
        elif align == 'bottom':
            if i == 1:
                for obj in list(bpy.data.objects):
                    if obj.blign == True:
                        vertices = np.array([obj.matrix_world @ Vector(c) for c in obj.bound_box])
                        top_blign = vertices[np.argsort(vertices[:, 2])[0]]
                for obj in oblist:
                    vertices = np.array([obj.matrix_world @ Vector(c) for c in obj.bound_box])
                    top_obj = vertices[np.argsort(vertices[:, 2])[0]]
                    delta = top_blign - top_obj
                    if axis == 'x-axis':
                        obj.location.y += delta[1]
                        obj.location.z += delta[2]
                    if axis == 'y-axis':
                        obj.location.x += delta[0]
                        obj.location.z += delta[2]
                    if axis == 'z-axis':
                        obj.location.x += delta[0]
                        obj.location.y += delta[1]
            else:
                pass

        return {'FINISHED'}


class Blign_Align_Button2(bpy.types.Operator):
    """Defines the Align button."""
    bl_idname = "rigidbody.blign_align_button2"
    bl_label = "Align"
    bl_description = "Align selected objects"

    def execute(self, context):
        """Iterates through all objects, counts number of blign objects.

        If number of blign objects = 2, aligns selected objects along the line between the 2 blign objects.
        """
        i = 0
        for object in list(bpy.data.objects):
            if object.blign == True:
                i += 1

        if i == 2:
            p1, p2 = [np.array(o.location)
                      for o in bpy.data.objects if o.blign]
            u = p2 - p1
            a = np.array([[(u ** 2).sum()]])

            for obj in context.selected_objects:
                p = np.array([obj.location.x, obj.location.y, obj.location.z])
                b = np.array([[(u * (p - p2)).sum()]])
                t = np.linalg.solve(a, b)
                v = u * t[0][0] + (p2 - p)
                obj.location.x += v[0]
                obj.location.y += v[1]
                obj.location.z += v[2]
        else:
            pass

        return {'FINISHED'}


class Blign_Distribute_Button0(bpy.types.Operator):
    """Defines the Distribute button."""
    bl_idname = "rigidbody.blign_distribute_button0"
    bl_label = "Distribute"
    bl_description = "Distribute objects"

    def execute(self, context):
        """Distributes objects between first and last object.

        Indicate = the indicate spacing button. If unchecked, evenly distributes shapes. 
        If checked, distributes objects 'spacing' units apart.
        """
        indicate = bpy.context.scene.object_settings.indicate_spacing0
        axis = bpy.context.scene.object_settings.Axis0
        oblist = bpy.context.selected_objects
        dist_type = bpy.context.scene.object_settings.distribute_ops0

        i = 0
        for object in list(bpy.data.objects):
            if object.blign == True:
                i += 1

        if dist_type == 'center':
            if i == 0:
                if len(oblist) > 1:
                    if not indicate:
                        pos_list = []
                        if axis == 'x-axis':
                            pos_list = [o.location.x for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list)
                            default_spacing = distance / (len(pos_list) - 1)
                            for i, idx in enumerate(obj_idx):
                                oblist[idx].location.x = oblist[obj_idx[0]].location.x + \
                                    default_spacing * i
                        elif axis == 'y-axis':
                            pos_list = [o.location.y for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list)
                            default_spacing = distance / (len(pos_list) - 1)
                            for i, idx in enumerate(obj_idx):
                                oblist[idx].location.y = oblist[obj_idx[0]].location.y + \
                                    default_spacing * i
                        elif axis == 'z-axis':
                            pos_list = [o.location.z for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list)
                            default_spacing = distance / (len(pos_list) - 1)
                            for i, idx in enumerate(obj_idx):
                                oblist[idx].location.z = oblist[obj_idx[0]].location.z + \
                                    default_spacing * i
                    else:
                        spacing = bpy.context.scene.object_settings.Spacing0
                        if axis == 'x-axis':
                            pos_list = [o.location.x for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list)
                            for i, idx in enumerate(obj_idx):
                                oblist[idx].location.x = oblist[obj_idx[0]
                                                                ].location.x + spacing * i
                        elif axis == 'y-axis':
                            pos_list = [o.location.y for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list)
                            for i, idx in enumerate(obj_idx):
                                oblist[idx].location.y = oblist[obj_idx[0]
                                                                ].location.y + spacing * i
                        elif axis == 'z-axis':
                            pos_list = [o.location.z for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list)
                            for i, idx in enumerate(obj_idx):
                                oblist[idx].location.z = oblist[obj_idx[0]
                                                                ].location.z + spacing * i
            else:
                pass
        elif dist_type == 'edge':
            if i == 0:
                if len(oblist) > 1:
                    if not indicate:
                        pos_list = []
                        if axis == 'x-axis':
                            pos_list = [o.location.x for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list) + (
                                oblist[obj_idx[0]].dimensions.x / 2) + (oblist[obj_idx[-1]].dimensions.x / 2)
                            empty_space = distance
                            for o in oblist:
                                empty_space = empty_space - o.dimensions.x
                            d = empty_space / (len(oblist) - 1)
                            for i, idx in enumerate(obj_idx):
                                if i < max(obj_idx):
                                    oblist[obj_idx[i + 1]].location.x = oblist[idx].location.x + (
                                        oblist[idx].dimensions.x / 2) + d + (oblist[obj_idx[i + 1]].dimensions.x / 2)
                        elif axis == 'y-axis':
                            pos_list = [o.location.y for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list) + (
                                oblist[obj_idx[0]].dimensions.y / 2) + (oblist[obj_idx[-1]].dimensions.y / 2)
                            empty_space = distance
                            for o in oblist:
                                empty_space = empty_space - o.dimensions.y
                            d = empty_space / (len(oblist) - 1)
                            for i, idx in enumerate(obj_idx):
                                if i < max(obj_idx):
                                    oblist[obj_idx[i + 1]].location.y = oblist[idx].location.y + (
                                        oblist[idx].dimensions.y / 2) + d + (oblist[obj_idx[i + 1]].dimensions.y / 2)
                        elif axis == 'z-axis':
                            pos_list = [o.location.z for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list) + (
                                oblist[obj_idx[0]].dimensions.z / 2) + (oblist[obj_idx[-1]].dimensions.z / 2)
                            empty_space = distance
                            for o in oblist:
                                empty_space = empty_space - o.dimensions.z
                            d = empty_space / (len(oblist) - 1)
                            for i, idx in enumerate(obj_idx):
                                if i < max(obj_idx):
                                    oblist[obj_idx[i + 1]].location.z = oblist[idx].location.z + (
                                        oblist[idx].dimensions.z / 2) + d + (oblist[obj_idx[i + 1]].dimensions.z / 2)
                    else:
                        spacing = bpy.context.scene.object_settings.Spacing0
                        if axis == 'x-axis':
                            pos_list = [o.location.x for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            for i, idx in enumerate(obj_idx):
                                if i < max(obj_idx):
                                    oblist[obj_idx[i + 1]].location.x = oblist[idx].location.x + (
                                        oblist[idx].dimensions.x / 2) + spacing + (oblist[obj_idx[i + 1]].dimensions.x / 2)
                        elif axis == 'y-axis':
                            pos_list = [o.location.y for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            for i, idx in enumerate(obj_idx):
                                if i < max(obj_idx):
                                    oblist[obj_idx[i + 1]].location.y = oblist[idx].location.y + (
                                        oblist[idx].dimensions.y / 2) + spacing + (oblist[obj_idx[i + 1]].dimensions.y / 2)
                        elif axis == 'z-axis':
                            pos_list = [o.location.z for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            for i, idx in enumerate(obj_idx):
                                if i < max(obj_idx):
                                    oblist[obj_idx[i + 1]].location.z = oblist[idx].location.z + (
                                        oblist[idx].dimensions.z / 2) + spacing + (oblist[obj_idx[i + 1]].dimensions.z / 2)
            else:
                pass

        return {'FINISHED'}


class Blign_Distribute_Button1(bpy.types.Operator):
    """Defines the Distribute button."""
    bl_idname = "rigidbody.blign_distribute_button1"
    bl_label = "Distribute"
    bl_description = "Distribute objects"

    def execute(self, context):
        """Distributes objects between first and last object.

        Indicate = the indicate spacing button. If unchecked, evenly distributes shapes. 
        If checked, distributes objects 'spacing' units apart.
        """
        indicate = bpy.context.scene.object_settings.indicate_spacing1
        axis = bpy.context.scene.object_settings.Axis1
        oblist = bpy.context.selected_objects
        dist_type = bpy.context.scene.object_settings.distribute_ops1

        i = 0
        for object in list(bpy.data.objects):
            if object.blign == True:
                i += 1

        if dist_type == 'center':
            if i == 1:
                if len(oblist) > 1:
                    if not indicate:
                        pos_list = []
                        if axis == 'x-axis':
                            pos_list = [o.location.x for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list)
                            default_spacing = distance / (len(pos_list) - 1)
                            for i, idx in enumerate(obj_idx):
                                oblist[idx].location.x = oblist[obj_idx[0]].location.x + \
                                    default_spacing * i
                        elif axis == 'y-axis':
                            pos_list = [o.location.y for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list)
                            default_spacing = distance / (len(pos_list) - 1)
                            for i, idx in enumerate(obj_idx):
                                oblist[idx].location.y = oblist[obj_idx[0]].location.y + \
                                    default_spacing * i
                        elif axis == 'z-axis':
                            pos_list = [o.location.z for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list)
                            default_spacing = distance / (len(pos_list) - 1)
                            for i, idx in enumerate(obj_idx):
                                oblist[idx].location.z = oblist[obj_idx[0]].location.z + \
                                    default_spacing * i
                    else:
                        spacing = bpy.context.scene.object_settings.Spacing1
                        if axis == 'x-axis':
                            pos_list = [o.location.x for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list)
                            for i, idx in enumerate(obj_idx):
                                oblist[idx].location.x = oblist[obj_idx[0]
                                                                ].location.x + spacing * i
                        elif axis == 'y-axis':
                            pos_list = [o.location.y for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list)
                            for i, idx in enumerate(obj_idx):
                                oblist[idx].location.y = oblist[obj_idx[0]
                                                                ].location.y + spacing * i
                        elif axis == 'z-axis':
                            pos_list = [o.location.z for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list)
                            for i, idx in enumerate(obj_idx):
                                oblist[idx].location.z = oblist[obj_idx[0]
                                                                ].location.z + spacing * i
            else:
                pass
        elif dist_type == 'edge':
            if i == 1:
                if len(oblist) > 1:
                    if not indicate:
                        pos_list = []
                        if axis == 'x-axis':
                            pos_list = [o.location.x for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list) + (
                                oblist[obj_idx[0]].dimensions.x / 2) + (oblist[obj_idx[-1]].dimensions.x / 2)
                            empty_space = distance
                            for o in oblist:
                                empty_space = empty_space - o.dimensions.x
                            d = empty_space / (len(oblist) - 1)
                            for i, idx in enumerate(obj_idx):
                                if i < max(obj_idx):
                                    oblist[obj_idx[i + 1]].location.x = oblist[idx].location.x + (
                                        oblist[idx].dimensions.x / 2) + d + (oblist[obj_idx[i + 1]].dimensions.x / 2)
                        elif axis == 'y-axis':
                            pos_list = [o.location.y for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list) + (
                                oblist[obj_idx[0]].dimensions.y / 2) + (oblist[obj_idx[-1]].dimensions.y / 2)
                            empty_space = distance
                            for o in oblist:
                                empty_space = empty_space - o.dimensions.y
                            d = empty_space / (len(oblist) - 1)
                            for i, idx in enumerate(obj_idx):
                                if i < max(obj_idx):
                                    oblist[obj_idx[i + 1]].location.y = oblist[idx].location.y + (
                                        oblist[idx].dimensions.y / 2) + d + (oblist[obj_idx[i + 1]].dimensions.y / 2)
                        elif axis == 'z-axis':
                            pos_list = [o.location.z for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            distance = max(pos_list) - min(pos_list) + (
                                oblist[obj_idx[0]].dimensions.z / 2) + (oblist[obj_idx[-1]].dimensions.z / 2)
                            empty_space = distance
                            for o in oblist:
                                empty_space = empty_space - o.dimensions.z
                            d = empty_space / (len(oblist) - 1)
                            for i, idx in enumerate(obj_idx):
                                if i < max(obj_idx):
                                    oblist[obj_idx[i + 1]].location.z = oblist[idx].location.z + (
                                        oblist[idx].dimensions.z / 2) + d + (oblist[obj_idx[i + 1]].dimensions.z / 2)
                    else:
                        spacing = bpy.context.scene.object_settings.Spacing1
                        if axis == 'x-axis':
                            pos_list = [o.location.x for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            for i, idx in enumerate(obj_idx):
                                if i < max(obj_idx):
                                    oblist[obj_idx[i + 1]].location.x = oblist[idx].location.x + (
                                        oblist[idx].dimensions.x / 2) + spacing + (oblist[obj_idx[i + 1]].dimensions.x / 2)
                        elif axis == 'y-axis':
                            pos_list = [o.location.y for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            for i, idx in enumerate(obj_idx):
                                if i < max(obj_idx):
                                    oblist[obj_idx[i + 1]].location.y = oblist[idx].location.y + (
                                        oblist[idx].dimensions.y / 2) + spacing + (oblist[obj_idx[i + 1]].dimensions.y / 2)
                        elif axis == 'z-axis':
                            pos_list = [o.location.z for o in oblist]
                            obj_idx = np.argsort(pos_list)
                            for i, idx in enumerate(obj_idx):
                                if i < max(obj_idx):
                                    oblist[obj_idx[i + 1]].location.z = oblist[idx].location.z + (
                                        oblist[idx].dimensions.z / 2) + spacing + (oblist[obj_idx[i + 1]].dimensions.z / 2)
            else:
                pass

        return {'FINISHED'}


class Blign_Distribute_Button2(bpy.types.Operator):
    """Defines the Distribute button."""
    bl_idname = "rigidbody.blign_distribute_button2"
    bl_label = "Distribute"
    bl_description = "Distribute objects"

    def execute(self, context):
        """Distributes objects between first and last object.

        Indicate = the indicate spacing button. If unchecked, evenly distributes shapes. 
        If checked, distributes objects 'spacing' units apart.
        """
        indicate = bpy.context.scene.object_settings.indicate_spacing2
        oblist = bpy.context.selected_objects
        dist_type = bpy.context.scene.object_settings.distribute_ops2

        i = 0
        for object in list(bpy.data.objects):
            if object.blign == True:
                i += 1
        
        if dist_type == 'center':
            if i == 2:
                if len(oblist) > 1:
                    if not indicate:
                        pos_list = []
                        pos_list = [o.location.x for o in oblist]
                        obj_idx = np.argsort(pos_list)
                        distance = max(pos_list) - min(pos_list)
                        default_spacing = distance / (len(pos_list) - 1)
                        for i, idx in enumerate(obj_idx):
                            oblist[idx].location.x = oblist[obj_idx[0]].location.x + \
                                default_spacing * i

                        pos_list = [o.location.y for o in oblist]
                        obj_idx = np.argsort(pos_list)
                        distance = max(pos_list) - min(pos_list)
                        default_spacing = distance / (len(pos_list) - 1)
                        for i, idx in enumerate(obj_idx):
                            oblist[idx].location.y = oblist[obj_idx[0]].location.y + \
                                default_spacing * i

                        pos_list = [o.location.z for o in oblist]
                        obj_idx = np.argsort(pos_list)
                        distance = max(pos_list) - min(pos_list)
                        default_spacing = distance / (len(pos_list) - 1)
                        for i, idx in enumerate(obj_idx):
                            oblist[idx].location.z = oblist[obj_idx[0]].location.z + \
                                default_spacing * i
                    else:  # whenever spacing is checked and distribute is clicked multiple times it keeps moving all objects
                        spacing = bpy.context.scene.object_settings.Spacing2
                        p1, p2 = [np.array(o.location)for o in bpy.data.objects if o.blign]
                        v = p2 - p1
                        u = v / np.linalg.norm(v)  # magnitude of vector v
                        i = 0
                        for obj in context.selected_objects:
                            obj.location.x = p1[0] + u[0] * spacing * i
                            obj.location.y = p1[1] + u[1] * spacing * i
                            obj.location.z = p1[2] + u[2] * spacing * i
                            i += 1
                else:
                    pass
        elif dist_type == 'edge':
            if i == 2:
                if len(oblist) > 1:
                    if not indicate:
                        pos_list = [o.location.x for o in oblist]
                        obj_idx = np.argsort(pos_list)
                        distance = max(pos_list) - min(pos_list) + (oblist[obj_idx[0]].dimensions.x / 2) + (oblist[obj_idx[-1]].dimensions.x / 2)
                        empty_space = distance
                        for o in oblist:
                            empty_space = empty_space - o.dimensions.x
                        d = empty_space / (len(oblist) - 1)
                        for i, idx in enumerate(obj_idx):
                            if i < max(obj_idx):
                                oblist[obj_idx[i + 1]].location.x = oblist[idx].location.x + (oblist[idx].dimensions.x / 2) + d + (oblist[obj_idx[i + 1]].dimensions.x / 2)
                                        
                        pos_list = [o.location.y for o in oblist]
                        obj_idx = np.argsort(pos_list)
                        distance = max(pos_list) - min(pos_list) + (oblist[obj_idx[0]].dimensions.y / 2) + (oblist[obj_idx[-1]].dimensions.y / 2)
                        empty_space = distance
                        for o in oblist:
                            empty_space = empty_space - o.dimensions.y
                        d = empty_space / (len(oblist) - 1)
                        for i, idx in enumerate(obj_idx):
                            if i < max(obj_idx):
                                oblist[obj_idx[i + 1]].location.y = oblist[idx].location.y + (oblist[idx].dimensions.y / 2) + d + (oblist[obj_idx[i + 1]].dimensions.y / 2)

                        pos_list = [o.location.z for o in oblist]
                        obj_idx = np.argsort(pos_list)
                        distance = max(pos_list) - min(pos_list) + (oblist[obj_idx[0]].dimensions.z / 2) + (oblist[obj_idx[-1]].dimensions.z / 2)
                        empty_space = distance
                        for o in oblist:
                            empty_space = empty_space - o.dimensions.z
                        d = empty_space / (len(oblist) - 1)
                        for i, idx in enumerate(obj_idx):
                            if i < max(obj_idx):
                                oblist[obj_idx[i + 1]].location.z = oblist[idx].location.z + (oblist[idx].dimensions.z / 2) + d + (oblist[obj_idx[i + 1]].dimensions.z / 2)
                    else:
                        pass
                        # spacing = bpy.context.scene.object_settings.Spacing2
                        # pos_list = [o.location.x for o in oblist]
                        # obj_idx = np.argsort(pos_list)
                        # for i, idx in enumerate(obj_idx):
                        #     if i < max(obj_idx):
                        #         oblist[obj_idx[i + 1]].location.x = oblist[idx].location.x + (
                        #             oblist[idx].dimensions.x / 2) + spacing + (oblist[obj_idx[i + 1]].dimensions.x / 2)

                        # pos_list = [o.location.y for o in oblist]
                        # obj_idx = np.argsort(pos_list)
                        # for i, idx in enumerate(obj_idx):
                        #     if i < max(obj_idx):
                        #         oblist[obj_idx[i + 1]].location.y = oblist[idx].location.y + (
                        #             oblist[idx].dimensions.y / 2) + spacing + (oblist[obj_idx[i + 1]].dimensions.y / 2)

                        # pos_list = [o.location.z for o in oblist]
                        # obj_idx = np.argsort(pos_list)
                        # for i, idx in enumerate(obj_idx):
                        #     if i < max(obj_idx):
                        #         oblist[obj_idx[i + 1]].location.z = oblist[idx].location.z + (
                        #             oblist[idx].dimensions.z / 2) + spacing + (oblist[obj_idx[i + 1]].dimensions.z / 2)
            else:
                pass
        return {'FINISHED'}


class Blign(bpy.types.Panel):
    """Parent tab, all other tabs are within this one."""
    bl_label = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        """Outlines the Add and Remove buttons in the Blign tab.

        Finds the number of objects added.
        If one or more objects are added, shows remove button. 
        Does not allow user to add more than 2 objects as blign objects.
        Shows which objects have been added as blign objects below the add/remove button.
        """
        layout = self.layout
        layout.use_property_split = True

        blobs = []
        i = 0
        for object in list(bpy.data.objects):
            if object.blign == True:
                blobs.append(object.name)
                i += 1

        # this is here to fix the delete error, improve code at some point in future to fix
        try:
            if (bpy.context.object.blign == True):
                row = layout.row()
                row.operator('rigidbody.blign_remove_object')
            elif (bpy.context.object.blign == False):
                if (i < 2):
                    row = layout.row()
                    row.operator('rigidbody.blign_add_object')
        except AttributeError:
            pass

# Objects are always sorted alphabetically, figure out how to change
        if i == 1:
            row = layout.row()
            row.label(text="Object 1: {}".format(str(blobs[0])))
        if i == 2:
            row = layout.row()
            row.label(text="Object 1: {}".format(str(blobs[0])))

            row = layout.row()
            row.label(text="Object 2: {}".format(str(blobs[1])))


class BlignSettings(bpy.types.PropertyGroup):
    """All buttons used in the add-on are defined in this class."""

    Axis0: bpy.props.EnumProperty(
        name="Axis",
        items=[("x-axis", "x", "Align objects in the x direction"),
               ("y-axis", "y", "Align objects in the y direction"),
               ("z-axis", "z", "Align objects in the z direction")],
        default='x-axis',
        options={'HIDDEN'},
    )

    Axis1: bpy.props.EnumProperty(
        name="Axis",
        items=[("x-axis", "x", "Align objects in the x direction"),
               ("y-axis", "y", "Align objects in the y direction"),
               ("z-axis", "z", "Align objects in the z direction")],
        default='x-axis',
        options={'HIDDEN'},
    )

    indicate_spacing0: bpy.props.BoolProperty(
        name="",
        description="Choose whether or not to indicate spacing betweeen objects",
        options={'HIDDEN'},
        default=False
    )

    indicate_spacing1: bpy.props.BoolProperty(
        name="",
        description="Choose whether or not to indicate spacing betweeen objects",
        options={'HIDDEN'},
        default=False
    )

    indicate_spacing2: bpy.props.BoolProperty(
        name="",
        description="Choose whether or not to indicate spacing betweeen objects",
        options={'HIDDEN'},
        default=False
    )

    Spacing0: bpy.props.IntProperty(
        name="Spacing",
        description="Set distribution value between objects",
        default=1,
        options={'HIDDEN'},
    )

    Spacing1: bpy.props.IntProperty(
        name="Spacing",
        description="Set distribution value between objects",
        default=1,
        options={'HIDDEN'},
    )

    Spacing2: bpy.props.IntProperty(
        name="Spacing",
        description="Set distribution value between objects",
        default=1,
        options={'HIDDEN'},
    )

    align_to0: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("top", "Top", "Align to top of object"),
               ("bottom", "Bottom", "Align to bottom of object")],
        default='center',
        options={'HIDDEN'},
    )

    align_to1: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("top", "Top", "Align to top of object"),
               ("bottom", "Bottom", "Align to bottom of object")],
        default='center',
        options={'HIDDEN'},
    )

    distribute_ops0: bpy.props.EnumProperty(
        name="Distribute from",
        items=[("center", "Center", "Distribute from center of object"),
               ("edge", "Edge", "Distribute from edge of object")],
        default='center',
        options={'HIDDEN'},
    )

    distribute_ops1: bpy.props.EnumProperty(
        name="Distribute from",
        items=[("center", "Center", "Distribute from center of object"),
               ("edge", "Edge", "Distribute from edge of object")],
        default='center',
        options={'HIDDEN'},
    )

    distribute_ops2: bpy.props.EnumProperty(
        name="Distribute from",
        items=[("center", "Center", "Distribute from center of object"),
               ("edge", "Edge", "Distribute from edge of object")],
        default='center',
        options={'HIDDEN'},
    )


class Blign_Principal_Axes(bpy.types.Panel):
    """Class that outlines the Align tab."""
    bl_label = "Principal Axes"
    bl_parent_id = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        """The buttons within the tab are called here.

        settings is a PointerProperty that points to the class BlignSettings, where the buttons are defined.
        """
        layout = self.layout
        layout.use_property_split = True
        settings = context.scene.object_settings
        axis = bpy.context.scene.object_settings.Axis0

        row = layout.row()
        row.prop(settings, "Axis0", expand=True)

        if axis == 'x-axis' or axis == 'y-axis':
            row = layout.row()
            row.prop(settings, "align_to0", expand=True)
        else:
            pass

        row = layout.row()
        row.operator('rigidbody.blign_align_button0')

        row = layout.row()
        row.prop(settings, "distribute_ops0", expand=True)

        row = layout.row()
        row.prop(settings, "indicate_spacing0")
        row.prop(settings, 'Spacing0')

        row = layout.row()
        row.operator('rigidbody.blign_distribute_button0')


class Blign_One_Object(bpy.types.Panel):
    """Class that outlines the Align to One Object tab."""
    bl_label = "Align to One Object"
    bl_parent_id = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        """The buttons within the Align to One Object tab are called here."""
        layout = self.layout
        layout.use_property_split = True
        settings = context.scene.object_settings
        axis = bpy.context.scene.object_settings.Axis1

        row = layout.row()
        row.prop(settings, "Axis1", expand=True)

        if axis == 'x-axis' or axis == 'y-axis':
            row = layout.row()
            row.prop(settings, "align_to1", expand=True)
        else:
            pass

        row = layout.row()
        row.operator('rigidbody.blign_align_button1')

        row = layout.row()
        row.prop(settings, "distribute_ops1", expand=True)

        row = layout.row()
        row.prop(settings, "indicate_spacing1")
        row.prop(settings, 'Spacing1')

        row = layout.row()
        row.operator('rigidbody.blign_distribute_button1')


class Blign_Two_Objects(bpy.types.Panel):
    """Class that outlines the Align to Two Objects tab."""
    bl_label = "Align to Two Objects"
    bl_parent_id = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        """Buttons within Align to Two Objects tab are called here."""
        layout = self.layout
        layout.use_property_split = True
        settings = context.scene.object_settings

        row = layout.row()
        row.operator('rigidbody.blign_align_button2')

        row = layout.row()
        row.prop(settings, "distribute_ops2", expand=True)

        row = layout.row()
        row.prop(settings, "indicate_spacing2")
        row.prop(settings, 'Spacing2')

        row = layout.row()
        row.operator('rigidbody.blign_distribute_button2')


classes = (
    Add_Object,
    Remove_Object,
    Blign_Align_Button0,
    Blign_Align_Button1,
    Blign_Align_Button2,
    Blign_Distribute_Button0,
    Blign_Distribute_Button1,
    Blign_Distribute_Button2,
    Blign,
    BlignSettings,
    Blign_Principal_Axes,
    Blign_One_Object,
    Blign_Two_Objects,
)


def register():
    """Registers classes and defines scene.object_settings and object.blign.

    Creates new subset of bpy.types.scene called object_Settings that points to BlignSettings.
    Creates new subset of bpy.types.object called blign.
    """
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.object_settings = bpy.props.PointerProperty(
        type=BlignSettings)
    bpy.types.Object.blign = bpy.props.BoolProperty(
        name="Blign")


def unregister():
    """Unregisters classes."""

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.object_settings
    del bpy.types.Object.blign
