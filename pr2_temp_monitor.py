# program to check the H.W. temperature and report values
import urllib2
import urllib
import time
import sensors
from time import sleep
from datetime import datetime
import time
import numpy as np 
coretemp=np.array([0,0,0,0,0,0,0])
def print_feature(chip, feature):
    sfs = list(sensors.SubFeatureIterator(chip, feature)) # get a list of all subfeatures
    
    label = sensors.get_label(chip, feature)
    
    skipname = len(feature.name)+1 # skip common prefix
    vals = [sensors.get_value(chip, sf.number) for sf in sfs]
    
    if feature.type == sensors.feature.INTRUSION:
        # short path for INTRUSION to demonstrate type usage
        status = "alarm" if int(vals[0]) == 1 else "normal"
        print("\t"+label+"\t"+status)
        return
    
    names = [sf.name[skipname:].decode("utf-8") for sf in sfs]
    data = list(zip(names, vals))
    
    str_data = ", ".join([e[0]+": "+str(e[1]) for e in data])
    print("\t"+label+"\t"+str_data)

class paste_it():
    #Class Variables

    #Pastebin API Key
    api_dev_key = 'cuKgwoRorO9qZ5r1RZBhIxEsI-_T03Cx'
    #Pastebin Username
    username = 'sender_account'
    #Pastebin Password
    password = 'pass'
    #Max results
    api_results_limit = 50 #default=50, min=1, max=1000

    def user_key(self):
        #create user key
        user_key_data = {'api_dev_key':self.api_dev_key,
                         'api_user_name':self.username,
                         'api_user_password':self.password}
        req = urllib2.urlopen('https://pastebin.com/api/api_login.php', urllib.urlencode(user_key_data).encode('utf-8'), timeout=7)
        return req.read().decode()

    def create_paste(self,data):
        #Create paste on api user's account
        api_option = 'paste'
        api_paste_code = data           #paste text body
        api_paste_private = 0           #0=public, 1=unlisted, 2=private
        api_paste_name = 'PR2 Critical Hardware Temperature Alarm report'        #title of paste
        api_paste_expire_data = 'N'     #available: N=never, 10M=10min, 1H=1hour, 1D=1Day, 1W=1week, 2W=2weeks, 1M=1Month, 6M=6months, 1Y=1year
        api_paste_format = 'text'       #text=None, mysql-MYSQL, perl=Perl, python=Python, sql=SQL, vbscript=VBscript, xml=XML, html4strict=HTML, html5=HTML5,
        data = {'api_dev_key':self.api_dev_key,
                'api_user_key':self.user_key(),
                'api_option':api_option,
                'api_paste_code':api_paste_code,
                'api_paste_private':api_paste_private,
                'api_paste_name':api_paste_name,
                'api_paste_expire_data':api_paste_expire_data,
                'api_paste_format':api_paste_format}
        req = urllib2.urlopen('https://pastebin.com/api/api_post.php', urllib.urlencode(data).encode('utf-8'),timeout=7)
        return req.read().decode()

if __name__ == "__main__":
    # Please write your Email username and password
    USER=""  
    PASS=""
    sensors.init() # optionally takes config file
    
    print("libsensors version: "+sensors.version)
    import smtplib
    
    critical_alarm0=0
    critical_alarm1=0
    critical_alarm2=0
    critical_alarm3=0
    critical_alarm4=0
    critical_alarm5=0

    rep=0
    url=""
    while True:
        
	if critical_alarm0==1 or critical_alarm1==1 or critical_alarm2==1 or critical_alarm3==1 or critical_alarm4==1 or critical_alarm4==1:

           end = time.time()
           temp = end-start
           minutes = temp//60
           #print(minutes)
           if minutes>15:
                  rep=1
                  critical_alarm0=0
 		  critical_alarm1=0
		  critical_alarm2=0
   	  	  critical_alarm3=0
    		  critical_alarm4=0
    		  critical_alarm5=0
        #print("*********************************")
        print "Time :  %f " %  time.time()
        cnt=0
        for chip in sensors.ChipIterator(): # optional arg like "coretemp-*" restricts iterator
            #print(sensors.chip_snprintf_name(chip)+" ("+sensors.get_adapter_name(chip.bus)+")")
            print("*********************************")
            for feature in sensors.FeatureIterator(chip):
                #print_feature(chip, feature)
                #value = sensors.get_value(chip, feature.number)
		
                #print(value)
		#print(feature.number)
                if cnt==1:
                   coretemp[0] = sensors.get_value(chip, 4)
                   coretemp[1] = sensors.get_value(chip, 8)
                   coretemp[2] = sensors.get_value(chip, 12)
                   coretemp[3] = sensors.get_value(chip, 16)
                   coretemp[4] = sensors.get_value(chip, 20)
                   coretemp[5] = sensors.get_value(chip, 24)

		   dateTimeObj = datetime.now()
	           timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
	           report_statement= "An alarm was released at " + timestampStr + "  reporting a violation in PR2 Robot's hardware temperature. The current processor core temperature in degree Celsius values are reported:    Core 0 : " + str(coretemp[0])+" Core 1 :  "+ str(coretemp[1])+" Core 2 :  "+ str(coretemp[2])+" Core 3 :  "+ str(coretemp[3])+" Core 4 :  "+ str(coretemp[4])+"  Core 5 : "+ str(coretemp[5])
	           data=report_statement

		if cnt==0:
                   power = sensors.get_value(chip, 0)
		if (cnt==1 and feature.number==1):
                   coretemp[0] = sensors.get_value(chip, 4)
	           print "Core 0 Temperature: %f "%coretemp[0]

		   if coretemp[0]>80 and critical_alarm0==0:
		      try:
		         paste = paste_it()
		         url=paste.create_paste(data)
   
		         #print(url)
		      except Exception as e:
		         print "[!] API Error:",e
			   
                      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                      server.login(USER, PASS)
		      mess="Warning PR2 core 1 temperature is larger than 80 Degree Celsius full cores temperatures are provided in  "+str(url)
                      server.sendmail("your_gmail_account@gmail.com", "sending_to_account1@uni-bremen.de",mess)
                      server.sendmail("your_gmail_account@gmail.com", "sending_to_account2@cs.uni-bremen.de",mess)
                      server.sendmail("your_gmail_account@gmail.com", "sender_account@uni-bremen.de",mess)
                      server.quit()
		      critical_alarm0=1
                      start = time.time()
                if (cnt==1 and feature.number==2):
                   coretemp[1] = sensors.get_value(chip,feature.number*4)
	           print "Core 1 Temperature: %f "%coretemp[1]
		   
		   if coretemp[1]>80 and critical_alarm1==0:
			
		      try:
		         paste = paste_it()
		         url=paste.create_paste(data)
   
		         #print(url)
		      except Exception as e:
		         print "[!] API Error:",e
			   
                      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                      server.login(USER, PASS)
		      mess="Warning PR2 core 1 temperature is larger than 80 Degree Celsius full cores temperatures are provided in  "+str(url)
                      server.sendmail("your_gmail_account@gmail.com", "sending_to_account1@uni-bremen.de",mess)
                      server.sendmail("your_gmail_account@gmail.com", "sending_to_account2@cs.uni-bremen.de",mess)
                      server.sendmail("your_gmail_account@gmail.com", "sender_account@uni-bremen.de", mess)
                      server.quit()
		      critical_alarm1=1
		      start = time.time()
      		if (cnt==1 and feature.number==3):
                   coretemp[2] = sensors.get_value(chip,feature.number*4)
	           print "Core 2 Temperature: %f "%coretemp[2]
		   if coretemp[2]>80 and critical_alarm2==0:
		      try:
		         paste = paste_it()
		         url=paste.create_paste(data)
   
		         #print(url)
		      except Exception as e:
		         print "[!] API Error:",e
			   

                      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                      server.login(USER, PASS)
		      mess="Warning PR2 core 2 temperature is larger than 80 Degree Celsius full cores temperatures are provided in  "+str(url)
                      server.sendmail("your_gmail_account@gmail.com", "sending_to_account1@uni-bremen.de",mess)
                      server.sendmail("your_gmail_account@gmail.com", "sending_to_account2@cs.uni-bremen.de",mess)
                      server.sendmail("your_gmail_account@gmail.com", "sender_account@uni-bremen.de", mess)
                      server.quit()
		      critical_alarm2=1
		      start = time.time()
		if (cnt==1 and feature.number==4):
                   coretemp[3] = sensors.get_value(chip,feature.number*4)
	           print "Core 3 Temperature: %f "%coretemp[3]
		   if coretemp[3]>80 and critical_alarm3==0:
		      try:
		         paste = paste_it()
		         url=paste.create_paste(data)
   
		         #print(url)
		      except Exception as e:
		         print "[!] API Error:",e
			   

                      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                      server.login(USER, PASS)
		      mess="Warning PR2 core 3 temperature is larger than 80 Degree Celsius full cores temperatures are provided in  "+str(url)
                      server.sendmail("your_gmail_account@gmail.com", "sending_to_account1@uni-bremen.de",mess)
                      server.sendmail("your_gmail_account@gmail.com", "sending_to_account2@cs.uni-bremen.de",mess)
                      server.sendmail("your_gmail_account@gmail.com", "sender_account@uni-bremen.de", mess)
                      server.quit()
		      critical_alarm3=1
		      start = time.time()
		if (cnt==1 and feature.number==5):
                   coretemp[4] = sensors.get_value(chip,feature.number*4)
	           print "Core 4 Temperature: %f "%coretemp[4]
		   if coretemp[4]>80 and critical_alarm4==0:
		      try:
		         paste = paste_it()
		         url=paste.create_paste(data)
   
		         #print(url)
		      except Exception as e:
		         print "[!] API Error:",e
			   

                      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                      server.login(USER, PASS)
		      mess="Warning PR2 core 4 temperature is larger than 80 Degree Celsius full cores temperatures are provided in  "+str(url)
                      server.sendmail("your_gmail_account@gmail.com", "sending_to_account1@uni-bremen.de",mess)
                      server.sendmail("your_gmail_account@gmail.com", "sending_to_account2@cs.uni-bremen.de",mess)
                      server.sendmail("your_gmail_account@gmail.com", "sender_account@uni-bremen.de", mess)
                      server.quit()
		      critical_alarm4=1
		      start = time.time()
		if (cnt==1 and feature.number==6):
                   coretemp[5] = sensors.get_value(chip,feature.number*4)
	           print "Core 5 Temperature: %f "%coretemp[5]
		   if coretemp[5]>80 and critical_alarm5==0:
		      try:
		         paste = paste_it()
		         url=paste.create_paste(data)
   
		         #print(url)
		      except Exception as e:
		         print "[!] API Error:",e
			   

                      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                      server.login(USER, PASS)
		      mess="Warning PR2 core 5 temperature is larger than 80 Degree Celsius full cores temperatures are provided in  "+str(url)
                      server.sendmail("your_gmail_account@gmail.com", "sending_to_account1@uni-bremen.de",mess)
                      server.sendmail("your_gmail_account@gmail.com", "sending_to_account2@cs.uni-bremen.de",mess)
                      server.sendmail("your_gmail_account@gmail.com", "sender_account@uni-bremen.de",mess)
                      server.quit()
		      critical_alarm5=1
		      start = time.time()

	    cnt=cnt+1	

        sleep(0.5)
        
    sensors.cleanup()



