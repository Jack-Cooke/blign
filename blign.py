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


class Blign(bpy.types.Panel):
    bl_label = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True


class BlignSettings(bpy.types.PropertyGroup):
    Button: bpy.props.BoolProperty(
        name="Button",
        description="Does this make a button",
        options={'HIDDEN'},
        default=True,
    )

    Axis: bpy.props.EnumProperty(
        name="Axis",
        items=[("hi", "hi", "Hello my name is Jack"),
               ("bye", "bye", "Goodbye")],
        default='hi',
        options={'HIDDEN'},
    )


class Blign_Obect_Settings(bpy.types.Panel):
    bl_label = "Object Settings"
    bl_parent_id = "Blign"
    bl_category = "Geometry"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
# settings is needed as argument in row
        settings = context.scene.object_settings

# layout.row() creates a button on a new row

        row = layout.row()
        row.prop(settings, "Axis", expand=True)

        row = layout.row()
        row.prop(settings, "Button")


classes = (
    Blign,
    BlignSettings,
    Blign_Obect_Settings,


)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

# creates a new subset of bpy.context.scene called "object_settings"
# needs to point to the class where the info is given to the buttons, not to where "object settings" is actually used in Blign_Object_Settings

    bpy.types.Scene.object_settings = bpy.props.PointerProperty(
        type=BlignSettings)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
