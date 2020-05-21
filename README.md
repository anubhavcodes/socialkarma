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


### Usage

Make sure the follwoing environment variables are set:

```bash
TWITTER_HANDLE=anubhavcodes
KEYBASE_HANDLE=anubhavyadav
LINKEDIN_USERNAME="yourlinkedinemail"
LINKEDIN_PASSWORD="yourlinkedinpassword"
LINKEDIN_PROFILE_HANDLE=/in/anubhavcodes
GITHUB_USERNAME=anubhavcodes
STACKOVERFLOW_HANDLE=12928701
```

```bash
$ python app.py
```

### Usage with docker

Make sure the above environment variables are present in a file `.env` present at the root of the repo.

```bash
./scripts/run-int
```

Or if you have `direnv` installed you can just do

```bash
run-init
```

### Direnv support
You can install [direnv](https://direnv.net) and then run `direnv allow` to have access to
all the scripts without explicitly typing `./scripts/script-name` and directly running `script-name`
on the command line. Pretty cool.

### Setting up git hooks

You can do `run-init` or `./scripts/run-init` to install precommit git hooks.
Make sure you have [precommit](https://pre-commit.com) installed on your environment.

### Todo

- [✅] Write documentation on how to setup the project.
- [✅] Dockerize the application.
- [✅] Add precommit hooks.
- [ ] Switch to a better package manager.
- [ ] More???
- [ ] Deploy on heroku or something similar for one off dynos.


It's a heavy WIP and I will think more about the features and decide on an MVP release
soon.
