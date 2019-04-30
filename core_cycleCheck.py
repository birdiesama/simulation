import pymel.core as pm ;

class CycleCheckUtil_GUI ( object ) :

    def __init__ ( self ) :
        pass ;

    def __str__ ( self ) :
        pass ;

    def __repr__ ( self ) :
        pass ;

    def enableCycle_cmd ( self , *args ) :
        pm.cycleCheck ( e = 1 ) ;
        self.updateCycleCheckGUI ( ) ;
        #print pm.cycleCheck ( q = True , e = True ) ;

    def disableCycle_cmd ( self , *args ) :
        pm.cycleCheck ( e = 0 ) ;
        self.updateCycleCheckGUI ( ) ;
        #print pm.cycleCheck ( q = True , e = True ) ;

    def setCycleCheckBtnState ( self , state ) :

        if state :
            pm.button ( self.enableCycle_btn , e = True , nbg = True ) ;
            pm.button ( self.disableCycle_btn , e = True , nbg = False ) ;  

        else :
            pm.button ( self.enableCycle_btn , e = True , nbg = False ) ;
            pm.button ( self.disableCycle_btn , e = True , nbg = True ) ;  

    def updateCycleCheckGUI ( self ) :
        
        cycleCheck_state = pm.cycleCheck ( q = True , e = True ) ;

        if cycleCheck_state :
            self.setCycleCheckBtnState ( True ) ;
        else :
            self.setCycleCheckBtnState ( False ) ;

    def insert ( self , width ) :

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/2 ) , ( 2 , width/2 ) ] ) :

            self.enableCycle_btn = pm.button ( 'enableCycle_btn' , label = 'Enable Cycle Check' , width = width/2 , c = self.enableCycle_cmd ) ;
            self.disableCycle_btn = pm.button ( 'disableCycle_btn' , label = 'Disable Cycle Check' , width = width/2 , c = self.disableCycle_cmd ) ;

            self.updateCycleCheckGUI() ;