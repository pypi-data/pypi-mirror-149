# ssb-altinn3-util
A library of handy modules and utilities that can be used and built on when integrating with Altinn 3 and SSB's Altinn 3 data collection solutions


## To build package locally during development run (from root directory of project):

python setup.py install

## Testing from other Python apps

- Push the changes to a branch of `ssb-altinn3-util`
- Uninstall previous ssb-altinn3-util in the app: `pip uninstall ssb-altinn3-util`
- Add the following in your requirements.txt in the app `git+ssh://git@github.com/statisticsnorway/ssb-altinn3-util@<your_branch_name>

After the testing is finished, remember to revert the `requirements.txt` before pushing the changes!

## Releasing to PyPi

- Update version in `setup.py`
- Create a GitHub release and the pipeline will push the package to PyPi
