import bpy

bl_info = {"name": "Align Shapes x",
           "author": "Team Cobra",
           "location": "View3D > Align > Shape > x axis",
           "version": (1, 0, 0),
           "blender": (2, 80, 0),
           "description": "Align shapes along the x axis",
           "category": "Align Shape", }


class AlignShapesx(bpy.types.Operator):
    bl_idname = "action.align_shapesx"
    bl_label = "Align Shapes x"

    def invoke(self, context, event):
        i = 0
        # in order to change spacing between objects, change the number that i is multiplied by in the for loop
        for object in list(bpy.context.collection.objects):
            object.select_set(state=True)
            object.location.x = i*10
            object.location.y = 0
            object.location.z = 0
            object.select_set(state=False)
            i += 1
        return {"FINISHED"}


classes = (AlignShapesx,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
