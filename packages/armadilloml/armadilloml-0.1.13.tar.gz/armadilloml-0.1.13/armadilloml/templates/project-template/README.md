# Armadillo ML - Starter Template
This is projected was bootsrapped with **Armadillo ML**. Here's what's in an Armadillo ML starter template:

- `pyproject.toml`: We use [Python Poetry](https://python-poetry.org/) for dependency management. So to add new libraries or dependencies, simply run `poetry add some-library`. This will update `pyproject.toml` and save the dependency locally.
- `.gitattributes`: We use [git-lfs](https://git-lfs.github.com/) to manage big files like ML models. You can commit them to git like any other file and git lfs will simply store a pointer to the file instead of the file itself. `.gitattributes` is how git lfs knows which file extensions to target.
- `app.py`: We use [Flask](https://flask.palletsprojects.com/en/2.1.x/) for model inference. Add all your model serving code to this file.
- `.github/workflows/cloud-run.yml`: We use [Google Cloud Run](https://cloud.google.com/run) to deploy the model into production. This happens automatically with each `git push` using the Github actions configured in this file. 

## Workflow
When you are finished training your model and writing your inference code locally, simply commit and then push your changes. This will automatically trigger a build of your ML service using GitHub Actions and then make it available as a block in Armadillo!