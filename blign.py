import math
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


def count_blign_objects():
    """
    Counts the number of selected Blign objects.
    Arguments
    ---------
    Returns
    -------
    len.... : int
        Number of Blign objects.
    """
    return len([obj for obj in list(bpy.data.objects) if obj.blign == True])


def find_alignment_points(direction, vertex_sign):
    """
    Finds the points on the Blign objects that makes up the alignment line.
    Arguments
    ---------
    direction : str
        Direction in 3D space ['x', 'y', 'z'].
    vertex_sign : str
        Sign of the vertex ['+', '-'].
    Returns
    -------
    p1 : numpy array
        Desired vertex on the first Blign object.
    p2 : numpy array
        Desired vertex on the second Blign object.
    """
    if count_blign_objects() == 2:
        blign1, blign2 = [np.array([obj.matrix_world @ Vector(
            c) for c in obj.bound_box]) for obj in bpy.data.objects if obj.blign]
        drx_idx = {'x': 0, 'y': 1, 'z': 2}[direction]
        vertex_idx = {'-': 0, '+': -1}[vertex_sign]
        p1, p2 = blign1[np.argsort(blign1[:, drx_idx])[vertex_idx]], blign2[np.argsort(
            blign2[:, drx_idx])[vertex_idx]]
    else:
        raise ValueError('There should be 2 Blign objects selected!')
    return p1, p2


def find_vertex(obj, direction, vertex_sign):
    """
    Finds the 3d coordinates for a specified vertex on a given object.
    Arguments
    ---------
    obj : Blender object
        Object to find the vertex
    direction : str
        Direction in 3D space ['x', 'y', 'z'].
    vertex_sign : str
        Sign of the vertex ['+', '-'].
    Returns
    -------
    p : numpy array
        Desired vertex on an object.
    """
    drx_idx = {'x': 0, 'y': 1, 'z': 2}[direction]
    vertex_idx = {'-': 0, '+': -1}[vertex_sign]
    vertices = np.array([obj.matrix_world @ Vector(c) for c in obj.bound_box])
    p = vertices[np.argsort(vertices[:, drx_idx])[vertex_idx]]
    return p


def transform_object(obj, v):
    """
    Transforms the object to the desired position.
    Arguments
    ---------
    obj : Blender object
        Object to find the vertex.
    v : float (or vector?)
        Vector along which the object needs to be transformed ['x', 'y', 'z'].
    Returns
    -------
    obj : Blender object
        Object to find the vertex.
    """
    obj.location.x += v[0]
    obj.location.y += v[1]
    obj.location.z += v[2]
    return obj


def find_default_spacing(axis):
    """
    Function finds the default distance between that objects are being distributed from their centers.
    Arguments
    ---------
    axis : str
        The axis that objects get aligned to.
    Returns
    -------
    default_spacing : float
        Distance between objects' centers when distributed.
    obj_idx : list
        An indexed numpy list of all object locations.
    """
    oblist = bpy.context.selected_objects
    if axis == 'x':
        pos_list = [o.location.x for o in oblist]
    elif axis == 'y':
        pos_list = [o.location.y for o in oblist]
    elif axis == 'z':
        pos_list = [o.location.z for o in oblist]
    obj_idx = np.argsort(pos_list)
    distance = max(pos_list) - min(pos_list)
    default_spacing = distance / (len(pos_list) - 1)
    return default_spacing, obj_idx


def find_d(obj_idx, direction):
    """
    Function that defines the distance between objects' edges.
    Arguments
    ---------
    obj_idx : list
        An indexed numpy list of all object locations.
    direction : str
        Either x y or z.
    Returns
    -------
    d : float
        distance between the edges of one object and the next.
    """
    drx_idx = {'x': 0, 'y': 1, 'z': 2}[direction]
    oblist = bpy.context.selected_objects
    obj_space = 0

    for i, idx in enumerate(obj_idx):
        vertices = np.array([oblist[obj_idx[i]].matrix_world @ Vector(c)
                             for c in oblist[obj_idx[i]].bound_box])
        p1 = vertices[np.argsort(vertices[:, drx_idx])[0]]
        p2 = vertices[np.argsort(vertices[:, drx_idx])[-1]]
        if i == 0:
            start = p1[drx_idx]
        elif i == max(obj_idx):
            end = p2[drx_idx]
        obj_space += p2[drx_idx] - p1[drx_idx]
    distance = end - start
    empty_space = distance - obj_space
    d = empty_space / (len(oblist) - 1)
    return d


def find_c_to_v(obj_idx, direction):
    """
    Function finds the default distance between that objects are being distributed from their centers.
    Arguments
    ---------
    obj_idx : list
        An indexed numpy list of all object locations.
    direction : str
        Either x y or z.
    Returns
    -------
    c_to_v1 : list
        A list of the distances from an object's most positive edge to its center.
    c_to_v1 : list
        A list of the distances from an object's most negative edge to its center.
    """
    drx_idx = {'x': 0, 'y': 1, 'z': 2}[direction]
    oblist = bpy.context.selected_objects
    c_to_v1 = []
    c_to_v2 = []
    for i, idx in enumerate(obj_idx):
        vertices = np.array([oblist[obj_idx[i]].matrix_world @ Vector(c)
                             for c in oblist[obj_idx[i]].bound_box])
        p1 = vertices[np.argsort(vertices[:, drx_idx])[-1]]
        p2 = vertices[np.argsort(vertices[:, drx_idx])[0]]
        if direction == 'x':
            loc = oblist[idx].location.x
        elif direction == 'y':
            loc = oblist[idx].location.y
        elif direction == 'z':
            loc = oblist[idx].location.z
        dist1 = p1[drx_idx] - loc
        dist2 = loc - p2[drx_idx]
        c_to_v1.append(dist1)
        c_to_v2.append(dist2)
    return c_to_v1, c_to_v2


def align_axis_0():
    """
    Aligns the object on the principal, function called in Blign_Align_Button0.
    Arguments
    ---------
    Returns
    -------
    """
    axis = bpy.context.scene.object_settings.Axis0
    oblist = bpy.context.selected_objects
    directionx = bpy.context.scene.object_settings.x_selected0
    directiony = bpy.context.scene.object_settings.y_selected0
    directionz = bpy.context.scene.object_settings.z_selected0

    if axis == 'x':
        if directionx == 'center':
            for obj in oblist:
                obj.location.y = 0
                obj.location.z = 0
        else:
            for obj in oblist:
                v = find_vertex(obj, directionx[1], directionx[0])
                obj = transform_object(obj, [0, -v[1], -v[2]])
    elif axis == 'y':
        if directiony == 'center':
            for obj in oblist:
                obj.location.x = 0
                obj.location.z = 0
        else:
            for obj in oblist:
                v = find_vertex(obj, directiony[1], directiony[0])
                obj = transform_object(obj, [-v[0], 0, -v[2]])
    elif axis == 'z':
        if directionz == 'center':
            for obj in oblist:
                obj.location.x = 0
                obj.location.y = 0
        else:
            for obj in oblist:
                v = find_vertex(obj, directionz[1], directionz[0])
                obj = transform_object(obj, [-v[0], -v[1], 0])


def align_plane_0():
    """
    Aligns the object to the same plane as an added Blign object, function called in Blign_Align_Button1.
    Arguments
    ---------
    Returns
    -------
    """
    plane = bpy.context.scene.object_settings.Plane0
    oblist = bpy.context.selected_objects
    directionyz = bpy.context.scene.object_settings.yz_selected0
    directionxz = bpy.context.scene.object_settings.xz_selected0
    directionxy = bpy.context.scene.object_settings.xy_selected0

    if plane == 'y-z':
        if directionyz == 'center':
            for obj in oblist:
                obj.location.x = 0
        else:
            for obj in oblist:
                v = find_vertex(obj, directionyz[1], directionyz[0])
                obj = transform_object(obj, [-v[0], 0, 0])
    elif plane == 'x-z':
        if directionxz == 'center':
            for obj in oblist:
                obj.location.y = 0
        else:
            for obj in oblist:
                v = find_vertex(obj, directionxz[1], directionxz[0])
                obj = transform_object(obj, [0, -v[1], 0])
    elif plane == 'x-y':
        if directionxy == 'center':
            for obj in oblist:
                obj.location.z = 0
        else:
            for obj in oblist:
                v = find_vertex(obj, directionxy[1], directionxy[0])
                obj = transform_object(obj, [0, 0, -v[2]])


def align_axis_1():
    """
    Aligns the object to an added Blign object, function called in Blign_Align_Button1.
    Arguments
    ---------
    Returns
    -------
    """
    axis = bpy.context.scene.object_settings.Axis1
    oblist = bpy.context.selected_objects
    directionx = bpy.context.scene.object_settings.x_selected1
    directiony = bpy.context.scene.object_settings.y_selected1
    directionz = bpy.context.scene.object_settings.z_selected1

    if axis == 'x':
        if directionx == 'center':
            for obj in list(bpy.data.objects):
                if obj.blign == True:
                    locy = obj.location.y
                    locz = obj.location.z
            for obj in oblist:
                obj.location.y = locy
                obj.location.z = locz
        else:
            for obj in list(bpy.data.objects):
                if obj.blign == True:
                    blign_vertex = find_vertex(
                        obj, directionx[1], directionx[0])
            for obj in oblist:
                v = find_vertex(obj, directionx[1], directionx[0])
                delta = blign_vertex - v
                obj = transform_object(obj, [0, delta[1], delta[2]])
    elif axis == 'y':
        if directiony == 'center':
            for obj in list(bpy.data.objects):
                if obj.blign == True:
                    locx = obj.location.x
                    locz = obj.location.z
            for obj in oblist:
                obj.location.x = locx
                obj.location.z = locz
        else:
            for obj in list(bpy.data.objects):
                if obj.blign == True:
                    blign_vertex = find_vertex(
                        obj, directiony[1], directiony[0])
            for obj in oblist:
                v = find_vertex(obj, directiony[1], directiony[0])
                delta = blign_vertex - v
                obj = transform_object(obj, [delta[0], 0, delta[2]])
    elif axis == 'z':
        if directionz == 'center':
            for obj in list(bpy.data.objects):
                if obj.blign == True:
                    locx = obj.location.x
                    locy = obj.location.y
            for obj in oblist:
                obj.location.x = locx
                obj.location.y = locy
        else:
            for obj in list(bpy.data.objects):
                if obj.blign == True:
                    blign_vertex = find_vertex(
                        obj, directionz[1], directionz[0])
            for obj in oblist:
                v = find_vertex(obj, directionz[1], directionz[0])
                delta = blign_vertex - v
                obj = transform_object(obj, [delta[0], delta[1], 0])


def align_plane_1():
    """
    Aligns the object to the same plane as the an added Blign object, function called in Blign_Align_Button1.
    Arguments
    ---------
    Returns
    -------
    """
    plane = bpy.context.scene.object_settings.Plane1
    oblist = bpy.context.selected_objects
    directionyz = bpy.context.scene.object_settings.yz_selected1
    directionxz = bpy.context.scene.object_settings.xz_selected1
    directionxy = bpy.context.scene.object_settings.xy_selected1

    if plane == 'y-z':
        if directionyz == 'center':
            for obj in list(bpy.data.objects):
                if obj.blign == True:
                    locx = obj.location.x
            for obj in oblist:
                obj.location.x = locx
        else:
            for obj in list(bpy.data.objects):
                if obj.blign == True:
                    blign_vertex = find_vertex(
                        obj, directionyz[1], directionyz[0])
            for obj in oblist:
                v = find_vertex(obj, directionyz[1], directionyz[0])
                delta = blign_vertex - v
                obj = transform_object(obj, [delta[0], 0, 0])
    elif plane == 'x-z':
        if directionxz == 'center':
            for obj in list(bpy.data.objects):
                if obj.blign == True:
                    locy = obj.location.y
            for obj in oblist:
                obj.location.y = locy
        else:
            for obj in list(bpy.data.objects):
                if obj.blign == True:
                    blign_vertex = find_vertex(
                        obj, directionxz[1], directionxz[0])
            for obj in oblist:
                v = find_vertex(obj, directionxz[1], directionxz[0])
                delta = blign_vertex - v
                obj = transform_object(obj, [0, delta[1], 0])
    elif plane == 'x-y':
        if directionxy == 'center':
            for obj in list(bpy.data.objects):
                if obj.blign == True:
                    locz = obj.location.z
            for obj in oblist:
                obj.location.z = locz
        else:
            for obj in list(bpy.data.objects):
                if obj.blign == True:
                    blign_vertex = find_vertex(
                        obj, directionxy[1], directionxy[0])
            for obj in oblist:
                v = find_vertex(obj, directionxy[1], directionxy[0])
                delta = blign_vertex - v
                obj = transform_object(obj, [0, 0, delta[2]])


def align_2():
    """
    Aligns the object to two added Blign objects, function called in Blign_Align_Button2.
    Arguments
    ---------
    Returns
    -------
    """
    align = bpy.context.scene.object_settings.align_to_2_ops
    oblist = bpy.context.selected_objects

    if align == 'center':
        p1, p2 = [np.array(o.location) for o in bpy.data.objects if o.blign]
    else:
        p1, p2 = find_alignment_points(align[1], align[0])

    u = p2 - p1
    a = np.array([[(u ** 2).sum()]])

    for obj in oblist:
        if obj.blign == False:
            if align == 'center':
                p = np.array([obj.location.x, obj.location.y, obj.location.z])
            else:
                p = find_vertex(obj, align[1], align[0])
            b = np.array([[(u * (p - p2)).sum()]])
            t = np.linalg.solve(a, b)
            v = u * t[0][0] + (p2 - p)

            obj = transform_object(obj, v)


def distribute_0_or_1(indicate, axis, dist_type, spacing):
    """
    Distributes objects from their centers or edges when 0 or 1 blign objects are added.
    Arguments
    ---------
    indicate : bool
        If True, user can set spacing. If False, Blign finds default spacing.
    axis: str
        Either x y or z.
    dist_type : str
        The user's choice to distribute from either center or edge.
    spacing : int
        number of units between objects (specified by user).
    Returns
    -------
    """
    oblist = bpy.context.selected_objects

    if dist_type == 'center':
        if len(oblist) > 1:
            if not indicate:
                default_spacing, obj_idx = find_default_spacing(axis)
                if axis == 'x':
                    for i, idx in enumerate(obj_idx):
                        oblist[idx].location.x = oblist[obj_idx[0]
                                                        ].location.x + default_spacing * i
                elif axis == 'y':
                    for i, idx in enumerate(obj_idx):
                        oblist[idx].location.y = oblist[obj_idx[0]
                                                        ].location.y + default_spacing * i
                elif axis == 'z':
                    for i, idx in enumerate(obj_idx):
                        oblist[idx].location.z = oblist[obj_idx[0]
                                                        ].location.z + default_spacing * i
            else:
                spacing = bpy.context.scene.object_settings.Spacing0
                obj_idx = find_default_spacing(axis)[1]
                if axis == 'x':
                    for i, idx in enumerate(obj_idx):
                        oblist[idx].location.x = oblist[obj_idx[0]
                                                        ].location.x + spacing * i
                elif axis == 'y':
                    for i, idx in enumerate(obj_idx):
                        oblist[idx].location.y = oblist[obj_idx[0]
                                                        ].location.y + spacing * i
                elif axis == 'z':
                    for i, idx in enumerate(obj_idx):
                        oblist[idx].location.z = oblist[obj_idx[0]
                                                        ].location.z + spacing * i
    elif dist_type == 'edge':
        if len(oblist) > 1:
            obj_idx = find_default_spacing(axis)[1]
            if not indicate:
                d = find_d(obj_idx, axis)
                c_to_v1, c_to_v2 = find_c_to_v(obj_idx, axis)
                if axis == 'x':
                    for i, idx in enumerate(obj_idx):
                        if i < max(obj_idx):
                            oblist[obj_idx[i + 1]].location.x = oblist[idx].location.x + \
                                c_to_v1[i] + d + c_to_v2[i + 1]
                elif axis == 'y':
                    for i, idx in enumerate(obj_idx):
                        if i < max(obj_idx):
                            oblist[obj_idx[i + 1]].location.y = oblist[idx].location.y + \
                                c_to_v1[i] + d + c_to_v2[i + 1]
                elif axis == 'z':
                    for i, idx in enumerate(obj_idx):
                        if i < max(obj_idx):
                            oblist[obj_idx[i + 1]].location.z = oblist[idx].location.z + \
                                c_to_v1[i] + d + c_to_v2[i + 1]
            else:
                c_to_v1, c_to_v2 = find_c_to_v(obj_idx, axis)
                if axis == 'x':
                    for i, idx in enumerate(obj_idx):
                        if i < max(obj_idx):
                            oblist[obj_idx[i + 1]].location.x = oblist[idx].location.x + \
                                c_to_v1[i] + spacing + c_to_v2[i + 1]
                elif axis == 'y':
                    for i, idx in enumerate(obj_idx):
                        if i < max(obj_idx):
                            oblist[obj_idx[i + 1]].location.y = oblist[idx].location.y + \
                                c_to_v1[i] + spacing + c_to_v2[i + 1]
                elif axis == 'z':
                    for i, idx in enumerate(obj_idx):
                        if i < max(obj_idx):
                            oblist[obj_idx[i + 1]].location.z = oblist[idx].location.z + \
                                c_to_v1[i] + spacing + c_to_v2[i + 1]


def distribute_2():
    """
    Distributes objects from their centers or edges when 2 blign objects are added.
    Arguments
    ---------

    Returns
    -------
    """
    indicate = bpy.context.scene.object_settings.indicate_spacing2
    oblist = bpy.context.selected_objects
    dist_type = bpy.context.scene.object_settings.distribute_ops2

    if dist_type == 'center':
        if len(oblist) > 1:
            if not indicate:
                default_spacing_x, obj_idx_x = find_default_spacing('x')
                for i, idx in enumerate(obj_idx_x):
                    oblist[idx].location.x = oblist[obj_idx_x[0]].location.x + \
                        default_spacing_x * i
                default_spacing_y, obj_idx_y = find_default_spacing('y')
                for i, idx in enumerate(obj_idx_y):
                    oblist[idx].location.y = oblist[obj_idx_y[0]].location.y + \
                        default_spacing_y * i
                default_spacing_z, obj_idx_z = find_default_spacing('z')
                for i, idx in enumerate(obj_idx_z):
                    oblist[idx].location.z = oblist[obj_idx_z[0]].location.z + \
                        default_spacing_z * i
            else:
                spacing = bpy.context.scene.object_settings.Spacing2
                p1, p2 = [np.array(o.location)
                          for o in bpy.data.objects if o.blign]
                v = p2 - p1
                u = v / np.linalg.norm(v)
                i = 0
                for obj in bpy.context.selected_objects:
                    obj.location.x = p1[0] + u[0] * spacing * i
                    obj.location.y = p1[1] + u[1] * spacing * i
                    obj.location.z = p1[2] + u[2] * spacing * i
                    i += 1


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
        If number of blign objects = 0, aligns selected objects to the selected axis or plane.
        """
        i = count_blign_objects()
        plane = bpy.context.scene.object_settings.check_plane0

        if i == 0:
            if plane == False:
                align_axis_0()
            else:
                align_plane_0()
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
        i = count_blign_objects()
        plane = bpy.context.scene.object_settings.check_plane1

        if i == 1:
            if plane == False:
                align_axis_1()
            else:
                align_plane_1()
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
        if count_blign_objects() == 2:
            align_2()
        else:
            pass

        return {'FINISHED'}


class Blign_Distribute_Button0(bpy.types.Operator):
    """Defines the Distribute button."""
    bl_idname = "rigidbody.blign_distribute_button0"
    bl_label = "Distribute"
    bl_description = "Distribute objects"

    def execute(self, context):
        indicate = bpy.context.scene.object_settings.indicate_spacing0
        axis = bpy.context.scene.object_settings.Axis0
        dist_type = bpy.context.scene.object_settings.distribute_ops0
        spacing = bpy.context.scene.object_settings.Spacing0

        if count_blign_objects() != 2:
            distribute_0_or_1(indicate, axis, dist_type, spacing)
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
        dist_type = bpy.context.scene.object_settings.distribute_ops1
        spacing = bpy.context.scene.object_settings.Spacing1

        if count_blign_objects() != 2:
            distribute_0_or_1(indicate, axis, dist_type, spacing)
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
        if count_blign_objects() == 2:
            distribute_2()
        else:
            pass

        return {'FINISHED'}


class BLIGN_PT_Blign(bpy.types.Panel):
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
        items=[("x", "x", "Align objects in the x direction"),
               ("y", "y", "Align objects in the y direction"),
               ("z", "z", "Align objects in the z direction")],
        default='x',
        options={'HIDDEN'},
    )

    check_plane0: bpy.props.BoolProperty(
        name="Align to Plane",
        description="Choose whether or not to align objects to a plane",
        options={'HIDDEN'},
        default=False
    )

    Plane0: bpy.props.EnumProperty(
        name="Plane",
        items=[("y-z", "y-z", "Align objects to the y-z plane"),
               ("x-z", "x-z", "Align objects to the x-z plane"),
               ("x-y", "x-y", "Align objects to the x-y plane")],
        default='y-z',
        options={'HIDDEN'},
    )

    Axis1: bpy.props.EnumProperty(
        name="Axis",
        items=[("x", "x", "Align objects in the x direction"),
               ("y", "y", "Align objects in the y direction"),
               ("z", "z", "Align objects in the z direction")],
        default='x',
        options={'HIDDEN'},
    )

    check_plane1: bpy.props.BoolProperty(
        name="Align to Plane",
        description="Choose whether or not to align objects to a plane",
        options={'HIDDEN'},
        default=False
    )

    Plane1: bpy.props.EnumProperty(
        name="Plane",
        items=[("y-z", "y-z", "Align objects to the y-z plane"),
               ("x-z", "x-z", "Align objects to the x-z plane"),
               ("x-y", "x-y", "Align objects to the x-y plane")],
        default='y-z',
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

    x_selected0: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+y", "+y", "Align objects to their most positive point in the y direction"),
               ("-y", "-y", "Align objects to their most negative point in the y direction"),
               ("+z", "+z", "Align objects to their most positive point in the z direction"),
               ("-z", "-z", "Align objects to their most negative point in the z direction")],
        default='center',
        options={'HIDDEN'},
    )

    y_selected0: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+x", "+x", "Align objects to their most positive point in the x direction"),
               ("-x", "-x", "Align objects to their most negative point in the x direction"),
               ("+z", "+z", "Align objects to their most positive point in the z direction"),
               ("-z", "-z", "Align objects to their most negative point in the z direction")],
        default='center',
        options={'HIDDEN'},
    )

    z_selected0: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+x", "+x", "Align objects to their most positive point in the x direction"),
               ("-x", "-x", "Align objects to their most negative point in the x direction"),
               ("+y", "+y", "Align objects to their most positive point in the y direction"),
               ("-y", "-y", "Align objects to their most negative point in the y direction")],
        default='center',
        options={'HIDDEN'},
    )

    yz_selected0: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+x", "+x", "Align objects to their most positive point in the y direction"),
               ("-x", "-x", "Align objects to their most negative point in the y direction")],
        default='center',
        options={'HIDDEN'},
    )

    xz_selected0: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+y", "+y", "Align objects to their most positive point in the y direction"),
               ("-y", "-y", "Align objects to their most negative point in the y direction")],
        default='center',
        options={'HIDDEN'},
    )

    xy_selected0: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+z", "+z", "Align objects to their most positive point in the y direction"),
               ("-z", "-z", "Align objects to their most negative point in the y direction")],
        default='center',
        options={'HIDDEN'},
    )

    x_selected1: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+y", "+y", "Align objects to their most positive point in the y direction"),
               ("-y", "-y", "Align objects to their most negative point in the y direction"),
               ("+z", "+z", "Align objects to their most positive point in the z direction"),
               ("-z", "-z", "Align objects to their most negative point in the z direction")],
        default='center',
        options={'HIDDEN'},
    )

    y_selected1: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+x", "+x", "Align objects to their most positive point in the x direction"),
               ("-x", "-x", "Align objects to their most negative point in the x direction"),
               ("+z", "+z", "Align objects to their most positive point in the z direction"),
               ("-z", "-z", "Align objects to their most negative point in the z direction")],
        default='center',
        options={'HIDDEN'},
    )

    z_selected1: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+x", "+x", "Align objects to their most positive point in the x direction"),
               ("-x", "-x", "Align objects to their most negative point in the x direction"),
               ("+y", "+y", "Align objects to their most positive point in the y direction"),
               ("-y", "-y", "Align objects to their most negative point in the y direction")],
        default='center',
        options={'HIDDEN'},
    )

    yz_selected1: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+x", "+x", "Align objects to their most positive point in the y direction"),
               ("-x", "-x", "Align objects to their most negative point in the y direction")],
        default='center',
        options={'HIDDEN'},
    )

    xz_selected1: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+y", "+y", "Align objects to their most positive point in the y direction"),
               ("-y", "-y", "Align objects to their most negative point in the y direction")],
        default='center',
        options={'HIDDEN'},
    )

    xy_selected1: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+z", "+z", "Align objects to their most positive point in the y direction"),
               ("-z", "-z", "Align objects to their most negative point in the y direction")],
        default='center',
        options={'HIDDEN'},
    )

    top_row2: bpy.props.BoolProperty(
        name="",
        description="If this button is clicked, options from the top row are available",
        options={'HIDDEN'},
        default=True
    )

    bottom_row2: bpy.props.BoolProperty(
        name="",
        description="If this button is clicked, options from the bottom row are available",
        options={'HIDDEN'},
        default=False
    )

    align_to_2_ops: bpy.props.EnumProperty(
        name="Align to",
        items=[("center", "Center", "Align to center of object"),
               ("+x", "+x", "Align objects to their most positive point in the x direction"),
               ("-x", "-x", "Align objects to their most negative point in the x direction"),
               ("+y", "+y", "Align objects to their most positive point in the y direction"),
               ("-y", "-y", "Align objects to their most negative point in the y direction"),
               ("+z", "+z", "Align objects to their most positive point in the z direction"),
               ("-z", "-z", "Align objects to their most negative point in the z direction")],
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
        items=[("center", "Center", "Distribute from center of object")],
        #    ("edge", "Edge", "Distribute from edge of object")],
        default='center',
        options={'HIDDEN'},
    )


class BLIGN_PT_Blign_Principal_Axes(bpy.types.Panel):
    """Class that outlines the Align tab."""
    bl_label = "Principal Axes/Planes"
    bl_parent_id = "BLIGN_PT_Blign"
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
        check_plane = bpy.context.scene.object_settings.check_plane0
        plane = bpy.context.scene.object_settings.Plane0

        row = layout.row()
        if check_plane == False:
            row.prop(settings, "Axis0", expand=True)
        elif check_plane == True:
            row.prop(settings, "Plane0", expand=True)

        if check_plane == False:
            if axis == 'x':
                row = layout.row()
                row.prop(settings, "x_selected0")
            elif axis == 'y':
                row = layout.row()
                row.prop(settings, "y_selected0")
            elif axis == 'z':
                row = layout.row()
                row.prop(settings, "z_selected0")
        elif check_plane == True:
            if plane == 'y-z':
                row = layout.row()
                row.prop(settings, "yz_selected0")
            elif plane == 'x-z':
                row = layout.row()
                row.prop(settings, "xz_selected0")
            elif plane == 'x-y':
                row = layout.row()
                row.prop(settings, "xy_selected0")

        row = layout.row()
        row.alignment = 'RIGHT'
        row.prop(settings, "check_plane0")

        row = layout.row()
        row.operator('rigidbody.blign_align_button0')

        row = layout.row()
        row.prop(settings, "distribute_ops0", expand=True)

        row = layout.row()
        row.prop(settings, "indicate_spacing0")
        row.prop(settings, 'Spacing0')

        row = layout.row()
        row.operator('rigidbody.blign_distribute_button0')


class BLIGN_PT_Blign_One_Object(bpy.types.Panel):
    """Class that outlines the Align to One Object tab."""
    bl_label = "Align to One Object"
    bl_parent_id = "BLIGN_PT_Blign"
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
        check_plane = bpy.context.scene.object_settings.check_plane1
        plane = bpy.context.scene.object_settings.Plane1

        row = layout.row()
        if check_plane == False:
            row.prop(settings, "Axis1", expand=True)
        elif check_plane == True:
            row.prop(settings, "Plane1", expand=True)

        if check_plane == False:
            if axis == 'x':
                row = layout.row()
                row.prop(settings, "x_selected1")
            elif axis == 'y':
                row = layout.row()
                row.prop(settings, "y_selected1")
            elif axis == 'z':
                row = layout.row()
                row.prop(settings, "z_selected1")
        elif check_plane == True:
            if plane == 'y-z':
                row = layout.row()
                row.prop(settings, "yz_selected1")
            elif plane == 'x-z':
                row = layout.row()
                row.prop(settings, "xz_selected1")
            elif plane == 'x-y':
                row = layout.row()
                row.prop(settings, "xy_selected1")

        row = layout.row()
        row.alignment = 'RIGHT'
        row.prop(settings, "check_plane1")

        row = layout.row()
        row.operator('rigidbody.blign_align_button1')

        row = layout.row()
        row.prop(settings, "distribute_ops1", expand=True)

        row = layout.row()
        row.prop(settings, "indicate_spacing1")
        row.prop(settings, 'Spacing1')

        row = layout.row()
        row.operator('rigidbody.blign_distribute_button1')


class BLIGN_PT_Blign_Two_Objects(bpy.types.Panel):
    """Class that outlines the Align to Two Objects tab."""
    bl_label = "Align to Two Objects"
    bl_parent_id = "BLIGN_PT_Blign"
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
        row.prop(settings, "align_to_2_ops")

        row = layout.row()
        row.operator('rigidbody.blign_align_button2')

        # row = layout.row()
        # row.prop(settings, "distribute_ops2", expand=True)

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
    BLIGN_PT_Blign,
    BlignSettings,
    BLIGN_PT_Blign_Principal_Axes,
    BLIGN_PT_Blign_One_Object,
    BLIGN_PT_Blign_Two_Objects,
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
    bpy.types.Object.blign = bpy.props.BoolProperty(name="BLIGN_PT_Blign")


def unregister():
    """Unregisters classes."""

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.object_settings
    del bpy.types.Object.blign
