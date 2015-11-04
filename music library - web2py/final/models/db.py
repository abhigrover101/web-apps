# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db=MEMDB(Client())
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## comment/uncomment as needed

from gluon.tools import *
auth=Auth(globals(),db)              # authentication/authorization

# mail=Mail()                                  # mailer
# mail.settings.server='smtp.gmail.com:587'    # your SMTP server
# mail.settings.sender='you@gmail.com'         # your email
# mail.settings.login='username:password'      # your credentials or None

auth.settings.hmac_key='sha512:2fddc896-8eaa-4d40-9ae6-425259dd0695'
auth.define_tables()                 # creates all needed tables
#auth.settings.table_user = db.define_table('auth_user',
       # db.Field('first_name', 'string', length=128, default=''),
      #  db.Field('last_name', 'string', length=128, default='', requires = IS_NOT_EMPTY()),
     #   db.Field('email', 'string', length=128, default=''),
    #    db.Field('password', 'password', requires = CRYPT(), readable=False),
   #     db.Field('registration_key', 'string', length=128, writable=False, readable=False, default=''),
  #      migrate=False)
##t = auth.settings.table_user
#t.email.requires = [IS_EMAIL(), IS_NOT_IN_DB(db, 'auth_user.email')]

##auth.define_tables()                 # creates all needed tables

#crud=Crud(globals(),db)              # for CRUD helpers using auth
#service=Service(globals())           # for json, xml, jsonrpc, xmlrpc, amfrpc
#crud.settings.auth=auth                      # enforces authorization on crud
#mail=Mail()         
#mail.settings.server='mail.iiit.ac.in:25'      # your SMTP server
#mail.settings.sender='music@students.iiit.ac.in' # your email
         # your email
# mail.settings.login='username:password'      # your credentials or None
##auth.settings.mailer=mail                    # for user email verification
##auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = True
##auth.messages.verify_email = 'Click on the link http://web.iiit.ac.in/~piyush'+'/%(key)s to verify your email'
# auth.settings.reset_password_requires_verification = True
# auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'
##auth.settings.create_user_groups = False
# auth.settings.mailer=mail          # for user email verification
# auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = True
# auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
# auth.settings.reset_password_requires_verification = True
# auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

# crud.settings.auth=auth            # enforces authorization on crud

## more options discussed in gluon/tools.py
#########################################################################

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
import datetime
     
db.define_table(
  'songs_database',
  Field('song_name','string',requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'songs_database.song_name')]),
  Field('upload_song','upload',requires=IS_NOT_EMPTY()),
  Field('upload_song_cover','upload'),
  Field('album_name','string',default='unknown'),
  Field('artist','string',default='unknown'),
  Field('Genre'),
  Field('language','string',default='unknown',requires=IS_NOT_EMPTY()), 
  Field('uploaded_by','integer'),
  Field('year','integer',requires=IS_INT_IN_RANGE(1800,2020)),
  Field('no_down','integer',default=0,writable=False,readable=False)
  #rating plugin,likes plugin ,no' sdown, listen
  )

db.songs_database.uploaded_by.default=auth.user.id if auth.user else -1
db.songs_database.uploaded_by.writable=db.songs_database.uploaded_by.readable=False
db.songs_database.Genre.requires=IS_IN_SET(['Rock','Jazz','Pop','Bollywood','Classic','Quwalli','other'])  

db.define_table('comments',Field('user_name','string',requires=IS_NOT_EMPTY(),default=(auth.user.first_name if auth.user else 0),readable=False,writable=False),Field('song_id','integer',requires=IS_NOT_EMPTY(),readable=False,writable=False),Field('comment','text',requires=IS_NOT_EMPTY()),Field('time','datetime',default=request.now,writable=False))


db.define_table(
'like',Field('user_id','integer',requires=IS_NOT_EMPTY(),default=(auth.user.id if auth.user else -1),writable=False),
Field('song_id','integer',requires=[IS_NOT_EMPTY(),IS_IN_DB(db,'songs_database.song_name')])
)

db.define_table(
'notifications',Field('user_id',db.auth_user,requires=IS_NOT_EMPTY()),  #jisko notiication  jani hain 
Field('value','text',requires=IS_NOT_EMPTY()),
Field('song_id','integer',requires=IS_NOT_EMPTY())
)



db.define_table(
'new_playlist',Field('user_id',db.auth_user,requires=IS_NOT_EMPTY(),default=auth.user.id  if auth.user else -1,readable=False,writable=False),
Field('playlist_name','string',requires=IS_NOT_EMPTY()))


db.define_table(
'playlist',Field('playlist_id',db.new_playlist), ##value=arg(0) implemented in controller
Field('song_name','string',requires=IS_NOT_EMPTY()),Field('song_id','integer',requires=IS_NOT_EMPTY()))
#db.define_table(
#'autosearch',Fiel
