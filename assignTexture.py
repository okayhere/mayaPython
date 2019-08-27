import maya.cmds as cmds


def assignTexture(input, outputs):
    """ Get texture from input mesh and assign it to output mesh.
    
        Args:
            input (str): input mesh shape node name
            outputs (list(str)): output mesh shape node name
    """
    # get the shading group from input
    inputShader = _getShader(input)
       
    # check if file node exists
    nodeAttr = cmds.connectionInfo(inputShader + ".color", sourceFromDestination=True)    # file1.outColor
    
    # get the texturePath
    fileNode = nodeAttr.split(".")[0]
    texturePath = cmds.getAttr(fileNode + ".fileTextureName")
    
    # check if outputs already have texture
    for mesh in outputs:
        shader = _getShader(mesh)
        nodeAttr = cmds.connectionInfo(shader + ".color", sourceFromDestination=True)
    
        if nodeAttr == "":
            fileNode = _createFileNode(shader)
            cmds.setAttr(fileNode + ".fileTextureName", texturePath, type="string")
        else:
            fileNode = nodeAttr.split(".")[0]
            if cmds.getAttr(fileNode + ".fileTextureName") == "":
                cmds.setAttr(fileNode + ".fileTextureName", texturePath, type="string")

def _getShader(meshShape):
    """ Find shader node from mesh shape node
    
        Args:
            mesh (str): mesh shape node name
            
        Returns:
            shader (str): shader material node name
    """
    # get the shading group from input
    shadingGrps = cmds.listConnections(meshShape, type="shadingEngine")
    if len(shadingGrps) != 1:
       print("Shading Group node is not unique for {}".format(meshShape))
    shadingGrp = shadingGrps[0]
    # get the shader
    shaders = cmds.ls(cmds.listConnections(shadingGrp), materials=True)
    if len(shaders) != 1:
       print("Shader node is not unique for {}".format(shadingGrp))
    shader = shaders[0]    # lambert1
    
    return shader

def _createFileNode(shader):
    """ Create fileNode for shader and connect necessary attributes.
    
        Args:
            shader (str): shader material node name
            
        Returns:
            fileNode (str): created file node name
    """
    fileNode = cmds.shadingNode("file", asTexture=True, isColorManaged=True)
    p2t = cmds.shadingNode("place2dTexture", asUtility=True)

    cmds.connectAttr(p2t + ".coverage", fileNode + ".coverage", force=True)
    cmds.connectAttr(p2t + ".translateFrame", fileNode + ".translateFrame", force=True)
    cmds.connectAttr(p2t + ".rotateFrame", fileNode + ".rotateFrame", force=True)
    cmds.connectAttr(p2t + ".mirrorU", fileNode + ".mirrorU", force=True)
    cmds.connectAttr(p2t + ".mirrorV", fileNode + ".mirrorV", force=True)
    cmds.connectAttr(p2t + ".stagger", fileNode + ".stagger", force=True)
    cmds.connectAttr(p2t + ".wrapU", fileNode + ".wrapU", force=True)
    cmds.connectAttr(p2t + ".wrapV", fileNode + ".wrapV", force=True)
    cmds.connectAttr(p2t + ".repeatUV", fileNode + ".repeatUV", force=True)
    cmds.connectAttr(p2t + ".noiseUV", fileNode + ".noiseUV", force=True)
    cmds.connectAttr(p2t + ".offset", fileNode + ".offset", force=True)
    cmds.connectAttr(p2t + ".rotateUV", fileNode + ".rotateUV", force=True)
    cmds.connectAttr(p2t + ".vertexUvOne", fileNode + ".vertexUvOne", force=True)
    cmds.connectAttr(p2t + ".vertexUvTwo", fileNode + ".vertexUvTwo", force=True)
    cmds.connectAttr(p2t + ".vertexUvThree", fileNode + ".vertexUvThree", force=True)
    cmds.connectAttr(p2t + ".vertexCameraOne", fileNode + ".vertexCameraOne", force=True)
    cmds.connectAttr(p2t + ".outUV", fileNode + ".uv", force=True)
    cmds.connectAttr(p2t + ".outUvFilterSize", fileNode + ".uvFilterSize", force=True)
    cmds.connectAttr(fileNode + ".outColor", shader + ".color", force=True)
    
    return fileNode

    
# main
input = "pSphereShape1"
output = ["pSphereShape2", "pSphereShape3"]
assignTexture(input, output)
