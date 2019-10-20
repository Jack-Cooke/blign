import math
import mathutils
import bpy
import numpy as np
#from sympy import Eq, Symbol, solve
bl_info = {
    "name": "Blign",
    "author": "Wilmer Lab Group",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D View Sidebar > Geometry tab",
    "description": "Align and distribute objects about an axis",
    "tracker_url": "",
    "category": "Geometry"
}


class Add_Object(bpy.types.Operator):
    """Class that defines the Add Object button."""
    bl_idname = "rigidbody.blign_add_object"
    bl_label = "Add Object"
    bl_description = "Set selected object as a blign object"

    def execute(self, context):
        """Sets the object as object.blign."""
        for object in context.selected_objects:
            if not object.blign:
                context.view_layer.objects.active = object
                # Sets object as blign object
                object.blign = True

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
                # Sets object as blign object
                context.object.blign = False

        return {'FINISHED'}


class Blign_Align_Button1(bpy.types.Operator):
    """Class that defines Align button within the Align tab."""
    bl_idname = "rigidbody.blign_align_button1"
    bl_label = "Align"
    bl_description = "Align selected objects"

    def execute(self, context):
        """Moves objects to the chosen axis."""
        axis = bpy.context.scene.object_settings.Axis
        oblist = bpy.context.selected_objects
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

        return {'FINISHED'}


class Blign_Align_Button2(bpy.types.Operator):
    """Defines the Align button in the Align to One (and Two) Object tab."""
    bl_idname = "rigidbody.blign_align_button2"
    bl_label = "Align"
    bl_description = "Align selected objects"

    def execute(self, context):
        """Iterates through all objects, counts number of blign objects.

        If number of blign objects = 1, aligns selected objects to that one object.
        If number of blign objects = 2, will align all objects along the line between the 2 blign objects.
        """
        axis = bpy.context.scene.object_settings.Axis
        oblist = bpy.context.selected_objects
        i = 0
        for object in list(bpy.data.objects):
            if object.blign == True:
                i += 1

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
        # elif i == 2:
        #    blobs = []
        #    for object in list(bpy.data.objects):
        #        if object.blign == True:
        #            blobs.append(bpy.context.object.location)
        #    xdist = blobs[1][0] - blobs[0][0]
        #    ydist = blobs[1][1] - blobs[0][1]
        #    zdist = blobs[1][2] - blobs[0][2]

        #    v = mathutils.Vector((xdist, ydist, zdist))
        #    for object in oblist:
        #        # x = blobs[1][0] + v(0)t
        #        # y = blobs[1][1] + v(1)t
        #        # z = blobs[1][2] + v(2)t

        #        otherside = object.location.x * \
        #            v(0) + object.location.y * v(1) + object.location.z * v(2)
        #        t = Symbol('t')
        #        eqn = Eq(v(0)*(blobs[1][0]+v(0)*t)+v(1)*(blobs[1]
        #                                                 [1]+v(1)*t)+v(2)*(blobs[1][2]+v(2)*t), otherside)

        #        newt = solve(eqn)

        #        object.location.x = blobs[1][0] + v(0) * newt
        #        object.location.y = blobs[1][1] + v(1) * newt
        #        object.location.z = blobs[1][2] + v(2) * newt
        else:
            pass

        return {'FINISHED'}


# edge cases still need to be addressed, i.e. what if only one object is selected
class Blign_Distribute_Button(bpy.types.Operator):
    """Defines the Distribute button."""
    bl_idname = "rigidbody.blign_distribute_button"
    bl_label = "Distribute"
    bl_description = "Distribute objects"

    def execute(self, context):
        """Distributes objects between first and last object.

        Indicate = the indicate spacing button. If unchecked, evenly distributes shapes. 
        If checked, distributes objects 'spacing' units apart.
        """
        indicate = bpy.context.scene.object_settings.indicate_spacing
        axis = bpy.context.scene.object_settings.Axis
        oblist = bpy.context.selected_objects

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
            spacing = bpy.context.scene.object_settings.Spacing
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
        """
        layout = self.layout
        layout.use_property_split = True

        i = 0
        for object in list(bpy.data.objects):
            if object.blign == True:
                i += 1

        if (bpy.context.object.blign == True):
            row = layout.row()
            row.operator('rigidbody.blign_remove_object')
        elif (bpy.context.object.blign == False):
            if (i < 2):
                row = layout.row()
                row.operator('rigidbody.blign_add_object')


# Class that defines all simpler buttons
class BlignSettings(bpy.types.PropertyGroup):
    """All buttons used in the add-on are defined in this class."""
    Spacing: bpy.props.IntProperty(
        name="Spacing",
        description="Set distribution value between objects",
        default=1,
        options={'HIDDEN'},
    )

    indicate_spacing: bpy.props.BoolProperty(
        name="Indicate Spacing",
        description="Choose whether or not to indicate spacing betweeen objects",
        options={'HIDDEN'},
        default=False
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
    """Class that outlines the Align tab."""
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
        """The buttons within the tab are called here.

        settings is a PointerProperty that points to the class BlignSettings, where the buttons are defined.
        """
        layout = self.layout
        layout.use_property_split = True
        settings = context.scene.object_settings

        row = layout.row()
        row.prop(settings, "Axis", expand=True)

        row = layout.row()
        row.operator('rigidbody.blign_align_button1')


class Blign_One_Object(bpy.types.Panel):
    """Class that outlines the Align to One Object tab."""
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
        """The buttons within the Align to One Object tab are called here."""
        layout = self.layout
        layout.use_property_split = True
        settings = context.scene.object_settings

        row = layout.row()
        row.prop(settings, "Axis", expand=True)

        row = layout.row()
        row.operator('rigidbody.blign_align_button2')


class Blign_Two_Objects(bpy.types.Panel):
    """Class that outlines the Align to Two Objects tab."""
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

    # The buttons within the tab are called here
    def draw(self, context):
        """Buttons within Align to Two Objects tab are called here."""
        layout = self.layout
        layout.use_property_split = True

        # if len([o for o in context.selected_objects if o.blign]) == 2:
        #    align
        #    pass

        row = layout.row()
        row.operator('rigidbody.blign_align_button2')


class Blign_Distribute(bpy.types.Panel):
    """Class that outlines the Distribute tab."""
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
        """The buttons within the Distribute tab are called within this function."""
        layout = self.layout
        layout.use_property_split = True
        settings = context.scene.object_settings

        row = layout.row()
        row.prop(settings, "Axis", expand=True)

        row = layout.row()
        row.prop(settings, "indicate_spacing")

        row = layout.row()
        row.prop(settings, 'Spacing')

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
    """Registers classes and defines scene.object_settings and object.blign.

    Creates new subset of bpy.types.scene called object_Settings that points to BlignSettings.
    Creates new subset of bpy.types.object called blign.
    """
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.object_settings = bpy.props.PointerProperty(
        type=BlignSettings)
    bpy.types.Object.blign = bpy.props.BoolProperty(
        name="Blign")  # change bool to something


def unregister():
    """Unregisters classes."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
