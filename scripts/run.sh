curl -X 'POST' \
  'http://127.0.0.1:8001/uploadfiles/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@file1.txt' \
  -F 'files=@file2.txt'
