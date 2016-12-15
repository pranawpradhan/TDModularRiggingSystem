#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem.lib import System as System

#背骨のリギング
class TDSpineRigging():
    def __init__(self):
        #TDMRS.__init__()
        self.System  = System.ModularRiggingSystem()
        self.spineCtls    = [] #背骨コントローラー
        self.spineCtlOffset  = [] #背骨コントローラーのオフセットノード
        self.spineCtlNull = [] #背骨コントローラーのヌルノード
        self.spineNull    = [] #背骨ジョイントのオフセットノード
    """
    "-----コマンドの実行-----"
    def setSpineRigging(self,spineJoints,CtlColor,CtlScale):#,parentName,
        TDSpineRigging.createSpineJoint(self,spineJoints)
        TDSpineRigging.createSpineFKJoint(self,spineJoints)
        self.SpineCtlList = TDSpineRigging.createSpineFKCtl(self,spineJoints,CtlColor,CtlScale)
        TDSpineRigging.createSpineFKCtlConnection(self,spineJoints)
        self.SpineJointGrp = TDSpineRigging.setSpineRigLayering(self,spineJoints[0])
        #TDSpineRigging.createSpineNull(self)
        #TDSpineRigging.createSpineCtlNull(self)
        #self.rootConstraintGPList = TDSpineRigging.createRootCtlConstraint(self,parentName)

        print "--result Spine setup--\n",
        return [self.SpineCtlList[0],self.SpineCtlList[1],self.SpineJointGrp[0],self.SpineJointGrp[1]]
    """

    #背骨リグ用の新しいジョイントを作成
    def createSpineJoint(self,spineJoints):
        self.spineJoint = self.System.createRiggingJoint(spineJoints,1,"Add")

        return self.spineJoint

    #FKの背骨のジョイントを作成
    def createSpineFKJoint(self,spineJoints):
        self.FKSpineJoint = self.System.createRiggingJoint(spineJoints,0,"FK")

        return self.FKSpineJoint

    #FKの背骨のコントローラーの作成
    def createSpineFKCtl(self,spineJoints,CtlColor,CtlScale):
        for spines in range(len(spineJoints)):
            self.spineCtl = self.System.createRigController(self.System.TDcrc.TDCircle,"FK_"+spineJoints[spines],spineJoints[spines],CtlColor,20*CtlScale)
            if spines > 0:
                cmds.parent(self.spineCtl[0],self.spineCtls[spines-1])
            self.spineCtls.append(self.spineCtl[1])
            self.spineCtlOffset.append(self.spineCtl[0])

        self.spineCtlGP = self.System.createGP(self.spineCtlOffset[0],"%s_Grp"%self.spineCtls[0])
        return [self.spineCtlGP, self.spineCtls[-1]]

    #FK背骨コントローラーの関連付け
    def createSpineFKCtlConnection(self,spineJoints):
        for spines in range(len(spineJoints)):
            #cmds.parentConstraint(self.FKSpineJoint[spines],self.spineJoint[spines],mo=True)
            #cmds.parentConstraint(self.spineCtls[spines],self.FKSpineJoint[spines],mo=True)
            self.System.matrixConstraint(self.FKSpineJoint[spines],self.spineJoint[spines])
            self.System.matrixConstraint(self.spineCtls[spines],self.FKSpineJoint[spines])

    #背骨リグの階層分け
    def createSpineRigConnectNull(self,spineJoints):
        self.ConnectionGrp = self.System.createModuleConnectionNull(self.spineCtlGP, spineJoints)
        self.spineCtlGrp = cmds.group(self.ConnectionGrp,name="%s_Ctl_Grp"%spineJoints)
        self.spineJointGrp = cmds.group(self.spineJoint[0],self.FKSpineJoint[0],name="%s_Joint_Grp"%spineJoints)

        return self.spineJointGrp,self.ConnectionGrp
    """
    #背骨ジョイントのオフセットノードを作成
    def createSpineNull(self):
        for spineNulls in self.getSpineJoint():
            self.spineNullGP = self.createGP(spineNulls,"%s_Offset"%spineNulls)
            self.spineNull.append(self.spineNullGP)

    #背骨コントローラーのオフセットノードを作成
    def createSpineCtlNull(self):
        for spineCtlNulls in self.spineCtls:
            self.spineCtlNullGP = self.createGP(spineCtlNulls,"%s_Offset"%spineNulls)
            self.spineCtlNull.append(self.spineCtlNullGP)

    #ルートコントローラー関連づけ用のヌルを作成
    def createRootCtlConstraint(self,parentName):
        self.rootConstraintGP = self.System.createModuleParentNull(parentName,self.spineCtls[0])

        return self.rootConstraintGP
    """