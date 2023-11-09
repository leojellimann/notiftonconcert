# notiftonconcert
Website that sends you a notification by email if the artist you want to see in concert unlocked tickets to go to the concert

Once on the website you can type the name of the artist you want to see in concert :
![image](https://github.com/leojellimann/notiftonconcert/assets/93252510/e00365b4-7b00-4310-bbc6-1f4f5d36049e)

Once you clicked on the button "OK", a list of every concerts is diplayed.
You can select the one you want a ticket for and type your email adress.
![image](https://github.com/leojellimann/notiftonconcert/assets/93252510/0490c06c-5335-4120-8c1a-f4c46cbed7a8)

After you typed your email adress and clicked on "M'informer des nouvelles dispo", the Python script will be running daily on a server to detect if new tickets are available or not.

If new tickets are available, the python script sends you and email.
Otherwise, it keeps checking until the finale date of the concert arrives. 
In that case, it sends you an email to say there were no tickets available for the concert.
