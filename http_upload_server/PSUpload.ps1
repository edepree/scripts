$webClient = New-Object System.Net.WebClient
$webClient.UploadFile( 'http://localhost:9876', 'C:\test.txt' )