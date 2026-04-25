# Running the Docs Development Server

The docs server is best run inside the dev container.  The reason for this is that there are some pages that are automatically generated based on the Airflow DAGs.  This automation would break outside of Linux/Unix.

That being said there is of coruse no reason to spin up the devconatiner if your change to the docs is very simple such as correcting a typo or adding a simple description to something.

To run the ProperDocs development server frm inside the container cd into the docs folder and then run the below command.

```bash
uv run properdocs serve -a 0.0.0.0:8000
```

View the development site as `localhost:8000` in your web broswer.