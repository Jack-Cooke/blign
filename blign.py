from bpy.app.handlers import persistent
import math
import mathutils
from gpu_extras.batch import batch_for_shader
import gpu
import bpy
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


class Blign(bpy.types.Panel):
    bl_label = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        # settings = context.scene.object_settings

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

    Align: bpy.props.BoolProperty(
        name="Align",
        description="Aligns selected objects",
        options={'HIDDEN'},
        default=False,
    )

    Distribute: bpy.props.BoolProperty(
        name="Distribute",
        description="Distributes objects",
        options={'HIDDEN'},
        default=False,
    )

    Spacing: bpy.props.IntProperty(
        name="Spacing",
        description="Set distribution value between objects",
        default=1,
        options={'HIDDEN'},
    )
# these 2 were called s in projectile
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

    Positive: bpy.props.BoolProperty(
        name="Positive",
        description="Align objects in the positive x y or z direction",
        options={'HIDDEN'},
        default=True,
    )

    Negative: bpy.props.BoolProperty(
        name="Negative",
        description="Align objects in the negative x y or z direction",
        options={'HIDDEN'},
        default=False,
    )

    Axis: bpy.props.EnumProperty(
        name="Axis",
        items=[("x-axis", "x", "Align objects in the x direction"),
               ("y-axis", "y", "Align objects in the y direction"),
               ("z-axis", "z", "Align objects in the z direction")],
        default='x-axis',
        options={'HIDDEN'},
    )


class Blign_One_Object(bpy.types.Panel):
    bl_label = "One Object"
    bl_parent_id = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    # This function makes drop down menus available or unavailable depending on whether or not the object is added or not
    @classmethod
    def poll(self, context):
        if context.object and context.object.blign:
            return True
        return False

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
# settings is needed as argument in row
        settings = context.scene.object_settings

# layout.row() creates a button on a new row

        row = layout.row()
        row.prop(settings, "Axis", expand=True)

        row = layout.row()
        row.prop(settings, "Positive")

        row = layout.row()
        row.prop(settings, "Negative")


class Blign_Two_Objects(bpy.types.Panel):
    bl_label = "Two Objects"
    bl_parent_id = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(self, context):
        if context.object and context.object.blign:
            return True
        return False

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        object = context.object

        row = layout.row()
        row.prop(object.blign_props, 'ob1')

        row = layout.row()
        row.prop(object.blign_props, 'ob2')


class Align(bpy.types.Panel):
    bl_label = "Align"
    bl_parent_id = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(self, context):
        if context.object and context.object.blign:
            return True
        return False

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        settings = context.scene.object_settings

        row = layout.row()
        row.prop(settings, "Align")


class Distribute(bpy.types.Panel):
    bl_label = "Distribute"
    bl_parent_id = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(self, context):
        if context.object and context.object.blign:
            return True
        return False

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        object = context.object
        settings = context.scene.object_settings

        row = layout.row()
        row.prop(object.blign_props, 'Spacing')

        row = layout.row()
        row.prop(settings, "Distribute")


classes = (
    Add_Object,
    Remove_Object,
    Blign,
    BlignSettings,
    Blign_One_Object,
    Blign_Two_Objects,
    Align,
    Distribute,
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
