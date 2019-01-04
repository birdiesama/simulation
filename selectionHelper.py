import pymel.core as pm ;

type = 'mesh' ;
searchString = 'branch_' ;

selection_list = pm.ls ( sl = True ) ;
toSelect_list = [] ;

for selection in selection_list :
  if searchString in selection :
  
