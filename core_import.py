import pymel.core as pm ;
import os ;

class Import_GUI ( object ) :
    
    def __init__ ( self ) :
        self.currentProjectPath = pm.workspace ( q = True , rootDirectory = True ) ;
        self.shotCachePath      = self.currentProjectPath + 'data/shotCache/' ;
        # D:/TwoHeroes/film001/q0420/s0160/spiderGirlGod_001/
        # D:/TwoHeroes/film001/q0420/s0160/spiderGirlGod_001/data/shotCache/

        # get cache list from shot cache path
        if os.listdir ( self.shotCachePath ) :
            self.shotCache_list = os.listdir ( self.shotCachePath ) ;
        else :
            self.shotCache_list = [] ;

        # get default cam cache path
        self.defaultCameraPath = self.shotCachePath ;

        for shotCache in self.shotCache_list :
            if '.cam' in shotCache :
                self.defaultCameraPath += shotCache + '/' ;

        # get default character path
        self.defaultCharacterPath = self.shotCachePath ;

        currentCharacter = self.currentProjectPath.split ( '/' ) ;
        for each in currentCharacter :
            if each == '' :
                currentCharacter.remove ( each ) ;
        currentCharacter = currentCharacter [-1] ;

        for shotCache in self.shotCache_list :
            if '.' + currentCharacter + '.' in shotCache :
                self.defaultCharacterPath += shotCache + '/' ;

        # get default character transform path
        self.animGrpPath = self.defaultCharacterPath + 'transformGrp/ANIM_GRP.ma' ;
        self.oriGrpPath  = self.defaultCharacterPath + 'transformGrp/ORI_GRP.ma' ;

        # get default dyn path
        self.defaultDynPath = self.currentProjectPath + 'cache/alembic/' ;
        if os.path.exists ( self.defaultDynPath + 'DYN_ABC/' ) :
            self.defaultDynPath += 'DYN_ABC/' ;
        if os.path.exists ( self.currentProjectPath + 'cache/DYN_ABC/' ) :
            self.defaultDynPath = self.currentProjectPath + 'cache/DYN_ABC/' ;


    def __str__ ( self ) :
        pass ;

    def __repr__ ( self ) :
        pass ;

    def bwdGrp ( self , *args ) :

        if pm.objExists ( 'BWD_GRP' ) :
            bwd_grp = pm.general.PyNode ( 'BWD_GRP' ) ;
        else :
            bwd_grp = pm.group ( em = True , w = True , n = 'BWD_GRP' ) ;
            bwd_grp.t.lock() ;
            bwd_grp.r.lock() ;
            bwd_grp.s.lock() ;

        return bwd_grp ;

    def cameraPathBrowse_cmd ( self , *args ) :
        defaultPath = pm.textField ( self.camPath_textField , q = True , tx = True ) ;
        camPath     = pm.fileDialog2 ( dir = defaultPath , fileMode = 1 ) ; 
        if camPath :
            camPath = camPath[0] ;

        pm.textField ( self.camPath_textField , e = True , tx = camPath ) ;

    def importCamBtn_cmd ( self , *args ) :

        camPath = pm.textField ( self.camPath_textField , q = True , tx = True ) ;

        if os.path.isfile ( camPath ) :
            bwd_grp = self.bwdGrp() ;
            pm.system.importFile ( camPath , namespace = 'CAM' , gr = True , groupName = 'CAM_GRP' ) ;  
            camTopNode = pm.listRelatives ( 'CAM_GRP' , children = True ) ;

            for each in camTopNode :
                each.t.lock() ;
                each.r.lock() ;
                each.s.lock() ;

            pm.parent ( camTopNode , bwd_grp ) ;
            pm.delete ( 'CAM_GRP' ) ;

    def importOriGrpBtn_cmd ( self , *args ) :
        if os.path.isfile ( self.oriGrpPath ) :
            pm.system.importFile ( self.oriGrpPath ) ;

    def importAnimGrpBtn_cmd ( self , *args ) :
        if os.path.isfile ( self.animGrpPath ) :
            pm.system.importFile ( self.animGrpPath ) ;

    def charPathBrowse_cmd ( self , *args ) :

        defaultPath = pm.textField ( self.charPath_textField , q = True , tx = True ) ;
        charPath    = pm.fileDialog2 ( dir = defaultPath , fileMode = 1 ) ;
        if charPath :
            charPath = charPath[0] ;

        pm.textField ( self.charPath_textField , e = True , tx = charPath ) ;

    def importCharBtn_cmd ( self , *args ) :

        charPath = pm.textField ( self.charPath_textField , q = True , tx = True ) ;

        if os.path.isfile ( charPath ) :
            bwd_grp = self.bwdGrp() ;
            pm.system.importFile ( charPath , namespace = 'ABC' , gr = True , groupName = 'ABC_GRP' ) ;
            charTopNode = pm.listRelatives ( 'ABC_GRP' , children = True ) [0] ;

            ### connect char cache to CIN ###

            # connect alembic to CIN shapes
            if pm.checkBox ( self.charImportType_cbx , q = True , v = True ) :
                
                children = pm.listRelatives ( charTopNode , c = True ) ;
                
                for child in children :

                    try :
                        driver  = child ;
                        driven  = child.split(':')[1] + '_CIN' ;
                        bsnName = child.split(':')[1] + '_AbcBSH' ;

                        blendshape = pm.blendShape ( driver , driven , origin = 'world' , weight = [ 0 , 1.0 ] , n = bsnName ) ;

                    except :

                        try :
                            
                            childrenChildren = pm.listRelatives ( child , c = True ) ;

                            for childrenChild in childrenChildren :
                                driver  = childrenChild ;
                                driven  = childrenChild.split(':')[1] + '_CIN' ;
                                bsnName = childrenChild.split(':')[1] + '_AbcBSH' ;

                                blendshape = pm.blendShape ( driver , driven , origin = 'world' , weight = [ 0 , 1.0 ] , n = bsnName ) ;

                        except :
                            driver  = childrenChild ;
                            driven  = childrenChild.split(':')[1] + '_CIN' ;
                            print ( '{driver} is not blendshaped to {driven}, their shape or hierarchy are not identical'.format ( driver = driver , driven = driven ) ) ;

                charTopNode.t.lock() ;
                charTopNode.r.lock() ;
                charTopNode.s.lock() ;
                charTopNode.v.set ( 0 ) ;

                pm.parent ( charTopNode , bwd_grp ) ;
                pm.delete ( 'ABC_GRP' ) ;

                cinTopNode = pm.listRelatives ( charTopNode.split(':')[1] + '_CIN' , p = True ) [0] ;
                pm.parent ( cinTopNode , bwd_grp ) ;

            else :

                self.connectABC ( topNode = charTopNode ) ;
                pm.delete ( 'ABC_GRP' ) ;

    def dynPathBrowse_cmd ( self , *args ) :

        defaultPath = pm.textField ( self.dynPath_textField  , q = True , tx = True ) ;
        dynPath     = pm.fileDialog2 ( dir = defaultPath , fileMode = 4 ) ;

        if dynPath :
            if len(dynPath) == 1 :
                dynPath = dynPath[0] ;
                pm.textField ( self.dynPath_textField  , e = True , tx = dynPath ) ;
            else :
                dynPath_txt = '' ;
                for path in dynPath :
                    dynPath_txt += path + ' , ' ;
                pm.textField ( self.dynPath_textField  , e = True , tx = dynPath_txt ) ;

    def importDynBtn_cmd ( self , *args ) :

        dynPath = pm.textField ( self.dynPath_textField  , q = True , tx = True ) ;
        dynPath = dynPath.split ( ' , ' )  ;

        for path in dynPath :
            if path == '' :
                dynPath.remove ( path ) ;

        for path in dynPath :
            if os.path.isfile ( path ) :
               cmd = 'AbcImport -mode import -connect "/" "{path}";'.format ( path = path ) ;
               pm.mel.eval ( cmd ) ;

    def connectABC ( self , topNode = '' , *args ) :
        
        # copy transform
        if pm.objExists ( topNode.split(':')[1] + '_CIN' ) == True :
        
            self.copyAttr ( driver = topNode , driven = ( topNode.split(':')[1] + '_CIN' ) ) ;
            
            print ( '(succeeded/transform) %s >>> %s' % ( topNode , topNode.split(':')[1] + '_CIN' ) ) ; 
        
        else :
            print ( '(failed/transform) %s >>> %s' % ( topNode , topNode.split(':')[1] + '_CIN' ) ) ; 

        allNode = pm.listRelatives ( topNode , ad = True ) ;
        
        for each in allNode :
            
            if pm.nodeType ( each ) == 'transform' :
                if pm.objExists ( each.split (':')[1] + '_CIN' ) == True :
                    self.copyAttr ( driver = each , driven = each.split (':')[1] + '_CIN' ) ;
                    print ( '(succeeded/transform) %s >>> %s' % ( each , each.split (':')[1] + '_CIN' ) ) ; 
                else :
                    print ( '(failed/transform) %s >>> %s' % ( each , each.split (':')[1] + '_CIN' ) ) ;
            else : pass ;
        
        for each in allNode :
            
            if 'Shape' in str ( each ) :
                shape = each ;
                transform = each.split ( 'Shape' ) [0] ;
                
                outPolyMesh = pm.listConnections ( shape + '.inMesh' , p = True ) ;
                
                if outPolyMesh == [] :
                    print ( '(no connection/abc) %s >>> None' % ( each ) ) ; 
                else :
                    outPolyMesh = outPolyMesh [0] ;
                    try :
                        pm.connectAttr ( outPolyMesh , transform.split(':')[1] + '_CINShape.inMesh' , f = True ) ;
                        print ( '(succeeded/abc) %s >>> %s' % ( each , each.split (':')[1] + '_CIN' ) ) ; 
                    except :
                        print ( '(no connection/abc) %s >>> None' % ( each ) ) ; 
                        
        cinTopNode = pm.listRelatives ( topNode.split(':')[1] + '_CIN' , p = True ) [0] ;
        pm.parent ( cinTopNode , 'BWD_GRP' ) ;

    def copyAttr ( self , driver , driven , *args  ) :
    
        driver = pm.general.PyNode ( driver ) ;
        driven = pm.general.PyNode ( driven ) ;

        # unlock attribute
        for obj in [ driver , driven ] :
            for attr in [ 't' , 'r' , 's' ] :
                for axis in [ 'x' , 'y' , 'z' ] :
                    exec ( 'pm.setAttr ( "{obj}.{attr}{axis}" , lock = False ) ;'.format (  obj = obj , attr = attr , axis = axis ) ) ;
            exec ( 'pm.setAttr ( "{obj}.v" , lock = False ) ;'.format ( obj = obj ) ) ;

        # copy attribute 
        for attr in [ 't' , 'r' , 's' , 'v' ] :
            exec ( 'pm.setAttr ( "{driven}.{attr}" , pm.getAttr ( "{driver}.{attr}" ) ) ;'.format ( attr = attr , driver = driver , driven = driven ) ) ;
        
        # lock attribute
        for obj in [ driver , driven ] :
            for attr in [ 't' , 'r' , 's' ] :
                for axis in [ 'x' , 'y' , 'z' ] :
                    exec ( 'pm.setAttr ( "{obj}.{attr}{axis}" , lock = True ) ;'.format (  obj = obj , attr = attr , axis = axis ) ) ;
            #exec ( '{obj}.v.lock()' ) ;

    def globalImportBtn_cmd ( self , *args ) :
        
        self.importCamBtn_cmd() ;

        self.importCharBtn_cmd() ;
        self.importOriGrpBtn_cmd() ;
        self.importAnimGrpBtn_cmd() ;

        self.importDynBtn_cmd() ;

    def insert ( self , width ) :
        
        ### camera ###
        pm.text ( label = 'Camera' , bgc = ( 0.1 , 0.1 , 0.2 ) , h = 25 ) ;

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/4*3 ) , ( 2 , width/4 ) ] ) :
            self.camPath_textField  = pm.textField ( 'camPath_textField' , w = width/4*3 , tx = self.defaultCameraPath ) ;
            self.camPathBrowse_btn  = pm.button ( 'camPathBrowse_btn' , label = 'Browse' , w = width/4 , c = self.cameraPathBrowse_cmd )  ;

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/2 ) , ( 2 , width/2 ) ] ) :
            pm.text ( label = '' ) ;
            self.importCam_btn = pm.button ( 'importCam_btn' , label = 'Import Camera' , c = self.importCamBtn_cmd ) ;

        ### character ###
        pm.text ( label = 'Character Cache' , bgc = ( 0.1 , 0.1 , 0.2 ) , h = 25 ) ;

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/2 ) , ( 2 , width/2 ) ] ) :
            self.importOriGrp_btn       = pm.button ( 'importOriGrp_btn' , label = 'Import Ori Group' , w = width/2 , c = self.importOriGrpBtn_cmd ) ;
            self.importAnimGrp_btn      = pm.button ( 'importAnimGrp_btn' , label = 'Import Anim Group' , w = width/2 , c = self.importAnimGrpBtn_cmd ) ;
        
        pm.text ( label = '' ) ;

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/4*3 ) , ( 2 , width/4 ) ] ) :
            self.charPath_textField = pm.textField ( 'charPath_textField' , w = width/4*3 , tx = self.defaultCharacterPath ) ;
            self.charPathBrowse_btn = pm.button ( 'charPathBrowse_btn' , label = 'Browse' , c = self.charPathBrowse_cmd )

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/2 ) , ( 2 , width/2 ) ] ) :
            self.charImportType_cbx = pm.checkBox ( 'charImportType_cbx' , label = 'BlendShape' , v = True , enable = True  ) ;
            self.importChar_btn = pm.button ( 'importChar_btn' , label = 'Import Character Cache' , c = self.importCharBtn_cmd ) ;

        ### dyn cache (for Xgen, Yeti, Etc.) ###
        pm.text ( label = 'Dyn Cache' , bgc = ( 0.1 , 0.1 , 0.2 ) , h = 25 ) ;

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/4*3 ) , ( 2 , width/4 ) ] ) :
            self.dynPath_textField = pm.textField ( 'dynPath_textField' , w = width/4*3 , tx = self.defaultDynPath ) ;
            self.dynPathBrowse_btn = pm.button ( 'dynPathBrowse_btn' , label = 'Browse' , c = self.dynPathBrowse_cmd ) ;

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/2 ) , ( 2 , width/2 ) ] ) :
            pm.text ( label = '' ) ;
            self.importDyn_btn = pm.button ( 'importDyn_btn' , label = 'Import Dyn' , w = width/2 , c = self.importDynBtn_cmd ) ;

        #pm.text ( label = 'Global Import' , bgc = ( 0.2 , 0.1 , 0.1 ) , h = 25 ) ;
        pm.text ( label = '' , h = 25 ) ;

        with pm.rowColumnLayout ( nc = 1 , w = width ) :
            self.globalImport_btn = pm.button ( 'globalImport_btn' , label = 'Global Import' , w = width , c = self.globalImportBtn_cmd ) ;