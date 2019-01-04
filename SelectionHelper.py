import pymel.core as pm ;

searchType = 'mesh' ;
searchString = 'branch_' ;

selection_list = pm.ls ( sl = True ) ;
toSelect_list = [] ;

for selection in selection_list :
    
    if searchString in selection.nodeName() :
        if selection.getShape() :
            if selection.getShape().nodeType() == searchType :
                toSelect_list.append ( selection ) ;
    
    item_list = selection.listRelatives ( ad = True , type = searchType ) ;
    
    for item in item_list :
        if searchString in item.nodeName() :
            toSelect_list.append ( item.getParent() ) ;

pm.select ( toSelect_list ) ;
