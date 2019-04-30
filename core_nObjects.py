import pymel.core as pm ;

class NObjectUtil_GUI ( object ) :

    def __init__ ( self ) :
        pass ;

    def __str__ ( self ) :
        pass ;

    def __repr__ ( self ) :
        pass ;

    def enable ( node ) :
        node = pm.general.PyNode ( node ) ;
        node.enable.set(1) ;

    def disable ( node ) :
        node = pm.general.PyNode ( node ) ;
        node.enable.set(0) ;        

    def getNNode ( self , *args ) :
        # return [ [nCloth] , [nRigid] , [nHair] ] ;
        selection = pm.ls ( sl = True ) ;

        nCloth_list = [] ;
        nHair_list  = [] ;
        nRigid_list = [] ;
        return_list = [] ;

        for each in selection :

            # if what you select has a shape, just in case you select a group, nucleus, or the like
            if each.getShape() :

                # for when you select a mesh
                if each.getShape().nodeType() == 'mesh' :

                    nCloth = each.getShape().listConnections ( type = 'nCloth' ) ;
                    if nCloth :
                        nCloth_list.append ( nCloth[0].getShape() ) ;
                    
                    nRigid = each.getShape().listConnections ( type = 'nRigid' ) ;
                    if nRigid :
                        nRigid_list.append ( nRigid[0].getShape() ) ;
                
                # for when you select nObject directly
                else :
                    nCloth = each.getShape ( type = 'nCloth' ) ;
                    if nCloth :
                        nCloth_list.append ( nCloth ) ;

                    nRigid = each.getShape ( type = 'nRigid' ) ;
                    if nRigid :
                        nRigid_list.append ( nRigid ) ;

                    nHair = each.getShape ( type = 'hairSystem' ) ;
                    if nHair :
                        nHair_list.append ( nHair ) ;

        if nCloth_list :
            return_list.append ( nCloth_list ) ;

        if nRigid_list :
            return_list.append ( nRigid_list ) ;
        
        if nHair_list :
            return_list.append ( nHair_list ) ;

        return return_list ;

    def setNObjct_cmd ( self , state = 1 , *args ) :

        nObject_list = self.getNNode() ;

        for node_list in nObject_list :

            for node in node_list :                
                
                attr = None ;

                if ( node.nodeType() == 'nCloth' ) or ( node.nodeType() == 'nRigid' ) :
                    attr = [ 'isDynamic' , 0 , 1 ] ;
            
                elif node.nodeType() == 'hairSystem' :
                    attr = [ 'simulationMethod' , 0 , 3 ] ;
                    # off = 0 , on = 3

                if attr :

                    if state :
                        exec ( 'node.{attr1}.set({attr2})'.format ( attr1 = attr[0] , attr2 = attr[2] ) ) ;
                        print ( "{node} <<< is now enabled".format ( node = node ) ) ;
                    else :
                        exec ( 'node.{attr1}.set({attr2})'.format ( attr1 = attr[0] , attr2 = attr[1] ) ) ;
                        print ( "{node} <<< is now disabled".format ( node = node ) ) ;

    def enableNObject_cmd ( self , *args ) :
        self.setNObjct_cmd ( state = 1 ) ;
            
    def disableNObject_cmd ( self , *args ) :
        self.setNObjct_cmd ( state = 0 ) ;

    def insert ( self , width ) :

        with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width/2 ) , ( 2 , width/2 ) ] ) :

            self.enableNObject_btn  = pm.button ( 'enableNObject_btn'   , label = 'Enable nObject'      , w = width/2   , c = self.enableNObject_cmd    ) ;
            self.disableNObject_btn = pm.button ( 'disableNObject_btn'  , label = 'Disable nObjects'    , w = width/2   , c = self.disableNObject_cmd   ) ;

        pm.text ( 'Supported nObjects: nCloth; nHair; Passive Collider' ) ;