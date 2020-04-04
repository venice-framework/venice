https://rmoff.net/2018/12/15/docker-tips-and-tricks-with-ksql-and-kafka/

# Print the command a container will run upon startup

```
docker inspect --format='{{.Config.Entrypoint}}' confluentinc/cp-ksql-server:5.0.1
docker inspect --format='{{.Config.Cmd}}' confluentinc/cp-ksql-server:5.0.1
```

# Wait for an HTTP endpoint to be available before doing something

```
echo -e "\n\nWaiting for KSQL to be available before launching CLI\n"
while [ $(curl -s -o /dev/null -w %{http_code} http://ksql-server:8088/) -eq 000 ]
do 
  echo -e $(date) "KSQL Server HTTP state: " $(curl -s -o /dev/null -w %{http_code} http://ksql-server:8088/) " (waiting for 200)"
  sleep 5
done
```

`echo -e "\n\nWaiting for KSQL to be available before launching CLI\n"`
`echo` displays a line of text
`-e` enables interpretation of backslash escapes, so `\n` would be interpreted as a new line

`while [ $(curl -s -o /dev/null -w %{http_code} http://ksql-server:8088/) -eq 000 ]`
`-s`: silent; don't show progress meter or error messages, only the output
`-o /dev/null`: write output to /dev/null (i.e., trash it) instead of to stdout
`-w %{http_code}`: write out http_code (code of the last retrieved HTTP(s) of FTP(s) transfer)

`$(curl -s -o /dev/null -w %{http_code} http://ksql-server:8088/)`
returns the http code of sending a GET request to http://ksql-server:8088
`-eq` inside of single braces does arithmetic comparisons in bash scripting.
`-eq 000` would compare the code to 000. You could also use 0 but Robin Moffat does it this way, probably so it would look more like an HTTP code.