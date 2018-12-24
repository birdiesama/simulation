### revamped version , 2018/10/10 , (c) RiFF Animation Studio, Weerapot C. ### 

import pymel.core as pm ;

class General ( object ) :

    def __init__ ( self ) :
        super ( General , self ).__init__() ;

        self.colorDict = {} ;
        self.colorDict [ 'green' ]      = ( 0 , 1 , 0 ) ;       
        self.colorDict [ 'lightBlue' ]  = ( 0 , 1 , 1 ) ;
        self.colorDict [ 'red' ]        = ( 1 , 0 , 0 ) ;
        self.colorDict [ 'yellow' ]     = ( 1 , 1 , 0 ) ;
        self.colorDict [ 'white' ]      = ( 1 , 1 , 1 ) ;

    def clean ( self , target ) :
        # freeze transform, delete history
        target = pm.PyNode ( target ) ;
        pm.makeIdentity ( target , apply = True ) ;
        pm.delete ( target , ch = True ) ;

    def lockHideAttr ( self , target , attr ) :
        target = pm.PyNode ( target ) ;
        pm.setAttr ( target + '.' + attr , lock = True , keyable = False , channelBox = False ) ;

    def lockAllAttr ( self , target ) :
        target = pm.PyNode ( target ) ;
        for attr in [ 't' , 'r' , 's' ] :
            for axis in [ 'x' , 'y' , 'z' ] :
                pm.setAttr ( target + '.' + attr + axis , lock = True ) ;

    def setColor ( self , target , color ) :

        target      = pm.PyNode ( target ) ;
        targetShape = target.getShape() ; 

        targetShape.overrideEnabled.set ( True ) ;
        targetShape.overrideRGBColors.set ( True ) ;

        targetShape.overrideColorRGB.set ( color ) ;

class NucleusRig ( object ) :

    def __init__ ( self ) :

        super ( NucleusRig , self ).__init__() ;

        self.placementCtrl_point = [ ( -46.293479 , 0 , 11.57337 ) , ( -46.293479 , 0 , 23.14674 ) , ( -69.440219 , 0 , 0 ) , ( -46.293479 , 0 , -23.14674 ) , ( -46.293479 , 0 , -11.57337 ) , ( -23.14674 , 0 , -11.57337 ) , ( -11.57337 , 0 , -23.14674 ) , ( -11.57337 , 0 , -46.293479 ) , ( -23.14674 , 0 , -46.293479 ) , ( 0 , 0 , -69.440219 ) , ( 23.14674 , 0 , -46.293479 ) , ( 11.57337 , 0 , -46.293479 ) , ( 11.57337 , 0 , -23.14674 ) , ( 23.14674 , 0 , -11.57337 ) , ( 46.293479 , 0 , -11.57337 ) , ( 46.293479 , 0 , -23.14674 ) , ( 69.440219 , 0 , 0 ) , ( 46.293479 , 0 , 23.14674 ) , ( 46.293479 , 0 , 11.57337 ) , ( 23.14674 , 0 , 11.57337 ) , ( 11.57337 , 0 , 23.14674 ) , ( 11.57337 , 0 , 46.293479 ) , ( 23.14674 , 0 , 46.293479 ) , ( 0 , 0 , 69.440219 ) , ( -23.14674 , 0 , 46.293479 ) , ( -11.57337 , 0 , 46.293479 ) , ( -11.57337 , 0 , 23.14674 ) , ( -23.14674 , 0 , 11.57337 ) , ( -46.293479 , 0 , 11.57337 ) ] ;

        self.nucleusCtrl_point = [ ( -5.96046e-007 , 0 , 20.000002 ) , ( 0 , 0 , 0 ) , ( -5.96046e-007 , 0 , 20.000002 ) , ( 6.180339 , 0 , 19.021132 ) , ( 11.755705 , 0 , 16.180342 ) , ( 16.18034 , 0 , 11.755706 ) , ( 19.021132 , 0 , 6.18034 ) , ( 20 , 0 , 0 ) , ( 0 , 0 , 0 ) , ( 20 , 0 , 0 ) , ( 19.021143 , 0 , -6.180344 ) , ( 16.180351 , 0 , -11.755713 ) , ( 11.755713 , 0 , -16.180349 ) , ( 6.180343 , 0 , -19.021141 ) , ( 0 , 0 , -20.00001 ) , ( 0 , 0 , 0 ) , ( 0 , 0 , -20.00001 ) , ( -6.180343 , 0 , -19.021139 ) , ( -11.75571 , 0 , -16.180346 ) , ( -16.180346 , 0 , -11.755709 ) , ( -19.021135 , 0 , -6.180341 ) , ( -20.000004 , 0 , 0 ) , ( 0 , 0 , 0 ) , ( -20.000004 , 0 , 0 ) , ( -19.021135 , 0 , 6.180341 ) , ( -16.180344 , 0 , 11.755707 ) , ( -11.755707 , 0 , 16.180342 ) , ( -6.180341 , 0 , 19.021133 ) , ( -5.96046e-007 , 0 , 20.000002 ) , ( 0 , 0 , 0 ) , ( 0 , -40 , 0 ) , ( -1.24252e-007 , -40 , 4.16921 ) , ( 0 , -44.169209 , 0 ) , ( -4.169211 , -40 , 0 ) , ( 0 , -40 , 0 ) , ( 0 , -40 , -4.169212 ) , ( 0 , -44.169209 , 0 ) , ( 4.16921 , -40 , 0 ) , ( 0 , -40 , 0 ) , ( 4.16921 , -40 , 0 ) , ( 3.965157 , -40 , -1.288357 ) , ( 3.372964 , -40 , -2.450602 ) , ( 2.450602 , -40 , -3.372964 ) , ( 1.288357 , -40 , -3.965156 ) , ( 0 , -40 , -4.169212 ) , ( -1.288357 , -40 , -3.965156 ) , ( -2.450601 , -40 , -3.372963 ) , ( -3.372963 , -40 , -2.450601 ) , ( -3.965155 , -40 , -1.288357 ) , ( -4.169211 , -40 , 0 ) , ( -3.965155 , -40 , 1.288357 ) , ( -3.372962 , -40 , 2.450601 ) , ( -2.450601 , -40 , 3.372962 ) , ( -1.288357 , -40 , 3.965155 ) , ( -1.24252e-007 , -40 , 4.16921 ) , ( 1.288357 , -40 , 3.965155 ) , ( 2.4506 , -40 , 3.372962 ) , ( 3.372962 , -40 , 2.4506 ) , ( 3.965154 , -40 , 1.288357 ) , ( 4.16921 , -40 , 0 ) ] ;
        self.nucleusGimbalCtrl_point = [ ( 9.747901 , 0 , -9.747901 ) , ( 0 , -44.169209 , 0 ) , ( -9.747901 , 0 , -9.747901 ) , ( 0 , -44.169209 , 0 ) , ( -9.747901 , 0 , 9.747901 ) , ( 0 , -44.169209 , 0 ) , ( 9.747901 , 0 , 9.747901 ) , ( 9.747901 , 0 , -9.747901 ) , ( -9.747901 , 0 , -9.747901 ) , ( -9.747901 , 0 , 9.747901 ) , ( 9.747901 , 0 , 9.747901 ) ] ;

        self.windCtrl_point = [(0.0, 3.814697265625e-06, -4.184723690530397e-07), (-8.758682668030815e-08, -0.9549121856689453, 1.6732058720378236), (-1.205529258641036e-07, -2.0610740184783936, 3.0261625022715632), (-1.4171847340094246e-07, -3.4549150466918945, 3.917204030716436), (-1.4901161193847656e-07, -5.0, 4.2490761342554455), (-1.4171847340094246e-07, -6.5450849533081055, 3.917204030716436), (-1.205529258641036e-07, -7.9389262199401855, 3.0261625022715632), (-8.758682668030815e-08, -9.045084953308105, 1.6732058720378236), (0.0, -9.999999046325684, -4.184723690530397e-07), (0.0, -10.954914093017578, -1.6732070176422205), (0.0, -12.061073303222656, -3.0261641151741028), (0.0, -13.454915046691895, -3.9172063445661895), (0.0, -15.0, -4.249077980807056), (0.0, -16.54508399963379, -3.9172063445661895), (0.0, -17.938926696777344, -3.0261641151741028), (0.0, -19.045085906982422, -1.6732070176422205), (0.0, -20.0, -4.184723690530397e-07), (-8.758682668030815e-08, -20.954914093017578, 1.6732058720378236), (-1.205529258641036e-07, -22.061073303222656, 3.0261625022715632), (-1.4171847340094246e-07, -23.45491600036621, 3.917204030716436), (-1.4901161193847656e-07, -25.0, 4.2490761342554455), (-1.4171847340094246e-07, -26.54508399963379, 3.917204030716436), (-1.205529258641036e-07, -27.938926696777344, 3.0261625022715632), (-8.758682668030815e-08, -29.045085906982422, 1.6732058720378236), (0.0, -30.0, -4.184723690530397e-07), (0.0, -30.954912185668945, -1.6732070176422205), (0.0, -32.061073303222656, -3.0261641151741028), (0.0, -33.45491409301758, -3.9172063445661895), (0.0, -35.0, -4.249077980807056), (0.0, -36.54508590698242, -3.9172063445661895), (0.0, -37.938926696777344, -3.0261641151741028), (0.0, -39.04508972167969, -1.6732070176422205), (0.0, -40.00000762939453, -4.184723690530397e-07)] ;

        

        self.posDict = {} ;
        self.posDict [ 'up' ]       = [ 'tx' , 10 ] ;
        self.posDict [ 'down' ]     = [ 'tx' , -10 ] ;
        self.posDict [ 'left' ]     = [ 'tz' , 10 ] ;
        self.posDict [ 'right' ]    = [ 'tz' , -10 ] ;

    def createNucleusRigGroup ( self ) :

        nucleusRigGroupName = 'NucleusRig_Grp' ;

        if not pm.objExists ( nucleusRigGroupName ) :
            nucleusRigGrp = pm.group ( em = True , w = True , n = nucleusRigGroupName ) ;
        else :
            nucleusRigGrp = pm.PyNode ( nucleusRigGroupName ) ;

        return nucleusRigGrp ;

    def createCtrl ( self , name , point ) :
        # return ctrl , zroGrp

        ctrl = pm.curve ( d = 1 , point = point ) ;
        ctrl.rename ( name + '_Ctrl' ) ;

        for attr in [ 'sx' , 'sy' , 'sz' ] :
            self.clean ( target = ctrl ) ;
            # self.lockHideAttr ( target = ctrl , attr = attr ) ;

        ctrlZroGrp = pm.group ( em = True , w = True , n = name + 'CtrlZro_Grp' ) ;
        # self.lockAllAttr ( target = ctrlZroGrp ) ;

        pm.parent ( ctrl , ctrlZroGrp ) ;

        return ctrl , ctrlZroGrp ;

    def createNucleusIndividualRig ( self , nucleus ) :
        # return currentNucleusRigGrp , nucleusCtrl , windCtrl ;

        nucleusRigGrp = self.createNucleusRigGroup() ;

        currentNucleusRigGrp = pm.group ( em = True , n = nucleus.nodeName() + 'Rig_Grp' ) ;
        pm.parent ( currentNucleusRigGrp , nucleusRigGrp ) ;

        nucleus = pm.PyNode ( nucleus ) ;

        ### Nucleus Ctrl ###

        product_list    = self.createCtrl ( name = nucleus.nodeName() , point = self.nucleusCtrl_point ) ;
        nucleusCtrl     = product_list[0] ;
        nucleusCtrlShape = nucleusCtrl.getShape() ;
        nucleusCtrlZro  = product_list[1] ;

        product_list = self.createCtrl ( name = nucleus.nodeName() + 'Gmbl' , point = self.nucleusGimbalCtrl_point ) ;
        nucleusGmblCtrl     = product_list[0] ;
        nucleusGmblCtrlShape = nucleusGmblCtrl.getShape() ;
        self.setColor ( target = nucleusGmblCtrl , color = self.colorDict['white'] ) ;
        nucleusGmblCtrlZro  = product_list[1] ;

        pm.parent ( nucleusGmblCtrlZro , nucleusCtrl ) ;

        nucleusCtrlShape.addAttr ( 'gimbalCtrl' , keyable = True , attributeType = 'bool' ) ;
        nucleusCtrlShape.gimbalCtrl >> nucleusGmblCtrlShape.v ;

        gravityVtp = pm.createNode ( 'vectorProduct' ) ;
        gravityVtp.rename ( nucleus.nodeName() + 'Gravity_Vtp' ) ;

        nucleusGmblCtrl.worldMatrix >> gravityVtp.matrix ;

        gravityVtp.operation.set ( 3 ) ;
        gravityVtp.input1Y.set ( -1 ) ;
        gravityVtp.output >> nucleus.gravityDirection ;

        pm.parent ( nucleusCtrlZro , currentNucleusRigGrp ) ;

        ### Wind Ctrl ###

        product_list = self.createCtrl ( name = nucleus.nodeName() + 'Wind' , point = self.windCtrl_point ) ;
        windCtrl = product_list[0] ;
        self.setColor ( target = windCtrl , color = self.colorDict['white'] ) ;
        windCtrlZro = product_list[1] ;

        pm.parentConstraint ( nucleusCtrl , windCtrlZro , mo = False , skipTranslate = 'none' , skipRotate = [ 'x' , 'y' , 'z'] ) ;

        windVtp = pm.createNode ( 'vectorProduct' ) ;
        windVtp.rename ( nucleus.nodeName() + 'Wind_Vtp' ) ;

        windCtrl.worldMatrix >> windVtp.matrix ;

        windVtp.operation.set ( 3 ) ;
        windVtp.input1Y.set ( -1 ) ;
        windVtp.output >> nucleus.windDirection ;

        pm.parent ( windCtrlZro , currentNucleusRigGrp ) ;

        ### Parent Constraint Ctrl to the Nucleus ###

        pm.parentConstraint ( nucleusCtrl , nucleus , mo = False , skipTranslate = 'none' , skipRotate = [ 'x' , 'y' , 'z'] ) ;

        return currentNucleusRigGrp , nucleusCtrl , windCtrl ;

    def createNucleusRig ( self , *args ) :

        selection = pm.ls ( sl = True ) ;

        nucleusRigGrp = self.createNucleusRigGroup() ;

        if len ( selection ) == 1 :
            
            nucleus = selection[0] ;

            product_list = self.createNucleusIndividualRig ( nucleus = nucleus ) ;
            rigGroup    = product_list[0] ;
            nucluesCtrl = product_list[1] ;
            windCtrl    = product_list[2] ;

            pm.parent ( rigGroup , nucleusRigGrp ) ;
        
        else :

            ### create placement controller ###

            placementCtrl = pm.curve ( d = 1 , p = self.placementCtrl_point ) ;
            placementCtrl.rename ( 'NucleusPlacement_Ctrl' ) ;

            self.clean ( target = placementCtrl ) ;

            for attr in [ 's' ] :
                for axis in [ 'x' , 'y' , 'z' ] :
                    self.lockHideAttr ( target = placementCtrl , attr = attr + axis ) ;

            pm.parent ( placementCtrl , nucleusRigGrp ) ;

            ### now dealing with selected nucleus(s) ###

            # create position list
            pos_list = [] ;

            refPivotGrp = pm.group ( em = True ) ;
            refPosGrp   = pm.group ( em = True ) ;
            pm.parent ( refPosGrp , refPivotGrp ) ;
            
            pm.xform ( refPivotGrp , ws = True , t = ( 0 , 0 , 10 ) ) ;
            pm.xform ( refPivotGrp , ws = True , rp = ( 0 , 0 , 0 ) ) ;

            rotateValue = 360.00 / len(selection) ;

            for i in range ( 0 , len(selection) ) :
                refPivotGrp.ry.set ( rotateValue * i ) ;
                pos = pm.xform ( refPosGrp , q = True , ws = True , t = True ) ;
                pos_list.append ( pos ) ;

            pm.delete ( refPivotGrp , refPosGrp ) ;

            # create individual nucleus rig
            
            nucluesCtrl_list = [] ;

            for nucleus in selection :

                product_list = self.createNucleusIndividualRig ( nucleus = nucleus ) ;
                rigGroup    = product_list[0] ;
                nucluesCtrl = product_list[1] ;
                nucluesCtrl_list.append ( nucluesCtrl ) ;
                windCtrl    = product_list[2] ;

                pm.parent ( rigGroup , placementCtrl ) ;

            # set nucleusRigPosition and color

            colorList = [ 'green' , 'lightBlue' , 'red' , 'yellow' ] ;

            for i in range ( 0 , len(nucluesCtrl_list) ) :
                pm.xform ( nucluesCtrl_list[i] , ws = True , t = pos_list[i] ) ;
                color = colorList [ i % len(colorList) ] ;
                self.setColor ( target = nucluesCtrl_list[i] , color = self.colorDict[color] ) ;

    def deleteNucleusRig ( self , *args ) :

        selection = pm.ls ( sl = True ) ;

        # check if selected nucleus rig group exists
        for nucleus in selection :
            
            if pm.objExists ( nucleus.nodeName() + 'Rig_Grp' ) :

                rigGroup = pm.PyNode ( nucleus.nodeName() + 'Rig_Grp' ) ;

                connectionList = pm.listConnections ( selection , type = 'parentConstraint' ) ;
                connectionList = set ( connectionList ) ;
                parConList = list ( connectionList ) ;
                
                pm.delete ( parConList ) ;
                pm.delete ( rigGroup ) ;

        if pm.objExists ( 'NucleusPlacement_Ctrl' ) :
            
            placementCtrl = pm.PyNode ( 'NucleusPlacement_Ctrl' ) ;

            if not placementCtrl.listRelatives ( ad = True , type = 'transform' ) :
                pm.delete ( placementCtrl ) ;

        if pm.objExists ( 'NucleusRig_Grp' ) :

            rigGrp = pm.PyNode ( 'NucleusRig_Grp' ) ;

            if not rigGrp.listRelatives ( ad = True , type = 'transform' ) :
                pm.delete ( rigGrp ) ;

class Main ( General , NucleusRig ) :

    def __init__ ( self ) :
        super ( Main , self ).__init__() ;

def attach ( *args ) :
    main = Main() ;
    main.createNucleusRig() ;

def detach ( *args ) :
    main = Main() ;
    main.deleteNucleusRig() ;

# def testRun ( *args ) :
#     detach() ;

# testRun () ;
