import pymel.core as pm ;
import os ;

from sim.sim_simUtilities import core_general as gen ;
reload ( gen ) ;

from sim.sim_simUtilities import core_nucleus ;
reload ( core_nucleus ) ;

class Sim_GUI ( object ) :

    def __init__ ( self ) :
        self.currentProjectPath = pm.workspace ( q = True , rootDirectory = True ) ;
        self.dynCachePath       = self.currentProjectPath + 'cache/dyn_abc/' ;

    def __str__ ( self ) :
        pass ;

    def __repr__ ( self ) :
        pass ;

    def connectPlayblastGUI ( self , playblast_GUI ) :
        self.playblast_GUI = playblast_GUI ;

    def insert ( self , width ) :
        width = width*0.98

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/2 ) , ( 2 , width/2 ) ] ) :

            cw1 = width/2/5*2 ;
            cw2 = width/2/5*3 ;

            with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , cw1  ) , ( 2 , cw2 ) ] ) :

                pm.text ( label = 'Sim Type' , w = cw1 ) ;
                
                self.simType_opt = pm.optionMenu ( 'simType_opt' , w = cw2 ) ;
                with self.simType_opt :
                    pm.menuItem ( label = 'Replace'     ) ;
                    pm.menuItem ( label = 'Version'     ) ;
                    pm.menuItem ( label = 'Subversion'  ) ;

            with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , cw1  ) , ( 2 , cw2 ) ] ) :
                pm.text ( label = 'Step' , w = cw1 ) ;
                self.step_floatField = pm.floatField ( 'step_floatField' , pre = 2 , v = 1 , w = cw2 ) ;   
        
        self.simulation_btn = pm.button ( 'simulation_btn' , label = 'Simulate' , c = self.simulateBtn_cmd , width = width , bgc = ( 0 , 1 , 1 ) ) ;

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/2 ) , ( 2 , width/2 ) ] ) :
            self.exportDyn_btn = pm.button ( 'exportDyn_btn' , label = 'Export' , c = self.exportDynBtn_cmd ) ;
            self.importDyn_btn = pm.button ( 'importDyn_btn' , label = 'Import' , c = self.importDynBtn_cmd ) ;

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/2 ) , ( 2 , width/2 ) ] ) :

            with pm.rowColumnLayout ( nc = 3 , cw = [ ( 1 , width/2/10*1.75 ) , ( 2 , width/2/10*1.5 ) , ( 3 , width/2/10*6.75 ) ] ) :
                pm.text ( label = '' ) ;
                self.playblast_cbx = pm.checkBox ( 'playblast_cbx' , label = '' , value = False ) ;
                pm.text ( label = 'Auto Playblast' , align = 'left' ) ;

            with pm.rowColumnLayout ( nc = 3 , cw = [ ( 1 , width/2/10*0.5 ) , ( 2 , width/2/10*1.5 ) , ( 3 , width/2/10*8 ) ] ) :
                pm.text ( label = '' ) ;
                self.saveBeforePlayblast_cbx = pm.checkBox ( 'saveBeforePlayblast_cbx' , label = '' , value = False ) ;
                pm.text ( label = 'Save Before Playblast' , align = 'left' ) ;

    def exportDynBtn_cmd ( self , *args ) :

        if not os.path.exists ( self.dynCachePath ) :
            os.makedirs ( self.dynCachePath ) ;

        step = pm.floatField ( self.step_floatField , q = True , v = True ) ;
        timeSliderStart = pm.playbackOptions ( q = True , min = True ) ;
        timeSliderEnd   = pm.playbackOptions ( q = True , max = True ) ;

        selection = pm.ls ( sl = True ) ;

        selectionClean = [] ;
        for each in selection :
        	selectionClean.append ( each.nodeName() ) ;
        cacheName = gen.composeName ( selectionClean ) + '.dyn.' ;
        increment = gen.checkIncrement ( cacheName , self.dynCachePath  , incrementIncrement = True ) ;
        cacheName += increment + '.abc' ;

        cachePath = self.dynCachePath  + cacheName ;

        # export abc command 
        cmd = 'AbcExport -j ' ; # start command
        cmd += '"-frameRange {timeSliderStart} {timeSliderEnd} '.format ( timeSliderStart = timeSliderStart , timeSliderEnd = timeSliderEnd ) ;
        cmd += '-step {step} '.format ( step = step ) ;
        cmd += '-worldSpace -writeVisibility -eulerFilter -dataFormat ogawa' + ' ' ;

        for each in selection :
            cmd += '-root {longName} '.format ( longName = each.longName ( ) ) ;
        
        cmd += '-file {cachePath} " ;'.format ( cachePath = cachePath ) ;

        pm.mel.eval ( cmd ) ;

    def importDynBtn_cmd ( self , *args ) :

        selection = pm.ls ( sl = True ) ;

        selectionClean = [] ;
        for each in selection :
        	selectionClean.append ( each.nodeName() ) ;
        cacheName = gen.composeName ( selectionClean ) + '.dyn.' ;
        increment = gen.checkIncrement ( cacheName , self.dynCachePath  , incrementIncrement = False ) ;
        cacheName += increment + '.abc' ;

        cachePath = self.dynCachePath  + cacheName ;
        pm.system.importFile ( cachePath , namespace = 'dyn' , gr = True , groupName = 'dynImport_grp' ) ;
        
        dynImport_grp = pm.general.PyNode ( 'dynImport_grp' ) ;
        cacheTopNode = dynImport_grp.getChildren() ;

        if cacheTopNode :
                driver  = cacheTopNode ;
                driven	= selection ;
                bsnName = gen.composeName ( selectionClean ) + '_DynBSH' ;

                blendshape = pm.blendShape ( driver , driven , origin = 'world' , weight = [ 0 , 1.0 ] , n = bsnName ) ;

                pm.parent ( cacheTopNode , world = True ) ;

        pm.delete ( dynImport_grp ) ;

    def composeNCacheName ( self, *args ) :

        if pm.ls ( sl = True ) :
            selection_list = pm.ls ( sl = True ) ;

            name = selection_list[0].split('_')[0] ;
            name = name[0].lower() + name [1:] ;

            if len ( selection_list ) > 1 :
                for selection in selection_list[1:] :
                    name_tempt = selection.split('_')[0] ;
                    name_tempt = name_tempt[0].upper() + name_tempt[1:] ;
                    name += name_tempt ;
            return name ;

    def simulate ( self , *args ) :
        
        nCacheName = self.composeNCacheName() ;

        dynCachePath = self.currentProjectPath + 'data/DYN/' + nCacheName ;

        if not os.path.exists ( dynCachePath ) :
            os.makedirs ( dynCachePath ) ;

        type = pm.optionMenu ( self.simType_opt , q = True , value = True ) ;

        if type == 'Replace' :
            incrementVersion    = False ;
            incrementSubVersion = False ;

            delete_cmd = 'deleteCacheFile 2 { "delete", "" } ;' ;

        else :

            if type == 'Version' :
                incrementVersion    = True  ;
                incrementSubVersion = False ;

            elif type == 'Subversion' :
                incrementVersion    = False ;
                incrementSubVersion = True ;

                delete_cmd = 'deleteCacheFile 2 { "keep", "" } ;' ;

        version = gen.checkVersion (
            path    = dynCachePath ,
            name    = nCacheName ,
            incrementVersion    = incrementVersion ,
            incrementSubVersion = incrementSubVersion ) ;
    
        nCacheName += '_DYN_' + version ;

        step = pm.floatField ( self.step_floatField , q = True , v = True ) ;

        cmd = 'doCreateNclothCache 5 { "2", "1", "10", "OneFile", "1", ' ;
        cmd += '"{dynCachePath}"'.format ( dynCachePath = dynCachePath ) ;
        cmd += ',"0",' ;
        cmd += '"{nCacheName}"'.format ( nCacheName = nCacheName ) ;
        cmd += ',"0", "add", "0", ' ;
        cmd += '"{step}"'.format ( step = step ) ;
        cmd += ', "1","0","1","mcx" } ;'
        # doCreateNclothCache 5 { "2", "1", "10", "OneFile", "1", "D:/TwoHeroes/film001/q0420/s0160/spiderGirlGod_001/data/DYN/pSphere1PSphere3PSphere5","0","pSphere1PSphere3PSphere5_DYN_vv001_001","0", "add", "0", "1.0", "1","0","1","mcx" } ;

        try :
            pm.mel.eval ( delete_cmd ) ;
        except :
            pass ;
        
        pm.mel.eval ( cmd ) ;

    def simulateBtn_cmd ( self , *args ) :

        # simulate
        self.simulate() ;

        if pm.checkBox ( self.playblast_cbx , q = True , value = True ) and pm.checkBox ( self.saveBeforePlayblast_cbx , q = True , value = True ) :
            pm.system.saveFile ( force = True ) ;

        # playblast
        if pm.checkBox ( self.playblast_cbx , q = True , value = True ) :

            # disable nucleus before playblast
            nucleus = core_nucleus.NucleusNode ( ) ;
            nucleus.getEnableState ( ) ;
            nucleus.setEnable ( False ) ;

            self.playblast_GUI.playblastBtn_cmd ( ) ; 

            # set nucleus to its previous state
            nucleus.reset ( ) ;

        '''
        viewPlayblast ( ) ;     
        '''