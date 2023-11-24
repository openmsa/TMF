<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{
  create_var_def('relatedParties.0.role', 'String');
  create_var_def('relatedParties.0.id', 'String');
  create_var_def('relatedParties.0.name', 'String');
  create_var_def('externalId', 'String');

}

$found_value ='';
$relatedParties=$context['relatedParties'];
foreach ($relatedParties as $relatedPartie){
	if (isset ($relatedPartie["role"]) && isset ($relatedPartie["id"]) ) {
		if ($relatedPartie["role"] == 'SERVICE_PROVIDER'){
			$found_value = $relatedPartie["id"];
		}
	}
}

if (! $found_value ){
 task_error('Can not get relatedParties with "SERVICE_PROVIDER"');
	
}
$context['relatedParties_found_id'] = $found_value;


########################################################## 
## Getting access_token
########################################################## 

#$headers = ['Accept' => 'application/json' ] ;
#$headers = ['Accept' => 'application/form-data'];
  
$data = array(  
    'client_id'     => 'tm-nodered',
    'client_secret' => 'AzKvAsmdxe',
    'grant_type'    => 'password',
    'username'      => 'admin_aws_us',
    'password'      => 'Demo123!'  );
    
// $postdata = json_encode(  $data );
$postdata = http_build_query( $data );  # grant_type=password&client_id=tm-nodered...

$ci = curl_init(); 
curl_setopt($ci, CURLOPT_URL,'https://eu01.sb.infonova.com/auth/realms/SB_CATALYST/protocol/openid-connect/token');
curl_setopt($ci, CURLOPT_TIMEOUT, 200);
curl_setopt($ci, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'POST');
#curl_setopt($ci, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ci, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
curl_setopt($ci, CURLOPT_POSTFIELDS, $postdata);
curl_setopt($ci, CURLOPT_HTTPHEADER, array(  "cache-control: no-cache",  "content-type: application/x-www-form-urlencoded" ));
    
curl_setopt($ci, CURLOPT_SSL_VERIFYPEER, true);
curl_setopt($ci, CURLOPT_POST, true);
$token_result = curl_exec($ci);

// Closing
curl_close($ci);

/* Store the result in a variable      */    
#$context['token_result'] = $token_result;		# ={"access_token":"eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ6QWR1RkJYSjRjelRyeWp0YUE0dU9LWU1VRnRhTWhqejl1Qk9vSFNQMGZFIn0.eyJleHAiOjE2Njg0Mzg2NTYsImlhdCI6MTY2ODQzODM1NiwianRpIjoiNjUxOWM1ZjgtMTZjNS00OGU4LTljMTctMjk5MTFkZWRhNDg3IiwiaXNzIjoiaHR0cHM6Ly9ldTAxLnNiLmluZm9ub3ZhLmNvbS9hdXRoL3JlYWxtcy9TQl9DQVRBTFlTVCIsImF1ZCI6ImFjY291bnQiL...

$token_result = json_decode($token_result, true);

if (isset($token_result['access_token'])){
  $token = $token_result['access_token'];
}else{
  task_error('Can not get the token', $context, True);
}  
$context['infonova_access_token'] = $token ;
  
  
  
########################################################## 
##Sent notification
########################################################## 
$auth='Bearer '. $context['infonova_access_token'] ;
$headr = array();
$headr[] = 'Accept: application/json';
$headr[] = 'Content-Type: application/json';
$headr[] = 'Authorization: '.$auth.'' ;
#$headr[] = 'Content-length: 0'; 
    
/*
now = datetime.now(pytz.timezone("Europe/Paris"))
date_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")

date_time_str = "{0}:{1}".format(
  date_time[:-2],
  date_time[-2:]
)
next_date_time=datetime.strptime(date_time,"%Y-%m-%dT%H:%M:%S%z")
next_date_time=next_date_time  + timedelta(days=1)
next_date_time=next_date_time.strftime("%Y-%m-%dT%H:%M:%S%z")
next_date_time_str = "{0}:{1}".format(
  next_date_time[:-2],
  next_date_time[-2:]
)*/
$datetime = new DateTime();
$datetime->setTimezone(new DateTimeZone('Europe/Paris')); 
$date_time_str = $datetime->format('Y-m-d').'T'. $datetime->format('H:i:s').'+01:00';

$datetime->modify('+1 day');

$next_date_time_str = $datetime->format('Y-m-d').'T'. $datetime->format('H:i:s').'+01:00';

$data2 = array(
    'id' =>  $context['externalId'],
    'dateTime' =>  $date_time_str.'',
    'eventType' => 'orderStateChangeNotification',
    'serviceOrder' => array(
       'id' => ''.$context['externalId'].'',
       'externalId' => ''.$context['externalId'].'',
       'state'  => 'Completed',
       'priority' =>  4,
       'expectedCompletionDate' =>  ''.$next_date_time_str.'' )
    );

$data2_json       = json_encode( $data2);
$context['data2'] = $data2_json;
#$postdata         = http_build_query( $data2 );  # grant_type=password&client_id=tm-nodered...
$postdata         = $data2_json;   


$infonova_url = "https://eu01.sb.infonova.com/r6-api/" . $found_value . "/serviceordering/v1/notification";

$context['infonova_url'] = $infonova_url;

$ci = curl_init(); 
curl_setopt($ci, CURLOPT_URL, $infonova_url);
curl_setopt($ci, CURLOPT_TIMEOUT, 200);
curl_setopt($ci, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'POST');
curl_setopt($ci, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
curl_setopt($ci, CURLOPT_POSTFIELDS, $postdata);
curl_setopt($ci, CURLOPT_HTTPHEADER, $headr );
    
curl_setopt($ci, CURLOPT_SSL_VERIFYPEER, true);
curl_setopt($ci, CURLOPT_POST, true);
$notification_result = curl_exec($ci);

$context['infonova_result'] = $notification_result;
 
task_success('Infonova Order state Change Notification for order sent\n Status Code : '.$notification_result.'', $context, True);


?>