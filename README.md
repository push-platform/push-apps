# New Push Application

This repository contains a code for a New Push Application. This projects depends on RapidPro and all libs and services that RapidPro run.  

The idea for this project is: There is a folder `push-public` that contains all features for New Push. `push-public` folder must be couple inside a root for RapidPro project, and then there are all features about RapidPro and all exclusive features about New Push.

For run the features for New Push, you need to setup a [RapidPro](http://rapidpro.github.io/rapidpro/docs/) project, and then setup environment variables for New Push and libs.

### Configure `settings.py` for New Push

It's necessary to configure the `settings.py` to enable NewPush on RapidPro.. Then, Application for RapidPro can see templates and code (channel_types, installed_apps and etc).  

For configure the settings, must override the variables:

* `CHANNEL_TYPES = (*CHANNEL_TYPES, "a_list_contains_paths_for_new_channels_on_push")`

* `INSTALLED_APPS = (*INSTALLED_APPS, "push_public")`
	- If you need install libs for use in django project, must be add `INSTALLED_APPS` variable

* `BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`

* `TEMPLATES[0]["DIRS"] = [os.path.join(PROJECT_DIR, "../templates"), os.path.join(BASE_DIR, "push_public/templates")]`

### Environment Variables for New Push

For run New Push, it's necessary configure the settings and set some environment variables. The environment variables are:

#### Environment Variables for upload files to AWS and Setup Pushinho ChannelType

* `PUSH_WEB_SOCKET_URL`

* `PUSHINHO_ICONS_AWS_PATH`

* `AWS_ACCESS_KEY_ID`

* `AWS_SECRET_ACCESS_KEY`

* `AWS_DEFAULT_ACL`

* `AWS_STORAGE_BUCKET_NAME`

* `AWS_BUCKET_DOMAIN`

### Requirements Libs

This project have a file `requirements.txt` with all necessary libs for New Push.

After setup the [RapidPro environment](http://rapidpro.github.io/rapidpro/docs/development/), you must inside a folder `push-public` and run this command:

`pip install -r push_requirements.txt`
