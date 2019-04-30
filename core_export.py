import pymel.core as pm ;

from sim.sim_simUtilities import core_general as gen ;
reload ( gen ) ;

class Export_GUI ( object ) :

    def __init__ ( self ) :
        self.currentProjectPath = pm.workspace ( q = True , rootDirectory = True ) ;
        # D:/TwoHeroes/film001/q0420/s0160/spiderGirlGod_001/
        self.productPath        = self.currentProjectPath + 'cache/product/' ;
        
        
    def __str__ ( self ) :
        pass ;

    def __repr__ ( self ) :
        pass ;

    def insert ( self , width , *args ) :


        with pm.rowColumnLayout ( nc = 5 , cw = [ ( 1 , width/5 ) , ( 2 , width/5 ) , ( 3 , width/5 ) , ( 4 , width/5 ) , ( 5 , width/5 ) ] ) :

            pm.text ( label = '' ) ;
            
            with pm.rowColumnLayout ( nc = 1 , w = width/5 ) :
                self.cacheStart_intField = pm.intField ( 'cacheStart_intField' , w = width/5 ) ;
                pm.text ( label = 'Start' , w = width/5 ) ;
            
            pm.text ( label = '' ) ;

            with pm.rowColumnLayout ( nc = 1 , w = width/5 ) :
                self.cacheEnd_intField = pm.intField ( 'cacheEnd_intField' , w = width/5 ) ;
                pm.text ( label = 'End' , w = width/5 ) ;

            pm.text ( label = '' ) ;