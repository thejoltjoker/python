import os
import traceback
import tempfile
import shutil

import pymel.core as pm
import system.quicktime as quicktime
reload(quicktime)
import digital37.maya.general.scene as scene
reload(scene)

class PlayBlast(scene.Scene,quicktime.Quicktime):
    '''
    playblast
    '''
    def __init__(self):
        pass
        
    def set_pb_name(self,pb_name):
        self.PB_Name = pb_name
        
    # use outputDir to replace maya scene's full path name's 'anim'
    # example: scenes/shot/ep01/ep01_sc0010/anim/project_an_ep01_sc0010.mb
    #          scenes/shot/ep01/ep01_sc0010/outputDir/project_an_ep01_sc0010.mov
    def set_pb_name_by_folder(self,outputDir='playblast'):
        self.get_scene_name()
        # self.Scene_Name_Full_Path defined in scene.Scene
        if self.Scene_Name_Full_Path:
            self.set_pb_name( self.Scene_Name_Full_Path_Without_Ext.replace( '/anim/', ('/%s/' % outputDir) ) )
        else:
            return False
            
    def evalDeferred_playblast(self,fileName,width,height,fp):
        try:
            pm.evalDeferred( 'pm.playblast(format="iff",sequenceTime=0,clearCache=1,viewer=0,\
                    showOrnaments=1,fp='+str(fp)+',percent=100,compression="jpg",\
                    widthHeight=('+str(width)+','+str(height)+'),\
                    forceOverwrite=1,quality=100,filename=\"' + fileName + '\")' )
        except:
            self.Log.error('evalDeferred_playblast error')
            self.Log.error(traceback.format_exc())
            
    def eval_playblast(self,fileName,width,height,fp):
        try:
            pm.playblast(format='iff',sequenceTime=0,clearCache=1,viewer=0,\
                     showOrnaments=1,fp=fp,percent=100,compression="jpg",\
                     widthHeight=(width,height),\
                     forceOverwrite=1,quality=100,filename=fileName)
        except:
            self.Log.error('eval_playblast error')
            self.Log.error(traceback.format_exc())
                
    def before_playblast(self,outputDir=None,width=None,height=None):
        '''
        do before playBlast
        '''
        # get playBlast image's name
        self.get_scene_name()
        if self.Name_By_Folder:
            self.set_pb_name_by_folder(outputDir)
        else:
            if not outputDir:
                fd,outputDir = tempfile.mkdtemp()
                fObj = os.fdopen(fd,'w')
                fObj.write( '' )
                fObj.close()
            #print outputDir
            # set image's name to output folder
            self.set_pb_name( os.path.abspath(os.path.join(outputDir,self.Scene_Name_Short_Without_Ext)))
        
        # get playBack range
        self.MinTime, self.MaxTime = self.get_playback_info()
        
        # get image's width and height
        # if not set width and height, then use rendering settings
        # get render settings's width and height
        if not width:
            import digital37.maya.lighting.get_render_resolution as get_render_resolution
            width,height = get_render_resolution.main()
        self.Width = width
        self.Height = height
            
    def do_playblast(self,imageName=None):
        '''
        do plabyBlast 
        '''
        if not imageName:
            #set temp images name
            fd,imageName = tempfile.mkstemp(prefix='PlayBlast')
            fObj = os.fdopen(fd,'w')
            fObj.write( '' )
            fObj.close()          
        self.Images = imageName
        
        print 'self.Images:%s' % self.Images
        pm.playblast(format='iff',sequenceTime=0,clearCache=1,viewer=0,\
                     showOrnaments=1,fp=1,percent=100,compression="jpg",\
                     widthHeight=(self.Width,self.Height),\
                     forceOverwrite=1,quality=100,filename=self.Images)
        
    def after_playblast(self):
        '''
        do after playBlast
        '''
        # make movie from image sequence
        # add frame number and extension to make movie
        if self.Make_Movie: 
            self.make_mov( (self.Images + ('.%s.jpeg' % self.MinTime)), self.MinTime, self.MaxTime )
        
    def playBlast_with_mov(self,nameByFolder=False,outputDir='playblast',imageName=None,
                  width=None,height=None,quicktime_settings_file=None,quicktime_time=None):
        # check images name's path is relative with scene's name or not
        self.Name_By_Folder = nameByFolder
        self.Make_Movie = True
        if quicktime_settings_file:
            self.set_quicktime_settings(quicktime_settings_file)
            self.set_time(quicktime_time)
            # TODO 128 will be return in some pc when do playblast
            self.set_subprocess_returnCode([0,128])
                
            self.before_playblast(outputDir, width, height)
            self.do_playblast(imageName)
            self.after_playblast()
            
        else:
            self.Log.error('can not get quicktime_settings file')
        
        
    def playBlast(self,nameByFolder=False,outputDir='playblast',imageName=None,
                  width=None,height=None):
        self.Make_Movie = False
        # check images name's path is relative with scene's name or not
        self.Name_By_Folder = nameByFolder
        self.before_playblast(outputDir, width, height)
        self.do_playblast(imageName)
        self.after_playblast()
                
    def do_after_execute_cmd(self):
        '''override do_after_execute_cmd in system module
        '''
        self.Log.debug( 'PlayBlast:Success\r\n' )
        # copy movie
        # check folder exists or not
        self.create_dir( os.path.dirname(self.PB_Name + '.mov') )
        shutil.copy( (self.Images + '.mov'), (self.PB_Name + '.mov') )
        cmd = 'start '
        cmd += self.PB_Name + '.mov'
        try:
            os.system(cmd)
        except:
            self.Log.error( traceback.format_exc() )
        self.Log.debug("PlayBlast: %s",(self.PB_Name + '.mov') )
    
def main(log=None,nameByFolder=False,outputDir='playblast',imageName=None,
         width=None,height=None,makeMovie=False,quicktime_settings_file=None,quicktime_time=None):
    a = PlayBlast()
    if not log:
        a.get_stream_logger()
    if makeMovie:
        a.playBlast_with_mov(nameByFolder, outputDir, imageName, width, height, quicktime_settings_file,quicktime_time)
    else:
        a.playBlast(nameByFolder, outputDir, imageName, width, height)
    
if __name__ == '__main__' :
    #pass
    #main(None,None,None,None,None,None,False,'D:/RND/project/pipelineProject/quicktime/quicktime_export_settings.xml')
    main(None,None,None,None,None,None,True,'D:/RND/project/pipelineProject/quicktime/quicktime_export_settings.xml')