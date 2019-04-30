import pymel.core as pm ; 

class ModelPanel ( object ) :

    def __init__ ( self ) :     
        self.currentModelPanel = self.getCurrentModelPanel() ;

    def __str__ ( self ) :
        return str ( self.currentModelPanel ) ;

    def __repr__ ( self ) :
        return str ( self.currentModelPanel ) ;

    def getCurrentModelPanel ( self ) :
        # get all current active model panel

        modelPanel  = pm.getPanel ( type = 'modelPanel' ) ;
        activePanel = pm.getPanel ( vis = True ) ;

        currentModelPanel = [] ; 

        for each in activePanel :
            if each in modelPanel :
                currentModelPanel.append ( each ) ;

        return currentModelPanel ;

    