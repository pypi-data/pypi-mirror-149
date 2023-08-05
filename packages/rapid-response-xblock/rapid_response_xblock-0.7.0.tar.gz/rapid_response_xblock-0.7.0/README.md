# rapid-response-xblock
A django app plugin for edx-platform

__NOTE:__ We had to make several fixes to XBlock Asides in `edx-platform` in order to get rapid response working. 
The `edx-platform` branch/tag you're using must include these commits for rapid response to work:

- https://github.com/mitodl/edx-platform/commit/b26db017a55140bb7940c3fbfac5b4f27128bffd
- https://github.com/mitodl/edx-platform/commit/96578f832d786d90162c555f1cfa08f69ba294d2
- https://github.com/mitodl/edx-platform/commit/1bd36be3b31210faa8af09fc28ff4a885807e20e

## Setup

### 1) Add rapid response as a dependency

In production, the current practice as of 01/2021 is to add this dependency via Salt.

For local development, you can use one of the following options to add this as a dependency in the `edx-platform` repo:

1. **Install directly via pip.**

    ```
    # From the devstack directory, run bash in a running LMS container...
    make dev.shell.lms
    
    # In bash, install the package
    source /edx/app/edxapp/edxapp_env && pip install rapid-response-xblock==<version>

    # Do the same for studio
    make dev.shell.studio
    
    # In bash, install the package
    source /edx/app/edxapp/edxapp_env && pip install rapid-response-xblock==<version>
    ``` 
   
   To install a version of rapid-response-xblock which is not on pypi, you can clone this repo into the two containers. Install the package by running `source /edx/app/edxapp/edxapp_env && python setup.py install` for LMS and Studio.


1. **Add to one of the requirements files (`requirements/private.txt` et. al.), then re-provision with `make dev.provision.lms`.** This is very heavyweight
  as it will go through many extra provisioning steps, but it may be the most reliable way.
1. **Use ODL Devstack Tools.** [odl_devstack_tools](https://github.com/mitodl/odl_devstack_tools) was created to 
  alleviate some of the pain that can be experienced while running devstack with extra dependencies and config changes.
  If you set a few environment variables and create a docker compose file and config patch file, you can run devstack
  with your rapid response repo mounted and installed, and the necessary config changes (discussed below) applied. 

### 2) Update EdX config files 

As mentioned above, [odl_devstack_tools](https://github.com/mitodl/odl_devstack_tools) can be used to automatically
apply the necessary config changes when you start the containers. If you're not using that tool, you can manually 
    add/edit the relevant config files while running bash in the LMS container (`make dev.shell.lms`):

#### Juniper release or more recent

If you're using any release from Juniper onward, make sure the following property exists with the given value
in `/edx/etc/lms.yml` and `/edx/etc/studio.yml`:

```yaml
- ALLOW_ALL_ADVANCED_COMPONENTS: true
```

#### Any release before Juniper

If you're using any release before Juniper, make sure the following properties exist with the given values in
`/edx/app/edxapp/lms.env.json` and `/edx/app/edxapp/cms.env.json`:

```json
{
    "ALLOW_ALL_ADVANCED_COMPONENTS": true,
    "ADDL_INSTALLED_APPS": ["rapid_response_xblock"]
}
```

`ADDL_INSTALLED_APPS` may include other items. The list just needs to have `rapid_response_xblock` among its values.

### 3) Add database record

If one doesn't already exist, create a record for the `XBlockAsidesConfig` model 
(LMS admin URL: `/admin/lms_xblock/xblockasidesconfig/`).

### 4) Rapid Response for Studio and XML
[Studio Documentation](https://odl.zendesk.com/hc/en-us/articles/360007744011-Rapid-Response-for-Studio)
[XML Documentation](https://odl.zendesk.com/hc/en-us/articles/360007744151-Rapid-Response-for-XML)

## Database Migrations

If your `rapid-response-xblock` repo is mounted into the devstack container, you can create migrations for any
model changes as follows:

```
# From the devstack directory, run bash in a running LMS container...
make dev.shell.lms

# In bash, create the migrations via management command...
python manage.py lms makemigrations rapid_response_xblock --settings=devstack_docker
```

## Usage

_NOTE (4/2021)_: Rapid response is **only configured to work with multiple choice problems**.

Follow these steps to enable an individual problem for rapid response:
1. Load the problem in Studio
2. Click "Edit"
3. In the editing dialog UI there should be Editor, Settings, and Plugins in the title bar. Click "Plugins". (If this option doesn't exist, rapid response may not be properly configured)
4. Check the box ("Enable problem for rapid-response")
5. Save and publish

When you navigate to that problem in LMS, you should now see an option for opening the problem for rapid response.

To test rapid response functionality:
1. Login to your local edX instance as "staff"
2. In Studio go to the edX Demo Course. Create a new unit which is a multiple choice problem.
3. Edit the problem and turn on rapid response as described in the previous steps.
4. Publish and click "View Live Version"
5. Verify that the dropdown next to "View this course as" is "Staff". 
6. Scroll down and you should see an empty graph containing a button labeled "Open problem now". Click on the button and it should show a timer that starts counting.
7. Pick one of the answers and submit it. After a few seconds a bar should appear for the column for the answer.
8. Pick another answer, and the bar should disappear and a new one should appear at the new answer.
9. Click "Close problem now"
10. Click the dropdown next to "View this course as" to switch to "Audit". You should see a multiple choice question with two incorrect answers and one correct answer according to the labels. You should **not** see the rapid response functionality beneath the problem.
