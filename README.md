# Social Karma

An app to track the social media trends at a point in time. For ex: 

1. Twitter followers
2. GitHub commits
3. GitHub followers
3. GitLab commits
4. Website visits (blog)
5. LinkedIn views
6. Dev.to followers.

The app will run (dockerized on a cloud platform) and then send a json response to a webhook. 
It's upto the webhook to do whatever it wants to do with the data. 

My motivation is to create my own Grafana dashboard and track my social stats on a daily basis.
Just to see how my stats are looking at and measure my content creation on a daily basis. 

But users are free to use it as they seem fit. 

The application will read a config file (yaml, json etc) and then return the stats at the moment. 
To get a stream of monthly data, the user should run this on a daily basis, probably as a cron job.

### Todo

- [ ] Write documentation on how to setup the project. 
- [ ] Dockerize the application.
- [ ] Add precommit hooks.
- [ ] Switch to a better package manager.
- [ ] More???


It's a heavy WIP and I will think more about the features and decide on an MVP release
soon.
