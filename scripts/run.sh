: <<'END_COMMENT'
curl -X 'POST' \
  'http://127.0.0.1:8000/uploadfiles/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@file1.txt' \
  -F 'files=@file2.txt'
END_COMMENT

FILENAME="file1.txt"
CHECKSUM=$(md5sum $FILENAME); CHECKSUM="${CHECKSUM%% *}"
curl -X POST "http://localhost:8000/api/v1/storage/upload" \
  -H "X-Checksum: $CHECKSUM" \
  -H "X-Filename: $FILENAME" \
  --data-binary "@$FILENAME"
