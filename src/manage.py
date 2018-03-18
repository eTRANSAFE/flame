#! -*- coding: utf-8 -*-

##    Description    Flame Manage class
##
##    Authors:       Manuel Pastor (manuel.pastor@upf.edu)
##
##    Copyright 2018 Manuel Pastor
##
##    This file is part of Flame
##
##    Flame is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 3.
##
##    Flame is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with Flame. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import shutil

import utils

class Manage:

    def __init__ (self, model, version, action):

        self.model = model
        self.version = version
        self.action = action

        return

    def action_new (self, model):

        ndir = utils.base_path(model)
        
        # check if there is already a tree for this endpoint
        if os.path.isdir (ndir):
            return False, 'This endpoint already exists'
        try:
            os.mkdir (ndir)
        except:
            return False,'unable to create directory : '+ndir

        ndir+='/dev'
        try:
            os.mkdir (ndir)
        except:
            return False,'unable to create directory '+ndir

        # TODO: create templates directory with empty childs
        try:
            wkd = os.path.dirname(os.path.abspath(__file__))
            children_names = ['apply','control','idata','odata','learn']
            for cname in children_names:
                shutil.copy(wkd+'/children/'+cname+'_child.py',ndir+'/'+cname+'_child.py')
        except:
            return False,'unable to copy children classes at '+ndir

        return True,'version created OK'

    def action_kill (self, model):

        ndir = utils.base_path(model)
        
        if not os.path.isdir (ndir):
            return False, 'model not found'

        shutil.rmtree(ndir, ignore_errors=True)

        return True, 'manage OK'

    def action_publish (self, model):

        bdir = utils.base_path(model)

        if not os.path.isdir(bdir):
            return False, 'model not found'
    
        v = None
        try:
            v = [int(x[-6:]) for x in os.listdir (bdir) if x.startswith("ver")]
        except:
            pass

        if not v:
            max_version = 0
        else:
            max_version = max(v)

        new_dir = bdir+'/ver%0.6d'%(max_version+1)

        if os.path.isdir(new_dir):
            return False, 'version already exists'

        shutil.copytree(bdir+'/dev', new_dir)
        
        return True, 'manage OK'

    def action_remove (self, model, version):

        if version == 0:
            return False, 'development version cannot be removed'

        rdir = utils.model_path(model, version)
        if not os.path.isdir(rdir):
            return False, 'version not found'

        shutil.rmtree(rdir, ignore_errors=True)

        return True, 'manage OK'

    def action_list (self):
        print ('manage list')
        return True, 'manage OK'

    def run (self):
        ''' Executes a default predicton workflow '''

        if self.action == 'new':
            success, results = self.action_new (self.model)

        elif self.action == 'kill':
            success, results = self.action_kill (self.model)

        elif self.action == 'remove':
            success, results = self.action_remove (self.model, self.version)

        elif self.action == 'publish':
            success, results = self.action_publish (self.model)

        elif self.action == 'list':
            success, results = self.action_list ()

        return success, results

