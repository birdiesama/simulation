import pymel.core as pm ;

class NucleusUtil_GUI ( object ) :

    def __init__ ( self ) :
        pass ;

    def __str__ ( self ) :
        pass ;

    def __repr__ ( self ) :
        pass ;

    def setNucleusButtonState ( self , state ) :
        if state :
            pm.button ( self.enableNucleus_btn , e = True , nbg = True ) ;
            pm.button ( self.disableNucleus_btn , e = True , nbg = False ) ;  
        else :
            pm.button ( self.enableNucleus_btn , e = True , nbg = False ) ;
            pm.button ( self.disableNucleus_btn , e = True , nbg = True ) ;

    def updateNucleusGUI ( self , *args ) :

        nucleus_list            = pm.ls ( type = 'nucleus' ) ;
        textScroll_nucleus_list = pm.textScrollList ( self.nucleus_txtScrll , q = True , allItems = True ) ;

        # check if nucleus in text scroll list exists, if not remove from the list 
        for nucleus in textScroll_nucleus_list :
            if not pm.objExists ( nucleus ) :
                pm.textScrollList ( self.nucleus_txtScrll , e = True , removeItem = nucleus ) ;

        # check if nucleus is in the text scroll list, if not append it to the list
        for nucleus in nucleus_list :
            if nucleus not in textScroll_nucleus_list :
                pm.textScrollList ( self.nucleus_txtScrll , e = True , append = nucleus ) ;

        selectedNucleus_list = pm.textScrollList ( self.nucleus_txtScrll , q = True , selectItem = True ) ;

        if selectedNucleus_list :

            if len(selectedNucleus_list) == 1 :

                nucleus = pm.general.PyNode ( selectedNucleus_list[0] ) ;

                if nucleus.enable.get() :
                    self.setNucleusButtonState ( True ) ;
                else :
                    self.setNucleusButtonState ( False ) ;

            else :

                nucleusState_list = [] ;

                for nucleus in selectedNucleus_list :
                    nucleus = pm.general.PyNode ( nucleus ) ;
                    nucleusState_list.append ( nucleus.enable.get() ) ;

                nucleusState_list = set ( nucleusState_list ) ;
                nucleusState_list = list ( nucleusState_list ) ;

                if len ( nucleusState_list ) == 1 :
                    if nucleusState_list[0] :
                        self.setNucleusButtonState ( True ) ;
                    else :
                        self.setNucleusButtonState ( False ) ;
                else :
                    pm.button ( self.enableNucleus_btn , e = True , nbg = False ) ;
                    pm.button ( self.disableNucleus_btn , e = True , nbg = False ) ;

    def setNucleus_cmd ( self , state , *args )  :

        selectedNucleus_list = pm.textScrollList ( self.nucleus_txtScrll , q = True , selectItem = True ) ;

        if selectedNucleus_list :
            for nucleus in selectedNucleus_list :
                nucleus = pm.general.PyNode ( nucleus ) ;
                nucleus.enable.set ( state ) ;
        self.updateNucleusGUI() ;

    def enableNucleus_cmd ( self , *args ) :
        self.setNucleus_cmd ( True ) ;

    def disableNucleus_cmd ( self , *args ) :
        self.setNucleus_cmd ( False ) ;

    def insert ( self , width ) :
        
        self.nucleus_txtScrll = pm.textScrollList ( 'nucleus_txtScrll' , w = width , h = 60 , ams = True , sc = self.updateNucleusGUI ) ;

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/2 ) , ( 2 , width/2 ) ] ) :

            self.enableNucleus_btn  = pm.button ( 'enableNucleus_btn' , label = 'Enable Nucleus' , c = self.enableNucleus_cmd , w = width/2.0 ) ;
            self.disableNucleus_btn = pm.button ( 'disableNucleus_btn' , label = 'Disable Nucleus' , c = self.disableNucleus_cmd , w = width/2.0 ) ;

        self.updateNucleusGUI() ;

class NucleusNode ( object ) :
    
    def __init__ ( self ) :
        self.refreshNucleus() ;
        
    def __str__ ( self ) :
        return str(self.nucleus) ;
   
    def __repr__ ( self ) :
        return str(self.nucleus) ;

    def refreshNucleus ( self ) :
        self.nucleus = pm.ls ( type = 'nucleus' ) ;
        self.nucleus.sort() ;

    # query current enable state, to use when reset
    def getEnableState ( self ) :
        self.refreshNucleus() ;
        if self.nucleus :
            self.enable = [] ;
            for each in self.nucleus :
                each = pm.general.PyNode ( each ) ;
                self.enable.append ( each.enable.get() ) ;
        #print self.enable ;
    
    # reset enable state to getEnableState
    def reset ( self ) :
        self.refreshNucleus() ;
        if self.nucleus :
            for i in range ( 0 , len(self.nucleus) ) :
                self.nucleus[i].enable.set( self.enable[i] ) ;
    
    # set enable, disable
    def setEnable ( self , state ) :
        self.refreshNucleus() ;
        if self.nucleus :
            for each in self.nucleus :
                each = pm.general.PyNode ( each ) ;
                each.enable.set( state ) ;

    def pmDir ( self ) :
        for each in dir ( pm.general.PyNode ( self.nucleus[0] ) ) :
            print each ;
    
    def dir ( self ) :
        for each in dir ( self ) :
            print each ;