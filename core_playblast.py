import pymel.core as pm ;
import os , re ;

from sim.sim_simUtilities import core_nucleus ;
reload ( core_nucleus ) ;

nucleus = core_nucleus.NucleusNode ( ) ;

class Playblast_GUI ( object ) :

    def __init__ ( self ) :
        self.currentProject = pm.workspace ( q = True , rootDirectory = True ) ;
        self.preferencePath = self.getPreferencePath ( ) ;

    def __str__ ( self ) :
        pass ;

    def __repr__ ( self ) :
        pass ;

    def getPreferencePath ( self ) :
        
        myDocuments = os.path.expanduser('~') ;
        myDocuments = myDocuments.replace ( '\\' , '/' ) ;
        # C:/Users/Legion/Documents

        prefPath = myDocuments + '/birdScriptPreferences/simulationUtilities/'

        if not os.path.exists ( prefPath ) :
            os.makedirs ( prefPath ) ;

        return prefPath ;

    def openPlayblastPathBtn_cmd ( self , *args ) :

        path = pm.textField ( self.playblastPath_textField , q = True , tx = True ) ;

        if os.path.exists ( path ) :
           os.startfile ( path ) ;

    def browseBtn_cmd ( self , *args ) :

        startingDirectory = pm.textField ( self.playblastPath_textField , q = True , tx = True ) ;

        playblastLocationPath = pm.fileDialog2 ( fileMode = 3 , fileFilter = '0' , dir = startingDirectory ) [0] ;
        if playblastLocationPath[-1] != '/' :
            playblastLocationPath += '/'

        #print playblastLocationPath ;

        pm.textField ( self.playblastPath_textField , e = True , tx = playblastLocationPath ) ;

        playblastDefaultPathTxt_file = open ( self.preferencePath + '/playblastDefaultPath.txt' , 'w+' ) ;
        playblastDefaultPathTxt_file.write ( playblastLocationPath ) ;
        playblastDefaultPathTxt_file.close ( ) ;

    def updatePlayblastDefaultPathTextField ( self ) :

        if not os.path.exists ( self.preferencePath + '/playblastDefaultPath.txt' ) :
            pm.textField ( self.playblastPath_textField , e = True , tx = 'Please browse and select default directory' ) ;

        else :
            
            playblastDefaultPathTxt_file = open ( self.preferencePath + '/playblastDefaultPath.txt' , 'r+' ) ;
            playblastDefaultPath = playblastDefaultPathTxt_file.read() ;
            playblastDefaultPathTxt_file.close() ;

            pm.textField ( self.playblastPath_textField , e = True , tx = playblastDefaultPath ) ;

    def composePlayblastName ( self , *args ) :
        
        try :

            # self.currentProject ;
            # D:/TwoHeroes/film001/q0420/s0160/spiderGirlGod_001/

            nameElem = self.currentProject.split('/') ;

            for elem in nameElem :
                if elem == '' :
                    nameElem.remove ( elem ) ;

            sequence    = nameElem[-3] ;
            shot        = nameElem[-2] ;
            charName    = nameElem[-1] ;        
            
            scenePath       = pm.system.sceneName() ;
            
            if scenePath :
                scenePathElem   = scenePath.split('/') ;
                for elem in scenePathElem :
                    if elem == '' :
                        scenePathElem.remove ( elem ) ;

                sceneName = scenePathElem[-1] ;
            else :
                sceneName = 'untitled' ;

            version     = re.findall ( 'v' + '[0-9]{3}' + '_' + '[0-9]{3}' , sceneName ) ;
            if version :
                version = version[0] ;

            if '.' in sceneName :

                sceneNameElem = sceneName.split('.') ;

                #print sceneNameElem ;

                for elem in sceneNameElem :

                    if elem == '' :
                        sceneNameElem.remove ( elem ) ;
     
                #print sceneNameElem ;

                sceneName = sceneNameElem[-3] ;


            name = sequence + '.' + shot + '.' + charName + '.' + sceneName ;
            
            if version :
                name += '.' + version ;

        except :
            name = 'none' ;

        return name ;
        
    def updatePlayblastName ( self , *args ) :
         playblastName = self.composePlayblastName ( ) ;
         pm.textField ( self.playblastName_textField , e = True , tx = playblastName )

    def getSceneResolution ( self ) :
        width   = pm.getAttr ( "defaultResolution.width" ) ;
        height  = pm.getAttr ( "defaultResolution.height" ) ;
        return [ width , height ] ;

    def playblastBtn_cmd ( self , *args ) :
        # disable nucleus before playblast

        projectPathElem = self.currentProject.split('/') ;
        for elem in projectPathElem :
            if elem == '' :
                projectPathElem.remove ( elem ) ;
        charName    = projectPathElem [-1] ;

        sceneResolution = self.getSceneResolution () ;
        resW = sceneResolution[0] ;
        resH = sceneResolution[1] ;

        playblastStart  = pm.intField ( self.playblastStart_intField    , q = True , v = True ) ;
        playblastEnd    = pm.intField ( self.playblastEnd_intField      , q = True , v = True ) ;        
        incrementMethod = pm.optionMenu ( self.increment_opt , q = True , v = True ) ;
        scale           = pm.intField ( self.playblastScale_intField , q = True , v = True ) ;

        name            = pm.textField ( self.playblastName_textField , q = True , tx = True ) ;
        playblastPath   = pm.textField ( self.playblastPath_textField , q = True , tx = True ) ;
        increment       = self.checkIncrement ( name , playblastPath ) ;

        playblastType   = pm.optionMenu ( self.playblast_opt , q = True , v = True ) ;
        #print playblastPath + name + '.' + increment ;
        #print playblastPath + name + '.' + increment + '/' + charName ;

        nucleus.getEnableState ( ) ;
        nucleus.setEnable ( False ) ;

        if playblastType == 'Tiff' :

            if not os.path.exists ( playblastPath + name + '.' + increment ) :
                os.makedirs ( playblastPath + name + '.' + increment ) ;

            pm.playblast (
                format          = 'image' ,
                startTime       = playblastStart ,
                endTime         = playblastEnd ,
                filename        = playblastPath + name + '.' + increment + '/' + charName ,
                sequenceTime    = 0 ,
                clearCache      = 0 ,
                viewer          = 0 ,
                showOrnaments   = 0 ,
                offScreen       = True ,
                fp              = 4 , # framePadding
                percent         = scale ,
                compression     = 'tif' ,
                quality         = 100 ,
                widthHeight     = [ resW , resH ] ,
                ) ;

        if playblastType == 'Video' :

            pm.playblast (
                format          = 'qt' ,
                startTime       = playblastStart ,
                endTime         = playblastEnd ,
                filename        = playblastPath + name + '.' + increment + '.mov' ,
                clearCache      = True ,
                viewer          = True ,
                showOrnaments   = True ,
                offScreen       = True ,
                fp              = 4 , # framePadding
                percent         = scale ,
                compression     = "MPEG-4 Video" ,
                quality         = 100 ,
                widthHeight     = [ resW , resH ] ,
                forceOverwrite  = True ,
                ) ;

        if playblastType == 'View' :

            pm.playblast (
                format          = 'image' ,
                startTime       = playblastStart ,
                endTime         = playblastEnd ,
                sequenceTime    = 0 ,
                clearCache      = 1 ,
                viewer          = True ,
                showOrnaments   = True ,
                offScreen       = True ,
                fp              = 4 ,
                percent         = scale ,
                compression     = "maya" ,
                quality         = 100 ,
                widthHeight     = [ resW , resH ] ,
                ) ;

        nucleus.reset() ;

    def updateIncrementMethodGUI ( self , *args ) :

        if pm.optionMenu ( self.playblast_opt , q = True , v = True ) == 'View' :
            pm.optionMenu ( self.increment_opt , e = True , enable = False ) ;
        else :
            pm.optionMenu ( self.increment_opt , e = True , enable = True ) ;

    def checkIncrement ( self , name , path , incrementIncrement = False , *args ) :
        # check for '.xxxx.' e.g. '.0001.'

        ### add on start ###
        incrementMethod = pm.optionMenu ( self.increment_opt , q = True , v = True ) ;

        if incrementMethod == 'Version' :
            incrementIncrement = True ;

        playblastType   = pm.optionMenu ( self.playblast_opt , q = True , v = True ) ;
        extension       = '.mov'
        ### add on end ###

        file_list = os.listdir ( path ) ;
        increment_list = [] ;

        if not file_list :
            finalIncrement = '0001' ;

        else :
            for file in file_list :

                condition1 = False  ;
                condition2 = True   ;

                if name in str ( file ) :
                    condition1 = True ;

                if playblastType == 'Video' :
                    if not extension in str ( file ) :
                        condition2 = False ;
                else :
                    if extension in str ( file ) :
                        condition2 = False ;

                if condition1 and condition2 :
                    ### add on ###
                    increment = re.findall ( '\.' + '[0-9]{4}' , file ) ;
                    if increment :
                        increment = increment[0] ;
                        increment_list.append ( increment ) ;

            if not increment_list :
                finalIncrement = '0001' ;
            else :
                increment_list.sort() ;
                currentIncrement = increment_list[-1] ;
                increment = currentIncrement.split('.')
                for split in increment :
                    if split == '' :
                        increment.remove ( split ) ;
                increment = increment[0] ;
                increment = int ( increment ) ;

                if incrementIncrement :
                    increment += 1 ;

                finalIncrement = str(increment).zfill(4) ;

        return finalIncrement ;

    def insert ( self , width ) :
        width = width*0.98 ;

        with pm.rowColumnLayout ( nc = 5 , cw = [ ( 1 , width/5 ) , ( 2 , width/5 ) , ( 3 , width/5 ) , ( 4 , width/5 ) , ( 5 , width/5 ) ] ) :

            pm.text ( label = '' ) ;
            
            with pm.rowColumnLayout ( nc = 1 , w = width/5 ) :
                self.playblastStart_intField = pm.intField ( 'playblastStart_intField' , w = width/5 ) ;
                pm.text ( label = 'Start' , w = width/5 ) ;
            
            pm.text ( label = '' ) ;

            with pm.rowColumnLayout ( nc = 1 , w = width/5 ) :
                self.playblastEnd_intField = pm.intField ( 'playblastEnd_intField' , w = width/5 ) ;
                pm.text ( label = 'End' , w = width/5 ) ;

            pm.text ( label = '' ) ;

        with pm.rowColumnLayout ( nc = 3 , cw = [ ( 1 , width/3 ) , ( 2 , width/3 ) , ( 3 , width/3 ) ] ) :

            with pm.rowColumnLayout ( nc = 1 , w = width/3 ) :
                self.playblast_opt = pm.optionMenu ( 'playblast_opt' , w = width/3 , cc = self.updateIncrementMethodGUI ) ;
                with self.playblast_opt :
                    pm.menuItem ( label = 'View'    ) ;
                    pm.menuItem ( label = 'Video'   ) ;
                    pm.menuItem ( label = 'Tiff'    ) ; 
                pm.text ( label = 'Type' , w = width/3 ) ;

            with pm.rowColumnLayout ( nc = 1 , w = width/3 ) :
                self.increment_opt = pm.optionMenu ( 'increment_opt' , w = width/3 ) ;
                with self.increment_opt :
                    pm.menuItem ( label = 'Version' ) ;
                    pm.menuItem ( label = 'Replace' ) ;                    
                pm.text ( label = 'Increment' , w = width/3 ) ;

            with pm.rowColumnLayout ( nc = 1 , w = width/3 ) :
                self.playblastScale_intField = pm.intField ( 'playblastScale_intField' , value = 50 ) ;
                pm.text ( label = 'Scale (%)' ) ;

        pm.separator ( h = 5 , vis = False ) ;

        self.openPlayblast_btn = pm.button ( 'openPlayblast_btn' , label = 'Playblast Directory' , w = width , c = self.openPlayblastPathBtn_cmd ) ;
        self.playblastPath_textField = pm.textField ( 'playblastPath_textField' , w = width ) ;

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/3*2 ) , ( 2 , width/3 ) ] ) :
            pm.text ( label = '' ) ;
            self.browse_btn = pm.button ( 'browse_btn' , label = 'Browse' , c = self.browseBtn_cmd ) ;

        pm.text ( label = 'Playblast Name' , w = width ) ;
        self.playblastName_textField = pm.textField ( 'playblastName_textField' , w = width ) ;

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/3*2 ) , ( 2 , width/3 ) ] ) :
            pm.text ( label = '' ) ;
            self.refresh_btn = pm.button ( 'refresh_btn' , label = 'Refresh' , c = self.updatePlayblastName ) ;

        pm.separator ( h = 5 , vis = False ) ;

        self.playblast_btn = pm.button ( 'playblast_btn' , label = 'Playblast' , c = self.playblastBtn_cmd , w = width ) ;

        self.updateIncrementMethodGUI ( ) ;
        self.updatePlayblastDefaultPathTextField ( ) ;
        self.updatePlayblastName ( ) ;