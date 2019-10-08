from bpy.app.handlers import persistent
import math
import mathutils
from gpu_extras.batch import batch_for_shader
import gpu
import bpy
import numpy as np
bl_info = {
    "name": "Blign",
    "author": "Team Wilmer",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D View Sidebar > Geometry tab",
    "description": "Align and distribute objects about an axis",
    "tracker_url": "",
    "category": "Geometry"
}


class Add_Object(bpy.types.Operator):
    bl_idname = "rigidbody.blign_add_object"
    bl_label = "Add Object"
    bl_description = "Set selected object as a blign object"

    @classmethod
    def poll(cls, context):
        if context.object:
            return context.object.type == 'MESH'

    def execute(self, context):
        for object in context.selected_objects:
            if not object.blign:
                context.view_layer.objects.active = object
                # Make sure it is a rigid body
                if object.rigid_body is None:
                    bpy.ops.rigidbody.object_add()

                # Sets object as blign object
                object.blign = True
        return {'FINISHED'}


class Remove_Object(bpy.types.Operator):
    bl_idname = "rigidbody.blign_remove_object"
    bl_label = "Remove Object"
    bl_description = "Remove object from as a blign object"

    @classmethod
    def poll(cls, context):
        if context.object:
            return context.object.blign

    def execute(self, context):
        for object in context.selected_objects:
            if object.blign:
                context.view_layer.objects.active = object

                # Remove rigidbody if not already removed
                if bpy.context.object.rigid_body:
                    bpy.ops.rigidbody.object_remove()

                context.object.blign = False
        return {'FINISHED'}


class Blign_Align_Button1(bpy.types.Operator):
    bl_idname = "rigidbody.blign_align_button1"
    bl_label = "Align"
    bl_description = "Align selected objects"

    # @classmethod
    # def poll(cls, context):
    #    if context.object.blign:
    #        return context.object.type == 'MESH'

    # Code that gives button function goes here
    def execute(self, context):
        axis = bpy.context.scene.object_settings.Axis
        if axis == 'x-axis':
            for object in context.selected_objects:
                object.location.y = 0
                object.location.z = 0

        elif axis == 'y-axis':
            for object in context.selected_objects:
                object.location.x = 0
                object.location.z = 0

        elif axis == 'z-axis':
            for object in context.selected_objects:
                object.location.x = 0
                object.location.y = 0

        return {'FINISHED'}


class Blign_Align_Button2(bpy.types.Operator):
    bl_idname = "rigidbody.blign_align_button2"
    bl_label = "Align"
    bl_description = "Align selected objects"

    # @classmethod
    # def poll(cls, context):
    #    if context.object.blign:
    #        return context.object.type == 'MESH'

    # Code that gives button function goes here
    # def execute(self, context):
    # Apply transforms to all selected projectile objects
    # apply_transforms(context)

    # return {'FINISHED'}


# edge cases still need to be addressed, i.e. what if only one object is selected
class Blign_Distribute_Button(bpy.types.Operator):
    bl_idname = "rigidbody.blign_distribute_button"
    bl_label = "Distribute"
    bl_description = "Distribute objects"

    # @classmethod
    # def poll(cls, context):
    #    if context.object.blign:
    #        return context.object.type == 'MESH'

    # Code that gives button function goes here
    def execute(self, context):
        #spacing = bpy.context.object.blign_props.Spacing
        axis = bpy.context.scene.object_settings.Axis
        oblist = bpy.context.selected_objects
        i = 0
        j = 0
        if axis == 'x-axis':
            xlist = []
            for object in oblist:
                loc = object.location.x
                xlist.append(loc)
                i += 1
            xlist.sort()
            distance = xlist[-1] - xlist[0]
            default_spacing = distance / (i - 1)
            for object in oblist:
                object.location.x = xlist[0] + default_spacing * j
                j += 1
        elif axis == 'y-axis':
            ylist = []
            for object in oblist:
                loc = object.location.y
                ylist.append(loc)
                i += 1
            ylist.sort()
            distance = ylist[-1] - ylist[0]
            default_spacing = distance / (i - 1)
            for object in oblist:
                object.location.y = ylist[0] + default_spacing * j
                j += 1
        elif axis == 'z-axis':
            zlist = []
            for object in oblist:
                loc = object.location.z
                zlist.append(loc)
                i += 1
            zlist.sort()
            distance = zlist[-1] - zlist[0]
            default_spacing = distance / (i - 1)
            for object in oblist:
                object.location.z = zlist[0] + default_spacing * j
                j += 1

        return {'FINISHED'}


class Blign(bpy.types.Panel):
    bl_label = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        ob = context.object
        if (ob and ob.blign):
            row = layout.row()
            if(len([object for object in context.selected_objects if object.blign])) > 1:
                row.operator(
                    'rigidbody.blign_remove_object', text="Remove Objects")
            else:
                row.operator('rigidbody.blign_remove_object')

        else:
            row = layout.row()
            if len(context.selected_objects) > 1:
                row.operator('rigidbody.blign_add_object',
                             text="Add Objects")
            else:
                row.operator('rigidbody.blign_add_object')


class BlignSettings(bpy.types.PropertyGroup):
    # all update lines have been removed and probably have some real function

    Spacing: bpy.props.IntProperty(
        name="Spacing",
        description="Set distribution value between objects",
        default=1,
        options={'HIDDEN'},
    )

    ob1: bpy.props.FloatVectorProperty(
        name="Loc 1",
        description="Initial position for object 1",
        subtype='TRANSLATION',
        precision=4,
        options={'HIDDEN'},
    )

    ob2: bpy.props.FloatVectorProperty(
        name="Loc 2",
        description="Initial position for object 2",
        subtype='TRANSLATION',
        precision=4,
        options={'HIDDEN'},
    )

    Direction: bpy.props.EnumProperty(
        name="Direction",
        items=[("Positive", "+", "Align objects in the positive direction of axis"),
               ("Negative", "-", "Align objects in the negative direction of axis")],
        default='Positive',
        options={'HIDDEN'},
    )

    Axis: bpy.props.EnumProperty(
        name="Axis",
        items=[("x-axis", "x", "Align objects in the x direction"),
               ("y-axis", "y", "Align objects in the y direction"),
               ("z-axis", "z", "Align objects in the z direction")],
        default='x-axis',
        options={'HIDDEN'},
    )


class Blign_Align(bpy.types.Panel):
    bl_label = "Align"
    bl_parent_id = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    # This function makes drop down menus available or unavailable depending on whether or not the object is added or not
    # @classmethod
    # def poll(self, context):
    #    if context.object and context.object.blign:
    #        return True
    #    return False

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        settings = context.scene.object_settings

        row = layout.row()
        row.prop(settings, "Axis", expand=True)

        row = layout.row()
        row.operator('rigidbody.blign_align_button1')


class Blign_One_Object(bpy.types.Panel):
    bl_label = "Align to One Object"
    bl_parent_id = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    # @classmethod
    # def poll(self, context):
    #    if context.object and context.object.blign:
    #        return True
    #    return False

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        settings = context.scene.object_settings

        row = layout.row()
        row.prop(settings, "Axis", expand=True)

        row = layout.row()
        row.prop(settings, "Direction", expand=True)

        row = layout.row()
        row.operator('rigidbody.blign_align_button2')


class Blign_Two_Objects(bpy.types.Panel):
    bl_label = "Align to Two Objects"
    bl_parent_id = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    # @classmethod
    # def poll(self, context):
    #    if context.object and context.object.blign:
    #        return True
    #    return False

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        object = context.object

        row = layout.row()
        row.prop(object.blign_props, 'ob1')

        row = layout.row()
        row.prop(object.blign_props, 'ob2')

        row = layout.row()
        row.operator('rigidbody.blign_align_button2')


class Blign_Distribute(bpy.types.Panel):
    bl_label = "Distribute"
    bl_parent_id = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    # @classmethod
    # def poll(self, context):
    #    if context.object and context.object.blign:
    #        return True
    #    return False

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        object = context.object
        settings = context.scene.object_settings

        row = layout.row()
        row.prop(settings, "Axis", expand=True)

        row = layout.row()
        row.prop(object.blign_props, 'Spacing')

        row = layout.row()
        row.operator('rigidbody.blign_distribute_button')


classes = (
    Add_Object,
    Remove_Object,
    Blign_Align_Button1,
    Blign_Align_Button2,
    Blign_Distribute_Button,
    Blign,
    BlignSettings,
    Blign_Align,
    Blign_One_Object,
    Blign_Two_Objects,
    Blign_Distribute,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.object_settings = bpy.props.PointerProperty(
        type=BlignSettings)
    bpy.types.Object.blign = bpy.props.BoolProperty(name="Blign")
    bpy.types.Object.blign_props = bpy.props.PointerProperty(
        type=BlignSettings)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
