import json
from fabric.api import *
from fabric.state import env

env.release = 'current'
#env.config_file = 'deploy.yml'
def dev():
    #"dev server configs"
    devel = json.load(open('devel.json'))
    env.settings = 'Dev'
    env.user = 'root'
    env.app_path = devel["app_path"]
    env.app_user = devel["app_user"]
    env.app_user_group = devel["app_user_group"]
    env.hosts = devel["hosts"]
    env.key_filename = devel["sshkey"]
    env.mysql_host = devel["mysql_host"]
    env.mysql_database_name = devel["mysql_database_name"]
    env.mysql_user = devel["mysql_user"]
    env.mysql_password = devel["mysql_password"]
    env.skip_bad_hosts=True

def edit_settings():
    #Add mysql database settings
    run    
#@run_once
def intial():
    #intialize for the first time
    run('mkdir -p %(app_path)s; cd %(app_path)s; mkdir releases; mkdir repo' % env)
    git_clone_repo()
    git_pull_latest()
    run('mysql -h %(mysql_host)s -u %(mysql_user)s --password=%(mysql_password)s  %(mysql_database_name)s < /var/www/apps/devportal/repo/database/dc_portal.sql' % env)

#@task('hosts')
def deploy(GIT_REVISION):
    env.GIT_REVISION = GIT_REVISION
    git_pull_revision(GIT_REVISION)
    symlink_current()
    
def git_clone_repo():
    #deploy
     run('cd %(app_path)s; git clone git@github.com:apigeecs/nhhcn_dc_portal.git repo' % env)

def git_pull_latest():
    #update git and create symlinks
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')
    run("cd %(app_path)s/repo; git pull origin master" % env)
    run('cp -R %(app_path)s/repo %(app_path)s/releases/%(release)s; rm -rf %(app_path)s/releases/%(release)s/.git*' % env)
    
    
def git_pull_revision(GIT_REVISION):
    #update git with revision
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')
    run("cd %(app_path)s/repo; git reset --hard; git checkout master; git reset --hard HEAD; git pull ; git checkout %(GIT_REVISION)s ; git reset --hard %(GIT_REVISION)s" % env)
    run('cp -R %(app_path)s/repo %(app_path)s/releases/%(release)s; rm -rf %(app_path)s/releases/%(release)s/.git*' % env)
    
        
def symlink_current():
    #symlink current to release, have to add lines to exclude persistent or shared directories like files
    with settings(warn_only=True):
        run('cd %(app_path)s; rm -rf releases/previous; mv current releases/previous ;' % env)
        run('cd %(app_path)s; ln -s %(app_path)s/releases/%(release)s/ current' % env)
    #""" production settings"""
    #run('cd %(app_path)s/releases/current/; cp settings_%(settings)s.py myproject/settings.py' % env)
    #with settings(warn_only=True):
    #run('rm %(app_path)s/shared/static' % env)
    #run('cd %(app_path)s/releases/current/static/; ln -s %(app_path)s/releases/%(release)s/static %(app_path)s/shared/static ' %env)
    
#def restart_services():
    #with settings(warn_only=True):
 #   run('/etc/init.d/httpd' % env)

     
    
    
