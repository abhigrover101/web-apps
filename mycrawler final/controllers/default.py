# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import cStringIO
import csv
import re
import string
import subprocess
import time

#country list
country=['United States', 'Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Caribbean Nations', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Cook Islands', 'Costa Rica', "Cote D'Ivoire (Ivory Coast)", 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Federated States of Micronesia', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea', 'Korea (North)', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovak Republic', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City State (Holy See)', 'Venezuela', 'Vietnam', 'Virgin Islands (British)', 'Virgin Islands (U.S.)', 'Wallis and Futuna', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe', 'Other']

#country id list    
countryid=['us', 'af', 'ax', 'al', 'dz', 'as', 'ad', 'ao', 'ai', 'aq', 'ag', 'ar', 'am', 'aw', 'au', 'at', 'az', 'bs', 'bh', 'bd', 'bb', 'by', 'be', 'bz', 'bj', 'bm', 'bt', 'bo', 'ba', 'bw', 'br', 'io', 'bn', 'bg', 'bf', 'bi', 'kh', 'cm', 'ca', 'cv', 'cb', 'ky', 'cf', 'td', 'cl', 'cn', 'cx', 'cc', 'co', 'km', 'cg', 'ck', 'cr', 'ci', 'hr', 'cu', 'cy', 'cz', 'cd', 'dk', 'dj', 'dm', 'do', 'tp', 'ec', 'eg', 'sv', 'gq', 'er', 'ee', 'et', 'fk', 'fo', 'fm', 'fj', 'fi', 'fr', 'gf', 'pf', 'tf', 'ga', 'gm', 'ge', 'de', 'gh', 'gi', 'gr', 'gl', 'gd', 'gp', 'gu', 'gt', 'gg', 'gn', 'gw', 'gy', 'ht', 'hn', 'hk', 'hu', 'is', 'in', 'id', 'ir', 'iq', 'ie', 'im', 'il', 'it', 'jm', 'jp', 'je', 'jo', 'kz', 'ke', 'ki', 'kr', 'kp', 'kw', 'kg', 'la', 'lv', 'lb', 'ls', 'lr', 'ly', 'li', 'lt', 'lu', 'mo', 'mk', 'mg', 'mw', 'my', 'mv', 'ml', 'mt', 'mh', 'mq', 'mr', 'mu', 'yt', 'mx', 'md', 'mc', 'mn', 'me', 'ms', 'ma', 'mz', 'mm', 'na', 'nr', 'np', 'nl', 'an', 'nc', 'nz', 'ni', 'ne', 'ng', 'nu', 'nf', 'mp', 'no', 'om', 'pk', 'pw', 'ps', 'pa', 'pg', 'py', 'pe', 'ph', 'pn', 'pl', 'pt', 'pr', 'qa', 're', 'ro', 'ru', 'rw', 'sh', 'kn', 'lc', 'pm', 'vc', 'ws', 'sm', 'st', 'sa', 'sn', 'rs', 'sc', 'sl', 'sg', 'sk', 'si', 'sb', 'so', 'za', 'es', 'lk', 'sd', 'sr', 'sj', 'sz', 'se', 'ch', 'sy', 'tw', 'tj', 'tz', 'th', 'tl', 'tg', 'tk', 'to', 'tt', 'tn', 'tr', 'tm', 'tc', 'tv', 'ug', 'ua', 'ae', 'gb', 'uy', 'uz', 'vu', 'va', 've', 'vn', 'vg', 'vi', 'wf', 'eh', 'ye', 'zm', 'zw', 'oo']

#industries list
industries=['All Industries','Accounting', 'Airlines/Aviation', 'Alternative Dispute Resolution', 'Alternative Medicine', 'Animation', 'Apparel & Fashion', 'Architecture & Planning', 'Arts and Crafts', 'Automotive', 'Aviation & Aerospace', 'Banking', 'Biotechnology', 'Broadcast Media', 'Building Materials', 'Business Supplies and Equipment', 'Capital Markets', 'Chemicals', 'Civic & Social Organization', 'Civil Engineering', 'Commercial Real Estate', 'Computer & Network Security', 'Computer Games', 'Computer Hardware', 'Computer Networking', 'Computer Software', 'Construction', 'Consumer Electronics', 'Consumer Goods', 'Consumer Services', 'Cosmetics', 'Dairy', 'Defense & Space', 'Design', 'Education Management', 'E-Learning', 'Electrical/Electronic Manufacturing', 'Entertainment', 'Environmental Services', 'Events Services', 'Executive Office', 'Facilities Services', 'Farming', 'Financial Services', 'Fine Art', 'Fishery', 'Food & Beverages', 'Food Production', 'Fund-Raising', 'Furniture', 'Gambling & Casinos', 'Glass, Ceramics & Concrete', 'Government Administration', 'Government Relations', 'Graphic Design', 'Health, Wellness and Fitness', 'Higher Education', 'Hospital & Health Care', 'Hospitality', 'Human Resources', 'Import and Export', 'Individual & Family Services', 'Industrial Automation', 'Information Services', 'Information Technology and Services', 'Insurance', 'International Affairs', 'International Trade and Development', 'Internet', 'Investment Banking', 'Investment Management', 'Judiciary', 'Law Enforcement', 'Law Practice', 'Legal Services', 'Legislative Office', 'Leisure, Travel & Tourism', 'Libraries', 'Logistics and Supply Chain', 'Luxury Goods & Jewelry', 'Machinery', 'Management Consulting', 'Maritime', 'Marketing and Advertising', 'Market Research', 'Mechanical or Industrial Engineering', 'Media Production', 'Medical Devices', 'Medical Practice', 'Mental Health Care', 'Military', 'Mining & Metals', 'Motion Pictures and Film', 'Museums and Institutions', 'Music', 'Nanotechnology', 'Newspapers', 'Nonprofit Organization Management', 'Oil & Energy', 'Online Media', 'Outsourcing/Offshoring', 'Package/Freight Delivery', 'Packaging and Containers', 'Paper & Forest Products', 'Performing Arts', 'Pharmaceuticals', 'Philanthropy', 'Photography', 'Plastics', 'Political Organization', 'Primary/Secondary Education', 'Printing', 'Professional Training & Coaching', 'Program Development', 'Public Policy', 'Public Relations and Communications', 'Public Safety', 'Publishing', 'Railroad Manufacture', 'Ranching', 'Real Estate', 'Recreational Facilities and Services', 'Religious Institutions', 'Renewables & Environment', 'Research', 'Restaurants', 'Retail', 'Security and Investigations', 'Semiconductors', 'Shipbuilding', 'Sporting Goods', 'Sports', 'Staffing and Recruiting', 'Supermarkets', 'Telecommunications', 'Textiles', 'Think Tanks', 'Tobacco', 'Translation and Localization', 'Transportation/Trucking/Railroad', 'Utilities', 'Venture Capital & Private Equity', 'Veterinary', 'Warehousing', 'Wholesale', 'Wine and Spirits', 'Wireless', 'Writing and Editing']

#seniority list
seniority=['All Seniority Levels', 'Manager', 'Owner', 'Partner', 'CXO', 'VP', 'Director', 'Senior', 'Entry', 'Students & Interns', 'Volunteer']

#functions list
functions=['All Functions', 'Academics', 'Accounting', 'Administrative', 'Business development', 'Buyer', 'Consultant', 'Creative', 'Engineering', 'Entrepreneur', 'Finance', 'Human resources', 'Information technology', 'Legal', 'Marketing', 'Medical', 'Operations', 'Product', 'Public relations', 'Real estate', 'Sales', 'Support']

#options in title and company
currentpast=['CP', 'C','P', 'PNC']

#options list
cp=['Current or Past','Current','Past','Past not Current']

#THIS IS THE LOGIN PAGE
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    #login form
    form = SQLFORM.factory(
       Field('LinkedIn_User_Id'),
       Field('Password',type='password'))
       
    #checking if there is already a user logged in,i.e. creating a session
    if session.username:
        session.flash ='Login Successful'
        redirect(URL(r=request,f='enter_info')) 
       

    session.username=request.vars.LinkedIn_User_Id
    session.password=request.vars.Password
    #if form is accepted call enterinfo function
    if form.process().accepted:
        session.flash =T(session.username + ' is logged in')
        redirect(URL(r=request,f='enter_info')) 
    return dict(form=form)   

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
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

  
def enter_info():
    #form for entering information
    form = SQLFORM.factory(
       Field('First_Name'),
       Field('Last_Name'),
       Field('Keywords'),
       Field('Title'),
       Field('Title_Options',requires=IS_IN_SET(cp),default='Current or Past'),
       Field('Company'),
       Field('Company_Options',requires=IS_IN_SET(cp),default='Current or Past'),
       Field('School'),
       Field('File_Name',requires=IS_NOT_EMPTY()),
       Field('Country',requires=IS_IN_SET(country),default='United States'),
       Field('Industry',requires=IS_IN_SET(industries,multiple='multiple'),default='All Industries'),
       Field('Seniority_Levels',requires=IS_IN_SET(seniority,multiple='multiple'),default='All Seniority Levels'),
       Field('Functions',requires=IS_IN_SET(functions,multiple='multiple'),default='All Functions'))

    #response.flash = 'Refresh Page After Each Query'
    #if form accepted redirect to search function
    if form.process().accepted:
        session.flash = 'Refresh Page After Each Query'
        redirect(URL(r=request,f='search',vars=request.vars))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)
    
    
#actual search is done here
def search():
    import mechanize
    import cookielib
    import html2text
    from bs4 import BeautifulSoup
    # Browser    
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


    # The site we will navigate into, handling it's session    
    br.open('https://www.linkedin.com')

    # Select the first (index zero) form
    br.select_form(nr=0)

    # User credentials
    #br.form['session_key'] = 'mrigeshgaurav@gmail.com'
    #br.form['session_password'] = 'modeln@1234'
    
    #entering username and password user provided at login
    br.form['session_key'] = session.username
    br.form['session_password'] = session.password
    
    
    # Login by submitting form br
    br.submit()
    
    #opening the advanced search page straight away
    br.open('http://www.linkedin.com/search?trk=advsrch')
    
    #selecting the 1st form
    br.select_form(nr=1)

    #entering various fields and filters
    if request.vars.Last_Name:
        br["lname"]=request.vars.Last_Name

    if request.vars.First_Name:
        br["fname"]=request.vars.First_Name
    
    if request.vars.Keywords:
        br["keywords"]=request.vars.Keywords

    if request.vars.Company:
        br["company"]=request.vars.Company
        br["currentCompany"]=[currentpast[cp.index(request.vars.Company_Options)]]

    if request.vars.School:
        br["school"]=request.vars.School

    if request.vars.Title:
        br["title"]=request.vars.Title
        br["currentTitle"]=[currentpast[cp.index(request.vars.Title_Options)]]
        
    if request.vars.Country:
        br["countryCode"]=[countryid[country.index(request.vars.Country)]]
    
    if request.vars.Industry and request.vars.Industry!='All Industries':
        if isinstance(request.vars.Industry,list):
            for i in request.vars.Industry:
                br.find_control("facet_I").items[industries.index(i)-1].selected=True
        else:
            br.find_control("facet_I").items[industries.index(request.vars.Industry)-1].selected=True
    try:        
        if request.vars.Seniority_Levels and request.vars.Seniority_Levels!='All Seniority Levels':
            if isinstance(request.vars.Seniority_Levels,list):
                for i in request.vars.Seniority_Levels:
                    br.find_control("facet_SE").items[seniority.index(i)-1].selected=True
            else:
                br.find_control("facet_SE").items[seniority.index(request.vars.Seniority_Levels)-1].selected=True
            
        if request.vars.Functions and request.vars.Functions!='All Functions':
            if isinstance(request.vars.Functions,list):
                for i in request.vars.Functions:
                    br.find_control("facet_FA").items[functions.index(i)-1].selected=True
            else:
                br.find_control("facet_FA").items[functions.index(request.vars.Functions)-1].selected=True
    except:
        flag=1
        
    #submitting the form
    br.submit()
    
    #lists for retreiving the required data
    view_profile=[]
    firstname=[]
    titl=[]
    location=[]
    industry=[]
    current=[]
    middlename=[]
    lastname=[]
    company=[]
    emailid=[]
    
    #flag to make sure we get entries on 1st page
    flag=1
    
    #writing into file with given filename
    global csv_response

    csv_response = cStringIO.StringIO()
    
    spamWriter = csv.writer(csv_response, delimiter=',')
    
    #spamWriter = csv.writer(open(request.vars.File_Name+'.csv', 'wb'), delimiter=',')
    soup = BeautifulSoup(br.response().read())
    spamWriter.writerow(['FIRSTNAME','MIDDLENAME','LASTNAME','TITLE','CURRENT','LOCATION','INDUSTRY','PROFLEURL','COMPANYNAME','EMAIL'])
    
    #scans till there is a link to "next page"
    while soup.find('a',{"class" : "paginator-next"}) or flag==1:
        flag=0
        soup = BeautifulSoup(br.response().read())
        view_profile=[]
        firstname=[]
        titl=[]
        location=[]
        industry=[]
        current=[]
        middlename=[]
        lastname=[]
        company=[]
        emailid=[]
        
        #parsing for the html response to get information
        for k in soup.find_all('dl',{"class" : "vcard-basic"}):
            if k.find('dd',{"class" : "title"}):
                    titl.append(k.find('dd',{"class" : "title"}).get_text())
            else:
                    titl.append('NONE')
                            
            if k.find('span',{"class" : "location"}):
                    location.append(k.find('span',{"class" : "location"}).get_text())
            else:
                    location.append('NONE')
            if k.find('span',{"class" : "industry"}):
                    industry.append(k.find('span',{"class" : "industry"}).get_text())
            else:
                    industry.append('NONE')
                
        for k in soup.find_all('dl',{"class" : "vcard-expanded"}):
            temp1=[]
            temp2=[]
            if k.find('span',{"class" : "current-details more-text"}):
                    less=k.find('span',{"class" : "current-details more-text"}).get_text()
                    temp1=less[0:len(less)-4].encode('utf-8').split(' at ',1)
                    if(len(temp1)>1):
                        try:
                            temp2=temp1[1].encode('utf-8').split(',',1)
                        except:
                            temp2=['NONE']
                    else:
                        temp2=['NONE']
                    company.append(temp2[0])
                    current.append(less[0:len(less)-4])
            elif k.find('span',{"class" : "current-details"}):
                    less=k.find('span',{"class" : "current-details"}).get_text()
                    current.append(less)
                    temp1=less.encode('utf-8').split(' at ',1)
                    if(len(temp1)>1):
                        try:
                            temp2=temp1[1].encode('utf-8').split(',',1)
                        except:
                            temp2=['NONE']
                    else:
                        temp2=['NONE']
                    company.append(temp2[0])
            else:
                    current.append('NONE')
                    company.append('NONE')
               
        for l in soup.find_all('a',{"title" : "View Profile"}):
            temp=[]
            view_profile.append('http://www.linkedin.com'+l.get('href'))
            temp.append(l.get_text().encode('utf-8').split(None,2))
            if temp[0][0]:
                firstname.append(temp[0][0].strip())
            else:
                firstname.append('None')
            if temp[0][1] and (len(temp[0])-1)==1:
                lastname.append(temp[0][1].strip())
                middlename.append('None')
            else:
                lastname.append(temp[0][len(temp[0])-1].strip())
                middlename.append(temp[0][1])

        
        for i in range(0,len(firstname)):
            e=''
            w=''
            for row in db(db.email_info.Company_Name==company[i]).select():
                if row.First_String=='firstname':
                    e=e+firstname[i]
                if row.First_String=='f':    
                    e=e+firstname[i][0]
                if row.First_String=='lastname':
                    e=e+lastname[i]
                if row.First_String=='l':
                    e=e+lastname[i][0]
                
                e=e+row.Delimiter
                 
                if row.Second_String=='firstname':
                    e=e+firstname[i]
                if row.Second_String=='f':    
                    e=e+firstname[i][0]
                if row.Second_String=='lastname':
                    e=e+lastname[i]
                if row.Second_String=='l':
                    e=e+lastname[i][0]
                e=e+'@'
                e=e+row.Domain_Name
                w=string.lower(e)                                    
                emailid.append(w)
                
            if e=='':
                for r in db(db.email_info.id > 0).select():
                    if company[i].startswith(r.Company_Name):
                        First_String=r.First_String
                        Delimiter=r.Delimiter
                        Second_String=r.Second_String
                        Domain_Name=r.Domain_Name
                    
                        if First_String=='firstname':
                            e=e+firstname[i]
                        if First_String=='f':    
                            e=e+firstname[i][0]
                        if First_String=='lastname':
                            e=e+lastname[i]
                        if First_String=='l':
                            e=e+lastname[i][0]
                
                        e=e+Delimiter
                 
                        if Second_String=='firstname':
                            e=e+firstname[i]
                        if Second_String=='f':    
                            e=e+firstname[i][0]
                        if Second_String=='lastname':
                            e=e+lastname[i]
                        if Second_String=='l':
                            e=e+lastname[i][0]
                        e=e+'@'
                        e=e+Domain_Name
                        w=string.lower(e)                                    
                        emailid.append(w)
                        break
                  
                    if r.Company_Name.startswith(company[i]):
                        First_String=r.First_String
                        Delimiter=r.Delimiter
                        Second_String=r.Second_String
                        Domain_Name=r.Domain_Name
                    
                        if First_String=='firstname':
                            e=e+firstname[i]
                        if First_String=='f':    
                            e=e+firstname[i][0]
                        if First_String=='lastname':
                            e=e+lastname[i]
                        if First_String=='l':
                            e=e+lastname[i][0]
                
                        e=e+Delimiter
                 
                        if Second_String=='firstname':
                            e=e+firstname[i]
                        if Second_String=='f':    
                            e=e+firstname[i][0]
                        if Second_String=='lastname':
                            e=e+lastname[i]
                        if Second_String=='l':
                            e=e+lastname[i][0]
                        e=e+'@'
                        e=e+Domain_Name
                        w=string.lower(e)                                    
                        emailid.append(w)
                        break    
                        
            if e=='':
                emailid.append('NONE')        

        
        for i in range(0,len(firstname)):
            try:
                spamWriter.writerow([firstname[i].encode('utf-8').strip(),middlename[i].encode('utf-8').strip(),lastname[i].encode('utf-8').strip(),titl[i].encode('utf-8').strip(),current[i].encode('utf-8').strip(),location[i].encode('utf-8').strip(),industry[i].encode('utf-8').strip(),view_profile[i].encode('utf-8').strip(),company[i].encode('utf-8').strip(),emailid[i].encode('utf-8').strip()])
            except:
                continue
        if soup.find('a',{"class" : "paginator-next"}):
            br.open('http://www.linkedin.com'+ soup.find('a',{"class" : "paginator-next"}).get('href'))
        #soup = BeautifulSoup(br.response().read())
        
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=%s.csv' % request.vars.File_Name
    return csv_response.getvalue()

#for adding company information into the database    
def email_info():
     name=SQLFORM(db.email_info)
     if(name.accepts(request.vars,session)):
         #db.playlist.insert(playlist_id=request.vars.id)
         session.flash='New Entry Made'
         redirect(URL(r=request,f='email_info'))
     return dict(name=name)
     
#list companies present in table     
def list_companies():
    return dict(companies=db(db.email_info.id>0).select())

#logout          
def logout():
    session.username=[]
    session.password=[]
    session.flash =T('Logout Successful')
    redirect(URL(r=request,f='index'))

#del a company from database    
def delete():
    db(db.email_info.id==request.args(0)).delete()
    session.flash='Company Info Deleted'
    redirect(URL(r=request,f='list_companies'))

#extract all contacts on the local machine    
def extract():  
    #subprocess.call("java -cp \"/var/www/web2py/applications/mycrawler/dataloader/econtacts/config\" com.salesforce.dataloader.process.ProcessRunner process.name=econtacts")
    
    #this script is used for adding company name to the contacts extracted from the salesforce.com
    #1st give the name of the file which is taken as input
    #then give name of the file where you want new data with appended field to be stored
    #then give the name of the file where all accounts are stored i.e. where company names(account names) are hashed to accountids


    #opening input file which needs to be edited
    #infile=raw_input('Enter Input Filename for Editing (eg extracted.csv):')
    o=open('/var/www/web2py/applications/mycrawler/dataloader/econtacts.csv', 'rb')
    inp = csv.reader(o, delimiter=',')

    #opening new file for writing data
    #newin=raw_input('Enter Input Filename for Newfile (eg extracted.csv):')
    w=open('/var/www/web2py/applications/mycrawler/dataloader/contacts.csv','wb')
    wri=csv.writer(w,delimiter=',')

    #opening file from where company names will be matched to the accountids
    #in1=raw_input('Enter accounts filename (eg allaccounts.csv):')
    a = open('/var/www/web2py/applications/mycrawler/dataloader/allaccount.csv', 'rb')
    acc = csv.reader(a, delimiter=',')

    #stores header line
    headers=inp.next()
    head1=acc.next()

    keys=set()

    accid=dict()
    
    #finding index for field ID in accounts file
    id=head1.index('ID')
    #finding index for field NAME in accounts file
    accountname=head1.index('NAME')

    #finding index of accountid in the input file
    accountid=headers.index('ACCOUNTID')

    #creating a dictionary where accountids are mapped to accountnames(companynames)
    #acc means accessing accounts file

    for entry in acc:
        #search in a set is order 1 where as search in list is order N...
        keys.add(entry[id])
        accid[entry[id]]=entry[accountname]

    #writing new header line in the new file generated
    headers.append('COMPANYNAME')
    wri.writerow(headers)

    #inp means accessing input file

    for entry in inp:
        #for each entry in input file we check if accountid is present in the set generated from accounts file
        #if we use accid.keys() instead of set keys it will take N^2 time hence using set
    
        if(entry[accountid] in keys):
            entry.append(accid[entry[accountid]])
            wri.writerow(entry)
        else:
            entry.append('None')
            wri.writerow(entry)


    w.close()
    o.close()
    a.close()

    cpy()
    #redirect(URL(r=request,f='enter_info'))
    return cp_response.getvalue()

#for writing into the file
def cpy():
    global cp_response
    cp_response = cStringIO.StringIO()
    writer = csv.writer(cp_response, delimiter=',')
    o=open('/var/www/web2py/applications/mycrawler/dataloader/contacts.csv', 'rb')
    reader = csv.reader(o, delimiter=',')
    for row in reader:
        writer.writerow(row)
        
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=allcontacts.csv'
    
#opens check data page.....   
def upload():
    global fname
    global saveas
    form = SQLFORM(db.files)
    if form.process().accepted:
       fname=form.vars.Upload_File
       saveas=request.vars.Save_As
       temp()
       db(db.files.id>0).delete()
       return up_response.getvalue()
    elif form.errors:
       response.flash = 'form has errors'
         
    return dict(form=form)
    
#checking data by comparing it with salesforce data...    
def temp():
    global up_response
    global fname
    
    up_response = cStringIO.StringIO()
    writer = csv.writer(up_response, delimiter=',')
    
    k='/var/www/web2py/applications/mycrawler/uploads/' + fname
    c=open(k, 'rb')
    check = csv.reader(c, delimiter=',')
    
    #infile=raw_input('Enter Input Filename for Comparing (eg extracted.csv):')
    o=open('/var/www/web2py/applications/mycrawler/dataloader/contacts.csv', 'rb')
    inp = csv.reader(o, delimiter=',')

    #checkfile=raw_input('Enter Input Filename to be checked (eg in.csv):')
    #c=open(checkfile, 'rb')


    head1=check.next()
    headers=inp.next()

    email=headers.index('EMAIL')
    firstname=headers.index('FIRSTNAME')
    lastname=headers.index('LASTNAME')

    companyname=headers.index('COMPANYNAME')

    em=head1.index('EMAIL')
    fname=head1.index('FIRSTNAME')
    lname=head1.index('LASTNAME')
    title=head1.index('TITLE')
    cname=head1.index('COMPANYNAME')

    unique=[]
    kept=set()
    kept1=set()
    records=dict()

    for entry in inp:
        if(entry[email] not in kept):
            records[entry[email]]=entry;
        if((entry[firstname]+entry[lastname]+entry[companyname]) not in kept1):
            records[(entry[firstname]+entry[lastname]+entry[companyname])]=entry
        kept.add(entry[email])
        kept1.add(entry[firstname]+entry[lastname]+entry[companyname])

    # and (entry[fname]+entry[lname]+entry[aid]) not in kept1
    for entry in check:
        if((entry[em] not in kept or entry[em]=='' or entry[em]=='NONE') and ((entry[fname]+entry[lname]+entry[cname]) not in kept1)):
            kept.add(entry[em])
            records[entry[em]]=['None','None',entry[lname],entry[fname],entry[em],entry[title],'None','None','None','None','None','None','None','None','None','None','None','None',entry[cname]]
            records[(entry[fname]+entry[lname]+entry[cname])]=['None','None',entry[lname],entry[fname],entry[em],entry[title],'None','None','None','None','None','None','None','None','None','None','None','None',entry[cname]]
            kept1.add(entry[fname]+entry[lname]+entry[cname])
            
            unique.append(['None','None',entry[lname],entry[fname],entry[em],entry[title],'None','None','None','None','None','None','None','None','None','None','None','None',entry[cname]])
        elif (entry[em] in kept and entry[em]!=''):
           # print entry[em]
            unique.append(records[entry[em]])
        else:
           # print entry[fname]
            unique.append(records[entry[fname]+entry[lname]+entry[cname]])
    

       
    writer.writerow(headers)
    for i in unique:
        writer.writerow(list(i))
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=%s.csv' % saveas
    o.close()
    c.close()

#save contacts on server as well as append a new term company name    
def contactsonserver():  
    #subprocess.call("java -cp \"/var/www/web2py/applications/mycrawler/dataloader/*\" -Dsalesforce.config.dir=\"/var/www/web2py/applications/mycrawler/dataloader/econtacts/config\" com.salesforce.dataloader.process.ProcessRunner process.name=econtacts")
    
    #this script is used for adding company name to the contacts extracted from the salesforce.com
    #1st give the name of the file which is taken as input
    #then give name of the file where you want new data with appended field to be stored
    #then give the name of the file where all accounts are stored i.e. where company names(account names) are hashed to accountids


    #opening input file which needs to be edited
    #infile=raw_input('Enter Input Filename for Editing (eg extracted.csv):')
    o=open('/var/www/web2py/applications/mycrawler/dataloader/econtacts.csv', 'rb')
    inp = csv.reader(o, delimiter=',')

    #opening new file for writing data
    #newin=raw_input('Enter Input Filename for Newfile (eg extracted.csv):')
    w=open('/var/www/web2py/applications/mycrawler/dataloader/contacts.csv','wb')
    wri=csv.writer(w,delimiter=',')

    #opening file from where company names will be matched to the accountids
    #in1=raw_input('Enter accounts filename (eg allaccounts.csv):')
    a = open('/var/www/web2py/applications/mycrawler/dataloader/allaccount.csv', 'rb')
    acc = csv.reader(a, delimiter=',')

    #stores header line
    headers=inp.next()
    head1=acc.next()

    keys=set()

    accid=dict()
    
    #finding index for field ID in accounts file
    id=head1.index('ID')
    #finding index for field NAME in accounts file
    accountname=head1.index('NAME')

    #finding index of accountid in the input file
    accountid=headers.index('ACCOUNTID')

    #creating a dictionary where accountids are mapped to accountnames(companynames)
    #acc means accessing accounts file

    for entry in acc:
        #search in a set is order 1 where as search in list is order N...
        keys.add(entry[id])
        accid[entry[id]]=entry[accountname]

    #writing new header line in the new file generated
    headers.append('COMPANYNAME')
    wri.writerow(headers)

    #inp means accessing input file

    for entry in inp:
        #for each entry in input file we check if accountid is present in the set generated from accounts file
        #if we use accid.keys() instead of set keys it will take N^2 time hence using set
    
        if(entry[accountid] in keys):
            entry.append(accid[entry[accountid]])
            wri.writerow(entry)
        else:
            entry.append('None')
            wri.writerow(entry)


    w.close()
    o.close()
    a.close()
    session.flash='Contacts Updated'
    redirect(URL(r=request,f='upload'))
    return dict()
    
#update accounts on server    
def accountsonserver():  
    #subprocess.call("java -cp \"/var/www/web2py/applications/mycrawler/dataloader/*\" -Dsalesforce.config.dir=\"/var/www/web2py/applications/mycrawler/dataloader/eaccounts/config\" com.salesforce.dataloader.process.ProcessRunner process.name=eaccounts")
    session.flash='Accounts Updated'   
    redirect(URL(r=request,f='upload'))
    return dict()

#save accounts on pc    
def accountsonpc():
    #subprocess.call("java -cp \"/var/www/web2py/applications/mycrawler/dataloader/*\" -Dsalesforce.config.dir=\"/var/www/web2py/applications/mycrawler/dataloader/eaccounts/config\" com.salesforce.dataloader.process.ProcessRunner process.name=eaccounts")
    acc_response = cStringIO.StringIO()
    accwrite = csv.writer(acc_response, delimiter=',')
    
    a = open('/var/www/web2py/applications/mycrawler/dataloader/allaccount.csv', 'rb')
    acc = csv.reader(a, delimiter=',')
    
    for entry in acc:
        accwrite.writerow(entry)           
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=accounts.csv'
    a.close()
    return acc_response.getvalue()
    return dict()
    
def create_email():
    global newname
    global save
    form = SQLFORM(db.files)
    if form.process().accepted:
       newname=form.vars.Upload_File
       save=request.vars.Save_As
       em()
       db(db.files.id>0).delete()
       return em_response.getvalue()
    elif form.errors:
       response.flash = 'form has errors'
    return dict(form=form)
       
def em():
    global em_response
    global newname
    
    em_response = cStringIO.StringIO()
    writer = csv.writer(em_response, delimiter=',')
    
    k='/var/www/web2py/applications/mycrawler/uploads/' + newname
    c=open(k, 'rb')
    check = csv.reader(c, delimiter=',')
    
    headers=check.next()
    firstname=headers.index('FIRSTNAME')
    lastname=headers.index('LASTNAME')
    companyname=headers.index('COMPANYNAME')
    headers.append('EMAIL')
    writer.writerow(headers)
    
    for entry in check:
        e=''
        w=''
        for row in db(db.email_info.Company_Name==entry[companyname]).select():
            if row.First_String=='firstname':
                e=e+entry[firstname]
            if row.First_String=='f':    
                e=e+entry[firstname][0]
            if row.First_String=='lastname':
                e=e+entry[lastname]
            if row.First_String=='l':
                e=e+entry[lastname][0]
                
            e=e+row.Delimiter
                 
            if row.Second_String=='firstname':
                e=e+entry[firstname]
            if row.Second_String=='f':    
                e=e+entry[firstname][0]
            if row.Second_String=='lastname':
                e=e+entry[lastname]
            if row.Second_String=='l':
                e=e+entry[lastname][0]
                
            e=e+'@'
            e=e+row.Domain_Name
            w=string.lower(e)                                    
            #emailid.append(w)
                
        if e=='':
            for r in db(db.email_info.id > 0).select():
                if entry[companyname].startswith(r.Company_Name):
                    First_String=r.First_String
                    Delimiter=r.Delimiter
                    Second_String=r.Second_String
                    Domain_Name=r.Domain_Name
                    
                    if First_String=='firstname':
                        e=e+entry[firstname]
                    if First_String=='f':    
                        e=e+entry[firstname][0]
                    if First_String=='lastname':
                        e=e+entry[lastname]
                    if First_String=='l':
                        e=e+entry[lastname][0]
                
                    e=e+Delimiter
                 
                    if Second_String=='firstname':
                        e=e+entry[firstname]
                    if Second_String=='f':    
                        e=e+entry[firstname][0]
                    if Second_String=='lastname':
                        e=e+entry[lastname]
                    if Second_String=='l':
                        e=e+entry[lastname][0]
                    e=e+'@'
                    e=e+Domain_Name
                    w=string.lower(e)                                    
                    #emailid.append(w)
                    break
                  
                if r.Company_Name.startswith(entry[companyname]):
                    First_String=r.First_String
                    Delimiter=r.Delimiter
                    Second_String=r.Second_String
                    Domain_Name=r.Domain_Name
                    
                    if First_String=='firstname':
                        e=e+entry[firstname]
                    if First_String=='f':    
                        e=e+entry[firstname][0]
                    if First_String=='lastname':
                        e=e+entry[lastname]
                    if First_String=='l':
                        e=e+entry[lastname][0]
                
                    e=e+Delimiter
                 
                    if Second_String=='firstname':
                        e=e+entry[firstname]
                    if Second_String=='f':    
                        e=e+entry[firstname][0]
                    if Second_String=='lastname':
                        e=e+entry[lastname]
                    if Second_String=='l':
                        e=e+entry[lastname][0]
                    e=e+'@'
                    e=e+Domain_Name
                    w=string.lower(e)                                    
                    #emailid.append(w)
                    break
                        
        if e=='':
            w='NONE'
        entry.append(w)
        writer.writerow(entry)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=%s.csv' % save
    c.close()
    return dict()    
#finish


###########################################################################################################    
    #redirect(URL(r=request,f='enter_info'))       
    #for link in soup.find_all('a'):
    #    if link.get('title')=='View Profile':
    #        #print(link.get('href'))
    #        #print link.get_text()
    #        view_profile.append('http://www.linkedin.com'+link.get('href'))
    #        name.append(link.get_text())
#for l in soup.find_all("span", { "class" : "given-name" }):
    #print l.get_text()

        

#    for l in soup.find_all('dd',{"class" : "title"}):
        #print l.get_text()
#        titl.append(l.get_text())
    
#    for l in soup.find_all('span',{"class" : "location"}):
        #print l.get_text()
#        location.append(l.get_text())

#    for l in soup.find_all('span',{"class" : "industry"}):
        #print l.get_text()
#        industry.append(l.get_text())
        
#    for l in soup.find_all('span', {"class" : "current-details"}):
#        k=l.get_text()
#        if k[len(k)-4:len(k)]!='more':
#            current.append(k)
        #elif(l.get["class"]=='current-details more text'):
        #    current.append(l.get_text())
    #for l in soup.find_all('span',{"class" : "current-details"}):
        #print l.get_text()
        #current.append(l.get_text())

    
    #global filename,csv_response

    #csv_response = cStringIO.StringIO()
    
    #spamWriter = csv.writer(csv_response, delimiter=',')
    
    #spamWriter.writerow(['NAME','JOB-TITLE','COMPANY-NAME','LOCATION','INDUSTRY','PROFLE-URL'])
   
    #spamWriter = csv.writer(open(request.vars.File_Name+'.csv', 'wb'), delimiter=',')
    #spamWriter.writerow(['NAME','JOB-TITLE','Current','LOCATION','INDUSTRY','PROFLE-URL'])
    #for i in range(1,10):
    #    spamWriter.writerow([name[i].encode('utf-8'),titl[i],current[i],location[i],industry[i],view_profile[i]])
        
        
    #,titl[i],current[i],location[i],industry[i],view_profile[i]
    #response.headers['Content-Type'] = 'text/csv'
    #response.headers['Content-Disposition'] = 'attachment; filename=%s' % request.vars.File_Name

    
    #return dict(view_profile=view_profile,name=name,location=location,industry=industry,titl=titl,current=current)
