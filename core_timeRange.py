import pymel.core as pm ;
import os , ast ;

# save playblast start, end frame as well ;

class TimeRange_GUI ( object ) :

    def __init__ ( self ) :
        self.currentProjectPath = pm.workspace ( q = True , rootDirectory = True ) ;

    def __str__ ( self ) :
        pass ;

    def __repr__ ( self ) :
        pass ;

    def connectSimGUI ( self , sim_GUI ) :
        self.simulation_btn = sim_GUI.simulation_btn ;

    def connectPlayblastGUI ( self , playblast_GUI ) :
        self.playblastStart_intField    = playblast_GUI.playblastStart_intField ;
        self.playblastEnd_intField      = playblast_GUI.playblastEnd_intField ;
        self.playblast_btn              = playblast_GUI.playblast_btn ;

    def connectExportGUI ( self , export_GUI ) :
        self.cacheStart_intField    = export_GUI.cacheStart_intField ;
        self.cacheEnd_intField      = export_GUI.cacheEnd_intField ;

    def save ( self , *args  ) :
        
        textFilePath = self.currentProjectPath + 'data/timerange.txt' ;
        timeRange_file = open ( textFilePath , 'w+' ) ;

        guiTimeRange = self.getGuiTimeRange() ;

        timeRange_dict = {} ;
        timeRange_dict['pre roll']  = guiTimeRange[0] ;
        timeRange_dict['start']     = guiTimeRange[1] ;
        timeRange_dict['end']       = guiTimeRange[2] ;
        timeRange_dict['post roll'] = guiTimeRange[3] ;

        timeRange_dict['playblastStart']    = guiTimeRange[4] ;
        timeRange_dict['playblastEnd']      = guiTimeRange[5] ;
        
        text = str ( timeRange_dict ) ;
        timeRange_file.write ( text ) ;
        timeRange_file.close ( ) ;

    def setTimeRange ( self , *args ) :
        
        currentStart    = pm.playbackOptions ( q = True , min = True ) ;
        currentEnd      = pm.playbackOptions ( q = True , max = True ) ;

        guiTimeRange = self.getGuiTimeRange() ;
        preRoll     = guiTimeRange[0] ;
        start       = guiTimeRange[1] ;
        end         = guiTimeRange[2] ;
        postRoll    = guiTimeRange[3] ;

        if ( currentStart == preRoll ) and ( currentEnd == postRoll ) :
            pm.playbackOptions ( min = start , max = end ) ;

        elif ( currentStart == start ) and ( currentEnd == end ) :
            pm.playbackOptions ( min = preRoll , max = postRoll ) ;

        else :
            pm.playbackOptions ( min = preRoll , max = postRoll ) ;

        self.updateSetTimeRangeBtnClr ( ) ;
        self.setStartBsh ( start = preRoll ) ;

    def updateSetTimeRangeBtnClr ( self , *args ) :

        currentStart    = pm.playbackOptions ( q = True , min = True ) ;
        currentEnd      = pm.playbackOptions ( q = True , max = True ) ;
        
        guiTimeRange = self.getGuiTimeRange() ;
        preRoll     = guiTimeRange[0] ;
        start       = guiTimeRange[1] ;
        end         = guiTimeRange[2] ;
        postRoll    = guiTimeRange[3] ;

        if ( currentStart == start ) and ( currentEnd == end ) :
            pm.button ( self.setTimeRange_btn   , e = True , bgc = ( 1 , 0.4 , 0.25 ) ) ;
            pm.button ( self.simulation_btn     , e = True , bgc = ( 0.361 , 0.361 , 0.361 ) ) ;
            pm.button ( self.playblast_btn      , e = True , bgc = ( 1 , 0.4 , 0.25 ) ) ;

        elif ( currentStart == preRoll ) and ( currentEnd == postRoll ) :
            pm.button ( self.setTimeRange_btn   , e = True , bgc = ( 0 , 1 , 1 ) ) ;
            pm.button ( self.simulation_btn     , e = True , bgc = ( 0 , 1 , 1 ) ) ;
            pm.button ( self.playblast_btn      , e = True , bgc = ( 0.361 , 0.361 , 0.361 ) ) ;

        if currentStart not in [ preRoll , start ] or currentEnd not in [ end , postRoll ] :
            pm.button ( self.setTimeRange_btn   , e = True , bgc = ( 0.361 , 0.361 , 0.361 ) ) ;
            pm.button ( self.simulation_btn     , e = True , bgc = ( 0.361 , 0.361 , 0.361 ) ) ;
            pm.button ( self.playblast_btn      , e = True , bgc = ( 0.361 , 0.361 , 0.361 ) ) ;


    def setStartBsh ( self , start , *args ) :
        
        if pm.objExists ( 'CIN_COL_BSH' ) :
            bsn = pm.general.PyNode ( 'CIN_COL_BSH' ) ;
            key = pm.listAttr ( bsn.w , m = True ) ;
            pm.cutKey ( bsn , at = key , option = 'keys' ) ;
            pm.setKeyframe ( bsn , at = key , t = start , v = 0 ) ;
            pm.setKeyframe ( bsn , at = key , t = start + 10 , v = 1 ) ;

        nucleus_list = pm.ls ( type = 'nucleus' ) ;
        if nucleus_list :
            for nucleus in nucleus_list :
                nucleus.startFrame.set ( start ) ;

    def initializeTimeRange ( self , *args ) :
        
        textFilePath = self.currentProjectPath + 'data/timerange.txt' ;

        if os.path.exists ( textFilePath ) :
            
            timeRange_file  = open ( textFilePath , 'r' ) ;
            timeRange_txt   = timeRange_file.read() ;
            timeRange_file.close() ;

            timeRange = ast.literal_eval ( timeRange_txt ) ;

            pm.intField ( self.preRoll_intField     , e = True , value = timeRange ['pre roll'] ) ;
            pm.intField ( self.start_intField       , e = True , value = timeRange ['start'] ) ;
            pm.intField ( self.end_intField         , e = True , value = timeRange ['end'] ) ;
            pm.intField ( self.postRoll_intField    , e = True , value = timeRange ['post roll'] ) ;

            try :
                pm.intField ( self.playblastStart_intField  , e = True , value = timeRange ['playblastStart'] ) ;
            except :    
                pm.intField ( self.playblastStart_intField  , e = True , value = timeRange ['start'] ) ;
    
            try :
                pm.intField ( self.playblastEnd_intField , e = True , value = timeRange ['playblastEnd'] ) ;
            except :
                pm.intField ( self.playblastEnd_intField , e = True , value = timeRange ['end'] ) ;

            pm.intField ( self.cacheStart_intField      , e = True , value = timeRange ['start'] - 5 ) ;
            pm.intField ( self.cacheEnd_intField        , e = True , value = timeRange ['end'] + 5 ) ;
             
    def getGuiTimeRange ( self ) :

        preRoll     = pm.intField ( self.preRoll_intField   , q = True , value = True ) ;
        start       = pm.intField ( self.start_intField     , q = True , value = True ) ;
        end         = pm.intField ( self.end_intField       , q = True , value = True ) ;
        postRoll    = pm.intField ( self.postRoll_intField  , q = True , value = True ) ;

        playblastStart  = pm.intField ( self.playblastStart_intField , q = True , value = True ) ;
        playblastEnd    = pm.intField ( self.playblastEnd_intField , q = True , value = True ) ;

        return [ preRoll , start , end , postRoll , playblastStart , playblastEnd ] ;

    def insert ( self , width , *args ) :

        # time range layout
        with pm.rowColumnLayout ( nc = 5 , cw = [ ( 1 , width/5 ) , ( 2 , width/5 ) , ( 3 , width/5 ) , ( 4 , width/5 ) , ( 5 , width/5 ) ] ) :

            self.preRoll_intField   = pm.intField ( 'preRoll_intField'  , w = width/5 ) ;
            self.start_intField     = pm.intField ( 'start_intField'    , w = width/5 ) ;
            self.save_btn           = pm.button ( 'save_btn' , label = 'Save' , c = self.save , bgc = ( 0.55 , 0.9 , 0.55 ) , w = width/5 ) ;
            self.end_intField       = pm.intField ( 'end_intField'      , w = width/5 ) ;
            self.postRoll_intField  = pm.intField ( 'postRoll_intField' , w = width/5 ) ;

            pm.text ( label = 'Pre Roll' ) ;
            pm.text ( label = 'Start' ) ;
            pm.text ( label = '' ) ;
            pm.text ( label = 'end' ) ;
            pm.text ( label = 'postRoll' ) ;

        # set time layout
        self.setTimeRange_btn = pm.button ( 'setTimeRange_btn' , label = 'Set Time Range' , c = self.setTimeRange ) ; 
            # set time range to sim --> color change