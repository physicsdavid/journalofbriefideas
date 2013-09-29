To run, first create an Figshare application here:

* http://figshare.com/account/applications

Then clone the code and install the requirements:

```
virtualenv journal_env
cd journal_env
git clone https://github.com/physicsdavid/journalofbriefideas
cd journalofbriefideas/app
cp figshare_credentials.py.example figshare_credentials.py
#fill in the oauth credentials for your app
../../bin/pip install -r requirements.txt
sudo ../../bin/python app.py
```

I used lvh.me to get oauth to work, callback URL = `http://lvh.me/login/authorized`

The figshare folks asked us not to public test articles, so please keep that in mind while developing/testing.
