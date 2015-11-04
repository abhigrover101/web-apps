# -*- coding: utf-8 -*- 

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

def index():
    
    #response.title = 'IIIT Hyderabad'
    #response.subtitle = 'PGSSP'
    #response.menu = None
    #response.menu_edit = None
    #r = db(db.details.personid == auth.user.id).select() if auth.user else None
    #details = r[0] if r else None
    #return dict(details=details)
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    return dict(p=db(db.songs_database.id>0).select())

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[adb.notifications.insert(user_id=ss[0].uploaded_by, value='%(p)s commented \"%(v)s\" on %(o)s '%{'p':auth.user.first_name,'v':request.vars.comment,'o':ss[0].song_name},song_id=ss[0].id)pp]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()

@auth.requires_login()
def upload_box():
    form=SQLFORM(db.songs_database)
    if form.accepts(request.vars,session):
        response.flash='New Song uploaded'
    return dict(upload=form)

@auth.requires_login()
def search_box():
    form=FORM(TABLE(TR('Find:',INPUT(_type='string',_name='Find',requires=IS_NOT_EMPTY())),TR('',INPUT(_type='submit',_value='search')))) 
    d=[]  
    if form.accepts(request.vars,session):
         s=''
         p=request.vars.Find
         i=0     
         for i in range(0,len(p)+1):                     
               if(len(p)==i or p[i]==' '):
                r=db((s==db.songs_database.song_name) | (s==db.songs_database.artist) | (s==db.songs_database.Genre) | (s==db.songs_database.album_name) ).select()
                if len(r)!=0:
                  o=0                
                  for o in range(0,len(r)):
                    if r[o].id not in d: 
                      d+=[r[o].id]
                s=''
               else:
                  s=s+p[i]   
         if(len(d)==0):
            response.flash='sorry no result'          
         else:  
          response.flash='search complete'            
    return dict(form=form,d=d,h=(db(db.songs_database.id>0).select()))


@auth.requires_login()
def list_songs():
    u=request.args(0)
    if u==None: u=0 
    return dict(songs=db(db.songs_database.id>0).select(),u=int(u))

def view_song():
    image_id = request.args(0) or redirect(URL(r=request,f='index'))
   # if image_id>(db(db.songs_database.id>0).count()):
    #        redirect(URL(r=request,f='index'))
    form=SQLFORM(db.comments)
    db.comments.song_id.default = image_id
    s=db(db.comments.song_id==image_id).select()
    so=db(db.comments.song_id==image_id).count()
    u=db(db.songs_database.id==image_id).select()
    if (form.accepts(request.vars,session)):
        ss=db(db.songs_database.id==image_id).select()
        print (ss[0].uploaded_by) , int(ss[0].uploaded_by)
        if (int(auth.user.id) != int(ss[0].uploaded_by)): 
           print auth.user.id , ss[0].uploaded_by
           db.notifications.insert(user_id=ss[0].uploaded_by, value='%(p)s commented \"%(v)s\" on %(o)s '%{'p':auth.user.first_name,'v':request.vars.comment,'o':ss[0].song_name},song_id=ss[0].id)
    return dict(u=u,so=so,songs=db(db.songs_database.id==image_id).select(),form=form,s=s)
    
@auth.requires_login()
def create_playlist():
       name=SQLFORM(db.new_playlist)
       if(name.accepts(request.vars,session)):
           #    db.playlist.insert(playlist_id=request.vars.id)
               session.flash='new playlist created'
               redirect(URL(r=request,f='select_songs',args=name.vars.id))
       return dict(name=name)

@auth.requires_login()
def select_songs(): 
       i=request.args(0) 
       return dict(i=i,songs=db(db.songs_database.id>0).select())
       
@auth.requires_login()
def play():
    return dict(l=db(db.new_playlist.user_id==auth.user.id).select()) 

@auth.requires_login()    
def del_play():
     db(db.new_playlist.id==request.args(0)).delete()
     db(db.playlist.playlist_id==request.args(0)).delete()
     redirect(URL(r=request,f='play'))
     return dict(a=1)
     
@auth.requires_login()
def playlist():
    return dict(play=db(db.playlist.playlist_id==request.args(0)).select())

@auth.requires_login()
def add():
    a=request.args(0)
    b=request.args(1)
    d=db(db.playlist.playlist_id==a).select()
    for i in d:
        print  i.song_name, b
        if i.song_name==b :
           session.flash="already present"
           redirect(URL(r=request,f='select_songs',args=a))                
    db.playlist.insert(playlist_id=request.args(0),song_name=request.args(1),song_id=request.args(2))
    redirect(URL(r=request,f='select_songs',args=a))
    return dict(a=a,b=b)

@auth.requires_login()
def del_play_song():
    db(db.playlist.playlist_id==request.args(0) and db.playlist.song_name==request.args(1)).delete()
    redirect(URL(r=request,f='playlist',args=request.args(0)))
    return dict(a=1)   
     
@auth.requires_login()
def edit():       
    row = db.songs_database[request.args(0)]
    form = SQLFORM(db.songs_database,row,deletable=True)
    if form.accepts(request.vars, session):
        response.flash = 'record updated'
    return dict(form=form)
    
         # db(db.songs_database.id > 0).count()
@auth.requires_login()
def notify():
    p=db(db.notifications.user_id==auth.user.id).select() 
    return dict(p=p)
    
@auth.requires_login()    
def del_notification():
   if db(db.notifications.id==request.args(0)).delete():
        response.flash ='song deleted'
        redirect(URL(r=request,f='notify'))
   return dict(a=1) 
       
@auth.requires_login()
def all():
    p=request.args(0)
    u=request.args(1)
    s=db(db.comments.song_id==p).select()
    return dict(s=s,p=p,u=int(u))

def last_uploads():
    return dict(p=db(db.songs_database.id>0).select())

@auth.requires_login()    
def my_uploads():
    if request.args(0)==None: 
        u=0
    else: u=int(request.args(0))
    print u
    return dict(p=db(db.songs_database.uploaded_by==auth.user.id).select(),u=u)

@auth.requires_login()
def del_my():
     db(db.songs_database.id==request.args(0)).delete()
     redirect(URL(r=request,f='my_uploads'))
     return dict(a=1)
@auth.requires_login()
def down():
 #print "yaaaaa" , request.args(1)
 d=db(db.songs_database.id==request.args(1)).select()
 db(db.songs_database.id==request.args(1)).update(no_down=d[0].no_down+1)
 redirect(URL(r=request,f='download',args=request.args(0)))

@auth.requires_login()
def likes():
 ss=db(db.songs_database.id==request.args(0)).select()
 if (int(auth.user.id) != int(ss[0].uploaded_by)):
    db.notifications.insert(user_id=ss[0].uploaded_by, value='%(p)s likes "%(o)s" '%{'p':auth.user.first_name,'o':ss[0].song_name},song_id=ss[0].id)
    
 redirect(URL(r=request,f='view_song',args=request.args(0)))
 return dict(a=1)
