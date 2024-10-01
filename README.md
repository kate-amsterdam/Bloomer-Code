# Bloomer Instructions

### Setup

- Clone this repo to get the code on your local compute. See [github instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
- Once the repo is on your machine, in the terminal, run the following commands:
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Add AWS credentials. You need to have the correct access and secret key available for this to work. Then, run the following commands in your terminal:
```
export AWS_ACCESS_KEY=<access_key>
export AWS_SECRET_ACCESS_KEY=<secret_key>
```

Now, the code is ready to run!

### Running the code 

There are two commands you can run with this code:

1. Fetch new Instagram posts for Bloomer account, and upload these posts to DynamoDB database
2. Fetch new media insights for all instagram posts in the DynamoDB database.

If you want to update the data in DynamoDB with the latest data from instagram, you will want to run both of the above commands in order. Below are further instructions on how to do so.

### Getting new IG posts

Run the following code in the same terminal you used during the "Setup" phase:
```
python3 ig_inserter.py insert_media <start-date> <end-date>
```
This will get all posts created between <start-date> and <end-date> and put them in the database. For example, `python3 ig_inserter.py insert_media 2024-09-01 2024-10-01` gets all posts created in September and puts them into the DyanmoDB table named `ig_media`


### Getting insights

Run the following code (**Run the code in "Getting new IG posts" section first!**) in the same terminal you used during the "Setup" phase:
```
python3 ig_inserter.py update_media_insights
```
This will get media insights (like number of views, likes, comments, etc.) for ALL posts in the dyanmoDB database. This is why it's important to run the code in "Getting new IG posts" first, since it will add new posts to the database, which this code will then see and get insights for.


