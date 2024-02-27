from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import glob
import os as os
import logging
import json
import pandasql as ps

#logging.basicConfig(filename=r'X:\All Of Us Program\Retention Pilot- Hassan\HP_API\Scripts\Logs\std.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S' )
#logger=logging.getLogger()
#logger.setLevel(logging.DEBUG) 
# pip install -r requirements.txt 

# Set path to your key.json
credentials = service_account.Credentials.from_service_account_file(r'X:Key\key.json')
scoped_credentials = credentials.with_scopes(
  ['https://www.googleapis.com/auth/cloud-platform',
   'https://www.googleapis.com/auth/userinfo.email'])
authed_session = AuthorizedSession(scoped_credentials)

headers = {'content-type': 'application/json', 'Authorization': authed_session , 'Accept':'application/json','charset':'utf-8'}
payload= {"retentionType": ['PASSIVE' ], "activityStatus":['not_withdrawn'],"consentForStudyEnrollment":['SUBMITTED'], "retentionEligibleStatus":['ELIGIBLE'],"deceasedStatus":['UNSET']}
response= authed_session.get('https://all-of-us-rdr-prod.appspot.com/rdr/v1/ParticipantSummary?&awardee=COLUMBIA&activityStatus=not_withdrawn&consentForStudyEnrollment=SUBMITTED&retentionEligibleStatus=ELIGIBLE&deceasedStatus=UNSET&retentionType!=ACTIVE&organization=COLUMBIA_HARLEM&_count=10000',headers=headers).json()
#response= authed_session.get('https://all-of-us-rdr-prod.appspot.com/rdr/v1/ParticipantSummary?&awardee=COLUMBIA&organization=COLUMBIA_HARLEM&_count=10000',headers=headers, params=payload).json()

#logger.info("Starting GET") 
print(response)

#good_cols= ['participantId', 'lastName', 'firstName','dateOfBirth', 'retentionType', 'retentionEligibleStatus', 'retentionEligibleTime', 'lastActiveRetentionActivityTime'
#            ,'enrollmentSite','site','consentCohort','email', 'phoneNumber']
good_cols= [
'participantId',
'ageRange',
'sex',
'race',
'education',
'income']
# ,,,,,,'genderIdentity','phoneNumber''language','retentionEligibleStatus', 'retentionEligibleTime', 'retentionType', 'clinicPhysicalMeasurementsStatus']

data=[]
for entry in response['entry']:
    item = []
    for col in good_cols:
        for key, val in entry['resource'].items():
            if col == key:
                if key == 'dateOfBirth':                    
                    item.append(datetime.strptime(val, '%Y-%m-%d'))
                else:
                    item.append(val)  

    data.append(item)
frame = pd.DataFrame(data, columns=good_cols)
data_df=frame.dropna() #removes no email participants
#data_df=frame.where(pd.notna(frame),'')
#print(frame)
print('this is data_df')
print(data_df)
current_datetime=datetime.now().strftime("%m-%d-%y %H-%M-%S")
str_current= str(current_datetime)

print(data_df)

df= data_df.set_index('participantId', inplace=True)
sql_q= '''select * from data_df where participantId 
in 
(
'P999999999'
)

; '''

df_r=ps.sqldf(sql_q_rand,locals())
print(df_r)

df_r.to_csv(f"X:Retention_Demo.csv",index=False,
header=[
'PMI ID',
'Age Range',
'Sex',
'Race',
'Education',
'Income']
 
 , date_format='%Y/%m/%d %H:%M:%S'
 )

#logger.info("Process completed") 
