# Get Set FOSS Leaderboard

Official leaderboard for Get Set FOSS.

## Setup

1. Clone the repository:

    ```
    $ git clone https://github.com/dojutsu-user/Get-Set-Foss---Leaderboard.git
    ```

2. Create a virtual environment, activate it and install all dependencies:

    ```bash
    $ virtualenv venv --python=python3.7
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    ```

3. Run the `makemigrations` and `migrate` command:

    ```bash
    $ python manage.py makemigrations
    $ python manage.py migrate
    ```

4. Create a super user:

    ```bash
    $ python manage.py createsuperuser
    ```

5. Collect all static files:

   ```
   $ python manage.py collectstatic
   ```

6. Run the server:

    ```bash
    $ python manage.py runserver
    ```

## Automating The Leaderboard

1. Add participating repositories from the admin panel.
2. Every participant must sign in with GitHub.
3. Only merged PRs will result into points.
4. Each merged PR must have two labels so that it gets counted:

    * `getsetfoss2019`: Every PR must have this label so that it gets recognized as a valid PR for the event. If the PR doesn't have this label, it will get ignored and no points will be rewarded.
        * To change this to some other label, edit the `MAIN_LABEL` variable in `settings.py`.
    * Every PR must have a label which corresponds to its points. Valid labels are: `extra` (5 points), `very easy` (10 points), `easy` (15 points), `medium` (25 points), `hard` (30 points), `pro` (50 points) and `codeburst` (100 points).
        * To add/remove any label, edit the `POINTS_DATA` in `settings.py`.
        * Always run these two commands after editing `POINTS_DATA`:
            ```bash
            $ python manage.py makemigrations
            $ python manage.py migrate
            ```
5. To sync the latest data, run `sync_data` command:
    ```bash
    $ python manage.py sync_data
    ```
