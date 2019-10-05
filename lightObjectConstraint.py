import maya.cmds as cmds
import mtoa.core

arnoldLightTransform = mtoa.core.createArnoldNode("aiAreaLight").name()
mayaLightShape = cmds.createNode("spotLight")

# listRelatives: find hierarchy in outliner
mayaLightTransform = cmds.listRelatives(mayaLightShape, parent=True)[0]

# point constraint
cmds.pointConstraint(arnoldLightTransform, mayaLightTransform)

# orient constraint
cmds.orientConstraint(arnoldLightTransform, mayaLightTransform)

# lock transform / rotation / scale
cmds.setAttr("{}.tx".format(mayaLightTransform), lock=True)
cmds.setAttr("{}.ty".format(mayaLightTransform), lock=True)
cmds.setAttr("{}.tz".format(mayaLightTransform), lock=True)
cmds.setAttr("{}.rx".format(mayaLightTransform), lock=True)
cmds.setAttr("{}.ry".format(mayaLightTransform), lock=True)
cmds.setAttr("{}.rz".format(mayaLightTransform), lock=True)
cmds.setAttr("{}.sx".format(mayaLightTransform), lock=True)
cmds.setAttr("{}.sy".format(mayaLightTransform), lock=True)
cmds.setAttr("{}.sz".format(mayaLightTransform), lock=True)

# light attribute
arnoldLightShape = cmds.listRelatives(arnoldLightTransform, children=True)[0]
cmds.connectAttr(arnoldLightShape + ".intensity", mayaLightShape + ".intensity")
