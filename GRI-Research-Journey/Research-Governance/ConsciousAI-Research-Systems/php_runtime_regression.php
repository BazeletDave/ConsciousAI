<?php
/* Benign CLI runtime regression, not a CVE exploit proof of concept. */
$results=[];
$results['version']=PHP_VERSION;
$results['array_lifecycle']=(function(){$a=['x'=>1];unset($a);$b=['y'=>2];return $b['y']===2;})();
$results['json_roundtrip']=json_decode(json_encode(['a'=>1,'b'=>[2,3]]),true)['b'][1]===3;
$results['exception_cleanup']=(function(){try{throw new RuntimeException('expected');}catch(RuntimeException $e){return $e->getMessage()==='expected';}})();
$results['memory_baseline']=memory_get_usage(true)>0;
echo json_encode($results,JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES),"\n";
